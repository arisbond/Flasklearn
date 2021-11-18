from flask import Flask, render_template, request, session
from webapp.vsearch import search4vowels
from webapp.DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '10.1.80.29',
                          'port': 3307,
                          'user': 'root',
                          'password': 'lhtest12#@',
                          'database': 'test'}
app.secret_key = 'guess'


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'Good bye!'


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are logged in ~'
    return 'You are not login ~'


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4vowels(phrase, letters))
    log_request(request, results)
    title = 'Hear are your results:'
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as vlog:
        print(req, req.form, req.remote_addr, req.user_agent, res, file=vlog, sep='|')

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = '''insert into log values (null,%s,now(),%s,%s,%s,%s,%s)'''
        cursor.execute(_SQL, (req, req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent, res))


@app.route('/viewlog')
def view_log() -> 'html':
    logs = []
    with open('vsearch.log') as log:
        for line in log:
            logs.append([])
            pars = line.split("|")
            for item in pars:
                logs[-1].append(item)
    titles = ['Request', 'Form Data', 'Remote_addr', 'User_agent', 'Results']
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=logs)


@app.route('/viewdblog')
def view_log_from_db() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = '''select request,phrase,letters,ip,browser_string,results from log'''
        cursor.execute(_SQL)
        logs = cursor.fetchall()
    titles = ['Request', 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results']
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=logs)


if __name__ == '__main__':
    app.run(debug=True)
