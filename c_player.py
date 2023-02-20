# Creat a player
class Player():
    def __init__(self, player_numero, player_name, player_id, player_id_bot_channel):
        self.n_player = player_numero
        self.pseudo = player_name
        self.id = player_id
        self.id_bot_private_channel = player_id_bot_channel
        self.score = 0
        # 0 : don't have start the game | 1 : in FR game | 2 : game finish | 3 : in EN game
        self.game = 0
        self.chance = 0
        self.suggested_word = None
        self.emoji_day_word = None
        self.emoji_suggested_word = None