import tkinter as tk
import random as r


# W = width, H = height, X = x-coordinate, Y = y-coordinate
WINDOW_W = 550
WINDOW_H = 305
CANVAS_W = 400
CANVAS_H = 300
BOARD_X = CANVAS_W+15
BALL_W = 30
BASKET_W = 90
BASKET_X = 160
BASKET_Y = 100

# Info of game
GAME_POINT = 0
TIME = 10


class Ball(tk.Button):
    def __init__(self, root, num):
        super().__init__(
            root, text = 'ball', width=1, height=2, font=("",10)
        )
        self.mouse_xy = None  # coordinates of a cursor
        self.xy = None        # coordinates of a ball
        self.ball_place()

        # Event handlers for clicking, moving, and releasing a ball
        self.bind("<Button-1>",self.ball_click)
        self.bind("<B1-Motion>",self.ball_move)
        self.bind("<ButtonRelease-1>",self.ball_stop)

    # Randomly locate the first position of a ball in a canvas field without overlapping a basket
    def ball_place(self):
        num = r.randint(0,1)
        num2 = r.randint(2,3)
        if num == 0:
            x = r.randint(10, CANVAS_W-40)
            if num2 == 2:
                y = r.randint(10, BASKET_Y-40)
            else:
                y = r.randint(BASKET_Y+BASKET_W, CANVAS_H-40)
        else:
            if num2 == 2:
                x = r.randint(10, BASKET_X-40)
            else:
                x = r.randint(BASKET_X+BASKET_W, CANVAS_W-40)
            y = r.randint(10, CANVAS_H-40)
        self.place(x = x, y = y)
    
    # Detect cordinates of a ball and a cursor
    def ball_click(self, evnt):
        self.mouse_xy = (evnt.x_root, evnt.y_root)
        place_info = evnt.widget.place_info()
        ball_x = int(place_info['x'])
        ball_y = int(place_info['y'])
        self.xy = (ball_x, ball_y)

    def ball_move(self, evnt):
        # Distance between coordinates of a mouse after moved and those at origin
        dst = (evnt.x_root - self.mouse_xy[0], evnt.y_root - self.mouse_xy[1])

        # Coordinates of a ball at origin + moving distance
        place_info = evnt.widget.place_info()
        place_info['x'] = self.xy[0] + dst[0]
        place_info['y'] = self.xy[1] + dst[1]
        evnt.widget.place_configure(place_info)

    # Inittialize coordinates
    def ball_stop(self, evnt):
        self.ball_evaluate(evnt)
        self.mouse_xy = None
        self.xy = None

    # Evaluate a spot where a ball has been dropped down
    def ball_evaluate(self, evnt):
        global GAME_POINT

        # Get coordinates of a ball
        place_info = evnt.widget.place_info()
        ball_x = int(place_info["x"])
        ball_y = int(place_info["y"])
        
        # Whether a ball is outside canvas?
        if ((ball_x < 0)
        or (ball_y < 0)
        or (CANVAS_W < ball_x+BALL_W)
        or (CANVAS_H < ball_y+BALL_W)):
            self.ball_place()

        # Whether a ball is in a basket?
        elif ((BASKET_X < ball_x)
        and (ball_x+BALL_W < BASKET_X+BASKET_W)
        and (BASKET_Y < ball_y)
        and (ball_y+BALL_W < BASKET_Y+BASKET_W)):
            self.ball_place()
            GAME_POINT += 1


class CanvasField(tk.Canvas):
    def __init__(self, root):
        # Set up a canvas 
        super().__init__(
            root, width=CANVAS_W, height=CANVAS_H, bg="black"
        )
        self.place(x = 0, y = 0)

        # Draw a basket field in a canvas
        self.create_oval(
            BASKET_X, BASKET_Y,
            BASKET_X+BASKET_W, BASKET_Y+BASKET_W,
            fill = "Red"
        )

        # "Basket" at the center
        lbl_basket = tk.Label(root, font = ("System", 16), text = "Basket", foreground='White', background='Red')
        lbl_basket.place(x = BASKET_X+(BASKET_W/2-27), y = BASKET_Y+(BASKET_W/2-11))


class ScoreBoard():
    def __init__(self, root):
        self.root = root
        self.score = tk.Label(root, font = ("System", 16), text = f"Score : {GAME_POINT}")
        self.score.place(x = BOARD_X, y = WINDOW_H/4)
        self.timer = tk.Label(root, font = ("System", 16), text = f"Time : {TIME}s")
        self.timer.place(x = BOARD_X, y = WINDOW_H/3)
        
        # ButtonRelease-1 = left click
        root.bind("<ButtonRelease-1>", self.update_score)

    # Update a score board
    def update_score(self, evnt):
        self.score["text"] = f"Score : {GAME_POINT}"

    # Update timer and a time board
    def update_time(self):
        global TIME
        TIME -= 1
        self.timer["text"] = f"Time : {TIME}s"
        if TIME == 0:
            return
        self.root.after(1000, self.update_time)


class BallTossGame():
    # global TIME
    def __init__(self, root):
        self.root = root
        self.board = ScoreBoard(root)
        self.canvas = CanvasField(root)
        self.balls = []  # Ball instances go in

    # Create a ball instance
    def ball_create(self):
        for num in range(1,6):
            ball = Ball(self.root, num)
            self.balls.append(ball)

    # Delete all ball instances
    def ball_destroy(self):
        for ball in self.balls:
            ball.destroy()

    # Start a timer
    def timer_start(self):
        self.root.after(1000, self.board.update_time)

    # Reset info of the game point, time, and score board and direct deletion of balls
    def game_reset(self):
        global GAME_POINT, TIME
        GAME_POINT = 0
        TIME = 10
        self.board.score["text"] = f"Score : {GAME_POINT}"
        self.board.timer["text"] = f"Time : {TIME}s"
        self.ball_destroy()


class GameHandler():
    def __init__(self, root, game):
        self.root = root
        self.game = game
        
        # Start button
        self.btn = tk.Button(root, text='START', command = self.game_start)
        self.btn.place(x= BOARD_X, y=WINDOW_H/8)

    # Start a game after clicking a start button
    def game_start(self):
        self.game_btn_toggle()
        self.game.game_reset()
        self.game.ball_create()
        self.game.timer_start()
        self.root.after(10000, self.game_end)

    # Operation after a game has finished
    def game_end(self):
        self.game_btn_toggle()
        self.game.ball_destroy()

    # Switch activeness of a start button
    def game_btn_toggle(self):
        if self.btn["state"] == "normal":
            self.btn["state"] = "disable"
        else:
            self.btn["state"] = "normal"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Application window
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.title("Ball-toss game")

        # Create game objects
        game = BallTossGame(self)
        GameHandler(self, game)


def main():
    # Create GUI application
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()