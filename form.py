import re
import pandas as pd
from deep_translator import GoogleTranslator
import detectlanguage
import flet as ft

detectlanguage.configuration.api_key = "026adcb6587baa3b9f2afc05e991d327"

class WordForm(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.filepath = 'words.csv'
        
        self.word = ft.TextField(
            label="Word/phrase",
            on_change=self.word_changed,
            border_radius=10,
            border_color=ft.colors.WHITE30
        )
        self.translate_button = ft.ElevatedButton(
            'Translate',
            on_click=self.translate_click
        )
        self.translated_word = ft.TextField(
            read_only=True,
            label="Translation",
            border_radius=10,
            border_color=ft.colors.WHITE30
        )
        self.save_button = ft.ElevatedButton(
            'Save',
            on_click=self.save_word,
            disabled=True
        )

        self.languages_list = ['en', 'uk', 'ru']
        self.source_language = None
        self.target_language = None

        self.state = {
            'empty': False,
            'unlettered': False,
            'undef_lang': False,
            'unrec': False
        }

    def show_error(self, text):
        self.page.dialog = ft.SnackBar(content=ft.Text(text), bgcolor=ft.colors.TEAL_400)
        self.page.dialog.open = True
        self.page.update()

    def word_changed(self, e):
        self.save_button.disabled = True
        self.translated_word.value = ''
        self.state = {st: False for st in self.state}
        self.update()

    def translate_word(self, source_language, target_language, text):
        return GoogleTranslator(source=source_language, target=target_language).translate(text)
    
    def change_lang(self):
        translation = self.translate_word('ru', 'uk', self.word.value)
        if translation != self.word.value:
            self.show_error(f"Word '{self.word.value}' was replaced by '{translation}'")
            self.word.value = translation
        self.update()
    
    def process_word(self):

        self.word.value = self.word.value.strip()

        if not self.word.value:
            self.state['empty'] = True

        elif all(not char.isalpha() for char in self.word.value):
            self.state['unlettered'] = True
            
        else:
            self.source_language = detectlanguage.simple_detect(self.word.value)
            print(self.source_language)

            if self.source_language not in self.languages_list:
                self.state['undef_lang'] = True

            elif self.source_language == 'ru':
                self.change_lang()
                self.source_language = 'uk'
                self.target_language = 'en'
                return self.translate_word(self.source_language, self.target_language, self.word.value)
            else:
                self.target_language = 'en' if self.source_language == 'uk' else 'uk'
                return self.translate_word(self.source_language, self.target_language, self.word.value)
                
    def translate_click(self, e):
        translation = self.process_word()
        
        if self.state['empty'] or self.state['unlettered']:
            self.show_error('Enter a word.')
        elif self.word.value == translation:
            self.show_error('The word cannot be translated.')
        elif self.state['undef_lang']:
            self.show_error('Use English or Ukrainian languages.')
        else:
            self.translated_word.value = translation
            self.save_button.disabled = False
        self.update()

    def save_word(self, e):
        self.data = pd.read_csv(self.filepath)
        
        if self.word.value.lower() in self.data[self.source_language].values and \
            self.translated_word.value.lower() in self.data[self.target_language].values:
            self.show_error('Word is already in the dictionary.')
            
        else:
            en_word = self.translated_word.value.lower() if self.target_language == 'en' else self.word.value.lower()
            uk_word = self.word.value.lower() if self.target_language == 'en' else self.translated_word.value.lower()

            new_data = pd.DataFrame({'en': [en_word], 'uk': [uk_word]})
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.data.to_csv(self.filepath, index=False)
            
            self.save_button.disabled = True
            self.show_error(f'The word "{self.word.value}" was added to the dictionary.')

        self.update()

    def build(self):
        return ft.Container(
            ft.Column(
                controls=[
                    ft.Container(height=10),
                    self.word,
                    self.translate_button,
                    ft.Container(height=10),
                    self.translated_word,
                    self.save_button
                ],
                horizontal_alignment='center'
            )
        )