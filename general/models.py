# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

DATA_SOURCE = (
    ('FanDuel', 'FanDuel'),
    ('DraftKings', 'DraftKings'),
    ('Yahoo', 'Yahoo'),
    ('Fanball', 'Fanball')
)

class Player(models.Model):
    uid = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=250, default="/static/img/nba.ico")
    injury = models.CharField(max_length=250, blank=True, null=True)
    opponent = models.CharField(max_length=50)
    
    minutes = models.FloatField(default=0)              # ampg
    money_line = models.IntegerField(default=0)
    over_under = models.FloatField(default=0)           # smpg
    point_spread = models.FloatField(default=0)
    position = models.CharField(max_length=50)
    actual_position = models.CharField(max_length=50)
    proj_ceiling = models.FloatField(default=0)
    proj_custom = models.FloatField(default=0)
    proj_floor = models.FloatField(default=0)
    proj_original = models.FloatField(default=0)
    proj_points = models.FloatField(default=0)
    proj_rotowire = models.FloatField(default=0)
    proj_site = models.FloatField(default=0)            # sfp
    proj_third_party_one = models.FloatField(default=0)
    proj_third_party_two = models.FloatField(default=0)  
    salary = models.IntegerField(default=0)
    salary_custom = models.FloatField(default=0)        # afp
    salary_original = models.FloatField(default=0)      # l3a
    team = models.CharField(max_length=50)
    team_points = models.FloatField(default=0)
    value = models.FloatField(default=0)
    
    play_today = models.BooleanField(default=False)
    data_source = models.CharField(max_length=30, choices=DATA_SOURCE, default='FanDuel')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class FavPlayer(models.Model):
    player = models.ForeignKey(Player)

    def __str__(self):
        return '{} {}'.format(self.player.first_name, self.player.last_name)


GAME_RESULT = (
    ('W', 'Win'),
    ('L', 'Loss'),
)

class PlayerGame(models.Model):
    name = models.CharField("Player", max_length=50)
    team = models.CharField("Tm", max_length=50)
    location = models.CharField("H-A", max_length=50)
    opp = models.CharField("Vs", max_length=50)
    game_result = models.CharField("W-L", max_length=50, choices=GAME_RESULT)

    mp = models.FloatField("MP")
    fg = models.IntegerField("FG")
    fga = models.IntegerField("FGA")
    fg_pct = models.FloatField("FG%", null=True, blank=True)
    fg3 = models.IntegerField("3P")
    fg3a = models.IntegerField("3PA")
    fg3_pct = models.FloatField("3P%", null=True, blank=True)
    ft = models.IntegerField("FT")
    fta = models.IntegerField("FTA")
    ft_pct = models.FloatField("FT%", null=True, blank=True)
    trb = models.IntegerField("REB")
    ast = models.IntegerField("AST")
    stl = models.IntegerField("ST")
    blk = models.IntegerField("BLK")
    tov = models.IntegerField("TO")
    pf = models.IntegerField("PF")
    pts = models.IntegerField("PTS")
    fpts = models.FloatField("FPTS", default=-1)
    date = models.DateField()

    def __str__(self):
        return self.name


GAME_STATUS = (
    ('started', 'Started'),
    ('upcomming', 'Upcomming')
)

class Game(models.Model):
    home_team = models.CharField(max_length=20)
    visit_team = models.CharField(max_length=20)
    ou = models.FloatField(default=0)
    ml = models.CharField(max_length=20)
    date = models.DateTimeField()
    game_status = models.CharField(max_length=50, choices=GAME_STATUS, default='started')

    def __str__(self):
        return '{} - {}'.format(self.home_team, self.visit_team)


# Team Matchup Sheet Cache
class TMSCache(models.Model):
    team = models.CharField(max_length=10)
    type = models.IntegerField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.team
