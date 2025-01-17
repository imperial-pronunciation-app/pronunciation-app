from flask import Flask, render_template, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    return "<h1>Hello World</h1>"

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=443)
