from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, world! Check this out!"

@app.route('/students/')
def get_students():
    return "This will be a list of all students at the university."

@app.route('/students/<int:student_id>/')
def get_specific_student(student_id):
    return f"This will be a page displaying information about student number {student_id}."

if __name__ == '__main__':
    app.run(debug=True)