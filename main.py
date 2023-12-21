import flet as ft
from form import WordForm
from quiz import Quiz
from dictionary import Dictionary

def main(page: ft.Page):
    page.title = 'DICTIONARY'
    page.theme = ft.Theme(color_scheme_seed='teal')

    def show_exp(e):
        text = (
        '1. The application uses free API Google Translator and free API for language detection, so translation errors are possible.\n\n'
        '2. Words used in the quiz are limited to the list in your dictionary (synonyms are counted similarly).\n\n'
        '3. Created by Xirex.'
        )
        page.dialog = ft.BottomSheet(ft.Container(ft.Text(text, weight=ft.FontWeight.W_400, size=18), padding=15))
        page.dialog.open = True
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text('DICTIONARY'),
        bgcolor=ft.colors.TEAL_700,
        actions=[ft.IconButton(ft.icons.INFO_OUTLINED, on_click=show_exp)]
    )
    
    def change_view(e):
        if e.control.selected_index == 0:
            page.go('/dict')
        elif e.control.selected_index == 1:
            page.go('/form')
        elif e.control.selected_index == 2:
            page.go('/quiz')
    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.MENU_BOOK, label='Dictionary'),
            ft.NavigationDestination(icon=ft.icons.EDIT_NOTE, label='Add word'),
            ft.NavigationDestination(icon=ft.icons.QUIZ, label='Quiz'),
        ],
        selected_index=1,
        height=60,
        on_change=lambda e: change_view(e)
    )

    def route_change(route):
        page.views.clear()
        if page.route == '/form':
            page.views.append(
                ft.View(
                    route='/form',
                    controls=[
                        WordForm(),
                        page.appbar,
                        page.navigation_bar,
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                )
            )   
        elif page.route == "/dict":
            page.views.append(
                ft.View(
                    route="/dict",
                    controls=[
                        Dictionary(),
                        page.appbar,
                        page.navigation_bar,
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                )
            )
        elif page.route == "/quiz":
            page.views.append(
                ft.View(
                    route="/quiz",
                    controls=[
                        Quiz(),
                        page.appbar,
                        page.navigation_bar,
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/form')

ft.app(target=main)