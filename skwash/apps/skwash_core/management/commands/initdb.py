from django.core.management.base import BaseCommand
from skwash.apps.website.models import RankingBoard, MatchChallenge
from django.contrib.auth.models import User
from friendship.models import Friend, FriendshipRequest

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

        self.player7 = User.objects.create_user('Christian Risom', 'christian@shape.dk', 'test1234')
        self.player8 = User.objects.create_user('Nicolas Thomsen', 'nicolas@shape.dk', 'test1234')
        self.player9 = User.objects.create_user('Ole Gammelgaard', 'ole@shape.dk', 'test1234')
        self.player10 = User.objects.create_user('Philip Bruce', 'philip@shape.dk', 'test1234')
        self.player11 = User.objects.create_user('Rasmus Nutzhorn', 'rvn@shape.dk', 'test1234')
        self.player12 = User.objects.create_user('Mikkel Selsoe', 'mikkel@shape.dk', 'test1234')
        self.player13 = User.objects.create_user('Rasmus Nielsen', 'rasmus@shape.dk', 'test1234')
        self.player14 = User.objects.create_user('Kasper Kronborg', 'kasper@shape.dk', 'test1234')
        self.player15 = User.objects.create_user('Jonas Lysgaard', 'jonas@shape.dk', 'test1234')
        self.player16 = User.objects.create_user('David Jorgensen', 'david@shape.dk', 'test1234')
        self.player17 = User.objects.create_user('Casper Storm', 'casper@shape.dk', 'test1234')
        self.player18 = User.objects.create_user('Kacper Kawecki', 'kacper@shape.dk', 'test1234')
        self.player19 = User.objects.create_user('Soren Ulrikkeholm', 'soren@shape.dk', 'test1234')

        self.player20 = User.objects.create_user('Emil Hveisel', 'emil@email.com', 'test1234')
        self.player21 = User.objects.create_user('Toke Bundgaard', 'toke@email.com', 'test1234')
        self.player22 = User.objects.create_user('Riccardo Pietri', 'ricci@email.com', 'test1234')

        self.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8, self.player9, self.player10, self.player11, self.player12, self.player13, self.player14, self.player15, self.player16, self.player17, self.player18, self.player19, self.player20, self.player21, self.player22]

        self.ranking_board1 = RankingBoard.objects.create(owner=self.player1, title='League by 10')
        self.ranking_board2 = RankingBoard.objects.create(owner=self.player3, title='League by 30')
        self.ranking_board3 = RankingBoard.objects.create(owner=self.player4, title='League by 40')

        self.ranking_board4 = RankingBoard.objects.create(owner=self.player19, title='Shape Liga')
        self.ranking_board5 = RankingBoard.objects.create(owner=self.player19, title='Noerrebrohallen')

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

        self.ranking_board4.players.add(self.player7)
        self.ranking_board4.players.add(self.player8)
        self.ranking_board4.players.add(self.player9)
        self.ranking_board4.players.add(self.player10)
        self.ranking_board4.players.add(self.player11)
        self.ranking_board4.players.add(self.player12)
        self.ranking_board4.players.add(self.player13)
        self.ranking_board4.players.add(self.player14)
        self.ranking_board4.players.add(self.player15)
        self.ranking_board4.players.add(self.player16)
        self.ranking_board4.players.add(self.player17)
        self.ranking_board4.players.add(self.player18)
        self.ranking_board4.players.add(self.player19)

        self.ranking_board5.players.add(self.player19)
        self.ranking_board5.players.add(self.player20)
        self.ranking_board5.players.add(self.player21)
        self.ranking_board5.players.add(self.player22)
        
        self.player2.get_profile().challenge(self.player1, self.ranking_board1)
        self.player3.get_profile().challenge(self.player1, self.ranking_board1)
        self.player4.get_profile().challenge(self.player1, self.ranking_board1)
        self.player1.get_profile().challenge(self.player4, self.ranking_board1)
        self.player1.get_profile().challenge(self.player5, self.ranking_board1)
        self.player4.get_profile().challenge(self.player5, self.ranking_board1)


        new_relationship = Friend.objects.add_friend(self.player19, self.player10)
        new_relationship.accept()
        new_relationship = Friend.objects.add_friend(self.player19, self.player11)
        new_relationship.accept()
        new_relationship = Friend.objects.add_friend(self.player19, self.player13)
        new_relationship.accept()
        new_relationship = Friend.objects.add_friend(self.player20, self.player19)
        new_relationship.accept()
        new_relationship = Friend.objects.add_friend(self.player21, self.player19)
        new_relationship.accept()
        new_relationship = Friend.objects.add_friend(self.player22, self.player19)
        new_relationship.accept()

        new_relationship = Friend.objects.add_friend(self.player7, self.player19)
        new_relationship = Friend.objects.add_friend(self.player16, self.player19)
        
        new_relationship = Friend.objects.add_friend(self.player14, self.player19)
        new_relationship = Friend.objects.add_friend(self.player12, self.player19)
        new_relationship = Friend.objects.add_friend(self.player8, self.player19)
        new_relationship = Friend.objects.add_friend(self.player9, self.player19)
        new_relationship = Friend.objects.add_friend(self.player18, self.player19)
        new_relationship = Friend.objects.add_friend(self.player17, self.player19)


