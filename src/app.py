from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



### Entry point.

if __name__ == "__main__":
    # Switch methods for deployment.
	# app.run(host='0.0.0.0')
    app.run()
