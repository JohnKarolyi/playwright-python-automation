import json
import os

class FileHandler:
    @staticmethod
    def read_json(file_path):
        """Beolvas egy JSON fájlt és szótárként adja vissza."""
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path, data):
        """Kiírja az adatokat egy JSON fájlba."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)