"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from skwash.apps.website.models import RankingBoard, MatchChallenge
from django.contrib.auth.models import User


class RankingBoardTest(TestCase):
    def setUp(self):
        self.player1 = User.objects.create_user('Player1', 'test1@example.com', 'test1234')
        self.player2 = User.objects.create_user('Player2', 'test2@example.com', 'test1234')
        self.player3 = User.objects.create_user('Player3', 'test3@example.com', 'test1234')
        self.player4 = User.objects.create_user('Player4', 'test4@example.com', 'test1234')
        self.player5 = User.objects.create_user('Player5', 'test4@example.com', 'test1234')
        self.player6 = User.objects.create_user('Player6', 'test4@example.com', 'test1234')
        self.player7 = User.objects.create_user('Player7', 'test4@example.com', 'test1234')
        self.player8 = User.objects.create_user('Player8', 'test4@example.com', 'test1234')
        self.player9 = User.objects.create_user('Player9', 'test4@example.com', 'test1234')
        # self.players = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8, self.player9]
        self.players = [self.player1, self.player2, self.player3, self.player4]

        self.ranking_board = RankingBoard.objects.create(owner=self.player1, title='League of Test')

        self.ranking_board.add_player(self.player1)
        self.ranking_board.add_player(self.player2)
        self.ranking_board.add_player(self.player3)
        self.ranking_board.add_player(self.player4)
        # self.ranking_board.add_player(self.player5)
        # self.ranking_board.add_player(self.player6)
        # self.ranking_board.add_player(self.player7)
        # self.ranking_board.add_player(self.player8)
        # self.ranking_board.add_player(self.player9)
        
        self.player2.get_profile().challenge(self.player1, self.ranking_board)
        self.player3.get_profile().challenge(self.player1, self.ranking_board)
        self.player4.get_profile().challenge(self.player1, self.ranking_board)
        self.player1.get_profile().challenge(self.player4, self.ranking_board)
        
        # Just some extra data to test that the model does not get confused
        self.ranking_board2 = RankingBoard.objects.create(owner=self.player1)
        self.ranking_board2.add_player(self.player1)
        self.ranking_board2.add_player(self.player2)
        self.ranking_board2.add_player(self.player3)
        self.ranking_board2.add_player(self.player4)
        self.player2.get_profile().challenge(self.player1, self.ranking_board2)
        self.player3.get_profile().challenge(self.player1, self.ranking_board2)
        self.player4.get_profile().challenge(self.player1, self.ranking_board2)
        self.player1.get_profile().challenge(self.player4, self.ranking_board2)


    def test_aaaaalways_first(self):
        """
        Print out the setup.
        """
        print '====Players===='
        print self.players
        print
        print '====RankingBoard===='
        print self.ranking_board
        self.assertEqual(1 + 1, 2)


    def test_add_player(self):
        """
        Test that a player only gets added once to the ranking board.
        """
        before_count = len(self.ranking_board.players.all())
        self.ranking_board.add_player(self.player1)
        self.ranking_board.add_player(self.player1)
        self.ranking_board.add_player(self.player2)
        after_count = len(self.ranking_board.players.all())
        self.assertTrue(before_count == after_count)


    def test_accept_challenge(self):
        """
        Test that challenge status is pending until player accepts where it changes to accepted.
        Also verify that only challengee can accept.
        """
        challenges = self.player1.challenges_received.all()
        for c in challenges:
            self.assertTrue(c.status == MatchChallenge.STATUS_PENDING)
            c.accept(self.player1)
            self.assertTrue(c.status == MatchChallenge.STATUS_ACCEPTED)
            self.assertRaises(Exception, c.accept, self.player4)



    def test_decline_challenge(self):
        """
        Test that challenge status is pending until player delines where it changes to declined.
        Also verify that only challengee can decline.
        """
        challenges = self.player1.challenges_received.all()
        for c in challenges:
            self.assertTrue(c.status == MatchChallenge.STATUS_PENDING)
            c.decline(self.player1)
            self.assertTrue(c.status == MatchChallenge.STATUS_DECLINED)

            self.assertRaises(Exception, c.decline, self.player4)


    def test_played_matches(self):
        """
        Test that matches get registered as played when a winner has been set.
        """
        matches = self.player1.get_profile().get_played_matches() # make sure we don't get an exception
        self.assertTrue(len(matches) == 0)
        challenges = self.player1.challenges_received.all()
        [c.accept(self.player1) for c in challenges]
        matches = self.player1.get_profile().get_pending_matches()
        self.assertTrue(len(matches) > 0)

        for idx, match in enumerate(matches):
            if idx % 2 == 0:
                match.winner = match.challenge.challenger
            else:
                match.winner = match.challenge.challengee
            match.save()

        matches = self.player1.get_profile().get_played_matches()
        self.assertTrue(len(matches) > 0)


    def test_ranking(self):
        """
        Test that ranking changes correctly when players win matches.
        """
        import random

        print
        for i in range(40):
            random.shuffle(self.players)
            p1 = self.players[0]
            p2 = self.players[1]
            ps = [p1,p2]
            c = p1.get_profile().challenge(p2, self.ranking_board)
            m = c.accept(p2)
            winner = ps[random.randint(0,1)]
            ps.remove(winner)
            loser = ps[0]
            sw1 = winner.get_profile().get_ranking(self.ranking_board).score
            sl1 = loser.get_profile().get_ranking(self.ranking_board).score
            s = m.set_winner(winner)
            sw2 = winner.get_profile().get_ranking(self.ranking_board).score
            sl2 = loser.get_profile().get_ranking(self.ranking_board).score
            self.assertTrue(round(sw1 + s) == round(sw2))
            self.assertTrue(round(sl1 - s) == round(sl2))
            print '%s(%.2f) beats %s(%.2f)  -score->  (%.2f)' % (winner, sw1, loser, sl1, s)

        print
        print self.ranking_board


