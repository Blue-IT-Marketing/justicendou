import os
import jinja2
from flask import Blueprint, request, render_template

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

algorithms_handler_bp = Blueprint('algorithms_handler', __name__)


def route_algorithms():
    return render_template("algorithms/algos.html")


def route_strange():
    return render_template("algorithms/strange/strange.html")


def route_perlin():
    return render_template("algorithms/perlin/perlin.html")


def route_life():
    return render_template("algorithms/gameoflife/life.html")


def route_maze():
    return render_template("algorithms/maze/maze.html")


def route_path():
    return render_template("algorithms/pathfinder/path.html")


def route_matter():
    return render_template("algorithms/matter/matter.html")


def route_matrix():
    return render_template("games/matrix/matrix.html")


def route_plinko():
    return render_template("algorithms/plinko/plinko.html")


def route_maze_solver():
    return render_template("algorithms/mazepath/mazepath.html")


@algorithms_handler_bp.route('/algorithms/<string:path>', methods=['GET'])
def algorithms_handler(path: str):
    """

    :param path:
    :return:
    """
    if path == "strange":
        return route_strange()
    elif path == "perlin":
        return route_perlin()
    elif path == "matrix":
        return route_matrix()
    elif path == "gameoflife":
        return route_life()
    elif path == "maze":
        return route_maze()
    elif path == "path":
        return route_path()
    elif path == "plinko":
        return route_plinko()
    elif path == "mazesolver":
        return route_maze_solver()


def route_algorithms():
    return render_template("algorithms/algos.html")


@algorithms_handler_bp.route('/algorithms', methods=["GET"])
def algorithms():
    return route_algorithms()
