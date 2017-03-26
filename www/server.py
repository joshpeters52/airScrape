from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

def getData():
	DATA_PATH = "output.txt"
	text_file = open(DATA_PATH, "r")
	text = text_file.read().split('\n')

	return text

if __name__ == "__main__":
	app.run()
