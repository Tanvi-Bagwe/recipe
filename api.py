from flask import Blueprint, jsonify
import json

api_bp = Blueprint('api', __name__)

def load_recipes():
    """Read recipes from JSON file"""
    with open('data/recipes.json', 'r') as f:
        return json.load(f)


@api_bp.route("/api/recipe/<int:recipe_id>", methods=['GET'])
def recipe_api(recipe_id):
    """
    Retrieve a recipe by its ID
    ---
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
        description: The ID of the recipe to retrieve
    responses:
      200:
        description: Recipe found and returned successfully
        examples:
          application/json: {
            "id": 1,
            "title": "Spaghetti Bolognese",
            "ingredients": ["spaghetti", "beef", "tomato sauce"],
            "instructions": "Cook pasta. Brown beef. Mix with sauce."
          }
      404:
        description: Recipe not found
        examples:
          application/json: { "error": "Recipe not found" }
    """
    recipes = load_recipes()
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    else:
        return jsonify({"error": "Recipe not found"}), 404
