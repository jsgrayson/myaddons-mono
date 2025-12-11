from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talents')
def talents():
    return render_template('talents.html')

@app.route('/gear')
def gear():
    return render_template('gear.html')

@app.route('/gold')
def gold():
    return render_template('gold.html')

@app.route('/api/status')
def status():
    return jsonify({"status": "RUNNING", "service": "SkillWeaver"})

if __name__ == '__main__':
    print("🌐 Starting SkillWeaver (Python) on http://127.0.0.1:3000")
    app.run(port=3000, debug=True)
