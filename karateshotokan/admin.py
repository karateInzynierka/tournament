from django.contrib import admin
from karateshotokan.models import ShotokanPlayersCategory
from karateshotokan.models import ShotokanCategory
from karateshotokan.models import Round

admin.site.register(ShotokanPlayersCategory)
admin.site.register(ShotokanCategory)


class RoundAdmin(admin.ModelAdmin):
    list_display = ['category', 'number', 'playerT_first', 'playerT_second', 'who_win']


admin.site.register(Round, RoundAdmin)

