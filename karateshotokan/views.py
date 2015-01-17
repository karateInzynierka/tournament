# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import itertools
from main.models import Tournament
from main.models import Manager
from main.models import Player
from main.models import Team
from main.models import PlayerTournament
from main.models import Coach

from karateshotokan.forms import ShotokanCategoryCreateForm, ShotokanPlayerCreateForm
from karateshotokan.models import ShotokanCategory
from karateshotokan.models import Round


# Widok glowny systemu shotokan
def KarateShotokanMain(request):
    template = loader.get_template('shotokan-main.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


# Turnieje tylko typu shotokan
def ShotokanTournaments(request):
    tournaments = Tournament.objects.all().filter(type='SHO')

    return render(request, 'shotokanTournaments.html', {'tournaments': tournaments, })


# Zawodnicy tylko na zawodach shotokan
@login_required
def ShotokanPlayers(request, tournament_id):
    coach = Coach.objects.get(user_id__user=request.user)
    teams = Team.objects.filter(coach=coach)

    players = []

    for team in teams:
        players.extend(Player.objects.filter(team_id=team.id))

    return render(request, 'shotokanPlayers.html', {'players': players, 'tournament_id': tournament_id })


# Organizacja turnieju shotokan
def shotokanTournamentOrganization(request, tournament_id):
    template = loader.get_template('shotokanTournamentOrganization.html')
    tournament = Tournament.objects.get(id=tournament_id)
    manager = Manager.objects.get(tournament=tournament)
    categories = ShotokanCategory.objects.filter(tournament_id=tournament)
    players = Player.objects.all()
    context = RequestContext(request, {'tournament': tournament, 'categories': categories, 'manager': manager, 'players': players,})
    return HttpResponse(template.render(context))


# Tworzenie nowej kategorii
@login_required
def createCategoryShotokan(request, tournament_id):
    template = loader.get_template('shotokanCreateCategory.html')

    if request.method == 'POST':
        form = ShotokanCategoryCreateForm(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.get(id=tournament_id)
            instance = form.save()  # instance zawiera zapisany obiekt, takze z jego id
            ShotokanCategory.objects.filter(id=instance.id).update(tournament_id=tournament)
            return redirect('shotokanTournamentOrganization', tournament_id=tournament.id)
    else:
        form = ShotokanCategoryCreateForm()
    context = RequestContext(request, {'form': form, })
    return HttpResponse(template.render(context))


# Funkcje do losowania zawodnikow:
def check(who, tournament_pairs):
    for fighter in tournament_pairs:
        if who == fighter[0] or who == fighter[1]:
            return False
    return True

#Jezeli sam
def who_not_fight(tournament_pairs, fighters):
    final_fighters = list(itertools.chain(*tournament_pairs))

    return list(set(fighters) - set(final_fighters))

#Nastepna runda button
def get_checked(request, category_id, round_number):
    if request.method == 'POST':
        keys = [key for key in request.POST.keys() if key.isnumeric()]

        if len(keys) == 1:
            playerT = PlayerTournament.objects.get(pk=keys[0])

            round = Round.objects.filter(
                category=ShotokanCategory.objects.get(id=category_id),
                number=round_number,
                playerT_first=playerT
            )
            if round:
                round = round[0]

                round.who_win = round.playerT_first.id
            else:
                round = Round.objects.get(
                    category=ShotokanCategory.objects.get(id=category_id),
                    number=round_number,
                    playerT_second=playerT
                )
                round.who_win = round.playerT_second.id

            round.save()
        else:
            for playerT_id in keys:
                playerT = PlayerTournament.objects.get(pk=playerT_id)

                player = 1

                round = Round.objects.filter(
                    category=ShotokanCategory.objects.get(id=category_id),
                    number=round_number,
                    playerT_first=playerT
                )

                if not round:
                    player = 2

                    round = Round.objects.filter(
                        category=ShotokanCategory.objects.get(id=category_id),
                        number=round_number,
                        playerT_second=playerT
                    )

                round = round[0]

                if player == 1:
                    round.who_win = round.playerT_first.id
                    round.save()
                elif player == 2:
                    round.who_win = round.playerT_second.id
                    round.save()

    return HttpResponseRedirect('/shotokan-category/%s/%d/' % (category_id, int(round_number) + 1))


# Generowanie walk
def shotokanCategory(request, category_id, round_number=1):
    template = loader.get_template('shotokan-category.html')
    category = ShotokanCategory.objects.get(id=category_id)
    manager = Manager.objects.get(tournament=category.tournament_id)

    if request.method == 'POST':
        from main.utils import create_fights_pdf

        history_fights = {}

        if int(round_number) > 1:
            for number in xrange(1, int(round_number)):
                rounds = Round.objects.filter(
                    category=category,
                    number=number
                )

                history_fights[number] = []

                for round in rounds:
                    history_fights[number].append(round.who_fight())

        history_fights[int(round_number)] = []

        rounds = Round.objects.filter(
            category=category,
            number=round_number
        )

        for round in rounds:
            history_fights[int(round_number)].append((round.playerT_first, round.playerT_second))

        #utworz pdf
        create_fights_pdf(
            request.user,
            category.tournament_id.name,
            history_fights
        )

    if int(round_number) == 1:
        fighters = category.playerT_id.all().order_by('?')
    else:
        rounds = Round.objects.filter(
            category=category,
            number=int(round_number) - 1,
            who_win__isnull=False
        ).order_by('?')

        fighters = [PlayerTournament.objects.get(pk=round.who_win) for round in rounds]

    all_pairs = itertools.combinations(fighters, 2)

    tournament_pairs = []

    for pair in all_pairs:
        if check(pair[0], tournament_pairs):
            tournament_pairs.append(pair)

    alone_fighter = who_not_fight(tournament_pairs, fighters)

    if alone_fighter:
        tournament_pairs.append((alone_fighter[0], None))

    Round.objects.filter(
        category=category,
        number=round_number
    ).delete()

    for fight in tournament_pairs:
        round = Round(
            category=category,
            number=round_number,
            playerT_first=fight[0],
            playerT_second=fight[1]
        )
        round.save()

    winner = False
    final_number = None

    if tournament_pairs:
        if len(tournament_pairs) == 1 and not tournament_pairs[0][0] or not tournament_pairs[0][1]:
            winner = True

            round = Round.objects.get(
                category=category,
                number=round_number
            )

            if not round.who_win:
                if round.playerT_first:
                    round.who_win = round.playerT_first.id
                elif round.playerT_second:
                    round.who_win = round.playerT_second.id

                round.save()

    history_fights = None

    if int(round_number) > 1:
        history_fights = {}

        for number in xrange(1, int(round_number)):
            rounds = Round.objects.filter(
                category=category,
                number=number
            )

            history_fights[number] = []

            for round in rounds:
                history_fights[number].append(round.who_fight())

    context = RequestContext(request, {
        'category': category,
        'manager': manager,
        'fights': tournament_pairs,
        'history_fights': history_fights,
        'round_number': round_number,
        'winner': winner
    })

    return HttpResponse(template.render(context))

@login_required
def shotokanAddPlayersToCategory(request, category_id):
    template = loader.get_template('shotokanAddPlayerToCategory.html')
    category = ShotokanCategory.objects.get(id=category_id)
    playersT = PlayerTournament.objects.filter(tournament_id=category.tournament_id, acceptedbymanager=True,
                                               acceptedbycoach=True)
    players = list()
    for playerCat in category.playerT_id.all():
        playersT = playersT.exclude(id=playerCat.player_id.id)
    for playerT in playersT:
        players.append(playerT.player_id)
    context = RequestContext(request, {'category': category, 'players': players})
    return HttpResponse(template.render(context))


def shotokanPlayerToCategory(request, player_id, category_id):
    category = ShotokanCategory.objects.get(id=category_id)
    player = Player.objects.get(id=player_id)
    playerT = PlayerTournament.objects.get(player_id=player, tournament_id=category.tournament_id)
    category.playerT_id.add(playerT)
    return redirect('shotokanAddPlayersToCategory', category_id=category.id)


def shotokanDeletePlayerFromCategory(request, player_id, category_id):
    category = ShotokanCategory.objects.get(id=category_id)
    player = Player.objects.get(id=player_id)
    playerT = PlayerTournament.objects.get(player_id=player, tournament_id=category.tournament_id)
    category.playerT_id.remove(playerT)
    return redirect('shotokanCategory', category_id=category.id)


def shotokanDeletePlayerFromTournament(request, player_id, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    player = Player.objects.get(id=player_id)
    playerT = PlayerTournament.objects.get(player_id=player, tournament_id=tournament_id)
    tournament.playerT_id.remove(playerT)
    return redirect('shotokanCategory', tournament_id=tournament.id)


def shotokanDeleteTournament(request, tournament_id, category_id):
    category = ShotokanCategory.objects.get(id=category_id)
    tournament = Tournament.objects.get(id=tournament_id)
    playersT = PlayerTournament.objects.all()
    tournament.playersT_id.remove(playersT)
    tournament.remove(category)
    return redirect('shotokanCategory', category_id=category.id)

@login_required
def shotokanUpdateCategory(request, category_id):
    template = loader.get_template('shotokanUpdateCategory.html')
    category = ShotokanCategory.objects.get(id=category_id)
    if request.method == 'POST':
        form = ShotokanCategoryCreateForm(request.POST, instance=category)

        if form.is_valid():
            category = ShotokanCategory(
            name=form.cleaned_data.get('name'),
            type_fight=ShotokanCategory.objects.get(type_fight=form.cleaned_data.get("type_fights")),
            )
            category.save()

            return redirect('shotokanCategory', category_id=category.id)
    else:
        form = ShotokanCategoryCreateForm()

    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))


# Tworzenie zawodnika
@login_required
def createPlayerShotokan(request, tournament_id):
    template = loader.get_template('shotokanCreatePlayer.html')

    if request.method == 'POST':
        form = ShotokanPlayerCreateForm(request.POST)

        if form.is_valid():
            player = Player(
                name=form.cleaned_data.get('name'),
                surname=form.cleaned_data.get('surname'),
                team_id=Team.objects.get(name=form.cleaned_data.get('teams')),
                acceptedbycoachteam=True,
                acceptedbyplayer=True
            )
            player.save()

            player_tournament = PlayerTournament(
                player_id=player,
                tournament_id=Tournament.objects.get(pk=tournament_id),
                acceptedbymanager=True,
                acceptedbycoach=True
            )
            player_tournament.save()

            return redirect('/shotokanPlayers/%s/' % tournament_id)
    else:
        form = ShotokanPlayerCreateForm()

    context = RequestContext(request, {'form': form, })
    return HttpResponse(template.render(context))