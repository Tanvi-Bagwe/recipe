from flask import Flask, render_template, request, jsonify
from api import api_bp, load_recipes
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')

testimonials = []


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


@app.route("/testimonials")
def testimonials_page():
    return render_template("testimonials.html")


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

    testimonial = {"name": name, "feedback": feedback}
    testimonials.append(testimonial)

    return jsonify({"message": "Testimonial added successfully", "testimonial": testimonial}), 201


@app.route("/testimonial/all/", methods=["GET"])
def get_all_testimonials():
    return jsonify(testimonials), 200


if __name__ == "__main__":
    app.run(debug=True)
