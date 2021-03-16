import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Collector, Set


class LegoTestCase(unittest.TestCase):
    """This class represents the lego test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user_name = "postgres"
        self.database_name = "lego"
        self.password = "psql133"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.user_name, self.password,
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.manager_token = os.environ['MANAGER_TOKEN']
        self.director_token = os.environ['DIRECTOR_TOKEN']

        self.new_set = {
            'id': '21325',
            'name': 'Medieval Blacksmith',
            'year': '2021',
            'pieces': 2164
        }

        self.set_to_be_updated = {
            'id': '10295',
            'name': 'Porsche',
            'year': '2020',
            'pieces': 1458
        }

        self.update_set = {
            'name': 'Porsche 911',
            'year': '2021'
        }

        self.set_to_be_deleted = {
            'id': '10278',
            'name': 'Police Station',
            'year': '2021',
            'pieces': 2923
        }

        self.new_collector = {
            'name': 'Paul',
            'location': 'Liverpool',
            'legos': []
        }

        self.collector_to_be_updated = {
            'name': 'John',
            'location': 'Liverpool',
            'legos': []
        }

        self.update_collector = {
            'name': 'Ringo'
        }

        self.collector_to_be_deleted = {
            'name': 'George',
            'location': 'Liverpool',
            'legos': []
        }

        self.client().post(
            '/sets', json=self.set_to_be_updated,
            headers={'Authorization': self.manager_token})
        self.client().post(
            '/sets', json=self.set_to_be_deleted,
            headers={'Authorization': self.manager_token})
        self.client().post(
            '/collectors', json=self.collector_to_be_updated,
            headers={'Authorization': self.director_token})
        self.client().post(
            '/collectors', json=self.collector_to_be_deleted,
            headers={'Authorization': self.director_token})

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  Tests for sets
    #  ----------------------------------------------------------------

    def test_get_sets(self):
        res = self.client().get('/sets')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['sets']))

    def test_get_sets_405(self):
        res = self.client().get('/sets/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    def test_get_sets_detail_manager(self):
        res = self.client().get(
            '/sets-detail', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['sets']))

    def test_get_sets_detail_director(self):
        res = self.client().get(
            '/sets-detail', headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['sets']))

    def test_get_sets_detail_404(self):
        res = self.client().get(
            '/sets-detail/1', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_create_set(self):
        res = self.client().post(
            '/sets', json=self.new_set,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_set_422(self):
        res = self.client().post(
            '/sets', json=self.new_collector,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_update_set(self):
        res = self.client().patch(
            '/sets/10295', json=self.update_set,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_update_set_404(self):
        res = self.client().patch(
            '/sets/1000', json=self.update_set,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_delete_set(self):
        res = self.client().delete(
            '/sets/10278', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_set_404(self):
        res = self.client().delete(
            '/sets/1000', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    #  Tests for collectors
    #  ----------------------------------------------------------------

    def test_get_collectors(self):
        res = self.client().get('/collectors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['collectors']))

    def test_get_collectors_405(self):
        res = self.client().get('/collectors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    def test_get_collectors_detail_manager(self):
        res = self.client().get(
            '/collectors-detail',
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['collectors']))

    def test_get_collectors_detail_director(self):
        res = self.client().get(
            '/collectors-detail',
            headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['collectors']))

    def test_get_collectors_detail_404(self):
        res = self.client().get(
            '/collectors-detail/1',
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_create_collector_director(self):
        res = self.client().post(
            '/collectors', json=self.new_collector,
            headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_collector_manager_401(self):
        res = self.client().post(
            '/collectors', json=self.new_collector,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

    def test_create_collector_422(self):
        res = self.client().post(
            '/collectors', json=self.new_set,
            headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_update_collector(self):
        res = self.client().patch(
            '/collectors/1', json=self.update_collector,
            headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        set = Set.query.filter(Set.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_update_collector_manager_401(self):
        res = self.client().patch(
            '/collectors/1', json=self.update_collector,
            headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

    def test_update_collector_404(self):
        res = self.client().patch(
            '/collectors/1000', json=self.update_collector,
            headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_delete_collector(self):
        res = self.client().delete(
            '/collectors/2', headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        set = Set.query.filter(Set.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_collector_manager_401(self):
        res = self.client().delete(
            '/collectors/2', headers={'Authorization': self.manager_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

    def test_delete_collector_404(self):
        res = self.client().delete(
            '/collectors/1000', headers={'Authorization': self.director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
