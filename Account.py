import db


class Account:
    def __init__(self):
        self.player: db.Player = db.Player(-1, "Player", 1000, 0, 0)
        self.logged_in: bool = False
        db_uri: str = "" # TODO: Add your database URI here as a string

    def login(self, name: str, password: str) -> db.Player:
        pass

    def create_user(self, name: str, password: str):
        pass