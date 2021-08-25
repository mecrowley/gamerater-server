import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapi.models import Game, GameRating


class GameRatingTests(APITestCase):
    def setUp(self):
        """
        Create a new account
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

        game = Game()
        game.title = "Welcome To"
        game.description = "As an architect in Welcome To..., you want to build the best new town in the United States of the 1950s by adding resources to a pool, hiring employees, and more."
        game.designer = "Benoit Turpin"
        game.year_released = 2018
        game.number_of_players = 4
        game.gameplay_duration = 30
        game.age_recommendation = 10
        game.save()


    def test_create_gamerating(self):
        """
        Ensure we can create a new game rating.
        """
        url = "/gameratings"
        data = {
            "game": 1,
            "rating": 10,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["game"], 1)
        self.assertEqual(json_response["rating"], 10)


    def test_change_gameratingpy(self):
        """
        Ensure we can change an existing game.
        """
        gamerating = GameRating()
        gamerating.player_id = 1
        gamerating.game_id = 1
        gamerating.rating = 10
        gamerating.save()

        data = {
            "game": 1,
            "rating": 10
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/gameratings/{gamerating.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/gameratings/{gamerating.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["game"], 1)
        self.assertEqual(json_response["rating"], 10)
