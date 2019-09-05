from flask import Flask, render_template
import jenkins

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def hello_world():
    return "Yeah, hi"


@app.route('/jobs/<name>')
@app.route('/jobs')
def get_jobs(name=''):
    result = list()
    for url in app.config.get('JENKINS_URLS'):
        server = jenkins.Jenkins(url=url, username=app.config.get('JENKINS_USER'),
                                 password=app.config.get('JENKINS_PASSWORD'))
        jobs = server.get_job_info_regex(name)
        result += [(j.get('name', ''), j.get('url', ''), url) for j in jobs]

    jobs = sorted(result, key=lambda x: x[0])
    return render_template('jobs.html.j2', jobs=jobs)


if __name__ == '__main__':
    app.run(debug=1)
