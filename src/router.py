from flask import Flask, render_template

app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build/static")

@app.get("/")
def hello_world():
    return render_template('index.html')
