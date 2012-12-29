from django.conf.urls import patterns, include, url
from skwash.apps.website.custom_generic_views import ProtectedRankingBoardListView, ProtectedRankingBoardDetailView, ProtectedChallengesListView


urlpatterns = patterns('skwash.apps.website.views',
    (r'^$', ProtectedRankingBoardListView.as_view()),
    (r'^rankingboards/new/$', 'new_ranking_board'),
    (r'^rankingboards/(?P<pk>\d+)/$', ProtectedRankingBoardDetailView.as_view()),
    (r'^rankingboards/edit/(?P<ranking_board_id>\d+)/$', 'edit_ranking_board'),
    (r'^rankingboards/delete/(?P<ranking_board_id>\d+)/$', 'delete_ranking_board'),

    (r'^profile/$', 'profile'),

    (r'^challenges/$', ProtectedChallengesListView.as_view()),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/new/$', 'new_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/accept/$', 'accept_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/decline/$', 'decline_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/cancel/$', 'cancel_challenge'),

    (r'^matches/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/play/$', 'play_match'),
)
