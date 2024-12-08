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
        self.db_uri: str = ""  # TODO: Add your database URI here as a string
        if self.db_uri != "":
            self.game_db: db.GameDB = db.GameDB(self.db_uri)

    def login(self, name: str, password: str):
        """
        This method logs the player in.
        :param name: Player username
        :param password: Player password
        :return: a player object, if successful login returns the information from the database
        """
        self.player.id = self.game_db.validate_player_login(name, password)
        self.player = self.game_db.get_player_info(self.player.id)

    def create_user(self, name: str, password: str):
        """
        This method creates a new user.
        :param name: new Player's username
        :param password: new Player's password
        :return: the newly created Player object
        """
        self.game_db.add_player_user(name, password)
        self.player.id = self.game_db.validate_player_login(name, password)
        self.player = self.game_db.get_player_info(self.player.id)

    def update_player_stats(self, won: bool) -> None:
        """
        This method logs the game results and new token balance.
        :param won: True if the player won the game, False if they lost
        :return:
        """
        game_db: db.GameDB = db.GameDB(self.db_uri)
        try:
            game_db.log_game(self.player.id, won, self.player.tokens)
        except Exception as e:
            print(e)
