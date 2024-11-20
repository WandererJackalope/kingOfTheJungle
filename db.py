from dataclasses import dataclass
import psycopg2
# import hashlib


class InvalidLogin(Exception):
    pass


@dataclass
class Player:
    id: int
    name: str
    tokens: int
    win_count: int
    loss_count: int



class GameDB:
    def __init__(self, db_conn_uri: str):
        self.conn = psycopg2.connect(db_conn_uri)

    

    def validate_player_login(self, name: str, password: str) -> int:
        """
        Validates username and password and returns the user ID.
        Raises InvalidLogin when the login is incorrect.
        Returns an integer ID of the user on successful validation.
        """
        pass

    def add_player_user(self, name: str, password: str, tokens: int = 1000):
        """
        hash the password with sha256 and store the name, hashed password, and token amount into the database
        does not return anything
        """
        pass

    def log_game(self, player_id: int, won: bool, new_token_balance: int):
        """
        Logs game results and updates player statistics
        
        Args:
            player_id: int - The ID of the player
            won: bool - True if player won the game, False if they lost
            new_token_balance: int - The number of tokens the player now has
        """

        with self.conn.cursor() as cur:
            colm = "win_count" if won else "loss_count"
            query = f'UPDATE "Player" SET tokens = %(tokens)s, {colm} = {colm} + 1 WHERE id = %(id)s'
            values = {
            'tokens': new_token_balance,
            'id': player_id
             }
            cur.execute(query, values)
           

        

    def get_player_info(self, player_id: int) -> Player:
        """
        gets all player info:
        player id, player name, current stored token balance, win count, loss count
        """
        with self.conn.cursor() as cur:
            cur.execute('SELECT id, name, tokens, win_count, loss_count FROM "Player" WHERE id=%s', (player_id,))
            res = cur.fetchone()
            print(res)
            return Player(id=res[0], name=res[1], tokens=res[2], win_count=res[3], loss_count=res[4])


