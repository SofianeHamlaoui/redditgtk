from gettext import gettext as _
import praw
from datetime import datetime
from flask import Flask, request
from threading import Thread
from queue import Queue
from time import sleep
from redditgtk.confManager import ConfManager


def get_authorized_client(openLinkFunction=None, retry=False, reddit=None):
    if reddit is None:
        reddit = get_unauthorized_client()
    confman = ConfManager()
    refresh_token = ''
    code = ''
    if not retry:
        refresh_token = confman.conf['refresh_token']

    if refresh_token != '':
        try:
            return get_preauthorized_client(refresh_token)
        except Exception:
            print(
                _('Error getting client with refresh token, retrying...')
            )
            return get_authorized_client(openLinkFunction, True)
    else:
        q = Queue()

        def cb(code):
            q.put(code)

        t = Thread(target=start_auth_callback_server, args=(cb,))
        t.start()
        if openLinkFunction is not None:
            openLinkFunction(get_auth_link(reddit))
        code = q.get()
    try:
        refresh_token = reddit.auth.authorize(code)
        confman.conf['refresh_token'] = refresh_token
        confman.save_conf()
    except Exception:
        if not retry:
            print(
                _('Error authorizing reddit client, retrying...')
            )
            return get_authorized_client(openLinkFunction, retry=True)
        else:
            print(
                _('Error authorizing reddit client after retry, quitting...')
            )
            import sys
            sys.exit(1)
    return reddit


def get_auth_link(reddit):
    return reddit.auth.url(
        [
            'identity', 'history', 'mysubreddits', 'read', 'save', 'report',
            'submit', 'subscribe', 'vote', 'account', 'edit', 'livemanage'
        ],
        f'redditgtk-t{datetime.now().timestamp()}',
        'permanent'
    )


USER_AGENT = 'redditgtk by /u/gabmus'
CLIENT_ID = '5rQWiP4kMWi7CA'


def get_unauthorized_client():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        redirect_uri='http://localhost:8080',
        user_agent=USER_AGENT
    )


def get_preauthorized_client(refresh_token):
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=None,
        refresh_token=refresh_token,
        user_agent=USER_AGENT
    )


def start_auth_callback_server(callback):
    app = Flask(__name__)

    @app.route('/')
    def root():
        code = request.args.get('code')
        callback(code)
        request.environ.get('werkzeug.server.shutdown')()
        return 'ok'
    app.run(host='localhost', port=8080)
