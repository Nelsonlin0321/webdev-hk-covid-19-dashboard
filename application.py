from flask import Flask, render_template, redirect, url_for

application = Flask(__name__)


@application.route('/zh')
def main():
    return render_template('zh.html')


@application.route('/')
def index():
    return redirect(url_for("main"))


@application.route('/eng')
def main_eng():
    return render_template('eng.html')


if __name__ == "__main__":
    application.run(use_reloader=True, debug=False, port=5000)
