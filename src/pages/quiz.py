import flet as ft
from utils import show_error, validate_word_input
from src.data_manager.data_manager import DataManager

class Quiz(ft.Column):
    def __init__(self, page_ref: ft.Page):
        super().__init__()
        self._page_ref = page_ref
        self.data_manager = DataManager('data/words.csv')

        self.language = ft.Dropdown(
            options=[
                ft.dropdown.Option("EN"),
                ft.dropdown.Option("UK"),
            ],
            on_select=self.refresh,
            border_color=ft.Colors.WHITE30,
            border_radius=10,
            value='EN'
        )

        self.quest = ft.TextField(
            label="Word/phrase",
            read_only=True,
            border_color=ft.Colors.WHITE30,
            border_radius=10
        )
        self.word = ft.TextField(
            label="Your answer",
            border_color=ft.Colors.WHITE30,
            border_radius=10
        )

        self.check_but = ft.ElevatedButton('Check', on_click=self.check_answer)
        self.hint_but = ft.ElevatedButton('Hint', on_click=self.show_hint)

        self.answers = []
        self.answer_icon = ft.Icon(ft.Icons.QUESTION_MARK)
        self.answer = ft.TextField(
            label='Correct answer',
            visible=False,
            read_only=True,
            border_color=ft.Colors.WHITE30,
            border_radius=10
        )
        self.refresh_but = ft.ElevatedButton('Refresh', on_click=self.refresh)

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
                ft.Container(self.check_but, expand=1),
                ft.Container(self.hint_but, expand=1)
            ]),
        )
        
        self.controls = [
            ft.Container(height=10),
            quest_cont,
            ft.Container(height=10),
            answer_cont,
            ft.Container(height=10),
            but_cont,
            ft.Container(height=10),
            self.answer
        ]

    def refresh(self, e):
        self.word.value = ''
        self.answer_icon.icon, self.answer_icon.color = ft.Icons.QUESTION_MARK, ft.Colors.WHITE
        self.display_quiz()
        self.update()

    def check_answer(self, e):
        self.word.value = self.word.value.strip().lower()

        is_valid, error_msg = validate_word_input(self.word.value)
        if not is_valid:
            show_error(self._page_ref, error_msg)
        else:
            if self.word.value in self.answers:
                self.answer_icon.icon, self.answer_icon.color = ft.Icons.CHECK, ft.Colors.GREEN
            else:
                self.answer_icon.icon, self.answer_icon.color = ft.Icons.CLEAR, ft.Colors.RED
            self.answer.visible = True
        self.update()

    def show_hint(self, e):
        # Reveal the correct answer and mark as skipped
        if not hasattr(self, 'answers') or len(self.answers) == 0:
            self.display_quiz()
        self.answer.visible = True
        # ensure answer value is populated
        self.answer.value = ' / '.join(self.answers)
        self.answer_icon.icon, self.answer_icon.color = ft.Icons.SKIP_NEXT, ft.Colors.AMBER
        self.update()

    def display_quiz(self):
        self.answer.visible = False
        random_word = self.data_manager.get_random_word()
        
        self.quest.value = random_word['en'] if self.language.value == 'EN' else random_word['uk']
        language = 'en' if self.language.value == 'EN' else 'uk'
        self.answers = self.data_manager.get_translations(self.quest.value, language)
        
        self.answer.value = ' / '.join(self.answers)