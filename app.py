"""Flask app for Cupcakes"""
import os
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake, DEFAULT_CUPCAKE_URL


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def get_homepage_form_list():

    return render_template('index.html')

@app.get('/api/cupcakes')
def get_cupcakes():
    """Return JSON of all cupcakes
    Returns JSON like {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def get_a_cupcake(cupcake_id):
    """return JSON of one cupcake
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post('/api/cupcakes')
def create_a_cupcake():
    """Add one cupcake from posted JSON data and return it
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image_url = request.json['image_url'] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_a_cupcake(cupcake_id):
    """Update a cupcake and return JSON
    It expects a JSON request with optional fields to update the cupcake:
    'flavor', 'size', 'rating' and 'image_url' are optional, if not provided in
    the request, they remain the same
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    # cupcake.image_url = request.json.get('image_url', DEFAULT_CUPCAKE_URL)

    if 'image_url' in request.json:
        cupcake.image_url = request.json['image_url']
    else:
        cupcake.image_url = cupcake.image_url

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_a_cupcake(cupcake_id):
    """Delete a cupcake and returns JSON
    Returns JSON like {deleted:[cupcake-id]}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    # serialized = cupcake.serialize()

    return jsonify(deleted=cupcake_id)
