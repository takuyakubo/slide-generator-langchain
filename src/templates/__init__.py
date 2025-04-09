from pathlib import Path

def get_template(filename):
    current_directory = Path(__file__).parent
    file_path = current_directory / filename
    with file_path.open() as f:
        return f.read()