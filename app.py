from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS 
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "http://ravenousrafinki.com/dinner-box"}})

# Route to serve the front-end files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def get_db_connection():
    conn = sqlite3.connect('DinnerBox.db')
    conn.row_factory = sqlite3.Row  # This allows column access by name: row['column_name']
    return conn

@app.route('/api/protein')
def get_protein():
    filters = []
    # Check if kosher is selected and adjust filters accordingly
    is_kosher = request.args.get('is_kosher', 'false') == 'true'
    if is_kosher:
        # For kosher, we want to include items marked as kosher. This assumes your database marks kosher items as is_kosher = 1.
        filters.append("is_kosher = 1")
    else:
        # Non-kosher filters based on user selection
        if request.args.get('is_red_meat') == 'true':
            filters.append("is_red_meat = 0")
        if request.args.get('is_pork') == 'true':
            filters.append("is_pork = 0")
        if request.args.get('is_poultry') == 'true':
            filters.append("is_poultry = 0")
        if request.args.get('is_fish') == 'true':
            filters.append("is_fish = 0")
        if request.args.get('is_shellfish') == 'true':
            filters.append("is_shellfish = 0")

    where_clause = ' AND '.join(filters) if filters else '1=1'
    query = f"SELECT * FROM protein WHERE {where_clause} ORDER BY RANDOM()"
    quantity = request.args.get('quantity', default=1, type=int)
    
    conn = get_db_connection()
    protein = conn.execute(query).fetchall()
    conn.close()

    protein = protein[:quantity]
    return jsonify([{'name': row['name']} for row in protein])

@app.route('/api/additions')
def get_additions():
    filters = []
    is_kosher = request.args.get('is_kosher', 'false') == 'true'
    
    # Correctly filtering based on kosher selection
    if is_kosher:
        # If kosher, exclude dairy if any meat is included. This logic might need to be refined based on your exact requirements.
        filters.append("is_dairy = 0")

    where_clause = ' AND '.join(filters) if filters else '1=1'
    query = f"SELECT * FROM additions WHERE {where_clause} ORDER BY RANDOM()"
    quantity = request.args.get('additions_quantity', default=1, type=int)
    
    conn = get_db_connection()
    additions = conn.execute(query).fetchall()
    conn.close()

    additions = additions[:quantity]
    return jsonify([{'name': row['name']} for row in additions])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
