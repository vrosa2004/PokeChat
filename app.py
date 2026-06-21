from flask import Flask, render_template
from routes.chat_routes import chat_bp
from routes.pokemon_routes import pokemon_bp

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
app.register_blueprint(pokemon_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)