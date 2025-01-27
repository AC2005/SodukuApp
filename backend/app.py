from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from solver import solve_with_steps
from grid_extraction import process_sudoku
import os

app = Flask(__name__, static_folder="sudokuapp/frontend/build", static_url_path='')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/extract', methods=['POST'])
@cross_origin()
def solve_sudoku():
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = request.files['image']
    image_path = f"temp/{file.filename}"
    file.save(image_path)

    board = process_sudoku(image_path)
    return jsonify({"board": board})

@app.route('/solve', methods=['POST'])
def solve_board():
    data = request.get_json()
    if 'board' not in data:
        return jsonify({"error": "No board provided"}), 400
    board = data['board']
    try:
        states = solve_with_steps(board)  # This function returns all intermediate states
        return jsonify({"states": states})  # Return all states to the frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
