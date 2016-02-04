import functools
from bottle import app, route, run, redirect, request, static_file, jinja2_view
from beaker.middleware import SessionMiddleware
import yaml
import random

view = functools.partial(jinja2_view, template_lookup=['.'])

with open('questions.yaml') as f:
    questions = yaml.load(f)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)


def choose_questions():
    random.shuffle(questions)
    return questions[:10]


@route('/check-uk-visa')
@view('question.html')
def quiz():
    s = request.environ.get('beaker.session')
    quiz = s.get('quiz', {})
    quiz['counter'] = quiz.get('counter', -1) + 1
    question = quiz['qu'][quiz['counter']]
    print(question)
    s.save()
    if quiz['counter'] >= 9:
        redirect('/result')
    return {'quiz': quiz,
            'question_name': question['question'],
            'answers': question['answers'],
            }


@route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='./static/')


@route('/result')
@view('result.html')
def result():
    s = request.environ.get('beaker.session')
    quiz = s.get('quiz')
    return {'passed': False}


@route('/')
@view('start.html')
def index():
    s = request.environ.get('beaker.session')
    s['quiz'] = {
        'counter': 0,
        'score': 0,
        'qu': choose_questions(),
    }
    s.save()

run(app=app, host='0.0.0.0', port=8080)
