# -*- coding: utf-8 -*-

import os
import sys
import site

site.addsitedir("/home/student/apps/tournament/lib/python2.7/site-packages")

sys.path.append("/home/student/apps/tournament/src")
sys.path.append("/home/student/apps/tournament/src/tournament")

sys.path = sys.path[::-1]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tournament.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
