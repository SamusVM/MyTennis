from django.contrib import admin
from .models import *

admin.site.register(Backhand)
# admin.site.register(Choice)
admin.site.register(City)
admin.site.register(Court)
admin.site.register(Covering)
admin.site.register(Game)
admin.site.register(Game_Log)
admin.site.register(Hand)
admin.site.register(Match)
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

admin.site.register(Region)
admin.site.register(Set)
admin.site.register(Shot_Hand)
admin.site.register(Shot_Type)
admin.site.register(Stadium)
admin.site.register(Tag)
admin.site.register(Tourney_Group)
admin.site.register(Tourney)
admin.site.register(Torney_Group_Name)
admin.site.register(Torney_Group_Player)
admin.site.register(Torney_Round)
admin.site.register(Winner_type)


