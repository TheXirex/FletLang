import pandas as pd


class DataManager:
    """Manages CSV data operations for the word dictionary."""
    
    def __init__(self, filepath: str = 'words.csv'):
        """Initialize the data manager with the CSV file path."""
        self.filepath = filepath
    
    def read_data(self) -> pd.DataFrame:
        """Read data from CSV file."""
        return pd.read_csv(self.filepath)
    
    def save_data(self, data: pd.DataFrame):
        """Save data to CSV file."""
        data.to_csv(self.filepath, index=False)
    
    def add_word(self, en_word: str, uk_word: str) -> bool:
        """Add a new word pair to the dictionary."""
        data = self.read_data()

        if en_word.lower() in data['en'].values and uk_word.lower() in data['uk'].values:
            return False
        
        new_data = pd.DataFrame({'en': [en_word.lower()], 'uk': [uk_word.lower()]})
        data = pd.concat([data, new_data], ignore_index=True)
        self.save_data(data)

        return True
    
    def delete_word(self, index: int):
        """Delete a word by index."""
        data = self.read_data()
        data = data.drop(index)
        self.save_data(data)
    
    def get_random_word(self, max_length: int = 28) -> dict:
        """Get a random word pair from the dictionary."""
        data = self.read_data()
        while True:
            random_word = data.sample()
            if (len(random_word['en'].values[0]) <= max_length and 
                len(random_word['uk'].values[0]) <= max_length):
                return {
                    'en': random_word['en'].values[0],
                    'uk': random_word['uk'].values[0]
                }
    
    def get_translations(self, word: str, language: str) -> list:
        """Get all translations for a given word."""
        data = self.read_data()
        target_lang = 'uk' if language == 'en' else 'en'
        return list(data[data[language] == word][target_lang].values)
