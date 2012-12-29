from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.models import User
from skwash.apps.website.forms import RankingBoardForm, MatchForm
from skwash.apps.website.models import RankingBoard, MatchChallenge, Match
from skwash.apps.website.view_helpers import get_received_match_challenge, get_sent_match_challenge
from django.db.models import Q



def logout(request):
    return logout_then_login(request)


@login_required
def view_ranking_board(request, ranking_board_id):
    return HttpResponse()


@login_required
def new_ranking_board(request):
    if request.method == 'POST':
        form = RankingBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit = False)
            board.owner = request.user
            board.save()
            form.save_m2m()
            board.players.add(request.user)
            return redirect('/')
    else:
        form = RankingBoardForm()
    return render(request, 'website/rankingboard_form.html', {'form': form})

    # return create_object(
    #     request,
    #     form_class = RankingBoardForm,
    #     post_save_redirect = '/',
    #     template_name = 'website/ranking_board_form.html',
    #     extra_context = {'owner': request.user.id},
    # )


@login_required
def edit_ranking_board(request, ranking_board_id):
    board = get_object_or_404(RankingBoard, pk=ranking_board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
    return update_object(
        request,
        form_class = RankingBoardForm,
        object_id = ranking_board_id,
        post_save_redirect = '/',
        template_name = 'website/rankingboard_form.html',
    )


@login_required
def delete_ranking_board(request, ranking_board_id):
    board = get_object_or_404(RankingBoard, pk=ranking_board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
    return delete_object(
        request,
        model = RankingBoard,
        object_id = ranking_board_id,
        post_delete_redirect = '/',
        template_name = 'website/rankingboard_confirm_delete.html',
    )


@login_required
def profile(request):
    return render(request, 'website/player_detail.html')


@login_required
def play_match(request, ranking_board_id, opponent_id):
    user = request.user
    match = Match.objects.filter((Q(challenge__challenger_id=user.id) & Q(challenge__challengee_id=opponent_id)) | (Q(challenge__challengee_id=user.id) & Q(challenge__challenger_id=opponent_id))).filter(challenge__ranking_board_id=ranking_board_id).exclude(challenge__status=MatchChallenge.STATUS_PLAYED).exclude(challenge__status=MatchChallenge.STATUS_DECLINED)
    if match:
        match = match[0]
    else:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            match = form.save(commit = False)
            match.set_winner(match.winner)
            match.save()
            return redirect('/')
    else:
        form = MatchForm(instance=match)
        form.fields['winner'].queryset = User.objects.filter(id__in=[match.challenge.challenger_id, match.challenge.challengee_id])
    return render(request, 'website/match_form.html', {'form': form})


@login_required
def new_challenge(request, ranking_board_id, opponent_id):
    opponent = User.objects.get(id=opponent_id)
    board = RankingBoard.objects.get(id=ranking_board_id)
    request.user.get_profile().challenge(opponent, board)
    return redirect('/')


@login_required
def accept_challenge(request, ranking_board_id, opponent_id):
    mc = get_received_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.accept(request.user)
    return redirect('/')


@login_required
def decline_challenge(request, ranking_board_id, opponent_id):
    mc = get_received_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.decline(request.user)
    return redirect('/')


@login_required
def cancel_challenge(request, ranking_board_id, opponent_id):
    mc = get_sent_match_challenge(request, ranking_board_id, opponent_id)
    if not mc:
        return HttpResponseNotFound()
    mc.cancel(request.user)
    return redirect('/')


