import flet as ft
import pandas as pd

class Quiz(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.language = ft.Dropdown(
            options=[
                ft.dropdown.Option("EN"),
                ft.dropdown.Option("UK"),
            ],
            on_change=self.refresh,
            border_color=ft.colors.WHITE30,
            border_radius=10
        )

        self.quest = ft.TextField(
            label="Word/phrase",
            read_only=True,
            border_color=ft.colors.WHITE30,
            border_radius=10
        )
        self.word = ft.TextField(
            label="Your answer",
            border_color=ft.colors.WHITE30,
            border_radius=10
        )

        self.check_but = ft.ElevatedButton('Check', on_click=self.check_answer)

        self.answers = []
        self.answer_icon = ft.Icon(name=ft.icons.QUESTION_MARK)
        self.answer = ft.TextField(
            label='Correct answer',
            visible=False,
            read_only=True,
            border_color=ft.colors.WHITE30,
            border_radius=10
        )
        self.refresh_but = ft.ElevatedButton('Refresh', on_click=self.refresh)

    def show_error(self, text):
        self.page.dialog = ft.SnackBar(content=ft.Text(text), bgcolor=ft.colors.TEAL_400)
        self.page.dialog.open = True
        self.page.update()

    def refresh(self, e):
        self.word.value = ''
        self.answer_icon.name, self.answer_icon.color = ft.icons.QUESTION_MARK, ft.colors.WHITE
        self.display_quiz()
        self.update()

    def check_answer(self, e):
        self.word.value = self.word.value.strip().lower()

        if not self.word.value or all(not char.isalpha() for char in self.word.value):
            self.show_error('Enter a word.')
        else:
            if self.word.value in self.answers:
                self.answer_icon.name, self.answer_icon.color = ft.icons.CHECK, ft.colors.GREEN
            else:
                self.answer_icon.name, self.answer_icon.color = ft.icons.CLEAR, ft.colors.RED
            self.answer.visible = True
        self.update()

    def display_quiz(self):
        self.answer.visible = False
        data = pd.read_csv('words.csv')
        while True:
            random_word = data.sample()
            if len(random_word['en'].values[0]) <= 28 and len(random_word['uk'].values[0]) <= 28:
                break
        
        self.quest.value = random_word['en'].values[0] if self.language.value == 'EN' else random_word['uk'].values[0]
        if self.language.value == 'EN':
            self.answers = data[data['en'] == self.quest.value]['uk'].values
        else:
            self.answers = data[data['uk'] == self.quest.value]['en'].values
        
        self.answer.value = ' / '.join(self.answers)

    def build(self):
        self.language.value = 'EN'
        self.display_quiz()

        quest_cont = ft.Container(
            ft.Row(controls=[
                ft.Container(self.language, expand=1),
                ft.Container(self.quest, expand=5)
            ])
        )
        answer_cont = ft.Container(
            ft.Row(controls=[
                ft.Container(self.answer_icon, expand=1),
                ft.Container(self.word, expand=5)
            ])
        )
        but_cont = ft.Container(
            ft.Row(controls=[
                ft.Container(self.refresh_but, expand=1),
                ft.Container(self.check_but, expand=1)
            ]),
        )
        return ft.Column(controls=[
            ft.Container(height=10),
            quest_cont,
            ft.Container(height=10),
            answer_cont,
            ft.Container(height=10),
            but_cont,
            ft.Container(height=10),
            self.answer
        ])