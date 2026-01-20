import flet as ft
from pages.form import WordForm
from pages.quiz import Quiz
from pages.dictionary import Dictionary

def main(page: ft.Page):
    page.title = 'FletLang'
    page.theme = ft.Theme(color_scheme_seed='teal')
    
    # Fixed window size
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False

    def show_exp(e):
        text = (
        '1. The application uses free API Google Translator and free API for language detection, so translation errors are possible.\n\n'
        '2. Words used in the quiz are limited to the list in your dictionary (synonyms are counted similarly).\n\n'
        '3. Created by Xirex.'
        )
        bs = ft.BottomSheet(ft.Container(ft.Text(text, weight=ft.FontWeight.W_400, size=18), padding=15))
        page.overlay.append(bs)
        bs.open = True
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text('FletLang'),
        bgcolor=ft.Colors.TEAL_700,
        actions=[ft.IconButton(ft.Icons.INFO_OUTLINED, on_click=show_exp)]
    )

    # Create content instances
    form_content = WordForm(page)
    form_wrapper = ft.Container(
        content=form_content,
        padding=ft.Padding.symmetric(horizontal=20),
        expand=True,
        alignment=ft.Alignment.CENTER
    )
    dict_view = ft.Container(
        content=Dictionary(page),
        padding=ft.Padding.symmetric(horizontal=20),
        expand=True
    )
    quiz_view = ft.Container(
        content=Quiz(page),
        padding=ft.Padding.symmetric(horizontal=20),
        expand=True
    )

    # Scrollable container for switching content
    content = ft.Column(
        controls=[form_wrapper],
        scroll=None,
        expand=True
    )

    def change_view(e):
        idx = e.control.selected_index
        if idx == 0:
            content.controls = [dict_view]
            content.scroll = ft.ScrollMode.AUTO
            dict_view.content.display_words()
        elif idx == 1:
            content.controls = [form_wrapper]
            content.scroll = None
        elif idx == 2:
            content.controls = [quiz_view]
            content.scroll = ft.ScrollMode.AUTO
            quiz_view.content.display_quiz()
        page.update()
    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK, label='Dictionary'),
            ft.NavigationBarDestination(icon=ft.Icons.EDIT_NOTE, label='Add word'),
            ft.NavigationBarDestination(icon=ft.Icons.QUIZ, label='Quiz'),
        ],
        selected_index=1,
        height=60,
        on_change=change_view
    )

    page.add(content)

ft.run(main)