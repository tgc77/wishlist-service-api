
import logging


class Logger(logging.Logger):

    def __init__(self, name, level=0):
        super().__init__(name, level)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s: %(message)s [%(filename)s: %(lineno)s]')
        handler.setFormatter(formatter)
        self.addHandler(handler)


logger = Logger(name="app.logger", level=logging.INFO)
