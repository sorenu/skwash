from django.core.management.base import BaseCommand
from skwash.apps.website.models import RankingBoard, MatchChallenge
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.player1 = User.objects.create_user('Player10', 'test1@example.com', 'test1234')
        self.player2 = User.objects.create_user('Player20', 'test2@example.com', 'test1234')
        self.player3 = User.objects.create_user('Player30', 'test3@example.com', 'test1234')
        self.player4 = User.objects.create_user('Player40', 'test4@example.com', 'test1234')
        self.players = [self.player1, self.player2, self.player3, self.player4]

        self.ranking_board = RankingBoard.objects.create(owner=self.player1, title='League of Test')

        self.ranking_board.add_player(self.player1)
        self.ranking_board.add_player(self.player2)
        self.ranking_board.add_player(self.player3)
        self.ranking_board.add_player(self.player4)
        
        self.player2.get_profile().challenge(self.player1, self.ranking_board)
        self.player3.get_profile().challenge(self.player1, self.ranking_board)
        self.player4.get_profile().challenge(self.player1, self.ranking_board)
        self.player1.get_profile().challenge(self.player4, self.ranking_board)