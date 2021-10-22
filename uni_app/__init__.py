from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    The homepage route. 
    
    This will later contain information about what classes are available to enroll in.
    '/' is the address here, which means it will be available from our host domain. 
    During production this is localhost:5000 or 127.0.0.1:5000
    """
    return "Hello, world! Check this out!"

@app.route('/students/')
def get_students():
    """
    The students page. 

    This will later contain a list of all students enrolled at the university.
    Since we are specifying a route of '/students/', this page is available from the address
    127.0.0.1:5000/students/ (at least during production).
    """
    return "This will be a list of all students at the university."

@app.route('/students/<int:student_id>/')
def get_specific_student(student_id):
    """
    The individual student page.

    This route accepts a URL parameter called student_id (must be an integer).

    That means that any address of the form localhost:5000/students/<some_number_here>/ will
    be available and will call the get_specific_student function. 

    The student_id argument supplied will be whatever number is in the url, and
    it will be included in the text on the page!
    """
    return f"This will be a page displaying information about student number {student_id}."

@app.route('/calc/<int:f_num>/<string:operator>/<int:s_num>/')
def calc(f_num, operator, s_num):
    """
    This is just a fun demonstration route, to show how more than one URL parameter can be used.

    This address contains three URL parameters: f_num, operator, and s_num. That means that any
    address of the form localhost:5000/calc/<some_number>/<some_string>/<some_number>/ will be
    available on our page. The first number in the url will be handed over to our function
    as the f_num argument, the string will be handed over as the operator argument, and the second
    number will be handed over as the s_num argument.

    The function called when any address matching that pattern is visited works as follows:
    If the operator string supplied is either a plus symbol, a minus symbol, or an asterisk,
    then the function returns a mathematical evaluation of the three symbols. So for instance...
        /calc/1/+/2/ 
    will render a web page displaying
        1+2 = 3

    If the string supplied is not one of those three symbols, on the other hand, the page will
    display the message
        'Please enter a valid calculation.'
    """
    if operator in ["+", "-", "*"]:
        return f"{f_num}{operator}{s_num} = {eval(f'{f_num}{operator}{s_num}')}"
    return "Please enter a valid calculation."

if __name__ == '__main__':
    app.run(debug=True)