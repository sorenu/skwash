from django.core.management.base import BaseCommand
from skwash.apps.website.models import RankingBoard, MatchChallenge
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        [u.delete() for u in User.objects.all()]
        [r.delete() for r in RankingBoard.objects.all()]
        [m.delete() for m in MatchChallenge.objects.all()]


        self.player1 = User.objects.create_user('Player10', 'test1@example.com', 'test1234')
        self.player2 = User.objects.create_user('Player20', 'test2@example.com', 'test1234')
        self.player3 = User.objects.create_user('Player30', 'test3@example.com', 'test1234')
        self.player4 = User.objects.create_user('Player40', 'test4@example.com', 'test1234')
        self.player5 = User.objects.create_user('Player50', 'test4@example.com', 'test1234')
        self.player6 = User.objects.create_user('Player60', 'test4@example.com', 'test1234')
        self.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6]

        self.ranking_board1 = RankingBoard.objects.create(owner=self.player1, title='League by 10')
        self.ranking_board2 = RankingBoard.objects.create(owner=self.player3, title='League by 30')
        self.ranking_board3 = RankingBoard.objects.create(owner=self.player4, title='League by 40')

        self.ranking_board1.players.add(self.player1)
        self.ranking_board1.players.add(self.player2)
        self.ranking_board1.players.add(self.player3)
        self.ranking_board1.players.add(self.player4)
        self.ranking_board1.players.add(self.player5)
        self.ranking_board1.players.add(self.player6)

        self.ranking_board2.players.add(self.player1)
        self.ranking_board2.players.add(self.player3)
        self.ranking_board2.players.add(self.player4)
        self.ranking_board2.players.add(self.player6)

        self.ranking_board3.players.add(self.player4)
        self.ranking_board3.players.add(self.player6)
        
        self.player2.get_profile().challenge(self.player1, self.ranking_board1)
        self.player3.get_profile().challenge(self.player1, self.ranking_board1)
        self.player4.get_profile().challenge(self.player1, self.ranking_board1)
        self.player1.get_profile().challenge(self.player4, self.ranking_board1)
        self.player1.get_profile().challenge(self.player5, self.ranking_board1)
        self.player4.get_profile().challenge(self.player5, self.ranking_board1)



