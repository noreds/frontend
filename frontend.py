from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from modules.get_all import clustered_items

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def clusters():
    return render_template('clusters.html', clusters=list(clustered_items.values()))

if __name__ == '__main__':
    app.run(debug=True)
