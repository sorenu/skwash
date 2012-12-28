from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Q
from skwash.apps.website.models import RankingBoard


class ProtectedRankingBoardListView(ListView):
    template_name = 'website/rankingboard_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return RankingBoard.objects.filter(Q(owner=user) | Q(players__id__exact=user.id)).distinct()


class ProtectedRankingBoardDetailView(DetailView):
    model = RankingBoard
    template_name = 'website/rankingboard_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardDetailView, self).dispatch(*args, **kwargs)