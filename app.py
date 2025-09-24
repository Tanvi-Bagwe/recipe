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


# Detail page
@app.route("/recipie/<int:recipe_id>/")
def recipe_detail(recipe_id):
    recipes = load_recipes()
    recipe = None

    # Simple loop to find the recipe by ID
    for r in recipes:
        if r["id"] == recipe_id:
            recipe = r
            break

    if recipe is None:
        return "Recipe not found", 404

    return render_template("recipe_detail.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
