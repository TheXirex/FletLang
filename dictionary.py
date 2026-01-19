import flet as ft
import pandas as pd

class Dictionary(ft.Column):
    def __init__(self, page_ref: ft.Page):
        super().__init__()
        self._page_ref = page_ref
        self.filepath = 'words.csv'
        self.words_list = ft.Column(controls=[], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.search_field = ft.TextField(
            hint_text='Search words...',
            border_radius=10,
            on_change=self.on_search_but,
            border_color=ft.Colors.TEAL_400,
            focused_border_color=ft.Colors.TEAL_200,
            prefix_icon=ft.Icons.SEARCH,
            text_size=16,
            content_padding=ft.Padding.symmetric(horizontal=15, vertical=10),
            expand=True
        )
        
        self.display_words()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            ft.Container(height=15),
            self.search_field,
            ft.Container(height=15),
            self.words_list
        ]

    def delete_word(self, data_index, control_index, with_search):
        data = pd.read_csv(self.filepath)
        data = data.drop(data_index)
        data.to_csv(self.filepath, index=False)
        del self.words_list.controls[control_index]
        if with_search:
            self.activate_search()
        else:
            self.display_words()
        self.update()

    def display_words(self):
        data = pd.read_csv(self.filepath)
        displayed_rows = []
        for i in range(len(data)):
            displayed_rows.append(
                ft.Container(
                    ft.Row(
                        controls=[
                            ft.Container(
                                ft.Text(data.iloc[i]['en'], weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                                alignment=ft.Alignment.CENTER,
                                expand=5
                            ),
                            ft.Container(
                                ft.Text(data.iloc[i]['uk'], weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                                alignment=ft.Alignment.CENTER,
                                expand=5
                            ),
                            ft.Container(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_FOREVER,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e, data_index=i, control_index=i, with_search=False:
                                    self.delete_word(data_index, control_index, with_search)
                                ),
                                expand=1
                            )
                        ],
                    ),
                    border=ft.border.all(2, ft.Colors.WHITE30),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=0),
                    alignment=ft.Alignment.CENTER,
                    border_radius=10
                )
            )
        self.words_list.controls = displayed_rows

    def on_search_but(self, e):
        self.activate_search()
    
    def activate_search(self):
        if self.search_field.value == '':
            self.display_words()
        else:
            data = pd.read_csv(self.filepath)
            displayed_rows = []
            ind = 0
            for i in range(len(data)):
                if (
                    self.search_field.value in data.iloc[i]['en'].split()
                    or self.search_field.value in data.iloc[i]['uk'].split()
                    or self.search_field.value == data.iloc[i]['en'][:len(self.search_field.value)]
                    or self.search_field.value == data.iloc[i]['uk'][:len(self.search_field.value)]
                ):
                    displayed_rows.append(
                        ft.Container(
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        ft.Text(data.iloc[i]['en'], weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                                        alignment=ft.Alignment.CENTER,
                                        expand=5
                                    ),
                                    ft.Container(
                                        ft.Text(data.iloc[i]['uk'], weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                                        alignment=ft.Alignment.CENTER,
                                        expand=5
                                    ),
                                    ft.Container(
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_FOREVER,
                                            icon_color=ft.Colors.RED,
                                            on_click=lambda e, data_index=i, control_index=ind, with_search=True:
                                            self.delete_word(data_index, control_index, with_search)
                                        ),
                                        expand=1
                                    )
                                ],
                            ),
                            border=ft.border.all(2, ft.Colors.WHITE30),
                            padding=ft.Padding.symmetric(horizontal=10, vertical=2),
                            alignment=ft.Alignment.CENTER,
                            border_radius=10
                        )
                    )
                    ind += 1
            self.words_list.controls = displayed_rows
        self.update()