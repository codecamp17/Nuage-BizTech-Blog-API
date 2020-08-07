from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp


helper_module = imp.load_source('*', './app/blogs.py')
db = client.assignment
collection = db.blogs

@app.route("/")
def get_initial_response():
    """Nuapp Biz Technologies"""
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Internship Assignment'
    }
    resp = jsonify(message)
    return resp

@app.route("/api/blog", methods=['GET'])
def fetch_blogs():
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        if query_params:
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}            
            
            page = 1
            
            if 'page' in query:
                page = int(query['page'])
            
            if 'limit' not in query:
                query['limit'] = 7
            
            sort_order = 1
            sort_param = 'id'
            
            if 'sort' in query:
                if query['sort'][0] == '-':
                    sort_order = -1
                    sort_param = query['sort'][1:]
                else:
                    sort_param = query['sort']
 
            regex_q = {
                "$regex": query['name'],
                "$options" :'i'
            }
            
            blog_query = {"name":regex_q}
            records_fetched = collection.find(blog_query).sort(sort_param, sort_order).skip((page-1)*query['limit']).limit(query['limit'])

            if records_fetched.count() > 0:
                return dumps(records_fetched), 200
            else:
                del user_query['name']
                records_fetched = collection.find(blog_query).sort(sort_param, sort_order).skip((page-1)*query['limit']).limit(query['limit'])

            if records_fetched.count() > 0:
                return dumps(records_fetched), 200
            else:
                return "blog not found using query parameters", 404

        else:
            if collection.find().count > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500

@app.route("/api/blog", methods=['POST'])
def create_blog():
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            print "Request body not found"
            return ""

        blog_created = collection.insert(body)

        if isinstance(blog_created, list):
            return jsonify([str(v) for v in blog_created]), 201
        else:
            return jsonify(str(blog_created)), 201
    except:
        return "", 500

@app.route("/api/blog/<blog_id>", methods=['GET'])
def fetch_blog(blog_id):
    try:
        data_taken = collection.find({"id": int(blog_id)})

        if data_taken.count() > 0:
            return dumps(data_taken), 200
        else:
            return "Blog not found", 404
    except:
        return "", 500

@app.route("/api/blog/<blog_id>", methods=['PUT'])
def update_blog(blog_id):
    try:
        try:
            update_body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "Not available"

        records = collection.update_one({"id": int(blog_id)}, update_body)

        if records.modified_count > 0:
            return "", 200
        else:
            return "Not Updated", 404
    except:
        return "", 500


@app.route("/api/blog/<blog_id>", methods=['DELETE'])
def remove_blog(blog_id):
    """remove the blog.
       """
    try:
        delete = collection.delete_one({"id": int(blog_id)})

        if delete.deleted_count > 0 :
            return "", 200
        else:
            return "Unable to find blog", 404
    except:
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Not Found 404 status."""
    message = {
        "err":
            {
                "msg": "Not supported"
            }
    }
    response = jsonify(message)
    response.status_code = 404
    return response
