from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database tables before running the app
with app.app_context():
    db.create_all()

# Route to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    with app.app_context():
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': user_list})

# Route to create a new user
@app.route('/api/create_user', methods=['POST'])
def create_user():
    with app.app_context():
        new_user = User(username='new_user')
        db.session.add(new_user)
        db.session.commit()
    return 'User created successfully!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
