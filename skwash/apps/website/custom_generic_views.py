from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Q
from skwash.apps.website.models import RankingBoard, MatchChallenge, Match


class ProtectedRankingBoardListView(ListView):
    template_name = 'website/rankingboard_list.html'
    context_object_name = 'ranking_boards'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return RankingBoard.objects.filter(Q(owner=user) | Q(players__id__exact=user.id)).distinct()

    def get_context_data(self, **kwargs):
        context = super(ProtectedRankingBoardListView, self).get_context_data(**kwargs)
        user = self.request.user

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


class ProtectedRankingBoardDetailView(DetailView):
    model = RankingBoard
    template_name = 'website/rankingboard_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedRankingBoardDetailView, self).dispatch(*args, **kwargs)


class ProtectedChallengesListView(ListView):
    template_name = 'website/matchchallenge_list.html'
    context_object_name = 'match_challenges'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedChallengesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        # return user.get_profile().get_all_challenges()
        return MatchChallenge.objects.filter(Q(challenger=user) | Q(challengee=user))


# class ProtectedMatchDetailView(DetailView):
#     model = Match
#     template_name = 'website/match_detail.html'
    
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(ProtectedMatchDetailView, self).dispatch(*args, **kwargs)

#     def get_queryset(self):
#         user = self.request.user
#         print dir(self.request)
#         return Match.objects.all()

