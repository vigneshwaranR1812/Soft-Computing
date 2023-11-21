from flask import Flask, request, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from textblob import TextBlob
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
app = Flask(__name__)
try:
    CORS(app)
except Exception as e:
    print(str(e))


# MongoDB configuration
MONGO_URI = 'mongodb+srv://vicky:vicky@cluster0.hsaut5j.mongodb.net/7'  # Replace with your MongoDB URI
DB_NAME = 'sc'
COLLECTION_NAME1 = 'users'
COLLECTION_NAME2 = 'feeds'

# Connect to MongoDB using PyMongo
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection1 = db[COLLECTION_NAME1]
collection2 = db[COLLECTION_NAME2]

app = Flask(__name__)

# Fuzzy Logic Controller Setup
sentiment_polarity = ctrl.Antecedent(np.arange(0, 11, 1), 'sentiment_polarity')
feedback_length = ctrl.Antecedent(np.arange(0, 101, 1), 'feedback_length')
feedback_analysis = ctrl.Consequent(np.arange(0, 101, 1), 'feedback_analysis')

# Define membership functions for sentiment_polarity
sentiment_polarity['very_negative'] = fuzz.trapmf(sentiment_polarity.universe, [0, 0, 1, 2])
sentiment_polarity['negative'] = fuzz.trimf(sentiment_polarity.universe, [1, 3, 5])
sentiment_polarity['neutral'] = fuzz.trimf(sentiment_polarity.universe, [4, 6, 8])
sentiment_polarity['positive'] = fuzz.trimf(sentiment_polarity.universe, [7, 9, 10])
sentiment_polarity['very_positive'] = fuzz.trapmf(sentiment_polarity.universe, [9, 10, 11, 11])

# Define membership functions for feedback_length
feedback_length['very_short'] = fuzz.trapmf(feedback_length.universe, [0, 0, 10, 20])
feedback_length['short'] = fuzz.trimf(feedback_length.universe, [10, 20, 50])
feedback_length['medium'] = fuzz.trimf(feedback_length.universe, [20, 50, 80])
feedback_length['long'] = fuzz.trimf(feedback_length.universe, [50, 80, 100])
feedback_length['very_long'] = fuzz.trapmf(feedback_length.universe, [80, 90, 100, 100])

# Define membership functions for feedback_analysis
feedback_analysis['very_low'] = fuzz.trapmf(feedback_analysis.universe, [0, 0, 20, 30])
feedback_analysis['low'] = fuzz.trimf(feedback_analysis.universe, [20, 30, 50])
feedback_analysis['medium'] = fuzz.trimf(feedback_analysis.universe, [30, 50, 70])
feedback_analysis['high'] = fuzz.trimf(feedback_analysis.universe, [50, 70, 90])
feedback_analysis['very_high'] = fuzz.trapmf(feedback_analysis.universe, [70, 90, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(sentiment_polarity['very_negative'] & feedback_length['very_short'], feedback_analysis['very_low'])
rule2 = ctrl.Rule(sentiment_polarity['very_negative'] & feedback_length['short'], feedback_analysis['very_low'])
rule3 = ctrl.Rule(sentiment_polarity['very_negative'] & feedback_length['medium'], feedback_analysis['very_low'])
rule4 = ctrl.Rule(sentiment_polarity['very_negative'] & feedback_length['long'], feedback_analysis['very_low'])
rule5 = ctrl.Rule(sentiment_polarity['very_negative'] & feedback_length['very_long'], feedback_analysis['very_low'])
rule6 = ctrl.Rule(sentiment_polarity['negative'] & feedback_length['very_short'], feedback_analysis['low'])
rule7 = ctrl.Rule(sentiment_polarity['negative'] & feedback_length['short'], feedback_analysis['low'])
rule8 = ctrl.Rule(sentiment_polarity['negative'] & feedback_length['medium'], feedback_analysis['low'])
rule9 = ctrl.Rule(sentiment_polarity['negative'] & feedback_length['long'], feedback_analysis['very_low'])
rule10 = ctrl.Rule(sentiment_polarity['negative'] & feedback_length['very_long'], feedback_analysis['very_low'])
rule11 = ctrl.Rule(sentiment_polarity['neutral'] & feedback_length['very_short'], feedback_analysis['low'])
rule12 = ctrl.Rule(sentiment_polarity['neutral'] & feedback_length['short'], feedback_analysis['medium'])
rule13 = ctrl.Rule(sentiment_polarity['neutral'] & feedback_length['medium'], feedback_analysis['medium'])
rule14 = ctrl.Rule(sentiment_polarity['neutral'] & feedback_length['long'], feedback_analysis['medium'])
rule15 = ctrl.Rule(sentiment_polarity['neutral'] & feedback_length['very_long'], feedback_analysis['medium'])
rule16 = ctrl.Rule(sentiment_polarity['positive'] & feedback_length['very_short'], feedback_analysis['medium'])
rule17 = ctrl.Rule(sentiment_polarity['positive'] & feedback_length['short'], feedback_analysis['high'])
rule18 = ctrl.Rule(sentiment_polarity['positive'] & feedback_length['medium'], feedback_analysis['high'])
rule19 = ctrl.Rule(sentiment_polarity['positive'] & feedback_length['long'], feedback_analysis['high'])
rule20 = ctrl.Rule(sentiment_polarity['positive'] & feedback_length['very_long'], feedback_analysis['very_high'])
rule21 = ctrl.Rule(sentiment_polarity['very_positive'] & feedback_length['very_short'], feedback_analysis['high'])
rule22 = ctrl.Rule(sentiment_polarity['very_positive'] & feedback_length['short'], feedback_analysis['very_high'])
rule23 = ctrl.Rule(sentiment_polarity['very_positive'] & feedback_length['medium'], feedback_analysis['very_high'])
rule24 = ctrl.Rule(sentiment_polarity['very_positive'] & feedback_length['long'], feedback_analysis['very_high'])
rule25 = ctrl.Rule(sentiment_polarity['very_positive'] & feedback_length['very_long'], feedback_analysis['very_high'])
# Create a control system
feedback_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,rule21, rule22, rule23, rule24, rule25])
feedback_sim = ctrl.ControlSystemSimulation(feedback_ctrl)


# Fnction to calculate sentiment polarity using TextBlob
def calculate_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to interpret the numerical result into textual feedback analysis
def interpret_feedback_analysis(result):
    if result <= 30:
        return "Very Low Analysis: Significant Improvement Needed"
    elif 30 < result <= 60:
        return "Low Analysis: Improvement Needed"
    elif 60 < result <= 90:
        return "Medium Analysis: Acceptable"
    elif 90 < result <= 100:
        return "High Analysis: Good"
    else:
        return "Very High Analysis: Excellent"
#Dummy APi
@app.route('/api/print', methods=['GET'])
def printing():
        return "Hello world"

# API endpoint for customer feedback analysis
@app.route('/api/analyze-feedback', methods=['POST'])
def analyze_feedback():
    try:
        data = request.json  # Assuming JSON format with 'feedback' key
        sentiment_value = calculate_sentiment(data['feedback'])
        sentiment_value=int((sentiment_value + 1) * 5)
        length_value = len(data['feedback'])

        # Pass inputs to the fuzzy system
        feedback_sim.input['sentiment_polarity'] = sentiment_value
        feedback_sim.input['feedback_length'] = length_value
        print(sentiment_value)
        print(length_value)
        print(int((sentiment_value + 1) * 5))
       
        # Crunch the numbers
        feedback_sim.compute()

        # Return the output (feedback analysis)
        result = feedback_sim.output['feedback_analysis']

        # Convert numerical result to textual interpretation
        interpretation = interpret_feedback_analysis(result)
        res={'feedback':data['feedback'],'sentiment': sentiment_value, 'length': length_value, 'analysis_result': result, 'interpretation': interpretation}
        collection2.insert_one(res)
        return jsonify({'feedback':data['feedback'],'sentiment': sentiment_value, 'length': length_value, 'analysis_result': result, 'interpretation': interpretation})

    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/api/analyze-result', methods=['GET'])
def get_category_count():
    # Group by the 'category' field and get the count for each category
    pipeline = [
        {"$group": {"_id": "$interpretation", "count": {"$sum": 1}}}
    ]
    # Execute the aggregation pipeline
    result = list(collection2.aggregate(pipeline))
    return jsonify({'result':result})

@app.route('/api/remove-data', methods=['DELETE'])
def remove_data():
    try:
        # Replace 'your_collection_name' with the actual collection name in your MongoDB
        result = collection2.delete_many({})
        return jsonify({'message': f'{result.deleted_count} documents removed successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    type = data.get('type')

    # Check if the username already exists
    if collection1.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user document
    user_data = {'username': username, 'password': hashed_password,'type':type}
    collection1.insert_one(user_data)
    try:
        if user_data and check_password_hash(user_data['password'], password):
                user_details = {
                    'user_id': str(user_data['_id']),
                    'name': user_data['username'],
                    'type': user_data['type'],
                }
                return jsonify({'message': 'User Added',"user_detail":user_details}), 200
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    type = data.get('type')

    # Find the user in the database
    user = collection1.find_one({'username': username,"type":type})

    if user and check_password_hash(user['password'], password):
        user_details = {
                    'user_id': str(user['_id']),
                    'name': user['username'],
                    'type': user['type'],
                }
        return jsonify({'message': 'Logged in Successfully',"user_detail":user_details}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
