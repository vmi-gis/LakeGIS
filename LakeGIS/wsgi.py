import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LakeGIS.settings")

cwd = os.path.dirname(__file__)
sys.path.append(cwd)

virtualenv = os.path.join(os.path.join(os.path.dirname(cwd), 'bin/activate_this.py'))
try:
    execfile(virtualenv, dict(__file__ = virtualenv))
except:
    pass

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

