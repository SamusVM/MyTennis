import django_tables2 as tables
from .models import Player_Rank, Player

class RankTable(tables.Table):
    class Meta:
        model = Player
        # fields = ("player", "tourney", "delta_rahk", )
        # sequence = ("player",  "delta_rahk","tourney", )
        fields = ("person", "rnk", )
        # sequence = ("player",  "delta_rahk","tourney", )