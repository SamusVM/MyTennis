from django.db import models
from django.utils import timezone
from  django.db.models import Sum
import datetime
# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    class Meta:
        verbose_name = 'Регіон'
        verbose_name_plural = 'Регіони'
        ordering = ('name',)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank='TRUE', null='True')
    post_code = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Stadium(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank='TRUE', null='True')
    address = models.CharField(max_length=1000)
    t_open = models.TimeField()
    t_close = models.TimeField()
    act = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Стадіон'
        verbose_name_plural = 'Стадіони'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Covering(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Покриття'
        verbose_name_plural = 'Покриття'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Hand(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        verbose_name = 'Покриття'
        verbose_name_plural = 'Покриття'
        ordering = ('name',)
    def __str__(self):
        return self.name


class Backhand(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        verbose_name = 'Бекхенд'
        verbose_name_plural = 'Бекхенди'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=20)
    flag = models.ImageField()

    class Meta:
        verbose_name = 'Країна'
        verbose_name_plural = 'Країни'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=20)
    country =  models.ForeignKey(Country, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'
        ordering = ('name',)
    def __str__(self):
        return self.name



class Court(models.Model):
    name = models.CharField(max_length=200)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, blank='TRUE', null='True')
    covering = models.ForeignKey(Covering, on_delete=models.SET_NULL, blank='TRUE', null='True')
    allows_doubles =  models.BooleanField(default=True)
    is_roof = models.BooleanField(default=False)
    act = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Корт'
        verbose_name_plural = 'Корти'
        ordering = ('name',)
    def __str__(self):
        return self.name



class Person(models.Model):
    ss = (
        ('M','male',),
        ('F','female'),
    )
    sex = models.CharField(max_length=50,choices=ss, default='M')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(blank=True,null=True)
    foto = models.ImageField('Фото', upload_to='images', blank=True,null=True)
    d_birth = models.DateField(blank=True,null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Фізична особа'
        verbose_name_plural = 'Фізичні особи'
        ordering = ('last_name','first_name',)
    def full_name(self):
        return self.last_name + ' '+ self.first_name
    def __str__(self):
        return self.full_name()



class Player(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    is_profy = models.BooleanField(default=False)
    d_start = models.DateField(blank='TRUE', null='True')
    hand = models.ForeignKey(Hand, on_delete=models.SET_NULL, blank='TRUE', null='True',default=1)
    backhand = models.ForeignKey(Backhand, on_delete=models.SET_NULL, blank='TRUE', null='True',default=1)
    racket = models.CharField(max_length=50,blank='TRUE', null='True')
    strings = models.CharField(max_length=50, blank='TRUE', null='True')
    shoes = models.CharField(max_length=50,blank='TRUE', null='True')
    balls = models.CharField(max_length=50,blank='TRUE', null='True')
    atp_players = models.CharField(max_length=50,blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Гравець'
        verbose_name_plural = 'Гравці'
        ordering = ('person',)
    def __str__(self):
        return self.person.__str__()

class Match_type(models.Model):
    name = models.CharField(max_length=50)
    n_player = models.IntegerField(default=2)
    class Meta:
        verbose_name = 'Тип матчу'
        verbose_name_plural = 'Типи матчів'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Shot_Hand(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Удар'
        verbose_name_plural = 'Удари'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Shot_Type(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Тип удару'
        verbose_name_plural = 'Типи ударів'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Place_Court(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Частина корту'
        verbose_name_plural = 'Частини корту'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Winner_type(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Тип виграшу'
        verbose_name_plural = 'Типи виграшів'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Match(models.Model):
    game_type = models.ForeignKey(Match_type,db_index=True, on_delete=models.SET_NULL, blank='TRUE', null='True')
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, blank='TRUE', null='True')
    dt = models.DateTimeField(blank=True,null=True)
    is_official = models.BooleanField(default=True)
    player1 = models.ForeignKey(Player, related_name='p1',db_index=True, on_delete=models.SET_NULL, blank='TRUE', null='True')
    player2 = models.ForeignKey(Player, related_name='p2',db_index=True,on_delete=models.SET_NULL, blank='TRUE', null='True')
    player3 = models.ForeignKey(Player, related_name='p3',db_index=True,on_delete=models.SET_NULL, blank='TRUE', null='True')
    player4 = models.ForeignKey(Player, related_name='p4',db_index=True,on_delete=models.SET_NULL, blank='TRUE', null='True')
    s1 = models.IntegerField(default=0)
    s2 = models.IntegerField(default=0)
    g1 = models.IntegerField(default=0)
    g2 = models.IntegerField(default=0)
    is_winner = models.BooleanField(default=True)
    winner = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчі'
        ordering = ('-dt',)
    def __str__(self):
        if self.player3 and self.player4:
            return self.player1.__str__()+'/'+self.player3 .__str__() +' - '+ self.player2.__str__()+'/'+self.player4 .__str__()
        else:
            return self.player1.__str__()  + ' - ' + self.player2.__str__()

class Set(models.Model):
    match = models.ForeignKey(Match, db_index=True, on_delete=models.SET_NULL, blank='TRUE', null='True')
    nn = models.IntegerField(default=1)
    dt = models.DateTimeField(blank=True,null=True)
    g1 = models.IntegerField(default=0)
    g2 = models.IntegerField(default=0)
    is_tiebreak = models.BooleanField(default=False)
    tb1 = models.IntegerField(default=0)
    tb2 = models.IntegerField(default=0)
    is_winner = models.BooleanField(default=True)
    winner = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сети'
        ordering = ('-match',)
    def __str__(self):
        return self.match.__str__() + ' set '+str(self.nn)

class Game(models.Model):
    set = models.ForeignKey(Set, db_index=True, on_delete=models.SET_NULL, blank='TRUE', null='True')
    nn = models.IntegerField(default=1)
    is_winner = models.BooleanField(default=True)
    winner = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Гейм'
        verbose_name_plural = 'Гейми'
        ordering = ('-set',)
    def __str__(self):
        return self.set.__str__() + ' game '+self.nn

class Game_Log(models.Model):
    game = models.ForeignKey(Game,db_index=True, on_delete=models.SET_NULL, blank='TRUE', null='True')
    dt = models.DateTimeField(auto_now_add=True)
    winner = models.IntegerField(default=0)
    winner_type = models.ForeignKey(Winner_type, on_delete=models.SET_NULL, blank='TRUE', null='True')
    player = models.IntegerField(default=0)
    shot_hand = models.ForeignKey(Shot_Hand, on_delete=models.SET_NULL, blank='TRUE', null='True')
    shot_type = models.ForeignKey(Shot_Type, on_delete=models.SET_NULL, blank='TRUE', null='True')
    place_court = models.ForeignKey(Place_Court, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Хід гри'
        verbose_name_plural = 'Хід гри'
        ordering = ('-game',)
    def __str__(self):
        return self.game.__str__()


class Player_Rank(models.Model):
    player = models.ForeignKey(Player, db_index=True,on_delete=models.SET_NULL, blank='TRUE', null='True')
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank='TRUE', null='True')
    dt = models.DateTimeField(auto_now_add=True)
    delta_rahk = models.IntegerField(default=0)
    delta_rahk_doubles = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('-dt',)

class Torney_Group_Name(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Турнірна група(назва)'
        verbose_name_plural = 'Турнірні групи(назва)'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Torney_Round(models.Model):
    name = models.CharField(max_length=50)
    n_playr = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Раунд'
        verbose_name_plural = 'Раунди'
        ordering = ('name',)
    def __str__(self):
        return self.name

class Tourney(models.Model):
    name = models.CharField(max_length=200)
    dt = models.DateField(blank='True', null= 'True')
    rules = models.TextField()
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Турнір'
        verbose_name_plural = 'Турніри'
        ordering = ('-dt',)
    def __str__(self):
        return self.name

class Tourney_Group(models.Model):
    name = models.CharField(max_length=50)
    tourney = models.ForeignKey(Tourney, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Турнірна група'
        verbose_name_plural = 'Турнірні групи'
        ordering = ('name',)
    def __str__(self):
        return self.name + self.tourney.__str__()

class Torney_Group_Player(models.Model):
    tourney_group = models.ForeignKey(Tourney_Group, on_delete=models.SET_NULL, blank='TRUE', null='True')
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank='TRUE', null='True')
    class Meta:
        verbose_name = 'Гравець турніру'
        verbose_name_plural = 'Гравці турніру'
        ordering = ('tourney_group','player',)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    def all_votes(self):
        return self.choice_set.aggregate(Sum('votes'))#self.objects.aggregate(Choice.votes)


    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'
        ordering = ('-pub_date',)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def votes_per(self):
        vs = self.question.choice_set.aggregate(Sum('votes'))
        return self.votes / vs['votes__sum'] *100
    class Meta:
        verbose_name = 'Варіант відповіді'
        verbose_name_plural = 'Варіанти відповіді'
        ordering = ('question',)
    def __str__(self):
        return self.choice_text

class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тег'
        ordering = ('name',)

class News(models.Model):
    pub_date = models.DateTimeField()
    caption = models.CharField(max_length=200, primary_key=True)
    text = models.TextField()
    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ('-pub_date',)
    def __str__(self):
        return self.caption

class Myimage(models.Model):
    img = models.ImageField('Фото', upload_to='images')
    dt = models.DateTimeField(blank=True, null=True,)
    tag = models.ForeignKey(Tag,blank=True, null=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('-dt',)

class Order_court(models.Model):
    court = models.ForeignKey(Court,blank=True, null=True, on_delete=models.SET_NULL)
    d_start = models.DateTimeField('Дата початку')
    d_fin = models.DateTimeField('Дата завершення')
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank='TRUE', null='True')

    class Meta:
        verbose_name = 'Замовлення корту'
        verbose_name_plural = 'Замовлення корту'
        ordering = ('-d_start',)
    def __str__(self):
        return self.player +' '+self.court