from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from raterapi.models import GameRating, Game
from django.contrib.auth.models import User


class GameRatingView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        game_rating = GameRating()
        player = User.objects.get(id=request.auth.user_id)
        game_rating.player = player
        game = Game.objects.get(pk=request.data["game"])
        game_rating.game = game
        game_rating.rating = request.data["rating"]

        try:
            game_rating.save()
            serializer = GameRatingSerializer(game_rating, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = GameRating.objects.get(pk=pk)
            serializer = GameRatingSerializer(game, context={'request': request})
            return Response(serializer.data)
        except GameRating.DoesNotExist as ex:
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
        game_rating = GameRating.objects.get(pk=pk)
        game_rating.player = User.objects.get(id=request.auth.user_id)
        game_rating.game = Game.objects.get(pk=request.data["game"])
        game_rating.rating = request.data["rating"]

        game_rating.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game ratings by user
        game_ratings = GameRating.objects.all()

        # Support filtering game ratings by game
        game = self.request.query_params.get('gameId', None)
        if game is not None:
            game_ratings = game_ratings.filter(game__id=game)

        serializer = GameRatingSerializer(
            game_ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game_rating = GameRating.objects.get(pk=pk)
            game_rating.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['get'], detail=True)
    def user_rating(self, request, pk=None):
        """Retrieves single game rating by authorized user"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        try:
            # Handle the case if the client specifies a game
            # that doesn't exist
            game = Game.objects.get(pk=pk)
            game_ratings = GameRating.objects.filter(game__id=game.id)
            player = User.objects.get(id=request.auth.user_id)
            game_rating = game_ratings.filter(player__id=player.id)
            player_rating = game_rating[0]
            serializer = GameRatingSerializer(player_rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({})


class GameRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = GameRating
        fields = ('id', 'player', 'game', 'rating')