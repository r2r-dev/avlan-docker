from src.applications.dispatcher.application.AvlanDispatcherApplication import AvlanDispatcherApplication
from beaker.middleware import SessionMiddleware

'''
Note: technically we could use multiple WSGI servers for each app.
'''

# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.lockdir': 'sessionslock',
    'session.data_dir': 'sessionsdata',
    'auto': 'true',
}
avlan = AvlanDispatcherApplication()
application = SessionMiddleware(avlan, session_opts)
