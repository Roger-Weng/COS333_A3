
import flask
import dbconnect

app = flask.Flask(__name__, template_folder=".")

@app.route("/", methods=["GET"])
def index():
    dept = flask.request.args.get("dept")
    number= flask.request.args.get("number")
    area = flask.request.args.get("area")
    title = flask.request.args.get("title")
    if dept is None:
        dept = ''
    if number is None:
        number = ''
    if area is None:
        area = ''
    if title is None:
        title = ''


    query_results = dbconnect.search(dept, number, area, title)

    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response



