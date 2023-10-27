#!/usr/bin/python3
"""Places Amenities view module."""
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort
# Import your models and storage instance here
from models.place import Place
from models.amenity import Amenity
from models import storage

# Define your routes and views for Place-Amenity relationship here
@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
def place_amenities(place_id):
    """
    Handle GET and POST requests on the list of amenities for a place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'amenity_id' not in data:
            return jsonify({'error': 'Missing amenity_id'}), 400
        amenity_id = data['amenity_id']
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Handle DELETE requests to remove an amenity from a place.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    place.save()

    return jsonify({}), 200
