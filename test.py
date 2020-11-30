from flask import Flask, request, redirect, render_template
# from flask_cors import CORS
app = Flask(__name__)
# CORS(app)

@app.route("/", methods=["GET"])
def index():
  # return redirect("/static/index.html", code=302)
    return render_template('params.jinja', foos = [{"name": "foo", "link": "http://google.de"}, {"name": "foo", "link": "http://google.de"}])



@app.route("/api/function1", methods=["GET", "POST"])
def hello():
    return('Hello World from Python:')
    print(request)

# @app.route("/runs/", methods=["GET", "POST"])
# def runs():
#   # Returns a list of all runs to select from
#   pass



if __name__  == '__main__':
    app.run()
