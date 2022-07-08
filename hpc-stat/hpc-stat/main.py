from flask import Flask, render_template, redirect, url_for, request
from flask_babel import Babel
from local import setting
from view.StatView import StatView
from view.JobView import JobView
from view.NodeView import NodeView

app = Flask(__name__)
babel = Babel(app)

app.secret_key = setting.secret_key
app.debug = setting.DEBUG
app.env = setting.ENV

@babel.localeselector
def get_locale():
    if str(request.accept_languages)[:2] == "zh":
        return "zh"
    else:
        return "en"
    #return request.accept_languages.best_match(setting.LANGUAGES)

@app.route("/")
def index():
    return redirect(url_for("stat_index",cluster="hpc01"))

@app.route("/stat")
def stat_default():
    return redirect(url_for("stat_index",cluster="hpc01"))

@app.route("/stat/brief")
def stat_brief():
    cluster="hpc01"
    stat = StatView.factory(cluster)
    return stat.brief()

@app.route("/stat/<cluster>")
def stat_index(cluster):
    stat = StatView.factory(cluster)
    return stat.index()

@app.route("/stat/<cluster>/async")
def stat_async(cluster):
    stat = StatView.factory(cluster)
    return stat.async_data()

@app.route("/stat/<cluster>/history/<type>/<period>")
def stat_history(cluster,type,period):
    stat = StatView.factory(cluster)
    return stat.history(type,period)

@app.route("/stat/<cluster>/history/check/<type>/<start_date>/<end_date>")
def stat_history_check(cluster,type,start_date,end_date):
    stat = StatView.factory(cluster)
    return stat.history_check(type,start_date,end_date)

@app.route("/job")
def job_default():
    return redirect(url_for("job_index",cluster="hpc01"))

@app.route("/job/<cluster>")
def job_index(cluster):
    job = JobView.factory(cluster)
    return job.index()

@app.route("/job/<cluster>/all")
def job_all(cluster):
    job = JobView.factory(cluster)
    return job.jobs()

@app.route("/node")
def node_default():
    return redirect(url_for("node_index",cluster="hpc01"))

@app.route("/node/<cluster>")
def node_index(cluster):
    node = NodeView.factory(cluster)
    return node.index()

@app.route("/node/<cluster>/all")
def node_all(cluster):
    node = NodeView.factory(cluster)
    return node.nodes()

if __name__ == "__main__":
    app.run(
        host=setting.HOST,
        port=setting.PORT
    )
