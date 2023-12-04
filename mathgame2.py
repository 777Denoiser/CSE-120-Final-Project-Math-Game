import wx
import random
import operator
import time

class MathGame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Math Game", size=(300, 400))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # Set panel background to black

    
        self.title_label = wx.StaticText(self.panel, label="Math Game", pos=(100, 20))
        self.title_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.title_label.SetForegroundColour(wx.Colour(255, 255, 0))  # White text

        self.start_button = wx.Button(self.panel, label="START", pos=(100, 60), size=(100, 40))
        self.start_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button_clicked)

        self.single_player_button = wx.Button(self.panel, label="Single Player", pos=(70, 80), size=(150, 30))
        self.single_player_button.Bind(wx.EVT_BUTTON, self.on_single_player_button_clicked)
        self.single_player_button.Hide()

        self.pvp_button = wx.Button(self.panel, label="Player vs Player", pos=(70, 120), size=(150, 30))
        self.pvp_button.Bind(wx.EVT_BUTTON, self.on_pvp_button_clicked)
        self.pvp_button.Hide()

        self.player_1_score = 0
        self.player_2_score = 0

        self.player_turn_label = wx.StaticText(self.panel, label="", pos=(50, 50))
        self.player_turn_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.player_turn_label.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        
        self.question_label = wx.StaticText(self.panel, label="", pos=(50, 80))
        self.question_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.question_label.SetForegroundColour(wx.Colour(255, 255, 255))  # White text

    

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
        self.countdown_label.SetForegroundColour(wx.Colour(255, 255, 255))
        self.countdown_label.Hide()

        self.question_label = wx.StaticText(self.panel, label="", pos=(100, 120))
        self.question_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.question_label.SetForegroundColour(wx.Colour(255, 255, 255))  # White text


        self.answer_text_ctrl = wx.TextCtrl(self.panel, pos=(100, 150), size=(100, 20), style=wx.TE_PROCESS_ENTER)
        self.answer_text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_answer_enter)
        self.answer_text_ctrl.SetBackgroundColour(wx.Colour(0, 0, 0))  # Black background
        self.answer_text_ctrl.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        self.answer_text_ctrl.Hide()

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
        self.answers = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.high_scores = self.load_high_scores()
        self.timed_high_scores = self.load_timed_high_scores()
        self.pvp_mode = False
        self.player_1_turn = True

        self.generate_questions()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_check, self.timer)

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

    
    def show_question(self):
        if self.pvp_mode:
             player_text = "Player 1's turn" if self.player_1_turn else "Player 2's turn"
             self.question_label.SetLabel(f"{player_text}: {self.questions[self.current_question_index]}")
        else:
             self.question_label.SetLabel(self.questions[self.current_question_index])
             self.question_label.CenterOnParent(wx.HORIZONTAL)
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()
        self.Refresh()
        self.Update()

      
    def on_single_player_button_clicked(self, event):
        self.single_player_button.Hide()
        self.pvp_button.Hide()
        self.casual_button.Show()
        self.timed_button.Show()
        self.answer_text_ctrl.Hide()

    def on_pvp_button_clicked(self, event):
        self.single_player_button.Hide()
        self.pvp_button.Hide()
        self.casual_button.Show()
        self.timed_button.Show()
        self.answer_text_ctrl.Hide()
        self.pvp_mode = True
        self.player_1_turn = True
        self.generate_questions()
        self.show_question()

    def on_start_button_clicked(self, event):
        self.start_button.Hide()
        self.single_player_button.Show()
        self.pvp_button.Show()
        self.answer_text_ctrl.Hide()

    def on_casual_button_clicked(self, event):
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.next_button.Show()
        self.answer_text_ctrl.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.show_question()

    def on_timed_button_clicked(self, event):
        global start_time
        self.casual_button.Hide()
        self.timed_button.Hide()
        self.timed_next_button.Show()
        self.answer_text_ctrl.Show()
        self.leaderboard_button.Disable()
        self.timed_leaderboard_button.Disable()
        self.countdown_label.Show()
        self.countdown_label.SetLabel("60")

        start_time = time.time()
        self.timer.Start(1000)
        self.start_game()
        self.show_question()

    def on_next_button_clicked(self, event):
        if  self.pvp_mode:
            self.check_answer_pvp()
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.player_1_turn = not self.player_1_turn
                print("Player 1's turn" if self.player_1_turn else "Player 2's turn")
                self.show_question()
            else:
                self.show_pvp_score()

                
        else:
            self.check_answer()
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.show_question()
            else:
                self.show_score()

        
            

    def check_answer(self):
        user_answer = self.answer_text_ctrl.GetValue()
        correct_answer = eval(self.questions[self.current_question_index])
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def check_answer_pvp(self):
        user_answer = self.answer_text_ctrl.GetValue()
        question_parts = self.questions[self.current_question_index].split()
        num1, operator, num2 = int(question_parts[0]), question_parts[1], int(question_parts[2])

        if operator == '+':
            correct_answer = num1 + num2
        elif operator == '-':
            correct_answer = num1 - num2
        elif operator == '*':
            correct_answer = num1 * num2
        elif operator == '/':
            correct_answer = num1 / num2

        if str(correct_answer) == user_answer:
           if self.player_1_turn:
            self.player_1_score += 1
           else:
            self.player_2_score += 1


        

    def show_pvp_score(self):
       result = f"Player 1's score: {self.player_1_score}\nPlayer 2's score: {self.player_2_score}"
       wx.MessageBox(result, "PvP Game Over", wx.OK | wx.ICON_INFORMATION)
       self.restart_game()  

    def restart_game(self):
        self.current_question_index = 0
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_turn = True  
        self.questions = []  
        self.answers = []    
        self.generate_questions() 
        self.start_button.Hide()
        self.restart_button.Show()   
        self.Refresh()
        self.Update()



    def next_question_or_end_game(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            if self.pvp_mode:
                self.show_pvp_score()
            else:
                self.show_score()


    def show_score(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers / total_questions) * 100
        self.question_label.SetLabel(f"Your score: {score_percentage:.2f}%")
        self.next_button.Hide()
        self.restart_button.Show()
        self.update_high_scores(score_percentage)

    
    def on_restart_button_clicked(self, event):
        self.restart_game()
        self.restart_button.Hide()
        self.start_button.Show()

    def on_timed_next_button_clicked(self, event):
        self.check_answer()
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.show_score()

    def timer_check(self, event):
        global stopwatch
        global start_time
        stopwatch = time.time() - start_time
        countdown = 60.0 - stopwatch
        countdown = round(countdown)
        countdown = str(countdown)
        self.countdown_label.SetLabel(countdown)
        if stopwatch >= 60:
            self.timer.Stop()
            self.leaderboard_button.Enable()
            self.timed_leaderboard_button.Enable()
            self.countdown_label.SetLabel("")
            self.countdown_label.Hide()
            self.show_score()

    def on_answer_enter(self, event):
        if self.pvp_mode:
            self.check_answer_pvp()
            self.player_1_turn = not self.player_1_turn
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.show_question()
            else:
                self.show_pvp_score()
        else:
            self.check_answer()
            self.next_question_or_end_game()
            
        
        
    



    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [float(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            with open("high_scores.txt", "w"):
                high_scores = []
        return high_scores

    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.save_high_scores()

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    

    def load_timed_high_scores(self):
        try:
            with open("timed_high_scores.txt", "r") as file:
                timed_high_scores = [float(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            timed_high_scores = []
        return timed_high_scores
    
    def save_timed_high_scores(self):
        with open("timed_high_scores.txt", "w") as file:
            for score in self.timed_high_scores:
                file.write(f"{score}\n")

    def update_timed_high_scores(self, score):
        self.timed_high_scores.append(score)
        self.timed_high_scores.sort(reverse=True)
        self.timed_high_scores = self.timed_high_scores[:5]
        self.save_timed_high_scores()

    def show_leaderboard(self, event):
        leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}%" for i, score in enumerate(self.high_scores)])
        wx.MessageBox(f"Casual Leaderboard:\n{leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)

    def show_timed_leaderboard(self, event):
        timed_leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}" for i, score in enumerate(self.timed_high_scores)])##
        wx.MessageBox(f"Timed Leaderboard:\n{timed_leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)##


if __name__ == "__main__":
    app = wx.App()
    frame = MathGame(None)
    frame.Show()
    app.MainLoop()