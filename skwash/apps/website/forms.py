from skwash.apps.website.models import RankingBoard
from django.contrib.auth.models import User
from django import forms

class RankingBoardForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all())

    class Meta:
        model = RankingBoard
        fields = ('title', 'players')
        # filter_horizontal = ('players',)
