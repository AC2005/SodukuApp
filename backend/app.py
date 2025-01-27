from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from backend.solver import solve_with_steps
from backend.grid_extraction import process_sudoku
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path='')
CORS(app)

@app.route('/extract', methods=['POST'])
@cross_origin()
def solve_sudoku():
    # endpoint that, given a 9x9 board, will extract the digits from the board into an array
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = request.files['image']
    image_path = f"temp/{file.filename}"
    file.save(image_path)

    # extraction done here
    board = process_sudoku(image_path)
    return jsonify({"board": board})

@app.route('/solve', methods=['POST'])
def solve_board():
    # endpoint to solve the board
    data = request.get_json()
    if 'board' not in data:
        return jsonify({"error": "No board provided"}), 400
    board = data['board']
    try:
        states = solve_with_steps(board) 
        # return states to frontend
        return jsonify({"states": states}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    # what to load when the app starts
    return send_from_directory(app.static_folder, 'index.html')

# to catch all other requests
@app.route('/<path:path>')
def serve_react_app(path):
    # If the requested file exists in build/, serve it
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve index.html
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
