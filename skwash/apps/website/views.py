from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.views.generic.create_update import create_object, update_object, delete_object
from skwash.apps.website.forms import RankingBoardForm
from skwash.apps.website.models import RankingBoard


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



