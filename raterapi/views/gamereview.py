from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import GameReview, Game
from django.contrib.auth.models import User


class GameReviewView(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        game_review = GameReview()
        player = User.objects.get(id=request.auth.user_id)
        game_review.player = player
        game = Game.objects.get(pk=request.data["game"])
        game_review.game = game
        game_review.review = request.data["review"]

        try:
            game_review.save()
            serializer = GameReviewSerializer(game_review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = GameReview.objects.get(pk=pk)
            serializer = GameReviewSerializer(game, context={'request': request})
            return Response(serializer.data)
        except GameReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game_review = GameReview.objects.get(pk=pk)
        game_review.player = User.objects.get(id=request.auth.user_id)
        game_review.game = Game.objects.get(pk=request.data["game"])
        game_review.review = request.data["review"]

        game_review.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game reviews by user
        game_reviews = GameReview.objects.all()

        # Support filtering game reviews by game
        game = self.request.query_params.get('gameId', None)
        if game is not None:
            game_reviews = game_reviews.filter(game__id=game)

        serializer = GameReviewSerializer(
            game_reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game_review = GameReview.objects.get(pk=pk)
            game_review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GameReviewSerializer(serializers.ModelSerializer):

    player = PlayerSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ('id', 'player', 'game', 'review')