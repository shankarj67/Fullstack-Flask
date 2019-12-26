import os
import unittest
import tempfile
import app

class TestIndex:
    
    
    def test_index(self):
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        assert response.status_code == 200
       

    def test_database(Self):
        tester = os.path.exists("flasktdd.db")    
        assert tester


class TestFunctionality:

    @classmethod
    def setup_class(cls):
        """Set up a blank temp database before each test."""
        cls.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        cls.app = app.app.test_client()
        app.init_db()

    @classmethod
    def teardown_class(cls):
        os.close(cls.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function."""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function."""
        return self.app.get('/logout', follow_redirects=True)    

    def test_empty_db(self):
        """Ensure database is blank."""
        rv = self.app.get('/')
        

    def test_login_logout(self):
        """Test login and logout using helper functions."""
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(
            app.app.config['USERNAME'] + 'x',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data

    def test_messages(self):
        """Ensure that a user can post messages."""
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        