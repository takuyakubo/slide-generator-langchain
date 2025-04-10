from pathlib import Path


class TemplateManager:
    def __init__(self) -> None:
        self.current_directory = Path(__file__).parent
        self.file_path = None

    def check_(self, file_name):
        self.file_path = self.current_directory / file_name
        if not self.file_path.exists():
            raise Exception("そのようなtemplateはありません")

    @property
    def content(self):
        if self.file_path is None:
            raise Exception("取得の前にcheck_を実行して下さい。")
        with self.file_path.open() as f:
            return f.read()


templates = TemplateManager()
