import os


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TESTING_GUILD = os.getenv('TESTING_GUILD')

    @property
    def is_prod(self):
        return os.getenv('ENV', 'DEV') == 'PROD'
