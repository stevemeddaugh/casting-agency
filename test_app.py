import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import setup_db, Movie, Actor, db

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.database_name = "casting-agency"
        self.database_path = "postgres://postgres:stemed@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUzOWFmZjg0ZmNmMzIwY2FhOWNhMTFhIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDQwNTExMiwiZXhwIjoxNTg0NDkxNTEyLCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.gB5tgw6gMnMd4DAIjZ_hJrk_P7_qoZQEPdbJBe335louW0Bwpzzpx8PFilvq5zcWH8XqmDKSto2wubvGJ2u2XSnnT8AC42-tZs6DBHnONW9YtGDHNsCe2cPRd66snLJvHoZkTw52-XeEiegluxmn3og3yOZoSx6QRuNNSHlXC_iAL_CWCwSKb0Od_8CctUveLCBXePity1niVokesjdD4fpoDHMyRJ0-vN5O9d9lzzTYy_5SMEXNxP_Yu3TLnI4DCG_YBOUcps3QUKMw0Gv-ibuUrIumNwPzklxC8t8uV0XEXONPtWXWH5nYfjJYyXIK5kv7EcyRYPagw37cVhHjxA'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2YzE3MzUyYWU2YTgwYzhiYzI0NmUwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDQwNDk1MSwiZXhwIjoxNTg0NDkxMzUxLCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.WUQksuAWTpnpIIuHGSLfP9gRCS5EnucCDhnkgBiFHe4kLrpluPRCTIwXzI2P3amkFmi-9GWWkiRrSGElbeJ1L644iay_ua1AolOQCqG-wUHBMGe05FKQVlVIlrRYczzhO5PelE__ICVBhHMwEmSGxER5oewC1GJzyJUpduENbibr4r8XQg565mD4hbuHD17Y0udym-t7-ZTAXDCiJ28sjnmLAOiV24jfZnD730hmubgQRxA1BOXR_pMcYWNMULHlrm9ulOzIh9RTolgtycA9nMqjqNKeamS1IRc7gZv3DXmpPY3a2qSO3Hgll45BmvZtW11xlXM17VOlSfVx5BlRCg'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUyZjc1NTZiOGRhMjEwZTZlOWRlNmRjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDQwNjE1MSwiZXhwIjoxNTg0NDkyNTUxLCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.mNutgqOVrK9j-1Ck6Sywo77FbWO_YrkPWLOV6FcYyodJBf9JZuIXFhjmGgyj5fCxMUY4qhMuejhDHXbst_BG3FU5PRvrMlY8m2aIfdr8Ul0MPNQNAhcFvKnFwSfN_p8vCFHPjGV6qZLCeWVv2LWGhQkY6G3gdSW5jvyck3rX_XSAQS9rVVst3wzJWpnPdj-c-2HrjKnZeHWRtdLjDVvnBd-JYVNAZZvxSdUZJh2v9vhYLwmjFmnvJfQgjqW9-bRit0eb4QkP1Gwkikx3nCoSNOBC5ogC58SrcfqGYUXXlePiB7sU28Z7XCZCnJbMnz7jVlZi4N-7bA4SKZdK3atYNw'
        }

        self.movie = {
            'title': 'Avengers: Endgame',
            'release_date': '2019'
        }

        self.new_movie = {
            'title': 'Black Widow',
            'release_date': '2019'
        }

        self.actor = {
            'name': 'Scarlett Johansson',
            'age': '35',
            'gender': 'Female'
        }

        self.new_actor = {
            'name': 'Robert Downey Jr.',
            'age': '54',
            'gender': 'Male'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #Seed test data
        self.client().post('/movies', json=self.movie, headers=self.executive_producer_header)
        self.client().post('/actors', json=self.actor, headers=self.executive_producer_header)  

    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass

    # Test GET Actors
    def test_get_actors_public(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # Test GET Movies
    def test_get_movies_public(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_casting_director(self):
        res = self.client().get('/movies', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    # Test POST Actor
    def test_post_actors_public(self):
        res = self.client().post('/actors', json=self.new_actor)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_director(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_actors_executive_producer(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test POST Movie
    def test_post_movies_public(self):
        res = self.client().post('/movies', json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_executive_producer(self):
        original_count = len(Movie.query.all())

        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test PATCH Actor
    def test_patch_actors_public(self):
        res = self.client().patch('/actors/1', json={'age': "43"})

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_assistant(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_director(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_executive_producer(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch('/actors/1000', json={'age': "43"}, headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test PATCH Movie
    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_assistant(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_executive_producer(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch('/movies/1000', json={'title': "Updated Title"}, headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Actor
    def test_delete_actors_public(self):
        res = self.client().delete('/actors/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_assistant(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_director(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/1', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Movie
    def test_delete_movies_public(self):
        res = self.client().delete('/movies/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_assistant(self):
        res = self.client().delete('/movies/1', headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_director(self):
        res = self.client().delete('/movies/1', headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()