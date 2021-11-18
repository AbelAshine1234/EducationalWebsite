from flask import Blueprint,render_template,request,redirect,url_for,flash
from .models import Blog,User,Question,Course
from . import db
from flask_login import current_user,login_required

views = Blueprint('views',__name__)
@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')

 
  
@views.route('/edit/<int:id>')
def edit(id):
    user = User.query.filter_by().filter(id==id).all()
    

    return render_template('edit.html',users=user)
@views.route('/question',methods=['GET','POST'])
@login_required
def question():
    if request.method=="POST":
        questionasked = request.form['question']
        instructor = request.form.get('instructor')

        question = Question(question=questionasked
                    ,asked_by_id =current_user.id,
                    asked_to_id=instructor)

        db.session.add(question)
        db.session.commit()
        flash(current_user.first_name+"You have succesfully Posted your Question ")
        return redirect(url_for('views.question'))
    instructors = User.query.filter_by(type="instructor").all()
    return render_template('question.html',instructors=instructors)

@views.route('/answerquestion',methods=['GET','POST'])
@login_required
def unanswered():
    unansweredquestions = Question.query.filter_by(asked_to_id=current_user.id).filter(Question.answer==None).all()

    if request.method == 'POST':
        answer = request.form['answer']
        return answer
   

    # return str(unansweredquestions[2].question)
   
    return render_template('answerquestion.html',question=unansweredquestions)

@views.route('/allquestion')
def allquestion():
    questions = Question.query.filter_by().filter(Question.answer != None).all()
    users = User.query.all()
    return render_template('allquestions.html',questions=questions,users=users)

@views.route('/answerquestion/<int:id>',methods=['GET','POST'])
def hello(id):
    question =  Question.query.get_or_404(id)
    if request.method == 'POST':
        answer = request.form.get('answer')
        question.answer = answer
        db.session.commit()
        flash("You Have Answered The Question")
        return redirect(url_for('views.unanswered'))
    return render_template('answerquestions.html',question=question)


@views.route('/seemore/<string:subject>',methods=['GET','POST'])
def seemore(subject):
    blogs = Blog.query.filter_by().filter(Blog.subject==subject).all()
    
    return render_template('seemore.html',blogs=blogs)
# Blog need  to query the data

@views.route('/content/<int:id>',methods=['GET','POST'])
def content(id):
    blog = Blog.query.filter_by().filter(Blog.id==id).one()
    users = User.query.all()
    return render_template('content.html',blog=blog,users=users)
@views.route('/blog',methods=['GET','POST'])
def blog():
    if request.method == "POST":
        return "erg"
    allblogs = Blog.query.all()
    courses = Course.query.all()
   
    return render_template('blog.html',blogs=allblogs,courses=courses)
@views.route('/quiz')
def quiz():
    return render_template('quiz.html')

@views.route('/posts/<int:id>')

def posts(id):
    blog = Blog.query.filter_by(id=id).one()
    return render_template('posts.html',blog=blog)



# @views.route('/delete/<int:id>',methods=['GET','POST'])
@views.route('/delete/<string:type>/<int:id>',methods=['GET','POST'])
def delete(type,id):
    if type == "user":
        user =  User.query.filter_by().filter(User.id==id).delete()
        db.session.commit()     
        flash("User Deleted")
        return redirect(url_for('views.admin'))
        
    elif type == "blog":
        blog = Blog.query.filter_by().filter(Blog.id == id).delete()
        db.session.commit()
        flash("Blog Deleted")
        return redirect(url_for('views.admin'))
    elif type == "question":
        question = Question.query.filter_by().filter(Question.id == id).delete()
        db.session.commit()
        flash("Quetion Deleted")
        return redirect(url_for('views.admin'))
    elif type == "course":
        course = Course.query.filter_by().filter(Course.id == id).delete()
        db.session.commit()
        flash("Course Deleted")
        return redirect(url_for('views.admin'))
    # db.session.commit()
    
    flash("User Deleted")
    # return redirect(url_for('views.admin'))
    return type
@views.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        course = request.form.get('course')
        course1 = Course(coursename=course)
        db.session.add(course1)
        db.session.commit()
        flash("You added the course to the database")
        return redirect(url_for('views.admin'))
 

    users = User.query.all()
    questions = Question.query.all()
    blogs = Blog.query.all()
    courses = Course.query.all()

   
    return render_template('admin.html',users=users,questions=questions,blogs=blogs,courses=courses)
@views.route('/post',methods=['get','post'])
def post():
    courses = Course.query.all()
    if request.method == "POST": 
        
        chapter = request.form['chapter']
        section = request.form['section']
        author = request.form['username']
        subject = request.form.get('subject')
        content = request.form['articles']
        blog = Blog(chapter=chapter,section=section,subject=subject,teacher=author,content=content);
        blog1 = Blog.query.all()
        flash("You Are successfully Posted your Note On "+subject)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('views.post'))
      
    return render_template('post.html',courses=courses)
