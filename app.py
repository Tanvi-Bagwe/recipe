from flask import Flask, render_template, request, jsonify
from api import api_bp, load_recipes
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(api_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about-us")
def about():
    return render_template("about.html")

@app.route("/recipes")
def recipes_page():
    recipes = load_recipes()
    return render_template("recipies.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)