
'''CODE IMPORTED FROM 27.1 DEMO CODE'''


from unittest import TestCase

from app import app
from models import User, db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    '''------------SET UP / TEARDOWN -----------'''

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name='Jody', last_name='Mills',
                    image_url='https://www.users.com')

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    '''------------SET UP / TEARDOWN END -----------'''

    '''------------------ROUTES  TO TEST-----------------'''

    def test_root_redirect_200(self):
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('<button>Add User</button>', html)

    def test_root_redirect_302(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')

    def test_render_home(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Jody', html)
            self.assertIn('Mills', html)

    def test_show_add_user_form(self):
        with app.test_client() as client:
            response = client.get('/users/add')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Create New User</h1>', html)
            self.assertIn('<form method="POST">', html)
            self.assertIn('<h1>Create New User</h1>', html)

    def test_add_user_form_functionality(self):
        with app.test_client() as client:
            response = client.post(
                '/users/add', data={'first_name': 'Jane', 'last_name': 'Doe', 'image_url': 'www.jane-doe'})
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')

    def test_user_details_page(self):
        with app.test_client() as client:
            response = client.get('/users/7')
            html = response.get_data(as_text=True)
            '''These is one record om the DB blogly_test  where id=7'''

            self.assertEqual(response.status_code, 200)
            self.assertIn('Jody', html)
            self.assertIn('Mills', html)

    '''--------Problem test below'''

    def test_edit_user_form_redirect(self):
        with app.test_client() as client:
            response = client.post(
                '/users/1/add', data={'first_name': 'John', 'last_name': 'Dough', 'image_url': 'www.john-doe'})

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')
            self.assertEqual(response.location, '/users')

    def test_edit_user_form_functionality(self):
        with app.test_client() as client:
            response = client.post(
                '/users/1/add', data={'first_name': 'John', 'last_name': 'Dough', 'image_url': 'www.john-doe'}, follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.location, '/users')

    '''--------Problem tests above'''

    def test_delete_user_redirect(self):
        with app.test_client() as client:
            response = client.get('/users/1/delete')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/users')

    def test_delete_user_functionality(self):
        with app.test_client() as client:
            response = client.post(
                '/users/1/delete', data={'user_id': 1}, follow_rediredcts=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('Jody', html)
            self.assertIn('<h1>Users</h1>', html)
