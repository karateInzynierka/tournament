from django.contrib import admin
from main.models import *

# Register your models here.

class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'tournament']


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']


admin.site.register(Team)
admin.site.register(User)
admin.site.register(Coach)
admin.site.register(Player)
admin.site.register(PlayerTournament)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Tournament, TournamentAdmin)