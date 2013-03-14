from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from skwash.apps.website.custom_generic_views import ProtectedRankingBoardListView, ProtectedRankingBoardDetailView, ProtectedChallengesListView
from skwash.apps.website.form_views import RankingBoardCreate, RankingBoardUpdate, RankingBoardDelete

urlpatterns = patterns('skwash.apps.website.views',
    (r'^$', ProtectedRankingBoardListView.as_view()),

    (r'^rankingboards/new/$', RankingBoardCreate.as_view(success_url='/')),
    (r'^rankingboards/delete/(?P<pk>\d+)/$', RankingBoardDelete.as_view(success_url='/')),
    (r'^rankingboards/(?P<pk>\d+)/$', RankingBoardUpdate.as_view(success_url='/')),

    (r'^profile/$', 'profile'),

    (r'^challenges/$', ProtectedChallengesListView.as_view()),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/new/$', 'new_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/accept/$', 'accept_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/decline/$', 'decline_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/cancel/$', 'cancel_challenge'),

    (r'^matches/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/play/$', 'play_match'),
)
