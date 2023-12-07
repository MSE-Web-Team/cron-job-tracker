from flask import Flask
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

@app.route('/api')
def api_endpoint():
    # Create a user and add it to the database as an example
    new_user = User(username='example_user')
    db.session.add(new_user)
    db.session.commit()

    return 'Hello from the API endpoint!'

if __name__ == '__main__':
    # Create the database tables before running the app
    db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
