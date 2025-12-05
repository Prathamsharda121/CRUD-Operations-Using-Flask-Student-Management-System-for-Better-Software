from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='student_app/static')
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    course=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return f'<student{self.name}>'
    
@app.route('/')
def index():
    students= Student.query.all()
    return render_template('index.html',students=students)
@app.route('/add',methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']

        new_student = Student(name=name,email=email,course=course)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method=='POST':
        student.name=request.form['name']
        student.email=request.form['email']
        student.course=request.form['course']
        db.session.commit()
        return redirect(url_for('index'))
    return  render_template('edit.html',student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    