import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://postgres:123123@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actor_success(self):
        response = self.client().get('/actors')
        data = response.get_json()
        self.assertTrue(len(data['actors']) > 0)
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_get_movie_success(self):
        response = self.client().get('/movies')
        data = response.get_json()
        self.assertTrue(len(data['movies']) > 0)
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_add_actor_success(self):
        response = self.client().post('/actors',
                                      json={
                                          'name': "test1",
                                          'age': "33",
                                          'gender': "dd"
                                      })
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_add_actor_failed(self):
        response = self.client().post('/actors',
                                      json={
                                          'name': "test1",
                                          'age': "33"
                                      })
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 422)

    def test_add_movie_success(self):
        response = self.client().post('/movies',
                                      json={
                                          'title': "test1",
                                          'release': "33"
                                      })
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_add_movie_failed(self):
        response = self.client().post('/movies',
                                      json={
                                          'title': "test1"
                                      })
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 422)

    def test_patch_actor_success(self):
        response = self.client().post('/actors/1',
                                      json={
                                          'name': "test221"
                                      })
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_patch_actor_failed(self):
        response = self.client().patch('/actors/100',
                                       json={
                                           'name': "test221"
                                       })
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_patch_movie_success(self):
        response = self.client().patch('/movies/1',
                                       json={
                                           'title': "test12"
                                       })
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    def test_patch_movie_failed(self):
        response = self.client().patch('/movies/100',
                                       json={
                                           'title': "test12"
                                       })
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_delete_actor_success(self):
        response = self.client().delete('/actors/1')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_delete_actor_failed(self):
        response = self.client().delete('/actors/100')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_delete_movie_success(self):
        response = self.client().delete('/movies/1')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_delete_movie_failed(self):
        response = self.client().delete('/movies/100')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
