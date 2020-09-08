import praw
from datetime import datetime
from flask import Flask, request
from multiprocessing import Queue, Process
from time import sleep


def get_authorized_client(openLinkFunction):

    def cb(code):
        q.put(code)

    q = Queue()
    p = Process(target=start_auth_callback_server, args=(cb,))
    p.start()
    reddit = get_unauthorized_client()
    openLinkFunction(get_auth_link(reddit))
    code = q.get()
    sleep(1)  # give flask the time to respond
    p.terminate()
    p.join()
    reddit.auth.authorize(code)
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


def get_unauthorized_client():
    reddit = praw.Reddit(
        client_id='5rQWiP4kMWi7CA',
        client_secret=None,
        redirect_uri='http://localhost:8080',
        user_agent='redditgtk by /u/gabmus'
    )
    return reddit


def start_auth_callback_server(callback):
    app = Flask(__name__)

    @app.route('/')
    def root():
        code = request.args.get('code')
        callback(code)
        return 'ok'
    app.run(host='localhost', port=8080)
