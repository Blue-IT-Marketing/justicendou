import os
import jinja2
from flask import Blueprint, request, render_template
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

algorithms_handler_bp = Blueprint('algorithms_handler', __name__)


def route_algorithms():
    """
        **route_algorithms**
    :return:
    """
    # Load specific algos specific variables here
    return render_template("algorithms/algos.html"), 200


def route_strange():
    """load strange attractors settings here """
    return render_template("algorithms/strange/strange.html"), 200


def route_perlin():
    """load perlin settings here"""
    return render_template("algorithms/perlin/perlin.html"), 200


def route_life():
    """load game of life settings here"""
    return render_template("algorithms/gameoflife/life.html"), 200


def route_maze():
    """load maze settings here"""
    return render_template("algorithms/maze/maze.html"), 200


def route_path():
    """load routing algo settings here"""
    return render_template("algorithms/pathfinder/path.html"), 200


def route_matter():
    """load matter settings here"""
    return render_template("algorithms/matter/matter.html"), 200


def route_matrix():
    return render_template("games/matrix/matrix.html"), 200


def route_plinko():
    return render_template("algorithms/plinko/plinko.html"), 200


def route_maze_solver():
    return render_template("algorithms/mazepath/mazepath.html"), 200


@algorithms_handler_bp.route('/algorithms/<string:path>', methods=['GET'])
def algorithms_handler(path: str):
    """

    :param path:
    :return:
    """
    algorithm_lookup: dict = dict(strange=route_strange, perlin=route_perlin,
                                  matrix=route_matrix, gameoflife=route_life,
                                  maze=route_maze, path=route_path,
                                  plinko=route_plinko, mazesolver=route_maze_solver)

    return algorithm_lookup[path]()


@algorithms_handler_bp.route('/algorithms', methods=["GET"])
def algorithms():
    return route_algorithms()
