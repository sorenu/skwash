def get_received_match_challenge(request, ranking_board_id, opponent_id):
    user = request.user
    mc = user.challenges_received.filter(ranking_board_id=ranking_board_id, challenger_id=opponent_id)
    if mc:
        return mc[0]
    return None

def get_sent_match_challenge(request, ranking_board_id, opponent_id):
    user = request.user
    mc = user.challenges_sent.filter(ranking_board_id=ranking_board_id, challengee_id=opponent_id)
    if mc:
        return mc[0]
    return None