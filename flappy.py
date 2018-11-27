from tkinter import *
import random
import time
import pickle


class Score:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score

    def __lt__(self, other):
        if isinstance(other, Score):
            return self.score < other.score
        else:
            raise TypeError


class Ball:
    def __init__(self, canvas):
        self.move = True
        self.gravity = 1.5
        self.canvas = canvas
        self.id = self.canvas.create_oval(10, 180, 40, 210, fill='RED')

        # initial coordinates
        self.canvas.move(self.id, 30, 0)

    def fall(self):
        coords = self.get_position
        if self.move == True:
            self.canvas.move(self.id, 0, self.gravity)
            coords = self.get_position

        if coords[3] > 500:
            self.gravity = 0
            self.move = False

    def bounce(self, event):
        if self.move == True:
            self.canvas.move(self.id, 0, -40)

    @property
    def get_position(self):
        return self.canvas.coords(self.id)


class Pipe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.init_components()

    def init_components(self):
        starting_point = 400
        height_upper = random.randrange(120, 200)
        height_lower = random.randrange(230, 450)

        self.upper = self.canvas.create_rectangle(starting_point, 0, starting_point+60,
                                                  height_upper, fill='White')
        self.lower = self.canvas.create_rectangle(starting_point, height_lower, starting_point+60,
                                                  500, fill='White')

    def move(self):

        self.canvas.move(self.upper, -2.2, 0)
        self.canvas.move(self.lower, -2.2, 0)

    def hits(self, ball):
        coords_upper = self.canvas.coords(self.upper)
        coords_lower = self.canvas.coords(self.lower)
        coords = ball.get_position

        if coords[0] - coords_upper[0] <= 60 and coords[0] - coords_upper[0] >= -60 and coords[2] >= coords_upper[0]:
            if coords[1] + 30 >= coords_lower[1] or coords[1] <= coords_upper[3]:
                ball.move = False
                return True

    def dispose(self):
        self.canvas.delete(self.upper)
        self.canvas.delete(self.lower)
    
    def __del__(self):
        self.dispose()

class Game(Tk):
    def __init__(self):
        super().__init__()

        self.game = True
        self.title("Flappy Bird")
        self.resizable(0, 0)

        self.init_components()

    def init_components(self):
        self.canvas = Canvas(self, width=400, height=500, bg="orange")
        self.ball = Ball(self.canvas)

        self.canvas.pack()

    def start_game(self):
        score = 0
        frame_count = 0
        pipes = [Pipe(self.canvas)]
        difficulty = 85

        score_label = Label(self, text="0", fg="BLACK", font=("HELVETICA", 15))
        self.canvas.create_window(
            350, 40, window=score_label, width=40, height=40)
        self.canvas.bind('<Button-1>', self.ball.bounce)

        while self.game:
            self.ball.fall()
            for pipe in pipes:
                pipe.move()

            if pipes[0].hits(self.ball):
                self.game = False
                del pipes
                self.destroy()

                return score

            elif self.canvas.coords(pipes[0].upper)[0] + 60 < 0:
                score += 1
                score_label.config(text=str(score))
                pipes.pop(0)

            if frame_count % difficulty == 0 and frame_count:
                pipes.append(Pipe(self.canvas))
                frame_count = 0

            if score > 10:
                difficulty = 80
            elif score > 20:
                difficulty = 75

            frame_count += 1
            time.sleep(0.01)

            self.update()
            self.update_idletasks()


class GameOver(Tk):
    def __init__(self, score):
        super().__init__()

        self.resizable(0, 0)
        self.title("Game Over!")

        self.score = score
        self.init_components()
        self.mainloop()

    def init_components(self):
        self.canvas = Canvas(self, height=500, width=400)
        self.canvas.pack()

        self.canvas.create_text(200, 100, text='GAME OVER', fill='BLACK',
                                font=('Comic San MS', 50, 'bold'))
        self.canvas.create_text(200, 150, text='YOUR SCORE IS :'
                                + str(self.score), fill='BLACK',
                                font=('Comic San MS', 25, 'bold'))

        if self.check_leaderboard_eligibility(self.score):
            self.__get_name()

        else:
            self.__show_leaderboard()

    def __show_leaderboard(self):
        leaderboard = self.get_leaderboard()
        leaderboard = sorted(leaderboard, reverse=True)

        y = 300     # y coord of score text
        for score in leaderboard:
            self.canvas.create_text(200, y, text=score.name + ': '
                                    + str(score.score), fill='BLACK',
                                    font=('Comic San MS', 20, 'bold'))
            y = y + 50

        # restart button
        self.restart_button = Button(
            self.canvas, text='RESTART', command=self.restart)
        self.canvas.create_window(200, 200, window=(
            self.restart_button), height=30, width=80)

    @staticmethod
    def get_leaderboard():
        try:
            with open("leaderboards.txt", "rb") as f:
                scores = pickle.load(f)
        except FileNotFoundError:
            scores = [Score("name_1", 1), Score(
                "name_2", 2), Score("name_3", 3)]

            with open("leaderboards.txt", "wb") as f:
                pickle.dump(scores, f)

        return scores

    def __update_leaderboard(self):
        name = self.name.get()
        score = self.score
        new_score = Score(name, score)

        leaderboard = self.get_leaderboard()
        leaderboard.append(new_score)
        leaderboard = sorted(leaderboard, reverse=True)

        with open("leaderboards.txt", "wb") as f:
            pickle.dump(leaderboard[:3], f)

        for widget in self.name_entry_widgets:
            self.canvas.delete(widget)

        self.__show_leaderboard()

    @classmethod
    def check_leaderboard_eligibility(cls, current_score):
        scores = cls.get_leaderboard()
        for score in scores:
            if(score.score <= current_score):
                return True
        return False

    def restart(self):
        self.destroy()
        main()

    def __get_name(self):
        self.name_entry_widgets = []

        # name text field
        self.name = Entry(self.canvas)
        self.window_for_name = self.canvas.create_window(
            200, 420, window=(self.name), height=25, width=80)

        self.name_entry_widgets.append(self.window_for_name)

        # label for the text field
        self.for_name_entry = Label(
            self.canvas, text="ENTER YOUR NAME", bg="WHITE")
        self.window_for_name_label = self.canvas.create_window(
            80, 420, window=(self.for_name_entry), height=30, width=120)

        self.name_entry_widgets.append(self.window_for_name_label)

        # submit button
        self.submit = Button(self.canvas, text='ENTER',
                             command=self.__update_leaderboard)
        self.window_for_submit = self.canvas.create_window(
            200, 450, window=(self.submit), height=30, width=80)

        self.name_entry_widgets.append(self.window_for_submit)


def main():
    new_game = Game()
    score = new_game.start_game()
    end_game = GameOver(score)


if __name__ == '__main__':
    main()
