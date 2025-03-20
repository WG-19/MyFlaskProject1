import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

word_sets = [
    ["River", "Bright", "Shield"],
    ["Echo", "Silent", "Frame"],
    ["Lunar", "Swift", "Maple"],
    ["Crimson", "Horizon", "Frost"],
    ["Timber", "Shadow", "Orbit"]
]

def generate_arithmetic_sequence():
    start = random.randint(1, 20)
    difference = random.randint(1, 10)
    sequence_length = random.randint(3, 6)
    sequence = [start + (i * difference) for i in range(sequence_length)]
    next_number = sequence[-1] + difference  # Compute the next number
    return sequence, next_number  # Return sequence and correct answer

# Generate 10 number sequences dynamically
number_sets = [generate_arithmetic_sequence() for _ in range(10)]

@app.route('/wordrecall')
def wordrecall():
    return render_template('wordrecall.html')

@app.route('/get_words', methods=['POST'])
def get_words():
    data = request.json
    current_index = data.get('current_index', 0)

    if current_index >= len(word_sets):
        return jsonify({'game_over': True})

    words = word_sets[current_index]
    return jsonify({'words': words, 'game_over': False})

@app.route('/check_words', methods=['POST'])
def check_words():
    data = request.json
    current_index = data['current_index']
    user_words = data['user_words'].split()
    correct_words = word_sets[current_index]

    correct = user_words == correct_words
    return jsonify({'correct': correct, 'correct_words': correct_words})

# -------------------- Number Sequence Routes --------------------

@app.route('/numbersequence')
def numbersequence():
    return render_template('numbersequence.html')

@app.route('/get_numbers', methods=['POST'])
def get_numbers():
    data = request.json
    current_index = data.get('current_index', 0)

    if current_index >= len(number_sets):
        return jsonify({'game_over': True})

    sequence, correct_answer = number_sets[current_index]
    return jsonify({'numbers': sequence, 'game_over': False})

@app.route('/check_numbers', methods=['POST'])
def check_numbers():
    data = request.json
    current_index = data['current_index']
    user_input = data['user_numbers'].strip()

    try:
        user_input = int(user_input)
    except ValueError:
        return jsonify({'correct': False, 'message': "Invalid input. Please enter a number."})

    _, correct_answer = number_sets[current_index]
    correct = user_input == correct_answer

    return jsonify({'correct': correct, 'correct_answer': correct_answer})

# -------------------- Other Routes --------------------

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')

if __name__ == '__main__':
    app.run(debug=True)
