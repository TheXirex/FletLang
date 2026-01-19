import os
import pandas as pd
from deep_translator import GoogleTranslator
import detectlanguage
import flet as ft

detectlanguage.configuration.api_key = os.getenv('DETECTLANGUAGE_API_KEY')

class WordForm(ft.Column):
    def __init__(self, page_ref: ft.Page):
        super().__init__()
        self._page_ref = page_ref
        self.filepath = 'words.csv'
        
        self.word = ft.TextField(
            label="Word/phrase",
            on_change=self.word_changed,
            border_radius=10,
            border_color=ft.Colors.WHITE30,
            width=400
        )
        self.translate_button = ft.ElevatedButton(
            'Translate',
            on_click=self.translate_click
        )
        self.translated_word = ft.TextField(
            read_only=True,
            label="Translation",
            border_radius=10,
            border_color=ft.Colors.WHITE30,
            width=400
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

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 15
        self.controls = [
            self.word,
            self.translate_button,
            self.translated_word,
            self.save_button
        ]

    def show_error(self, text):
        snack = ft.SnackBar(content=ft.Text(text), bgcolor=ft.Colors.TEAL_400)
        self._page_ref.overlay.append(snack)
        snack.open = True
        self._page_ref.update()

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