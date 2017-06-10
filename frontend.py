from flask import Flask, render_template

from modules.get_all import cluster_items

app = Flask(__name__)


@app.route('/')
def clusters():
    return render_template('clusters.html')


if __name__ == '__main__':
    app.run()
