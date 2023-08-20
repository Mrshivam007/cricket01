from flask import Flask, render_template
from views.live import live_bp
app = Flask(__name__)

app.register_blueprint(live_bp)


if __name__ == '__main__':
    app.run(debug=True)
