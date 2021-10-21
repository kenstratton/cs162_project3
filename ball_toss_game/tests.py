# Tests for the classes of the project-3 appllication
from app import *
import pytest


# Objects from classes in the application
app = Application()
game = BallTossGame(app)
gm_hndlr = GameHandler(app, game)
board = ScoreBoard(app)
canvas = CanvasField(app)
ball = Ball(app)

# Tests for Application
def test_init_application():
    assert app.geometry()
    assert app.title() == "Ball-toss game"


# Tests for GameHandler
def test_init_gamehandler():
    assert gm_hndlr.root == app
    assert gm_hndlr.game == game
    assert gm_hndlr.btn["text"] == "START"


# Tests for BallTossGame
def test_init_game():
    assert game.canvas
    assert game.board

def test_methods_game():
    # Create balls
    game.ball_create()
    assert len(game.balls) == 5

    # Remove balls
    game.ball_destroy()
    assert len(game.balls) == 0


# Tests for ScoreBoard
def test_init_scoreboard():
    assert board.score["text"] == "Score : 0"
    assert board.timer["text"] == "Time : 10s"


# Tests for CanvasField
def test_init_canvas():
    assert canvas["bg"] == "black"
    assert canvas.lbl_basket["text"] == "Basket"


# Tests for Ball
def test_init_ball():
    assert ball["text"] == "ball"
    assert ball.mouse_xy == None
    assert ball.xy == None