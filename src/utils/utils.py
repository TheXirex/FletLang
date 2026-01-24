import flet as ft


def show_error(page_ref: ft.Page, text: str):
    """Show error message."""
    snack = ft.SnackBar(content=ft.Text(text), bgcolor=ft.Colors.TEAL_400)
    page_ref.overlay.append(snack)
    snack.open = True
    page_ref.update()


def validate_word_input(word: str) -> tuple[bool, str]:
    """Validate word input."""
    word = word.strip()
    
    if not word:
        return False, 'Enter a word.'
    
    if all(not char.isalpha() for char in word):
        return False, 'Enter a word.'
    
    return True, ''
