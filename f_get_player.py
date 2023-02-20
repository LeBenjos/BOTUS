# Get the current player
def get_player(id_player, list_players):
    for i in range (0,len(list_players),1):
        if id_player == list_players[i].id:
            return i
    return False

# Get the best player
def get_best_player(list_players):
    best_player_score = list_players[0].score
    best_player_indice = 0
    for i in range (0, len(list_players),1):
        if list_players[i].score > best_player_score:
            best_player_score = list_players[i].score
            best_player_indice = i
    return best_player_indice

# Get the target id
def get_target_id(t_id):
    target_id = list(str(t_id))
    del target_id[0]
    del target_id [0]
    del target_id [len(target_id)-1]
    target_id = "".join(target_id)
    return int(target_id)