import json
import os


class FileHandler:
    @staticmethod
    def read_json(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # GREEN FIX: mindig dict legyen
        if isinstance(data, list):
            return data[0]

        if not isinstance(data, dict):
            raise ValueError(f"Invalid JSON structure: {data}")

        return data

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)