from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testcase:testcase@localhost/testcases'
db = SQLAlchemy(app)

# Define the Testcase model
class Testcase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    estimate_time = db.Column(db.String(50), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Initialize the database and create tables if they don't exist
with app.app_context():
    db.create_all()

# Get all test cases
@app.route('/api/testcases', methods=['GET'])
def get_testcases():
    testcases = Testcase.query.all()
    return jsonify([{
        'id': testcase.id,
        'name': testcase.name,
        'estimate_time': testcase.estimate_time,
        'module': testcase.module,
        'priority': testcase.priority,
        'status': testcase.status
    } for testcase in testcases])

# Add a new test case
@app.route('/api/testcases', methods=['POST'])
def add_testcase():
    data = request.get_json()
    new_testcase = Testcase(
        name=data['name'],
        estimate_time=data['estimate_time'],
        module=data['module'],
        priority=data['priority'],
        status=data['status']
    )
    db.session.add(new_testcase)
    db.session.commit()
    return jsonify({'message': 'Test case added successfully'})

# Update a test case
@app.route('/api/testcases/<int:id>', methods=['PUT'])
def update_testcase(id):
    data = request.get_json()
    testcase = Testcase.query.get(id)
    if not testcase:
        return jsonify({'message': 'Test case not found'}), 404

    testcase.name = data['name']
    testcase.estimate_time = data['estimate_time']
    testcase.module = data['module']
    testcase.priority = data['priority']
    testcase.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Test case updated successfully'})

# Delete a test case
@app.route('/api/testcases/<int:id>', methods=['DELETE'])
def delete_testcase(id):
    testcase = Testcase.query.get(id)
    if not testcase:
        return jsonify({'message': 'Test case not found'}), 404

    db.session.delete(testcase)
    db.session.commit()
    return jsonify({'message': 'Test case deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

