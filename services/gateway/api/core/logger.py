

from pprint import pprint


class Logger:
    def info(self, message: str):
        print(f"[INFO] {message}")

    def error(self, message: str):
        print(f"[ERROR] {message}")

    def debug(self, message: str):
        pprint(f"[DEBUG] {message}")


logger = Logger()
