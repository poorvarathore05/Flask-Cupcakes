"""Flask app for Cupcakes"""
from flask.globals import request
from models import connect_db, Cupcake, db
from flask import Flask, render_template, flash, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/cupcake?user=postgres&password=postgresql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    all_cupcake = [cup.serialize() for cup in cupcakes]
    return jsonify(cupcakes=all_cupcake)


@app.route('/api/cupcakes/<int:cup_id>')
def get_single_cupcake(cup_id):
    cupcake = Cupcake.query.get_or_404(cup_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['Post'])
def create_cupcake():
    """Create dessert from form data & return it.

    Returns JSON {'cupcake': {id, name, calories}}
    """
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cup_id>', methods=['Patch'])
def edit_cupcake(cup_id):
    cupcake = Cupcake.query.get_or_404(cup_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image) or None

    db.session.commit()

    response_json = jsonify(cupcake.serialize())
    return (response_json)
