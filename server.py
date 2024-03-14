
import flask
import dbconnect

app = flask.Flask(__name__, template_folder=".")

@app.route("/", methods=["GET"])
def index():
    dept = flask.request.args.get("dept")
    number = flask.request.args.get("coursenum")
    area = flask.request.args.get("area")
    title = flask.request.args.get("title")
    print(title)
    if dept is None: 
        dept = ""
    if number is None:
        number = ""
    if area is None:
        area = ""
    if title is None:
        title = ""
    
    query_results = dbconnect.search(dept, number, area, title)
    if (query_results[0] == True):
        print(title)
        html_code = flask.render_template('index.html', courses=query_results[1], dept_search = dept, 
                                          number_search = number, area_search = area, title_search = title)
    else:
        html_code = flask.render_template('error.html')
    
    response = flask.make_response(html_code)
    response.set_cookie("dept", dept)
    response.set_cookie("number", number)
    response.set_cookie("area", area)
    response.set_cookie("title", title)
    return response

@app.route("/regdetails", methods=["GET"])
def regdetails():
   classid = flask.request.args.get("classid")
   if classid is None: 
       classid = ""
   
   dept = flask.request.cookies.get('dept')
   number = flask.request.cookies.get('number')
   area = flask.request.cookies.get('area')
   title = flask.request.cookies.get('title')

   querey_results = dbconnect.get_class_details(classid)
   if querey_results[0] == True:
       html_code = flask.render_template('regdetails.html', info = querey_results[1], classid = classid, dept = dept, 
                                         number = number, area = area, title = title)
   response = flask.make_response(html_code)
   return response

def escape_special_characters(string):
    return string.replace('_', '\\_').replace('%', '\\%')




