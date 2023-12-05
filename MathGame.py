import wx
import random
import operator
import time


# above we imported all of the necessary libraries and modules for the game

# below we create the main class of the main game which initializes the UI interface for the math game
# we initialize the labels and create the window, buttons and text controls for the game
# we also initialize variables and load higher scores and set up a timer for the game
class MathGame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Math Game", size=(300, 400))
        self.panel = wx.Panel(self)
        self.title_label = wx.StaticText(self.panel, label="Math Game", pos=(100, 20))
        self.title_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button = wx.Button(self.panel, label="START", pos=(100, 60), size=(100, 40))
        self.start_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button_clicked)
        self.casual_button = wx.Button(self.panel, label='CASUAL', pos=(50, 60), size=(80, 40))
        self.casual_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.casual_button.Bind(wx.EVT_BUTTON, self.on_casual_button_clicked)
        self.casual_button.Hide()
        self.timed_button = wx.Button(self.panel, label='TIMED', pos=(150, 60), size=(80, 40))
        self.timed_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.timed_button.Bind(wx.EVT_BUTTON, self.on_timed_button_clicked)
        self.timed_button.Hide()
        self.countdown_label = wx.StaticText(self.panel, label="", pos=(140, 60))
        self.countdown_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.countdown_label.Hide()
        self.question_label = wx.StaticText(self.panel, label="", pos=(100, 120))
        self.question_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.answer_text_ctrl = wx.TextCtrl(self.panel, pos=(100, 150), size=(100, 20), style=wx.TE_PROCESS_ENTER)
        self.answer_text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_answer_enter)
        self.next_button = wx.Button(self.panel, label="Next", pos=(100, 180), size=(100, 30))
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button_clicked)
        self.next_button.Hide()
        self.timed_next_button = wx.Button(self.panel, label="Next", pos=(100, 180), size=(100, 30))
        self.timed_next_button.Bind(wx.EVT_BUTTON, self.on_timed_next_button_clicked)
        self.timed_next_button.Hide()
        self.restart_button = wx.Button(self.panel, label="Restart", pos=(100, 180), size=(100, 30))
        self.restart_button.Bind(wx.EVT_BUTTON, self.on_restart_button_clicked)
        self.restart_button.Hide()
        self.leaderboard_button = wx.Button(self.panel, label="Casual Leaderboard", pos=(90, 220), size=(120, 30))
        self.leaderboard_button.Bind(wx.EVT_BUTTON, self.show_leaderboard)
        self.timed_leaderboard_button = wx.Button(self.panel, label="Timed Leaderboard", pos=(90, 260), size=(120, 30))
        self.timed_leaderboard_button.Bind(wx.EVT_BUTTON, self.show_timed_leaderboard)
        self.questions = []
        self.timed_questions = []
        self.timed_answers = []
        self.answers = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.high_scores = self.load_high_scores()
        self.timed_high_scores = self.load_timed_high_scores()
        self.generate_questions()
        self.generate_timed_questions()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_check, self.timer)

# below we generate 10 random arithmetics questions that can be increased by decreased
# in the definition below it randomly selects answers operators symbols from the dictonary,
# and generates the random numbers
# the questions are answers and stored in a separate list
    def generate_questions(self):
        operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        for _ in range(10):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator_symbol = random.choice(list(operators.keys()))
            question = f"{num1} {operator_symbol} {num2}"
            answer = operators[operator_symbol](num1, num2)
            self.questions.append(question)
            self.answers.append(answer)

# below this definition generates a list of 300 timed math questions. given a limited time to solve and many as you can
    def generate_timed_questions(self):
        operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        for _ in range(300):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator_symbol = random.choice(list(operators.keys()))
            question = f"{num1} {operator_symbol} {num2}"
            answer = operators[operator_symbol](num1, num2)
            self.timed_questions.append(question)
            self.timed_answers.append(answer)

# begin the definitions updates the labels of the questions and clearing the values,
    # keeps track of the current questions index
    def show_question(self):
        self.question_label.SetLabel(self.questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

# this definition does the same as the one above but for the timed mode
    def show_timed_question(self):
        self.question_label.SetLabel(self.timed_questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

# this definition triggers when the start button is clicked in the hides the buttons and shows two other buttons
    def on_start_button_clicked(self, event):
        self.start_button.Hide()
        self.casual_button.Show()
        self.timed_button.Show()

# when casual_button is clicked it selects the global variables gamemode to 1 and hides several buttons,
    # and calls the function show_question()
    def on_casual_button_clicked(self, event):
        global gamemode
        gamemode = 1
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.next_button.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.show_question()

# this definition does the same as the one above, but it starts a timer and calls the timed_questions
    def on_timed_button_clicked(self, event):
        global gamemode
        global start_time
        gamemode = 2
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.timed_next_button.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.countdown_label.Show()
        self.countdown_label.SetLabel("60")
        self.timer.Start(1000)
        start_time = time.time()
        self.show_timed_question()

# this definition is responsible for updating the countdown and calculates the elapsed time until the reset 60 seconds
    def timer_check(self, event):
        global stopwatch
        global start_time
        global gamemode
        stopwatch = time.time() - start_time
        countdown = 60.0 - stopwatch
        countdown = round(countdown)
        countdown = str(countdown)
        self.countdown_label.SetLabel(countdown)
        if stopwatch >= 60:
            print('Time!')
            self.timer.Stop()
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.countdown_label.SetLabel("")
            self.countdown_label.Hide()
            self.show_timed_score()
            gamemode = 3

#this definition checks the global variables called gamemode, and performs different actions based on its values
        #if gamemode must is 1 then it calls on next button clicked
    def on_answer_enter(self, event):
        global gamemode
        if gamemode == 1:
            self.on_next_button_clicked(event)
        elif gamemode == 2:
            self.on_timed_next_button_clicked(event)
        else:
            pass

    def on_next_button_clicked(self, event):
        self.check_answer()
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.show_score()

    def on_timed_next_button_clicked(self, event):
        global stopwatch
        global start_time
        self.check_timed_answer()
        self.current_question_index += 1
        stopwatch = time.time() - start_time
        print(stopwatch)
        self.show_timed_question()

    def on_restart_button_clicked(self, event):
        self.current_question_index = 0
        self.correct_answers = 0
        self.questions = []
        self.timed_questions = []
        self.answers = []
        self.timed_answers = []
        self.generate_questions()
        self.generate_timed_questions()
        self.restart_button.Hide()
        self.casual_button.Show()
        self.timed_button.Show()

    def check_answer(self):
        user_answer = self.answer_text_ctrl.GetValue()
        correct_answer = eval((self.questions[self.current_question_index]))
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def check_timed_answer(self):
        user_answer = self.answer_text_ctrl.GetValue()
        correct_answer = eval((self.timed_questions[self.current_question_index]))
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def show_score(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers / total_questions) * 100
        self.question_label.SetLabel(f"Your score: {score_percentage:.2f}%")
        self.next_button.Hide()
        self.restart_button.Show()
        self.update_high_scores(score_percentage)

    def show_timed_score(self):
        final_score = self.correct_answers * 10
        self.question_label.SetLabel(f"Your score: {final_score:.2f}")
        self.timed_next_button.Hide()
        self.restart_button.Show()
        self.update_timed_high_scores(final_score)

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [float(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            with open("high_scores.txt", "w"):
                high_scores = []
        return high_scores

    def load_timed_high_scores(self):
        try:
            with open("timed_high_scores.txt", "r") as file:
                timed_high_scores = [float(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            with open("timed_high_scores.txt", "w"):
                timed_high_scores = []
        return timed_high_scores

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def save_timed_high_scores(self):
        print('after save function called', self.timed_high_scores)
        with open("timed_high_scores.txt", "w") as file:
            print('after with opened', self.timed_high_scores)
            for score in self.timed_high_scores:
                file.write(f"{score}\n")

    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]   Keep only the top 5 scores
        self.save_high_scores()

    def update_timed_high_scores(self, score):
        print(score)
        self.timed_high_scores.append(score)
        print('after appending', score)
        self.timed_high_scores.sort(reverse=True)
        print('after sorting', score)
        self.timed_high_scores = self.timed_high_scores[:5]
        print('after dropping #6', score)
        self.save_timed_high_scores()

    def show_leaderboard(self, event):
        leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}%" for i, score in enumerate(self.high_scores)])
        wx.MessageBox(f"Casual Leaderboard:\n{leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)

    def show_timed_leaderboard(self, event):
        timed_leaderboard_str = "\n".join(
            [f"{i + 1}. {score:.2f}" for i, score in enumerate(self.timed_high_scores)])
        wx.MessageBox(f"Timed Leaderboard:\n{timed_leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App()
    frame = MathGame(None)
    frame.Show()
    app.MainLoop()
