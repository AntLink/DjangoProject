"""
WSGI config for DjangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")

application =get_wsgi_application()

# uwsgi --chdir=/home/antlink/Desktop/DjangoProject/DjangoProject --module=mysite.wsgi:application  --env DJANGO_SETTINGS_MODULE=mysite.settings  --master --pidfile=/tmp/project-master.pid  --socket=127.0.0.1:49152 --processes=5  --uid=1000 --gid=2000  --harakiri=20  --max-requests=5000  --vacuum  --home=/home/antlink/DjangoProjectPython2.7  --daemonize=/home/antlink/Desktop/DjangoProject/uwsgi_acces.log
