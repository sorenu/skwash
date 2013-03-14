from django.views.generic.edit import CreateView, UpdateView, DeleteView
from skwash.apps.website.models import RankingBoard

class RankingBoardCreate(CreateView):
    model = RankingBoard

class RankingBoardUpdate(UpdateView):
    model = RankingBoard

class RankingBoardDelete(DeleteView):
    model = RankingBoard