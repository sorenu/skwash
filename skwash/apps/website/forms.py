from skwash.apps.website.models import RankingBoard, Match
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput

class RankingBoardForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all())

    class Meta:
        model = RankingBoard
        fields = ('title', 'players')


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ('winner', 'challenge')
        widgets = {
            'challenge': HiddenInput(),
        }
