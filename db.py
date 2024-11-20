from dataclasses import dataclass
import psycopg2
import hashlib


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
       with self.conn.cursor() as cur:
        # Correct parameterized query
        cur.execute('SELECT hashed_password FROM "Player" WHERE name = %s LIMIT 1', (name,))
        result = cur.fetchone()
        
        if not result:
            raise InvalidLogin()

        stored_hash = result[0]
        hash_obj = hashlib.sha256(password.encode()).hexdigest()
        print(f"Stored Hash: {stored_hash}")
        print(f"Generated Hash: {hash_obj}")
        if stored_hash != hash_obj:
            raise InvalidLogin()

        # Fetch the player ID if password matches
        cur.execute('SELECT id FROM "Player" WHERE name = %s LIMIT 1', (name,))
        player_id = cur.fetchone()

        if not player_id:
            raise InvalidLogin()

        return player_id[0]


    def add_player_user(self, name: str, password: str, tokens: int = 1000):
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        try:
            with self.conn.cursor() as cur:
                cur.execute('INSERT INTO "Player" (name, hashed_password, tokens) VALUES (%s, %s, %s)', (name, hash_pass, tokens))
            self.conn.commit()  # Commit transaction
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            raise Exception("Player with this name already exists") from e



    def log_game(self, player_id: int, won: bool, new_token_balance: int):
        """
        Logs game results and updates player statistics
        
        Args:
            player_id: int - The ID of the player
            won: bool - True if player won the game, False if they lost
            new_token_balance: int - The number of tokens the player now has
        """
        try:
            with self.conn.cursor() as cur:
                colm = "win_count" if won else "loss_count"
                query = f'UPDATE "Player" SET tokens = %(tokens)s, {colm} = {colm} + 1 WHERE id = %(id)s'
                values = {
                    'tokens': new_token_balance,
                    'id': player_id
                }
                cur.execute(query, values)
                
                
                if cur.rowcount == 0:
                    raise ValueError(f"No player found with ID {player_id}")

        except (psycopg2.Error, ValueError) as e: 
            self.conn.rollback()
            raise

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


