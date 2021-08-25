import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapi.models import Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        url = "/games"
        data = {
            "title": "Welcome To",
            "description": "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more.",
            "designer": "Benoit Turpin",
            "year_released": 2018,
            "number_of_players": 4,
            "gameplay_duration": 30,
            "age_recommendation": 10,
            "categories": []
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["title"], "Welcome To")
        self.assertEqual(json_response["description"], "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more.")
        self.assertEqual(json_response["designer"], "Benoit Turpin")
        self.assertEqual(json_response["year_released"], 2018)
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["gameplay_duration"], 30)
        self.assertEqual(json_response["age_recommendation"], 10)
        self.assertEqual(json_response["categories"], [])

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """
        game = Game()
        game.title = "Welcome To"
        game.description = "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more."
        game.designer = "Benoit Turpin"
        game.year_released = 2018
        game.number_of_players = 4
        game.gameplay_duration = 30
        game.age_recommendation = 10
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "Welcome To")
        self.assertEqual(json_response["description"], "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more.")
        self.assertEqual(json_response["designer"], "Benoit Turpin")
        self.assertEqual(json_response["year_released"], 2018)
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["gameplay_duration"], 30)
        self.assertEqual(json_response["age_recommendation"], 10)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.title = "Welcome To"
        game.description = "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more."
        game.designer = "Benoit Turpin"
        game.year_released = 2018
        game.number_of_players = 4
        game.gameplay_duration = 30
        game.age_recommendation = 10
        game.save()

        data = {
            "title": "Welcome To",
            "description": "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more.",
            "designer": "Benoit Turpin",
            "year_released": 2017,
            "number_of_players": 5,
            "gameplay_duration": 45,
            "age_recommendation": 12
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "Welcome To")
        self.assertEqual(json_response["description"], "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more.")
        self.assertEqual(json_response["designer"], "Benoit Turpin")
        self.assertEqual(json_response["year_released"], 2017)
        self.assertEqual(json_response["number_of_players"], 5)
        self.assertEqual(json_response["gameplay_duration"], 45)
        self.assertEqual(json_response["age_recommendation"], 12)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.title = "Welcome To"
        game.description = "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more."
        game.designer = "Benoit Turpin"
        game.year_released = 2018
        game.number_of_players = 4
        game.gameplay_duration = 30
        game.age_recommendation = 10
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
