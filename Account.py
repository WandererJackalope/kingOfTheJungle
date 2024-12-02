import db


class Account:
    """
    This class is responsible for handling the player's account.
    """
    def __init__(self):
        """
        This method initializes the account class.
        """
        self.player: db.Player = db.Player(-1, "Player", 1000, 0, 0)
        self.logged_in: bool = False
        db_uri: str = ""  # TODO: Add your database URI here as a string

    def login(self, name: str, password: str) -> db.Player:
        """
        This method logs the player in.
        :param name: Player username
        :param password: Player password
        :return: a player object, if successful login returns the information from the database
        """
        pass

    def create_user(self, name: str, password: str) -> db.Player:
        """
        This method creates a new user.
        :param name: new Player's username
        :param password: new Player's password
        :return: the newly created Player object
        """
        pass
