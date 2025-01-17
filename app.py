from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, inspect, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

# Initialize the Flask app
app = Flask(__name__)

engine = create_engine(database_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
# check if the table exists
inspector = inspect(engine)
if not inspector.has_table('users'):
    Base.metadata.create_all(engine)
    new_user = User(name="James")
    session.add(new_user)
    session.commit()

# Homepage route
@app.route('/')
def home():
    user = session.query(User).first()
    return f"<h1>{user.name}</h1>"

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8000)
