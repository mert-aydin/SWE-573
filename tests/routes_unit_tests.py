import json
import unittest
from unittest.mock import patch, MagicMock
from flask import url_for
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User, Post
from app.routes import load_user


class MyTestCase(unittest.TestCase):

    @patch('app.User')
    def test_load_user(self, mock_user):
        # Arrange
        mock_query = MagicMock()
        mock_user.query = mock_query
        mock_user_id = 1
        expected_user = 'user'
        mock_query.get.return_value = expected_user

        # Act
        result = load_user(mock_user_id)

        # Assert
        self.assertEqual(result, expected_user)
        mock_query.get.assert_called_once_with(mock_user_id)

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        with patch('app.User.query') as mocked_query, \
                patch('app.db.session.add'), \
                patch('app.db.session.commit'):
            mocked_query.filter_by.return_value.first.return_value = None
            response = self.client.post(url_for('register'),
                                        data=dict(email='dummyuser1@example.com', password='123456', username='Lily'))
            self.assert_redirects(response, url_for('login'))

    def test_login(self):
        with patch('app.User.query') as mocked_query, \
                patch('app.login_user'):
            user = User(email='dummyuser1@example.com', username='Lily',
                        password_hash=generate_password_hash('123456', method='sha256'))
            mocked_query.filter_by.return_value.first.return_value = user
            response = self.client.post(url_for('login'),
                                        data=dict(email='dummyuser1@example.com', password='password'))
            self.assert_redirects(response, url_for('dashboard'))

    def test_logout(self):
        with patch('app.logout_user'):
            response = self.client.post(url_for('logout'))
            self.assert_redirects(response, url_for('login'))

    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    @patch('app.Post.query')
    @patch('app.current_user')
    def test_create_post(self, mock_current_user, mock_post_query, mock_db_add, mock_db_commit):
        mock_current_user.id = 1
        response = self.client.post(url_for('create_post'), data=dict(title='test', body='test body'),
                                    follow_redirects=True)
        self.assert200(response)
        mock_db_add.assert_called()
        mock_db_commit.assert_called()

    @patch('app.User.query')
    def test_profile(self, mock_user_query):
        mock_user_query.filter_by.return_value.first.return_value = self.user
        response = self.client.get(url_for('profile', user_id=1))
        self.assert200(response)

    @patch('app.db.session.commit')
    @patch('app.User.query')
    def test_like_post(self, mock_user_query, mock_db_commit):
        post = Post(title='test', body='test body', user_id=1)
        db.session.add(post)
        db.session.commit()

        mock_user_query.get.return_value = self.user
        response = self.client.post(url_for('like_post', post_id=1))
        self.assert200(response)
        self.assertEqual(json.loads(response.data), dict(success=True, message="Post liked", likes=1))


if __name__ == '__main__':
    unittest.main()
