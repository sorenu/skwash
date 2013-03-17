from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from skwash.apps.website.custom_generic_views import ProtectedRankingBoardListView, ProtectedRankingBoardDetailView, ProtectedChallengesListView
from skwash.apps.website.form_views import RankingBoardCreate, RankingBoardUpdate, RankingBoardDelete
from django.views.generic import TemplateView

urlpatterns = patterns('skwash.apps.website.views',
    (r'^$', ProtectedRankingBoardListView.as_view()),

    (r'^rankingboards/new/$', RankingBoardCreate.as_view(success_url='/')),
    (r'^rankingboards/delete/(?P<pk>\d+)/$', RankingBoardDelete.as_view(success_url='/')),
    (r'^rankingboards/(?P<pk>\d+)/$', RankingBoardUpdate.as_view(success_url='/')),
    (r'^rankingboards/html/(?P<board_id>\d+)/$', 'ranking_board_html'),

    (r'^profile/$', 'profile'),
    (r'^profile/(?P<username>\w+)/$', 'other_profile'),

    (r'^challenges/$', ProtectedChallengesListView.as_view()),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/new/$', 'new_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/accept/$', 'accept_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/decline/$', 'decline_challenge'),
    (r'^challenges/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/cancel/$', 'cancel_challenge'),

    (r'^matches/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/play/$', 'play_match'),
    (r'^matches/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/(?P<winner_id>\d+)/set_winner/$', 'set_match_winner'),

    (r'^challenge-button-state-cancel/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/$', 'challenge_button_cancel'),
    (r'^challenge-button-state-challenge/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/$', 'challenge_button_challenge'),
    (r'^challenge-button-state-play/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/$', 'challenge_button_play'),
    (r'^challenge-button-state-received/(?P<ranking_board_id>\d+)/(?P<opponent_id>\d+)/$', 'challenge_button_received'),

    (r'^buddies/$', 'friends_list'),
    (r'^buddies/(?P<user_id>\d+)/add/$', 'friends_add'),
    (r'^buddies/(?P<user_id>\d+)/button/$', 'friends_button'),
    (r'^buddies/(?P<user_id>\d+)/cancel/$', 'friends_cancel'),
    (r'^buddies/(?P<user_id>\d+)/remove/$', 'friends_remove'),
    (r'^buddies/(?P<request_id>\d+)/accept/$', 'friends_accept'),
)

urlpatterns += patterns('skwash.apps.website.search',
    (r'^search/$', 'search'),
)