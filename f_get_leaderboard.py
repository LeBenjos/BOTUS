# Make and return a leaderboard
def get_leaderboard(all_players):
    # If nobody was registered
    if len(all_players) <= 1:
        return all_players
    
    # Delet the fake players
    if all_players[0].id == None:
        del all_players[0]

    # Get the leaderboard
    pivot_value = all_players[-1].score
    pivot = []
    list_inf = []
    list_supp = []
    for i in range (0,len(all_players),1):
        if all_players[i].score < pivot_value:
            list_inf.append(all_players[i])
        elif all_players[i].score > pivot_value:
            list_supp.append(all_players[i])
        else:
            pivot.append(all_players[i])
    # Return the leaderboard
    return get_leaderboard(list_inf) + pivot + get_leaderboard(list_supp)
