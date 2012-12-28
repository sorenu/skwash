from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from skwash.apps.website.models import RankingBoard

class ProtectedRankingBoardListView(ListView):
    model = RankingBoard
    template_name = 'website/ranking_board_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardListView, self).dispatch(*args, **kwargs)

class ProtectedRankingBoardDetailView(DetailView):
    model = RankingBoard
    template_name = 'website/ranking_board_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardDetailView, self).dispatch(*args, **kwargs)