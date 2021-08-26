"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from raterapi.models import Game
from raterreports.views import Connection


def bottom5gameratings_list(request):
    """Function to build an HTML report of the top 5 games by ratings"""
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    g.title,
                    gr.game_id,
                    gr.rating
                FROM
                    raterapi_game g
                JOIN
                    raterapi_gamerating gr ON g.id = gr.game_id
                GROUP BY g.title
                ORDER BY gr.rating ASC
                LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            bottom5games = []

            for row in dataset:
                game = Game()
                game.game_id = row["game_id"]
                game.title = row["title"]
                game.rating = row["rating"]

                bottom5games.append(game)


        template = 'games/list_with_bottom_game_ratings.html'
        context = {
            'bottom5gameratings_list': bottom5games
        }

        return render(request, template, context)
