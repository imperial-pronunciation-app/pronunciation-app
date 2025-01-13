from flask import Flask, render_template, request, jsonify
import string
from tempfile import NamedTemporaryFile
import whisper

model = whisper.load_model("base")

# Initialize the Flask app
app = Flask(__name__)

# Homepage route
@app.route('/')
def home():
    return "<h1>Hello World</h1>"

# From https://www.geeksforgeeks.org/edit-distance-dp-5/
def edit_dist(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    prev = 0  # Stores dp[i-1][j-1]
    curr = list(range(n + 1))  # Stores dp[i][j-1] and dp[i][j]

    for i in range(1, m + 1):
        prev = curr[0]
        curr[0] = i
        for j in range(1, n + 1):
            temp = curr[j]
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev
            else:
                curr[j] = 1 + min(curr[j - 1], prev, curr[j])
            prev = temp
    return curr[n]

def similarity(target: str, transcribed: str) -> float:
    return 1 - edit_dist(target, transcribed) / len(target)

@app.route('/text-similarity/<target>', methods=['POST'])
def text_similarity(target: str):
    audio = request.files['audio']
    with NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
        audio.save(temp_audio.name)  # Save uploaded file to temp file
        transcribed = (
            model
            .transcribe(temp_audio.name)["text"] # Transcribe using Whisper
            .lower()
            .strip()
            .translate(str.maketrans('', '', string.punctuation)) # Remove punctuation
        )
    return jsonify({
        "transcribed": transcribed,
        "target": target,
        "similarity": similarity(target, transcribed)
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
