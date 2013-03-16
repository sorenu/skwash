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


def logout(request):
    return logout_then_login(request)


@login_required
def profile(request):
    return render(request, 'website/player_detail.html')


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

# @login_required
# def play_match(request, ranking_board_id, opponent_id):
#     user = request.user
#     match = Match.objects.filter((Q(challenge__challenger_id=user.id) & Q(challenge__challengee_id=opponent_id)) | (Q(challenge__challengee_id=user.id) & Q(challenge__challenger_id=opponent_id))).filter(challenge__ranking_board_id=ranking_board_id).exclude(challenge__status=MatchChallenge.STATUS_PLAYED).exclude(challenge__status=MatchChallenge.STATUS_DECLINED)
#     if match:
#         match = match[0]
#     else:
#         return HttpResponseNotFound()

#     if request.method == 'POST':
#         form = MatchForm(request.POST, instance=match)
#         if form.is_valid():
#             match = form.save(commit = False)
#             match.set_winner(match.winner)
#             match.save()
#             return redirect('/')
#     else:
#         form = MatchForm(instance=match)
#         form.fields['winner'].queryset = User.objects.filter(id__in=[match.challenge.challenger_id, match.challenge.challengee_id])
#     return render(request, 'website/match_form.html', {'form': form})


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


