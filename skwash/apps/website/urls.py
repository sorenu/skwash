from django.conf.urls import patterns, include, url
# from django.contrib.auth.models import User
# from skwash.apps.website.models import RankingBoard
# from django.views.generic import ListView
# from django.contrib.auth.decorators import login_required
from skwash.apps.website.custom_generic_views import ProtectedRankingBoardListView, ProtectedRankingBoardDetailView


urlpatterns = patterns('skwash.apps.website.views',
    (r'^$', ProtectedRankingBoardListView.as_view()),
    (r'^ranking_boards/new/$', 'new_ranking_board'),
    (r'^ranking_boards/(?P<pk>\d+)/$', ProtectedRankingBoardDetailView.as_view()),
    (r'^ranking_boards/edit/(?P<ranking_board_id>\d+)/$', 'edit_ranking_board'),
    (r'^ranking_boards/delete/(?P<ranking_board_id>\d+)/$', 'delete_ranking_board'),
    (r'^profile/$', 'profile'),
)
