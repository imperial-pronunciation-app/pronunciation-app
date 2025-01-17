from flask import Flask, render_template, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    return "<h1>Hello World</h1>"

# Run the app
if __name__ == '__main__':
    context = (r'/etc/ssl/certs/ssl-cert-snakeoil.pem', r'/etc/ssl/private/ssl-cert-snakeoil.key')
    app.run(debug=True, port=443, ssl_context=context)
