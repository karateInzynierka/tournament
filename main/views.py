# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.db import IntegrityError

from main.forms import *
from karatekyokushin.forms import *
from models import Tournament


# Create your views here.
def home(request):
    tournaments = Tournament.objects.all()

    for tournament in tournaments:
        print tournament.start
        print tournament.end

    return render(request, 'home.html', {
        'tournaments': tournaments,
    })

def register_succes(request):

    return render(request, 'signUpSuccess.html',{})

def signUp(request):
    if request.method == 'POST':
        form = UserFormSignUp(request.POST)

        if form.is_valid():
            try:
                # Create django based user
                dj_user = DjangoUser.objects.create_user(
                    form.cleaned_data.get('name'),
                    form.cleaned_data.get('email')
                )
                dj_user.first_name = form.cleaned_data.get('name')
                dj_user.last_name = form.cleaned_data.get('surname')
                dj_user.set_password(request.POST.get('password'))
                dj_user.save()

                # Create custom user
                user = User(
                    user=dj_user,
                    email=form.cleaned_data.get('email'),
                    name=form.cleaned_data.get('name'),
                    surname=form.cleaned_data.get('surname'),

                )
                user.save()

                return HttpResponseRedirect('/register_succes/')
            except IntegrityError:
                return render(request, 'signUp.html', {
                    'formset': UserFormSignUp(),
                    'integrity_error': u'E-mail jest już przypisany do innego konta!'
                })

            return HttpResponseRedirect('/')
    else:
        form = UserFormSignUp()
    return render(request, 'signUp.html', {
        'formset': form,
    })


def signIn(request):
    if request.method == 'POST':
        form = UserFormSignIn(request.POST)

        if form.is_valid():
            try:
                username = User.objects.get(email=form.data['email'])
            except User.DoesNotExist:
                return HttpResponseRedirect('/signIn/')

            auth_user = authenticate(
                username=username.user,
                password=form.data['password']
            )

            print auth_user
            print auth_user.is_active

            if auth_user and auth_user.is_active:
                print login(request, auth_user)

                return redirect('/user/')

        else:
            print 'bledy', form.errors

            return HttpResponseRedirect('/signIn/')
    else:
        form = UserFormSignIn()
        return render_to_response('signIn.html', RequestContext(request, {'formset': form}))


def logout(request):
    django_logout(request)

    return redirect('/')


@login_required
def user(request):
    template = loader.get_template('user.html')
    user = User.objects.get(user=request.user)

    playerteam = Player.objects.filter(acceptedbycoachteam=True, acceptedbyplayer=False)

    player = Player.objects.filter(acceptedbycoachteam=True, acceptedbyplayer=True)

    playersT = PlayerTournament.objects.filter(player_id=player, acceptedbymanager=True, acceptedbycoach=True)

    try:
        coach = Coach.objects.get(user_id__user=request.user)

        teams = Team.objects.filter(coach_id=coach)
    except Coach.DoesNotExist:
        coach = None

    if Coach.objects.filter(user_id=user):
        coach = Coach.objects.get(user_id=user)
        teams = Team.objects.filter(coach=coach)
        coachtournaments = Tournament.objects.filter(coaches=coach)
        AplayersT = list()
        for team in teams:
            playersC = Player.objects.filter(team_id=team)
            for playerC in playersC:
                if PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True,
                                                   acceptedbycoach=False):
                    AplayersT.append(PlayerTournament.objects.get(player_id=playerC, acceptedbymanager=True,
                                                                  acceptedbycoach=False))
    else:
        teams = None
        coachtournaments = None
        AplayersT = None

    if Manager.objects.filter(user_id=user.id):
        managers = Manager.objects.filter(user_id=user.id)
        managertournaments = list()
        EplayersT = list()
        for manager in managers:
            tournament = Tournament.objects.get(id=manager.tournament.id)
            managertournaments.append(tournament)
            for EplayerT in PlayerTournament.objects.filter(tournament_id=tournament, acceptedbymanager=False,
                                                            acceptedbycoach=True):
                EplayersT.append(EplayerT)
    else:
        managertournaments = None
        EplayersT = None
    if EplayersT:
        EplayersT.sort(key=lambda player: player.player_id.team_id.name, reverse=False)
    context = RequestContext(request, {'playersT': playersT, 'ctournaments': coachtournaments,
                                       'mtournaments': managertournaments, 'teams': teams, 'user': user,
                                       'playerteam': playerteam, 'AplayersT': AplayersT, 'EplayersT': EplayersT})
    return HttpResponse(template.render(context))

@login_required
def updateProfile(request):
    success = False

    user = User.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserFormUpdateProfile(request.POST, instance=user)

        print form.fields

        if form.is_valid():
            user.user.username = form.cleaned_data.get("name")
            user.user.first_name = form.cleaned_data.get("name")
            user.user.last_name = form.cleaned_data.get("surname")

            email = form.cleaned_data.get("email")

            print 'email', email
            if email:
                user.user.email = form.cleaned_data.get("email")


            password = form.cleaned_data.get("password")
            print 'password', password
            if password:
                user.user.set_password(password)

            user.user.save()

            up = form.save(commit=False)
            up.user = request.user
            up.save()

            success = True

            if password:
                logout(request)

                return redirect('signIn')

            return redirect('updateProfile')
    else:
        form = UserFormUpdateProfile(instance=user)

    return render_to_response('updateProfile.html', locals(), context_instance=RequestContext(request))


@login_required
def createTeam(request):
    template = loader.get_template('createteam.html')

    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            user = User.objects.get(user=request.user)
            instance = form.save()  # instance zawiera zapisany obiekt, takze z jego id
            coachobj, bool = Coach.objects.get_or_create(
                user_id=user,
                defaults={'name': user.name, 'surname': user.surname}
            )
            Team.objects.filter(id=instance.id).update(coach=coachobj)
            return redirect('/user/')
    else:
        form = CreateTeamForm()

    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))


@login_required
def editTeam(request, team_id):
    template = loader.get_template('editTeam.html')
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        form = EditTeamForm(request.POST, instance=team)
        if form.is_valid():
            user = User.objects.get(user=request.user)
            form.save()  # instance zawiera zapisany obiekt, takze z jego id
            return redirect('team', team_id=team.id)
    else:
        form = EditTeamForm()

    context = RequestContext(request, {'form': form, })
    return HttpResponse(template.render(context))


def team(request, team_id):
    template = loader.get_template('team.html')
    team = Team.objects.get(id=team_id)
    players = Player.objects.filter(team_id=team, acceptedbycoachteam=True, acceptedbyplayer=True)
    context = RequestContext(request, {'team': team, 'players': players, })
    return HttpResponse(template.render(context))


@login_required
def manageTeam(request, team_id):
    template = loader.get_template('manageTeam.html')
    team = Team.objects.get(id=team_id)
    players = Player.objects.filter(team_id=team, acceptedbycoachteam=True, acceptedbyplayer=True)
    context = RequestContext(request, {'team': team, 'players': players, })
    return HttpResponse(template.render(context))


@login_required
def addPlayers(request, team_id):
    template = loader.get_template('addPlayer.html')
    team = Team.objects.get(id=team_id)
    users = User.objects.all()

    for player in Player.objects.all():
        users = users.exclude(id=player.user_id.id)

    context = RequestContext(request, {'team': team, 'users': users, })
    return HttpResponse(template.render(context))


def userToAdd(request, user, team_id):
    user = User.objects.get(user=request.user)
    team = Team.objects.get(id=team_id)
    Player.objects.create(user=user, name=user.name, surname=user.surname, team_id=team, acceptedbycoachteam=True,
                          acceptedbyplayer=False)
    return redirect('addPlayers', team_id=team.id)


def playerToTeamAccept(request, player_id):
    Player.objects.filter(id=player_id).update(acceptedbyplayer=True)
    return redirect('/user/')


@login_required
def updateTournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == 'POST':
        form = UpdateTournamentForm(request.POST)

        if form.is_valid():
            tournament.name = form.cleaned_data.get("name")
            tournament.start = form.cleaned_data.get("start")
            tournament.end = form.cleaned_data.get("end")
            tournament.description = form.cleaned_data.get("description")

            tournament.save()

            return redirect('tournament', tournament_id=tournament.id)
    else:
        form = UpdateTournamentForm(instance=tournament)

    return render_to_response('updatetournament.html', RequestContext(request, {'form': form, }))

@login_required
def createTournament(request):

    if request.method == 'POST':
        form = CreateTournamentForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(user=request.user)

            tournament = Tournament(
                name=form.cleaned_data.get("name"),
                start=form.cleaned_data.get("start"),
                end=form.cleaned_data.get("end"),
                username=user,
                type=form.cleaned_data.get("type"),
                file=request.FILES.get("file"),
                description=form.cleaned_data.get("description")
            )
            tournament.save()

            Manager.objects.create(user_id=user, tournament=tournament)

            return redirect('/user/')
    else:
        form = CreateTournamentForm()

    return render_to_response('createtournament.html', RequestContext(request, {'form': form, }))


@login_required
def enterForTournament(request, tournament_id, user_id):
    template = loader.get_template('enterForTournament.html')
    players = None
    teams = None
    tournament = Tournament.objects.get(id=tournament_id)
    user_id = User.objects.get(user=request.user)
    if Coach.objects.filter(user_id=request.user):
        coach = Coach.objects.get(user_id=request.user)
        players = list()
        teams = list()
        for team in Team.objects.filter(coach=coach):
            teamTrue = False
            playersC = Player.objects.filter(team_id=team, acceptedbycoachteam=True, acceptedbyplayer=True)
            for playerC in playersC:
                if PlayerTournament.objects.filter(tournament_id=tournament, player_id=playerC).count() == 0:
                    players.append(playerC)
                    teamTrue = True
            if teamTrue:
                teams.append(team)
    context = RequestContext(request, {'tournament': tournament, 'players': players, 'teams': teams, })
    return HttpResponse(template.render(context))

@login_required
def enterAllPlayersToTournament(request, tournament_id, user_id):
    tournament = Tournament.objects.get(id=tournament_id)
    user = User.objects.get(user=request.user)
    if Coach.objects.filter(user_id=user):
        coach = Coach.objects.get(user_id=user)
        for team in Team.objects.filter(coach=coach):
            playersC = Player.objects.filter(team_id=team, acceptedbycoachteam=True, acceptedbyplayer=True)
            for playerC in playersC:
                if PlayerTournament.objects.filter(tournament_id=tournament, player_id=playerC).count() == 0:
                    PlayerTournament.objects.create(player_id=playerC, tournament_id=tournament,
                                                    acceptedbymanager=False, acceptedbycoach=True)
    return redirect('/user/')


def enterPlayersTeamTour(request, team_id, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    team = Team.objects.get(id=team_id)
    for player in Player.objects.filter(team_id=team):
        if PlayerTournament.objects.filter(tournament_id=tournament, player_id=player).count() == 0:
            PlayerTournament.objects.create(player_id=player, tournament_id=tournament, acceptedbymanager=False,
                                            acceptedbycoach=True)
    return redirect('enterForTournament', tournament_id=tournament.id, user_id=team.coach.user_id.id)


def allPlayersTourAcceptByC(request):
    user = User.objects.get(user=request.user)
    if Coach.objects.filter(user_id=user):
        coach = Coach.objects.get(user_id=user)
        teams = Team.objects.filter(coach=coach)
        for team in teams:
            playersC = Player.objects.filter(team_id=team)
            for playerC in playersC:
                for playerT in PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True,
                                                               acceptedbycoach=False):
                    playerT.tournament_id.coaches.add(coach)
                if PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True, acceptedbycoach=False):
                    PlayerTournament.objects.filter(player_id=playerC).update(acceptedbymanager=True,
                                                                              acceptedbycoach=True)
    return redirect('/user/')


def allPlayersTourAcceptByM(request):
    user = User.objects.get(id=request.session['user'])
    if Manager.objects.filter(user_id=user.id):
        managers = Manager.objects.filter(user_id=user.id)
        for manager in managers:
            tournament = Tournament.objects.get(id=manager.tournament.id)
            for EplayerT in PlayerTournament.objects.filter(tournament_id=tournament, acceptedbymanager=False,
                                                            acceptedbycoach=True):
                PlayerTournament.objects.filter(id=EplayerT.id).update(acceptedbymanager=True, acceptedbycoach=True)
                EplayerT.tournament_id.coaches.add(EplayerT.player_id.team_id.coach)
    return redirect('/user/')


def allTeamTourAcceptByM(request, team_id):
    team = Team.objects.get(id=team_id)
    for player in Player.objects.filter(team_id=team):
        if PlayerTournament.objects.filter(player_id=player, acceptedbymanager=False, acceptedbycoach=True):
            PlayerTournament.objects.filter(player_id=player).update(acceptedbymanager=True, acceptedbycoach=True)
    return redirect('/user/')


def tournament(request, tournament_id):
    tournament = None
    template = loader.get_template('tournament.html')
    tournament = Tournament.objects.get(id=tournament_id)

    manager = Manager.objects.get(tournament=tournament)

    teams = list()
    players = list()
    playersT = PlayerTournament.objects.filter(tournament_id=tournament, acceptedbymanager=True, acceptedbycoach=True)
    for playerT in playersT:
        player = playerT.player_id
        players.append(player)
        teams.append(Team.objects.get(id=player.team_id.id))

    if request.method == 'POST':
        form = SelectArtsTournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('tournament', tournament_id=tournament.id)
    else:
        form = SelectArtsTournamentForm()
    context = RequestContext(request, {'tournament': tournament, 'teams': teams, 'players': players, 'manager': manager,
                                       'form': form})
    return HttpResponse(template.render(context))


def player(request, player_id):
    template = loader.get_template('player.html')
    player = Player.objects.get(id=player_id)
    team = Team.objects.get(id=player.team_id.id)
    coach = Coach.objects.get(id=team.coach.id)
    playersT = PlayerTournament.objects.get(player_id=player)
    context = RequestContext(request, {'playersT': playersT, 'team': team, 'player': player, 'coach': coach, })
    return HttpResponse(template.render(context))


def addPlayersToTournament(request, tournament_id):
    template = loader.get_template('addPlayerToTournament.html')
    tournament = Tournament.objects.get(id=tournament_id)
    players = Player.objects.filter(acceptedbycoachteam=True, acceptedbyplayer=True)
    for playerT in PlayerTournament.objects.filter(tournament_id=tournament):
        players = players.exclude(id=playerT.player_id.id)
    context = RequestContext(request, {'tournament': tournament, 'players': players})
    return HttpResponse(template.render(context))


def playerToAdd(request, player_id, tournament_id):
    player = Player.objects.get(id=player_id)
    tournament = Tournament.objects.get(id=tournament_id)
    p = PlayerTournament.objects.create(
        player_id=player,
        tournament_id=tournament,
        acceptedbymanager=True,
        acceptedbycoach=False
    )
    return redirect('addPlayersToTournament', tournament_id=tournament.id)


def enterPlayerTour(request, player_id, tournament_id):
    player = Player.objects.get(id=player_id)
    tournament = Tournament.objects.get(id=tournament_id)
    p = PlayerTournament.objects.create(player_id=player, tournament_id=tournament, acceptedbymanager=False,
                                        acceptedbycoach=True)
    return redirect('enterForTournament', tournament_id=tournament.id, user_id=player.team_id.coach.user_id.id)


def playerToTournamentAccept(request, playerT_id):
    PlayerTournament.objects.filter(id=playerT_id).update(acceptedbymanager=True, acceptedbycoach=True)
    p = PlayerTournament.objects.get(id=playerT_id)
    p.tournament_id.coaches.add(Coach.objects.get(id=Team.objects.get(id=p.player_id.team_id.id).coach.id))
    return redirect('/user/')


def deletePlayerTour(request, player_id, tournament_id):
    player = Player.objects.get(id=player_id)
    tournament = Tournament.objects.get(id=tournament_id)
    coach = Coach.objects.get(id=Team.objects.get(id=player.team_id.id).coach.id)
    tournament.coaches.remove(coach)
    playerT = PlayerTournament.objects.get(player_id=player, tournament_id=tournament).delete()
    return redirect('tournament', tournament_id=tournament.id)