import os
import jinja2
from flask import Blueprint, request, render_template

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

games_handler_bp = Blueprint('games_handler', __name__)


def route_games():
    """load game specific resources here"""
    return render_template("games/games.html"), 200


def route_tetris():
    """load game specific resources here"""
    return render_template("games/tetris/tetris.html"), 200


def route_pacman():
    """load game specific resources here"""
    return render_template("games/pacman/pacman.html"), 200


def route_chess():
    """load game specific resources here"""
    return render_template("games/garbo/chess.html"), 200


def route_checkers():
    """load game specific resources here"""
    return render_template("games/checkers/checkers.html"), 200


def route_ping_pong():
    """load game specific resources here"""
    return render_template("games/pingpong/pingpong.html"), 200


def route_snake():
    """load game specific resources here"""
    return render_template("games/snake/snake.html"), 200


@games_handler_bp.route('/games', methods=['GET'])
def games():
    """load game specific resources here"""
    return route_games()


@games_handler_bp.route('/games/<string:path>', methods=['GET'])
def games_router(path: str) -> tuple:
    """
        **games_router**
            routes game requests by path and load the relevant template for the game
    :return: tuple
    """
    return dict(tetris=route_tetris, pacman=route_pacman, chess=route_chess, checkers=route_checkers,
                pingpong=route_ping_pong, snake=route_snake).get(path)()
