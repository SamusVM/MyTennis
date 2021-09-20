from django.forms import ModelForm, TextInput, formset_factory,SplitDateTimeWidget, RadioSelect, ModelChoiceField
from .models import  Match, Set,Tourney_Group_Player,Player_Rank,Tourney_Group
from django.contrib.admin.widgets import AdminSplitDateTime

class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['court','dt','score']
        widgets = {'score':TextInput }
    # def __init__(self, *args, **kwargs):
    #     super(MatchForm, self).__init__(*args, **kwargs)
    #     self.fields['dt'].widget = AdminSplitDateTime()


class MatchFormFullPP(ModelForm):
    class Meta:
        model = Match
        fields = ['court','dt','player1','player3','player2','player4','score']
        widgets = {'score':TextInput}

class MatchFormFullP(ModelForm):
    class Meta:
        model = Match
        fields = ['court','dt','player1','player2','score']
        widgets = {'score':TextInput}

class SetsForm(ModelForm):
    class Meta:
        model = Set
        fields = '__all__'

class TourneyGroupPlayerForm(ModelForm):
    class Meta:
        model = Tourney_Group_Player
        fields = ['player', 'player2' ,'nn','rank']


class TourneyGroupForm(ModelForm):
    class Meta:
        model = Tourney_Group
        fields = ['name','n_players','play_off', 'max_rank' ]

class PlayerRankForm(ModelForm):
    class Meta:
        model = Player_Rank
        fields = ['player', 'tourney', 'rank_in_tourney', 'delta_rahk']

class SelectTourneyGroupForm(ModelForm):
    g = ModelChoiceField(queryset=Tourney_Group.objects.all(), empty_label=None,widget=RadioSelect,label='Група')
    class Meta:
        model = Tourney_Group_Player
        fields = []
        widgets = {'tourney_group': RadioSelect()}

    def __init__(self, *args, **kwargs):
        tid = kwargs.pop('tid', None)
        super(SelectTourneyGroupForm, self).__init__(*args, **kwargs)

        if tid:
            # self.fields['tourney_group'].queryset = Tourney_Group.objects.filter(tourney_id=tid)
            self.fields['g'].queryset = Tourney_Group.objects.filter(tourney_id=tid,max_rank__gt=0)