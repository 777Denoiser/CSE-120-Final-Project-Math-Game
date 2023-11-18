import wx
import random


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

        self.questions = []
        self.current_question_index = 0
        self.correct_answers = 0

        self.generate_questions()
        self.show_question()

    def generate_questions(self):
        operators = ['+', '-', 'x', '/']
        for _ in range(10):
            num1 = random.randint(1, 99)
            num2 = random.randint(1, 99)
            operator = random.choice(operators)
            question = f"{num1} {operator} {num2}"
            self.questions.append(question)

    def show_question(self):
        self.question_label.SetLabel(self.questions[self.current_question_index])
        self.answer_text_ctrl.SetValue("")
        self.answer_text_ctrl.SetFocus()

    def on_start_button_clicked(self, event):
        self.start_button.Hide()
        self.next_button.Enable()
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
        correct_answer = eval(self.questions[self.current_question_index])
        if str(correct_answer) == user_answer:
            self.correct_answers += 1

    def show_score(self):
        score = self.correct_answers / len(self.questions) * 10
        self.question_label.SetLabel(f"Your score: {score}/10")
        self.next_button.Disable()
        self.restart_button.Show()


if __name__ == "__main__":
    app = wx.App()
    frame = MathGame(None)
    frame.Show()
    app.MainLoop()