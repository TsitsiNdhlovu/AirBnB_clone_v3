#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
        /stats:     dispaly total for all classes
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def status():
    '''
        this returns the JSON of OK status
    '''
    return jsonify({'status': 'OK'})

@app_views.route("/stats")
def storage_counts():
    '''
        this returns the counts of all classes in storage
    '''
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
