from bottle import app, route, run, redirect, request, template
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)


@route('/quiz')
def quiz():
    s = request.environ.get('beaker.session')
    quiz = s.get('quiz')
    quiz['counter'] += 1
    s.save()
    if quiz['counter'] >= 10:
        redirect('/result')
    return 'Test counter: %d' % quiz['counter']


@route('/result')
def result():
    s = request.environ.get('beaker.session')
    quiz = s.get('quiz')
    return template('result', quiz)


@route('/')
def index():
    s = request.environ.get('beaker.session')
    s['quiz'] = {
        'counter': 0,
    }
    s.save()
    return template('index')

run(app=app, host='0.0.0.0', port=8080)
