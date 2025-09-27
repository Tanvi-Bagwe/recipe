import json
import os

from flasgger import Swagger
from flask import Flask, render_template, request, jsonify, redirect, url_for

from keep_alive import start_scheduler

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')

DATA_FILE = "data/testimonials.json"


def load_recipes():
    """Read recipes from JSON file"""
    with open('data/recipes.json', 'r') as f:
        return json.load(f)


# Helper functions to read/write JSON
def load_testimonials():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_testimonials(testimonials):
    with open(DATA_FILE, "w") as f:
        json.dump(testimonials, f, indent=4)


@app.route("/")
def default_route():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about-us")
def about():
    return render_template("about.html")


@app.route("/recipes")
def recipes_page():
    recipes = load_recipes()
    return render_template("recipies.html", recipes=recipes)


@app.route("/testimonials")
def testimonials_page():
    return render_template("testimonials.html")


@app.route("/testimonial/all/", methods=["GET"])
def get_all_testimonials():
    testimonials = load_testimonials()
    return jsonify(testimonials), 200


# Detail page
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipes = load_recipes()
    recipe = None

    # Simple loop to find the recipe by ID
    for r in recipes:
        if r["id"] == recipe_id:
            recipe = r
            break

    if recipe is None:
        return render_template("not_found.html")

    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/testimonial/add/", methods=["POST"])
def add_testimonial():
    data = request.get_json()
    name = data.get("name")
    feedback = data.get("feedback")

    if not name or not feedback:
        return jsonify({"error": "Name and feedback are required"}), 400

    testimonials = load_testimonials()
    testimonial = {"name": name, "feedback": feedback}
    testimonials.append(testimonial)
    save_testimonials(testimonials)

    return jsonify({"message": "Testimonial added successfully", "testimonial": testimonial}), 201


if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)
