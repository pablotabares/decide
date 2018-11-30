from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 5},
                {'option': 'Option 2', 'number': 2, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votes': 3},
                {'option': 'Option 4', 'number': 4, 'votes': 2},
                {'option': 'Option 5', 'number': 5, 'votes': 5},
                {'option': 'Option 6', 'number': 6, 'votes': 1},
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5},
            {'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5},
            {'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3},
            {'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2},
            {'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_weighted_random_test1(self):
        # Test 1: It will check there is only one option which is selected.

        data = {
            'type': 'WEIGHTED-RANDOM',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 2},
                {'option': 'Option 2', 'number': 2, 'votes': 1}
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        selected = False
        for v in values:
            if selected and v['postproc'] == True:
                selected = False
                print("Two values are selected!")
                break
            if v['postproc'] == True:
                selected = True

        self.assertTrue(selected)

    def test_weighted_random_test2(self):
        # Test 2: It will check its first option is selected, because others options has no votes.

        data = {
            'type': 'WEIGHTED-RANDOM',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 1},
                {'option': 'Option 2', 'number': 2, 'votes': 0}
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        firstTrue = False
        if values[0]['postproc'] == True:
            firstTrue = True

        selected = False
        for v in values:
            if selected and v['postproc'] == True:
                selected = False
                print("Two values are selected!")
                break
            if v['postproc'] == True:
                selected = True

        self.assertTrue(firstTrue)
        self.assertTrue(selected)

    def test_weighted_random_test3(self):
        # Test 3: It will check no option is selected, because there is no votes.
        data = {
            'type': 'WEIGHTED-RANDOM',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votes': 0}
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        selected = False
        for v in values:
            if v['postproc'] == True:
                selected = True
                break

        self.assertFalse(selected)

    def test_hondt(self):
        data = {
            "type": "HONDT",
            "seats": 7,
            "options": [{
                "votes": 340000,
                "option": "Option 1",
                "number": 1
            }, {
                "votes": 280000,
                "option": "Option 2",
                "number": 2
            }, {
                "votes": 160000,
                "option": "Option 3",
                "number": 3
            }, {
                "votes": 60000,
                "option": "Option 4",
                "number": 4
            }, {
                "votes": 15000,
                "option": "Option 5",
                "number": 5
            }]
        }

        expected_result = [
            {
                "votes": 340000,
                "option": "Option 1",
                "number": 1,
                "postproc": 3
            },
            {
                "votes": 280000,
                "option": "Option 2",
                "number": 2,
                "postproc": 3
            },
            {
                "votes": 160000,
                "option": "Option 3",
                "number": 3,
                "postproc": 1
            },
            {
                "votes": 60000,
                "option": "Option 4",
                "number": 4,
                "postproc": 0
            },
            {
                "votes": 15000,
                "option": "Option 5",
                "number": 5,
                "postproc": 0
            }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_weight(self):
        data = {
            "type": "WEIGHT",
            "options": [{
                "votes": 2000,
                "option": "Option 1",
                "number": 1,
                "weight": 1
            }, {
                "votes": 1000,
                "option": "Option 2",
                "number": 2,
                "weight": 2
            }, {
                "votes": 1000,
                "option": "Option 3",
                "number": 3,
                "weight": 3
            }, {
                "votes": 501,
                "option": "Option 4",
                "number": 4,
                "weight": 2
            }, {
                "votes": 360,
                "option": "Option 5",
                "number": 5,
                "weight": 3
            }, {
                "votes": 100,
                "option": "Option 6",
                "number": 6,
                "weight": 3
            }]
        }

        expected_result = [
            {
                "votes": 1000,
                "option": "Option 3",
                "number": 3,
                "weight": 3,
                "postproc": 3000
            },
            {
                "votes": 2000,
                "option": "Option 1",
                "number": 1,
                "weight": 1,
                "postproc": 2000
            },
            {
                "votes": 1000,
                "option": "Option 2",
                "number": 2,
                "weight": 2,
                "postproc": 2000
            },
            {
                "votes": 360,
                "option": "Option 5",
                "number": 5,
                "weight": 3,
                "postproc": 1080
            },
            {
                "votes": 501,
                "option": "Option 4",
                "number": 4,
                "weight": 2,
                "postproc": 1002
            },
            {
                "votes": 100,
                "option": "Option 6",
                "number": 6,
                "weight": 3,
                "postproc": 300
            }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_borda(self):
        data = {
            "type": "BORDA",
            "options": [{
                "option": "Futbol",
                "positions": [1, 1, 4, 5, 1]
            }, {
                "option": "Baloncesto",
                "positions": [3, 3, 2, 1, 2]
            }, {
                "option": "Tenis",
                "positions": [5, 2, 5, 2, 3]
            }, {
                "option": "Natacion",
                "positions": [2, 5, 1, 3, 4]
            }, {
                "option": "Correr",
                "positions": [4, 4, 3, 4, 5]
            }]
        }

        expected_result = {
            "Futbol": 18,
            "Baloncesto": 19,
            "Tenis": 13,
            "Natacion": 15,
            "Correr": 10
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)