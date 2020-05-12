from django.contrib import admin
from .models import *

admin.site.register(Backhand)
admin.site.register(Balls)
admin.site.register(Brands)
admin.site.register(City)

admin.site.register(Country)
admin.site.register(Court)
admin.site.register(Covering)
admin.site.register(Game)
admin.site.register(Game_Log)
admin.site.register(Hand)

class SetInline(admin.TabularInline):
    model = Set
    extra = 1

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': [('game_type', 'court','dt', 'is_official','tourney_group', 'group_id')]}),
        ('Гравці', {'fields': [('player1','player2'), ('player3','player4')]}),
        ('Результати', {'fields': [('s1', 's2', 'g1', 'g2','is_winner', 'winner','withdrawal' )]}),
    ]
    inlines = [SetInline]
    list_display = ('pp','rez1', 'pplayer1','pplayer2', 'court' ,'dt', 'is_official','tourney_group')
    list_filter = ['dt','tourney_group__tourney','tourney_group']
    search_fields = ['player1__person__last_name','player2__person__last_name','player3__person__last_name','player4__person__last_name']

admin.site.register(Match, MatchAdmin)
admin.site.register(Match_type)
admin.site.register(Myimage)
admin.site.register(News)
admin.site.register(Order_court)
admin.site.register(Person)
admin.site.register(Place_Court)
admin.site.register(Player)
admin.site.register(Player_Rank)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Rackets)
admin.site.register(Region)
admin.site.register(Set)
admin.site.register(Shoes)
admin.site.register(Shot_Hand)
admin.site.register(Shot_Type)
admin.site.register(Strings)

admin.site.register(Stadium)
admin.site.register(Tag)
admin.site.register(Tourney_Group)
admin.site.register(Tourney)
admin.site.register(Tourney_Group_Name)

class PlayerInline(admin.StackedInline):
    model = Player
    extra = 4

class Tourney_Group_Player_Admin(admin.ModelAdmin):
    fieldsets = [
        ('Турнір',               {'fields': ['tourney_group']}),
        ('Гравець', {'fields': ['nn','player']}),
    ]
    # inlines = [PlayerInline]
    list_display = ('tourney_group','nn', 'player')
    ordering = ['tourney_group','nn']
    list_filter = ['tourney_group__tourney__name','tourney_group__name']
    search_fields = ['tourney_group']
admin.site.register(Tourney_Group_Player,Tourney_Group_Player_Admin)

admin.site.register(Tourney_Round)
admin.site.register(Winner_type)


