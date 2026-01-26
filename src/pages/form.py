import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import detectlanguage
from detectlanguage.exceptions import DetectLanguageError
import flet as ft
from utils import show_error
from data_manager import DataManager

load_dotenv()
detectlanguage.configuration.api_key = os.getenv('DETECTLANGUAGE_API_KEY')

class WordForm(ft.Column):
    def __init__(self, page_ref: ft.Page):
        super().__init__()
        self._page_ref = page_ref
        self.data_manager = DataManager('data/words.csv')
        
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
            show_error(self._page_ref, f"Word '{self.word.value}' was replaced by '{translation}'")
            self.word.value = translation
        self.update()
    
    def process_word(self):

        self.word.value = self.word.value.strip()

        if not self.word.value:
            self.state['empty'] = True

        elif all(not char.isalpha() for char in self.word.value):
            self.state['unlettered'] = True
            
        else:
            try:
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
            except DetectLanguageError as e:
                self.state['unrec'] = True
                return None
                
    def check_api_key(self):
        """Check if API key is set in .env file."""
        api_key = os.getenv('DETECTLANGUAGE_API_KEY')
        return api_key is not None and api_key.strip() != ''

    def translate_click(self, e):
        if not self.check_api_key():
            show_error(self._page_ref, 'API key is not configured. Please add DETECTLANGUAGE_API_KEY to .env file.')
            return
        
        translation = self.process_word()
        
        if self.state['empty'] or self.state['unlettered']:
            show_error(self._page_ref, 'Enter a word.')
        elif self.state['unrec']:
            show_error(self._page_ref, 'Invalid API key. Please check your DETECTLANGUAGE_API_KEY in .env file.')
        elif self.word.value == translation:
            show_error(self._page_ref, 'The word cannot be translated.')
        elif self.state['undef_lang']:
            show_error(self._page_ref, 'Use English or Ukrainian languages.')
        else:
            self.translated_word.value = translation
            self.save_button.disabled = False
        self.update()

    def save_word(self, e):
        en_word = self.translated_word.value if self.target_language == 'en' else self.word.value
        uk_word = self.word.value if self.target_language == 'en' else self.translated_word.value
        
        if self.data_manager.add_word(en_word, uk_word):
            self.save_button.disabled = True
            show_error(self._page_ref, f'The word "{self.word.value}" was added to the dictionary.')
        else:
            show_error(self._page_ref, 'Word is already in the dictionary.')

        self.update()