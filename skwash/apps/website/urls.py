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
    (r'^match/(?P<challenge_id>\d+)/(?P<ranking_board_id>\d+)/play/$', 'play_match'),
)
