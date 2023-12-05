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
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # Set panel background to black
        self.title_label = wx.StaticText(self.panel, label="MATH GAME", pos=(86, 20))
        self.title_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.title_label.SetForegroundColour(wx.Colour(255, 255, 0))  # Yellow text
        self.start_button = wx.Button(self.panel, label="START", pos=(100, 60), size=(100, 40))
        self.start_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button_clicked)
        self.single_player_button = wx.Button(self.panel, label="SINGLE PLAYER", pos=(55, 60), size=(190, 30))
        self.single_player_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.single_player_button.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text
        self.single_player_button.Bind(wx.EVT_BUTTON, self.on_single_player_button_clicked)
        self.single_player_button.Hide()
        self.pvp_button = wx.Button(self.panel, label="PLAYER v. PLAYER", pos=(55, 100), size=(190, 30))
        self.pvp_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.pvp_button.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text
        self.pvp_button.Bind(wx.EVT_BUTTON, self.on_pvp_button_clicked)
        self.pvp_button.Hide()
        self.player_turn_label = wx.StaticText(self.panel, label="", pos=(100, 55))
        self.player_turn_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.player_turn_label.Hide()
        self.casual_button = wx.Button(self.panel, label='CASUAL', pos=(55, 60), size=(90, 40))
        self.casual_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.casual_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.casual_button.Bind(wx.EVT_BUTTON, self.on_casual_button_clicked)
        self.casual_button.Hide()
        self.timed_button = wx.Button(self.panel, label='TIMED', pos=(155, 60), size=(90, 40))
        self.timed_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.timed_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.timed_button.Bind(wx.EVT_BUTTON, self.on_timed_button_clicked)
        self.timed_button.Hide()
        self.countdown_label = wx.StaticText(self.panel, label="", pos=(140, 55))
        self.countdown_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.countdown_label.SetForegroundColour(wx.Colour(0, 255, 0))
        self.countdown_label.Hide()
        self.question_label = wx.StaticText(self.panel, label="", pos=(100, 90))
        self.question_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.question_label.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        self.final_score_label = wx.StaticText(self.panel, label="", pos=(40, 90))
        self.final_score_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.final_score_label.SetForegroundColour(wx.Colour(255, 255, 255))
        self.answer_text_ctrl = wx.TextCtrl(self.panel, pos=(100, 130), size=(100, 30), style=wx.TE_PROCESS_ENTER)
        self.answer_text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_answer_enter)
        self.answer_text_ctrl.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.answer_text_ctrl.SetBackgroundColour(wx.Colour(0, 0, 0))  # Black background
        self.answer_text_ctrl.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        self.answer_text_ctrl.Hide()
        self.next_button = wx.Button(self.panel, label="NEXT", pos=(100, 170), size=(100, 30))
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button_clicked)
        self.next_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.next_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.next_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.next_button.Hide()
        self.timed_next_button = wx.Button(self.panel, label="NEXT", pos=(100, 180), size=(100, 30))
        self.timed_next_button.Bind(wx.EVT_BUTTON, self.on_timed_next_button_clicked)
        self.timed_next_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.timed_next_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timed_next_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.timed_next_button.Hide()
        self.pvp_next_button = wx.Button(self.panel, label="NEXT", pos=(100, 180), size=(100, 30))
        self.pvp_next_button.Bind(wx.EVT_BUTTON, self.on_pvp_next_button_clicked)
        self.pvp_next_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.pvp_next_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.pvp_next_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.pvp_next_button.Hide()
        self.restart_button = wx.Button(self.panel, label="RESTART", pos=(100, 180), size=(100, 30))
        self.restart_button.Bind(wx.EVT_BUTTON, self.on_restart_button_clicked)
        self.restart_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.restart_button.SetBackgroundColour(wx.Colour(255, 255, 255))  # White background
        self.restart_button.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text
        self.restart_button.Hide()
        self.leaderboard_button = wx.Button(self.panel, label="CASUAL LEADERBOARD", pos=(65, 220), size=(170, 30))
        self.leaderboard_button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.leaderboard_button.Bind(wx.EVT_BUTTON, self.show_leaderboard)
        self.leaderboard_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.leaderboard_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.timed_leaderboard_button = wx.Button(self.panel, label="TIMED LEADERBOARD", pos=(65, 260), size=(170, 30))
        self.timed_leaderboard_button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.timed_leaderboard_button.Bind(wx.EVT_BUTTON, self.show_timed_leaderboard)
        self.timed_leaderboard_button.SetBackgroundColour(wx.Colour(255, 255, 255))  # White background
        self.timed_leaderboard_button.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text
        self.questions = []
        self.timed_questions = []
        self.timed_answers = []
        self.answers = []
        self.pvp_questions = []
        self.pvp_answers = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.player_1_score = 0
        self.player_2_score = 0
        self.high_scores = self.load_high_scores()
        self.timed_high_scores = self.load_timed_high_scores()
        self.generate_questions()
        self.generate_timed_questions()
        self.generate_pvp_questions()
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

    def generate_pvp_questions(self):
        operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        for _ in range(20):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator_symbol = random.choice(list(operators.keys()))
            question = f"{num1} {operator_symbol} {num2}"
            answer = operators[operator_symbol](num1, num2)
            self.pvp_questions.append(question)
            self.pvp_answers.append(answer)

    def show_question(self):
        self.question_label.SetLabel(self.questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

    def show_timed_question(self):
        self.question_label.SetLabel(self.timed_questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

    def show_pvp_question(self):
        if self.current_question_index == 0:
            self.player_turn_label.Show()
        if self.current_question_index % 2 == 0:
            self.player_turn_label.SetForegroundColour(wx.Colour(255, 0, 0))  #red
            self.player_turn_label.SetLabel("PLAYER 1")
        else:
            self.player_turn_label.SetForegroundColour(wx.Colour(0, 0, 255))  # blue
            self.player_turn_label.SetLabel("PLAYER 2")
        self.question_label.SetLabel(self.pvp_questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

    def on_single_player_button_clicked(self, event):
        self.single_player_button.Hide()
        self.pvp_button.Hide()
        self.casual_button.Show()
        self.timed_button.Show()

    def on_pvp_button_clicked(self, event):
        global live_game
        global gamemode
        global redundant
        redundant = 0
        gamemode = 3
        self.single_player_button.Hide()
        self.pvp_button.Hide()
        self.question_label.Show()
        self.answer_text_ctrl.Show()
        self.pvp_next_button.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.show_pvp_question()
        live_game = 1

    def on_start_button_clicked(self, event):
        self.start_button.Hide()
        self.single_player_button.Show()
        self.pvp_button.Show()

    def on_casual_button_clicked(self, event):
        global live_game
        global gamemode
        global redundant
        redundant = 0
        gamemode = 1
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.question_label.Show()
        self.answer_text_ctrl.Show()
        self.next_button.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.show_question()
        live_game = 1

    def on_timed_button_clicked(self, event):
        global live_game
        global gamemode
        global start_time
        global redundant
        redundant = 0
        gamemode = 2
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.question_label.Show()
        self.answer_text_ctrl.Show()
        self.timed_next_button.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.countdown_label.Show()
        self.countdown_label.SetLabel("60")
        self.timer.Start(1000)
        start_time = time.time()
        self.show_timed_question()
        live_game = 1

    def timer_check(self, event):
        global live_game
        global stopwatch
        global start_time
        global gamemode
        stopwatch = time.time() - start_time
        countdown = 60.0 - stopwatch
        countdown = round(countdown)
        countdown = str(countdown)
        self.countdown_label.SetLabel(countdown)
        if stopwatch >= 60:
            live_game = 0
            self.timer.Stop()
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.countdown_label.SetLabel("")
            self.countdown_label.Hide()
            self.show_timed_score()

    def on_answer_enter(self, event):
        global redundant
        global live_game
        global gamemode
        if live_game == 1:
            if gamemode == 1:
                self.on_next_button_clicked(event)
            elif gamemode == 2:
                self.on_timed_next_button_clicked(event)
            elif gamemode == 3:
                self.on_pvp_next_button_clicked(event)
            else:
                pass
        else:
            if gamemode == 1:
                redundant = 1
                try:
                    self.leaderboard_button.Enable()
                    self.timed_leaderboard_button.Enable()
                except:
                    pass
                self.show_score()
            elif gamemode == 2:
                redundant = 1
                try:
                    self.timer.Stop()
                except:
                    pass
                try:
                    self.leaderboard_button.Enable()
                    self.timed_leaderboard_button.Enable()
                    self.countdown_label.SetLabel("")
                    self.countdown_label.Hide()
                except:
                    pass
                self.show_timed_score()
            elif gamemode == 3:
                redundant = 1
                try:
                    self.player_turn_label.SetLabel("")
                    self.player_turn_label.Hide()
                    self.leaderboard_button.Enable()
                    self.timed_leaderboard_button.Enable()
                except:
                    pass
                self.show_pvp_score()

    def on_next_button_clicked(self, event):
        global live_game
        self.check_answer()
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            live_game = 0
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.show_score()

    def on_timed_next_button_clicked(self, event):
        global stopwatch
        global start_time
        self.check_timed_answer()
        self.current_question_index += 1
        stopwatch = time.time() - start_time
        self.show_timed_question()

    def on_pvp_next_button_clicked(self, event):
        global live_game
        self.check_answer_pvp()
        self.current_question_index += 1
        if self.current_question_index < len(self.pvp_questions):
            self.show_pvp_question()
        else:
            live_game = 0
            self.player_turn_label.SetLabel("")
            self.player_turn_label.Hide()
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.show_pvp_score()

    def on_restart_button_clicked(self, event):
        self.current_question_index = 0
        self.correct_answers = 0
        self.player_1_score = 0
        self.player_2_score = 0
        self.questions = []
        self.timed_questions = []
        self.pvp_questions = []
        self.answers = []
        self.timed_answers = []
        self.pvp_answers = []
        self.generate_questions()
        self.generate_timed_questions()
        self.generate_pvp_questions()
        self.restart_button.Hide()
        self.final_score_label.Hide()
        self.question_label.Hide()
        self.answer_text_ctrl.Hide()
        self.next_button.Hide()
        self.timed_next_button.Hide()
        self.pvp_next_button.Hide()
        self.single_player_button.Show()
        self.pvp_button.Show()

    def check_answer(self):
        user_answer = self.answer_text_ctrl.GetValue()
        try:
            correct_answer = eval(self.questions[self.current_question_index])
        except:
            print('premature GAMEOVER. You held enter too long at some point during this game')
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.show_score()
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def check_timed_answer(self):##
        user_answer = self.answer_text_ctrl.GetValue()
        correct_answer = eval((self.timed_questions[self.current_question_index]))
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def check_answer_pvp(self):
        user_answer = self.answer_text_ctrl.GetValue()
        try:
            correct_answer = eval((self.pvp_questions[self.current_question_index]))
        except:
            print('premature GAMEOVER. You held enter too long at some point during this game. Restart to try again')
            self.player_turn_label.SetLabel("")
            self.player_turn_label.Hide()
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.show_pvp_score()
        if str(correct_answer) == user_answer and self.current_question_index % 2 == 0:
            self.player_1_score = self.player_1_score + 10
        if str(correct_answer) == user_answer and self.current_question_index % 2 == 1:
            self.player_2_score = self.player_2_score + 10

    def show_score(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers / total_questions) * 100
        self.final_score_label.SetLabel(f"YOUR SCORE: {score_percentage:.2f}%")
        try:
            self.next_button.Hide()
            self.restart_button.Show()
        except:
            pass
        if redundant == 0:
            self.update_high_scores(score_percentage)

    def show_timed_score(self):
        final_score = self.correct_answers * 10
        self.final_score_label.SetLabel(f"YOUR SCORE: {final_score:.2f}")
        try:
            self.timed_next_button.Hide()
            self.question_label.Hide()
            self.restart_button.Show()
        except:
            pass
        if redundant == 0:
            self.update_timed_high_scores(final_score)

    def show_pvp_score(self):
        result = f"PLAYER 1 SCORE: {self.player_1_score}\nPLAYER 2 SCORE: {self.player_2_score}"
        wx.MessageBox(result, "PvP GAME OVER", wx.OK | wx.ICON_INFORMATION)
        try:
            self.pvp_next_button.Hide()
            self.restart_button.Show()
        except:
            pass

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
        with open("timed_high_scores.txt", "w") as file:
            for score in self.timed_high_scores:
                file.write(f"{score}\n")

    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.save_high_scores()

    def update_timed_high_scores(self, score):
        self.timed_high_scores.append(score)
        self.timed_high_scores.sort(reverse=True)
        self.timed_high_scores = self.timed_high_scores[:5]
        self.save_timed_high_scores()

    def show_leaderboard(self, event):
        leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}%" for i, score in enumerate(self.high_scores)])
        wx.MessageBox(f"CASUAL LEADERBOARD:\n{leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)

    def show_timed_leaderboard(self, event):
        timed_leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}" for i, score in enumerate(self.timed_high_scores)])
        wx.MessageBox(f"TIMED LEADERBOARD:\n{timed_leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)



if __name__ == "__main__":
    app = wx.App()
    frame = MathGame(None)
    frame.Show()
    app.MainLoop()