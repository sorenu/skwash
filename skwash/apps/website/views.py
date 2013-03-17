from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from skwash.apps.website.forms import RankingBoardForm, MatchForm
from skwash.apps.website.form_views import RankingBoardCreate, RankingBoardUpdate
from skwash.apps.website.models import RankingBoard, MatchChallenge, Match
from skwash.apps.website.view_helpers import get_received_match_challenge, get_sent_match_challenge
from django.db.models import Q
from django.views.generic import TemplateView
from friendship.models import Friend, FriendshipRequest


def logout(request):
    return logout_then_login(request)


@login_required
def profile(request):
    return render(request, 'website/player_detail.html', {'profile_user': request.user})

def other_profile(request, username):
    user = User.objects.get(username=username)
    are_friends = Friend.objects.are_friends(request.user, user)
    return render(request, 'website/player_detail.html', {'profile_user': user, 'are_friends': are_friends})    


@login_required
def friends_list(request):
    buddy_requests = FriendshipRequest.objects.filter(to_user__id=request.user.id)
    all_friends = Friend.objects.friends(request.user)
    print all_friends
    return render(request, 'website/friends_list.html', {'buddy_requests': buddy_requests, 'all_friends': all_friends})


@login_required
def friends_add(request, user_id):
    other = User.objects.get(id=user_id)
    try:
        Friend.objects.add_friend(request.user, other)
    except:
        return HttpResponse()
    return HttpResponse()


@login_required
def friends_remove(request, user_id):
    other = User.objects.get(id=user_id)
    try:
        Friend.objects.remove_friend(request.user, other)
    except:
        return HttpResponse()
    return HttpResponse()


@login_required
def friends_accept(request, request_id):
    request = FriendshipRequest.objects.get(id=request_id)
    request.accept()
    return HttpResponse()


@login_required
def friends_cancel(request, user_id):
    other = User.objects.get(id=user_id)
    requests = Friend.objects.requests(other)
    for r in requests:
        print r.from_user
        print r.to_user
        if r.from_user == request.user:
            r.cancel()
            return HttpResponse()


@login_required
def friends_button(request, user_id):
    other = User.objects.get(id=user_id)
    are_friends = Friend.objects.are_friends(request.user, other)

    if are_friends:
        return render(request, 'website/buddy_button.html', {'are_friends': True, 'profile_user': other})

    requested = False
    requests = Friend.objects.requests(other)
    for r in requests:
        if r.from_user == request.user:
            requested = True
            break

    if requested:
        return render(request, 'website/buddy_button.html', {'requested': True, 'profile_user': other})
    return render(request, 'website/buddy_button.html', {'are_friends': False, 'profile_user': other})


@login_required
def set_match_winner(request, ranking_board_id, opponent_id, winner_id):
    user = request.user
    match = Match.objects.filter((Q(challenge__challenger_id=user.id) & Q(challenge__challengee_id=opponent_id)) | (Q(challenge__challengee_id=user.id) & Q(challenge__challenger_id=opponent_id))).filter(challenge__ranking_board_id=ranking_board_id).exclude(challenge__status=MatchChallenge.STATUS_PLAYED).exclude(challenge__status=MatchChallenge.STATUS_DECLINED)
    if match:
        match = match[0]
    else:
        return HttpResponseNotFound()

    winner = User.objects.get(id=winner_id)
    match.set_winner(winner)
    return HttpResponse()


@login_required
def play_match(request, ranking_board_id, opponent_id):
    return render(request, 'website/match_play.html', {'board_id': ranking_board_id, 'opponent_id': opponent_id})


@login_required
def new_challenge(request, ranking_board_id, opponent_id):
    opponent = User.objects.get(id=opponent_id)
    board = RankingBoard.objects.get(id=ranking_board_id)
    request.user.get_profile().challenge(opponent, board)
    return challenge_button_cancel(request, ranking_board_id, opponent_id)


@login_required
def accept_challenge(request, ranking_board_id, opponent_id):
    mc = get_received_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.accept(request.user)
    return challenge_button_play(request, ranking_board_id, opponent_id)


@login_required
def decline_challenge(request, ranking_board_id, opponent_id):
    mc = get_received_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.decline(request.user)
    return challenge_button_challenge(request, ranking_board_id, opponent_id)


@login_required
def cancel_challenge(request, ranking_board_id, opponent_id):
    mc = get_sent_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.cancel(request.user)
    return challenge_button_challenge(request, ranking_board_id, opponent_id)


def challenge_button_cancel(request, ranking_board_id, opponent_id):
    return render(request, 'website/challenge_buttons/challenge_button_cancel.html', {'board_id': ranking_board_id, 'opponent_id': opponent_id})

def challenge_button_challenge(request, ranking_board_id, opponent_id):
    return render(request, 'website/challenge_buttons/challenge_button_challenge.html', {'board_id': ranking_board_id, 'opponent_id': opponent_id})

def challenge_button_play(request, ranking_board_id, opponent_id):
    return render(request, 'website/challenge_buttons/challenge_button_play.html', {'board_id': ranking_board_id, 'opponent_id': opponent_id})

def challenge_button_received(request, ranking_board_id, opponent_id):
    return render(request, 'website/challenge_buttons/challenge_button_received.html', {'board_id': ranking_board_id, 'opponent_id': opponent_id})

def ranking_board_html(request, board_id):
    board = RankingBoard.objects.get(id=board_id)
    if not board:
        return HttpResponseNotFound()
    context = get_board_context({'board': board}, request)
    return render(request, 'website/board.html', context)


def get_board_context(context, request):
    user = request.user
    challenges_accepted = {}
    challenges_received = {}
    for c in user.challenges_received.all():
        challenges_received.setdefault(c.ranking_board_id, [])
        challenges_accepted.setdefault(c.ranking_board_id, [])
        if c.status == MatchChallenge.STATUS_PENDING:
            challenges_received[c.ranking_board_id].append(c.challenger_id)
        elif c.status == MatchChallenge.STATUS_ACCEPTED:
            challenges_accepted[c.ranking_board_id].append(c.challenger_id)

    challenges_sent = {}
    for c in user.challenges_sent.all():
        challenges_sent.setdefault(c.ranking_board_id, [])
        challenges_accepted.setdefault(c.ranking_board_id, [])
        # challenges_sent[c.ranking_board_id].append(c.challengee_id)
        if c.status == MatchChallenge.STATUS_PENDING:
            challenges_sent[c.ranking_board_id].append(c.challengee_id)
        elif c.status == MatchChallenge.STATUS_ACCEPTED:
            challenges_accepted[c.ranking_board_id].append(c.challengee_id)
            print c

    context['challenges_received'] = challenges_received
    context['challenges_sent'] = challenges_sent
    context['challenges_accepted'] = challenges_accepted

    return context


