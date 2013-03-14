from django.views.generic.edit import CreateView, UpdateView, DeleteView
from skwash.apps.website.models import RankingBoard
from skwash.apps.website.forms import RankingBoardForm

class RankingBoardCreate(CreateView):
    model = RankingBoard
    form_class= RankingBoardForm

    def form_valid(self, form):
        board = form.save(commit = False)
        board.owner = self.request.user
        board.save()
        form.save_m2m()
        board.players.add(self.request.user)
        board.save()
        return super(RankingBoardCreate, self).form_valid(form)

class RankingBoardUpdate(UpdateView):
    model = RankingBoard
    form_class= RankingBoardForm

class RankingBoardDelete(DeleteView):
    model = RankingBoard