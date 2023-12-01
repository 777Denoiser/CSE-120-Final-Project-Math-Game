import wx
import random
import operator

class MathGame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Math Game", size=(300, 400))
        self.panel = wx.Panel(self)
        self.title_label = wx.StaticText(self.panel, label="Math Game", pos=(100, 20))
        self.title_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button = wx.Button(self.panel, label="START", pos=(100, 60), size=(100, 40))
        self.start_button.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button_clicked)
        self.question_label = wx.StaticText(self.panel, label="", pos=(100, 120))
        self.question_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.answer_text_ctrl = wx.TextCtrl(self.panel, pos=(100, 150), size=(100, 20), style=wx.TE_PROCESS_ENTER)
        self.answer_text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_answer_enter)
        self.next_button = wx.Button(self.panel, label="Next", pos=(100, 180), size=(100, 30))
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button_clicked)
        self.next_button.Disable()
        self.restart_button = wx.Button(self.panel, label="Restart", pos=(100, 180), size=(100, 30))
        self.restart_button.Bind(wx.EVT_BUTTON, self.on_restart_button_clicked)
        self.restart_button.Hide()
        self.leaderboard_button = wx.Button(self.panel, label="Leaderboard", pos=(100, 220), size=(100, 30))
        self.leaderboard_button.Bind(wx.EVT_BUTTON, self.show_leaderboard)
        self.leaderboard_button.Disable()
        self.questions = []
        self.answers = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.high_scores = self.load_high_scores()
        self.generate_questions()
        self.show_question()

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
        self.question_label.SetLabel(self.questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

    def on_start_button_clicked(self, event):
        self.start_button.Hide()
        self.next_button.Enable()
        self.leaderboard_button.Enable()
        self.show_question()

    def on_answer_enter(self, event):
        self.check_answer()

    def on_next_button_clicked(self, event):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.show_score()

    def on_restart_button_clicked(self, event):
        self.current_question_index = 0
        self.correct_answers = 0
        self.generate_questions()
        self.show_question()
        self.restart_button.Hide()

    def check_answer(self):
        user_answer = self.answer_text_ctrl.GetValue()

        correct_answer = eval((self.questions[self.current_question_index]))
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

        self.show_score()

    def show_score(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers / total_questions) * 100
        self.question_label.SetLabel(f"Your score: {score_percentage:.2f}%")
        self.next_button.Disable()
        self.restart_button.Show()
        self.update_high_scores(score_percentage)

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [float(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            high_scores = []
        return high_scores

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.save_high_scores()

    def show_leaderboard(self, event):
        leaderboard_str = "\n".join([f"{i + 1}. {score:.2f}%" for i, score in enumerate(self.high_scores)])
        wx.MessageBox(f"Leaderboard:\n{leaderboard_str}", "High Scores", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = MathGame(None)
    frame.Show()
    app.MainLoop()