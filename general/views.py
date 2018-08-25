# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import mimetypes

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from django.views.decorators.csrf import csrf_exempt

from general.models import *
from general.lineup import *

def players(request):
    return render(request, 'players.html', { 'data_sources': DATA_SOURCE })

@csrf_exempt
def get_players(request):
    ds = request.POST.get('ds')
    players = Player.objects.filter(data_source=ds).order_by('-proj_points')
    return HttpResponse(render_to_string('player-list_.html', locals()))

def get_num_lineups(player, lineups):
    num = 0
    for ii in lineups:
        if ii.is_member(player):
            num = num + 1
    return num

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def gen_lineups(request):
    rosters = []
    ids = request.POST.getlist('ids')
    num_lineups = int(request.POST.get('num-lineups'))
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    lineups = calc_lineups(players, num_lineups)
    total_num_lineups = get_total_num_lineups(players)
    avg_points = mean([ii.projected() for ii in lineups])

    players_ = [{ 'name': ii.name, 'team': ii.team, 'lineups': get_num_lineups(ii, lineups)} 
                for ii in players]
    players_ = sorted(players_, key=lambda k: k['lineups'], reverse=True)
    return HttpResponse(render_to_string('player-lineup.html', locals()))

def export_lineups(request):
    ids = request.POST.getlist('ids')
    num_lineups = int(request.POST.get('num-lineups'))
    ids = [int(ii) for ii in ids]
    players = Player.objects.filter(id__in=ids)
    lineups = calc_lineups(players, num_lineups)

    csv_fields = ['FWD', 'FWD', 'MID', 'MID', 'MID', 'DEF', 'DEF', 'GK', 'Projected', 'Salary']
    path = "/tmp/.fantasy_nba.csv"

    with open(path, 'w') as f:
        f.write(','.join(csv_fields)+'\n')
        for ii in lineups:
            f.write(ii.get_csv())
    
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path ) ) # same here        
    return response

@csrf_exempt
def update_point(request):
    pid = int(request.POST.get('pid'))
    points = request.POST.get('val')
    Player.objects.filter(id=pid).update(points=points)
    return HttpResponse('')