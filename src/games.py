import os
import jinja2
from flask import Blueprint, request, render_template

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

games_handler_bp = Blueprint('games_handler', __name__)


def route_games():
    return render_template("games/games.html")


def route_tetris():
    return render_template("games/tetris/tetris.html")


def route_pacman():
    return render_template("games/pacman/pacman.html")


def route_chess():
    return render_template("games/garbo/chess.html")


def route_checkers():
    return render_template("games/checkers/checkers.html")


def route_ping_pong():
    return render_template("games/pingpong/pingpong.html")


def route_snake():
    return render_template("games/snake/snake.html")


@games_handler_bp.route('/games', methods=['GET'])
def games():
    return route_games()


@games_handler_bp.route('/games/<string:path>', methods=['GET'])
def games_router(path: str):
    """

    :return:
    """
    if path == 'tetris':
        return route_tetris()
    elif path == 'pacman':
        return route_pacman()
    elif path == 'chess':
        return route_chess()
    elif path == 'checkers':
        return route_checkers()
    elif path == 'pingpong':
        return route_ping_pong()
    elif path == 'snake':
        return route_snake()
