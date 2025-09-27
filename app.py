import json
import os

from flasgger import Swagger
from flask import Flask, render_template, jsonify, redirect, url_for

from scheduler import start_scheduler

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')

DATA_FILE = "data/testimonials.json"


def load_recipes():
    """Load recipe data from the JSON file.

        Returns:
            list: A list of recipe dictionaries loaded from `data/recipes.json`.
        """
    with open('data/recipes.json', 'r') as f:
        return json.load(f)


def load_testimonials():
    """Load testimonials from persistent storage.

        Returns:
            list: The list of testimonials read from `DATA_FILE`.
                  Returns an empty list if the file does not exist.
        """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_testimonials(testimonials):
    """Save the testimonials list to persistent storage.

        Args:
            testimonials (list): The list of testimonial dictionaries to write.
        """
    with open(DATA_FILE, "w") as f:
        json.dump(testimonials, f, indent=4)


@app.errorhandler(404)
def page_not_found(e):
    """Redirect to a custom 404 page."""
    return render_template('not_found.html'), 404


@app.route("/")
def default_route():
    """Redirect root path to the home page.

        Keeps a single canonical entrypoint for the site.
        """
    return redirect(url_for('home'))


@app.route("/home")
def home():
    """Render the home page template."""
    return render_template("home.html")


@app.route("/about-us")
def about():
    """Render the about page template."""
    return render_template("about.html")


from flask import request


@app.route("/recipes")
def recipes_page():
    """Render a listing of recipes, optionally filtered by type.

        Query parameters:
            type (str): 'veg', 'non-veg', or omitted for all recipes.

        Returns:
            Rendered template `recipies.html` with filtered recipes.
        """
    recipe_type = request.args.get("type", "all")
    all_recipes = load_recipes()
    filtered_recipes = []

    if recipe_type == "veg":
        for r in all_recipes:
            if r.get("is_veg"):
                filtered_recipes.append(r)
    elif recipe_type == "non-veg":
        for r in all_recipes:
            if not r.get("is_veg"):
                filtered_recipes.append(r)
    else:
        filtered_recipes = all_recipes

    return render_template("recipies.html", recipes=filtered_recipes, selected=recipe_type)


@app.route("/testimonials")
def testimonials_page():
    """Render the testimonials submission/view page."""
    return render_template("testimonials.html")


@app.route("/testimonial/all/", methods=["GET"])
def get_all_testimonials():
    """Return all testimonials as JSON.

        Used by client-side code to fetch existing testimonials.

        Returns:
            flask.Response: JSON array of testimonials with 200 status.
        """
    testimonials = load_testimonials()
    return jsonify(testimonials), 200


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    """Render a recipe detail page for the given recipe_id.

        Args:
            recipe_id (int): The numeric ID of the requested recipe.

        Returns:
            Rendered template `recipe_detail.html` if found, otherwise
            `not_found.html`.
        """
    recipes = load_recipes()
    recipe = None

    for r in recipes:
        if r["id"] == recipe_id:
            recipe = r
            break

    if recipe is None:
        return render_template("not_found.html")

    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/testimonial/add/", methods=["POST"])
def add_testimonial():
    """Add a new testimonial from JSON request body.

        Expected JSON body:
            {
                "name": "<user name>",
                "feedback": "<user feedback>"
            }

        Returns:
            JSON response with success message and created testimonial (201),
            or an error message (400) if required fields are missing.
        """
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


# Start the scheduler in a background thread
start_scheduler()

if __name__ == "__main__":
    app.run(debug=True)
