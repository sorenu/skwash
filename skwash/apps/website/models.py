from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



########################################################
#  GAME
########################################################

class RankingBoard(models.Model):
    owner = models.ForeignKey(User, related_name='owned_ranking_boards')
    players = models.ManyToManyField(User)
    title = models.CharField(max_length=200)

    def add_player(self, player):
        if (player not in self.players.all()):
            self.players.add(player)
            Ranking.objects.create(player=player, board=self).save()

    def ranked_players(self):
        players = list(self.players.all())
        players.sort(key=lambda p: p.get_profile().get_ranking(self).score, reverse=True)
        players = [(p, p.get_profile().get_ranking(self).score) for p in players]
        return players

    def __unicode__(self):
        string = 'Title: %s\n' % (self.title)
        string += 'Owner: %s\n' % (self.owner)
        for player in self.ranked_players():
            rank = player[0].get_profile().get_ranking(self).score
            wins, matches = player[0].get_profile().get_winnings()
            string += '%s: %.3f (%d / %d)\n' % (player, rank, len(wins), len(matches))
        return string


class Ranking(models.Model):
    player = models.ForeignKey(User)
    board = models.ForeignKey(RankingBoard)
    score = models.DecimalField(decimal_places=4, max_digits=20, default=1500)


class MatchChallenge(models.Model):
    STATUS_ACCEPTED = 1
    STATUS_PENDING = 0
    STATUS_DECLINED = -1

    ranking_board = models.ForeignKey(RankingBoard)
    challenger = models.ForeignKey(User, related_name='challenges_sent')
    challengee = models.ForeignKey(User, related_name='challenges_received')
    status = models.IntegerField() # -1 declined, 0 pending, 1 accepted

    def decline(self, declined_by):
        if declined_by.id == self.challengee.id:
            self.status = self.STATUS_DECLINED
            self.save()
        else:
            raise Exception('Only the challengee can decline a challenge!')

    def accept(self, accepted_by):
        if accepted_by.id == self.challengee.id:
            if self.status != self.STATUS_ACCEPTED:
                match = Match.objects.create(challenge=self)
                match.save()
                self.status = self.STATUS_ACCEPTED
                self.save()
                return match
        else:
            raise Exception('Only the challengee can accept a challenge!')

    def __unicode__(self):
        desc = 'Challenger: %s' % (self.challenger)
        desc += '\nChallengee: %s' % (self.challengee)
        desc += '\nStatus: %d' % (self.status)
        return desc


MAX_INCREASE = 32

class Match(models.Model):
    challenge = models.OneToOneField(MatchChallenge)
    winner = models.ForeignKey(User, blank=True, null=True)

    def set_winner(self, winner):
        p1 = self.challenge.challenger
        p2 = self.challenge.challengee
        loser = p1 if winner.id == p2.id else p2
        score = self.elo(winner, loser, self.challenge.ranking_board)
        self.winner = winner
        self.save()

        return score

    def elo(self, winner, loser, ranking_board):
        winner_ranking = Ranking.objects.filter(player__id=winner.id).filter(board=ranking_board)[0]
        loser_ranking = Ranking.objects.filter(player__id=loser.id).filter(board=ranking_board)[0]

        score = MAX_INCREASE * 1 / (1 + 10 ** ((winner_ranking.score - loser_ranking.score) / 400))

        winner_ranking.score += score
        loser_ranking.score -= score

        winner_ranking.save()
        loser_ranking.save()

        return score



########################################################
#  CUSTOM USER
########################################################

class UserProfile(models.Model):
    user = models.OneToOneField(User)   # This field is required.

    def challenge(self, opponent, ranking_board):
        mc = MatchChallenge.objects.create(ranking_board=ranking_board, challenger=self.user, challengee=opponent, status=MatchChallenge.STATUS_PENDING)
        mc.save()
        return mc

    def get_pending_matches(self):
        matches = list(self.user.challenges_received.select_related().filter(match__isnull=False).filter(match__winner__id__isnull=True))
        matches += list(self.user.challenges_sent.select_related().filter(match__isnull=False).filter(match__winner__id__isnull=True))
        return [m.match for m in matches]

    def get_played_matches(self):
        matches = list(self.user.challenges_received.select_related().filter(match__isnull=False).filter(match__winner__id__isnull=False))   
        matches += list(self.user.challenges_sent.select_related().filter(match__isnull=False).filter(match__winner__id__isnull=False))
        return [m.match for m in matches]

    def get_winnings(self):
        matches = self.get_played_matches()
        won_matches = []
        for m in matches:
            if m.winner.id == self.user.id:
                won_matches.append(m)

        return (won_matches, matches)

    def get_ranking(self, ranking_board):
        ranking = Ranking.objects.filter(player__id=self.user.id).filter(board=ranking_board)[0]
        return ranking

    # def get_all_challenges(self):
    #     challenges = list(self.user.challenges_received.all())
    #     challenges += list(self.user.challenges_sent.all())
    #     return challenges


    def __unicode__(self):
        challenges_received = self.user.challenges_received.all()
        challenges_received = '\n'.join([str(a) for a in challenges_received])
        challenges_sent = '\n'.join([str(a) for a in self.user.challenges_sent.all()])
        desc = '--Challenges received--\n%s' % (challenges_received)
        desc += '\n--Challenges sent--\n%s' % (challenges_sent)
        return desc


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)



