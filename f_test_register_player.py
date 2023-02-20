# Test if the player are already register
def test_register_player(id_player, players_list):
    for i in range(0,len(players_list),1):
        if id_player == players_list[i].id:
            return False
    return True