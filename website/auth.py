from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import  User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_required,login_user,logout_user,LoginManager

auth = Blueprint('auth',__name__)

# logout
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
         # getting the form input
        email = request.form.get('email')
        password = request.form.get('password')
        type = request.form.get('registertype')
        user = User.query.filter_by(email=email).first()
        # if there is user check the usser else go out
        if user:
            # checking if the user is teache or student
            if user.type != type:
                flash(user.first_name+"    is not    "+ type)
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password,password):
                flash("YOu have successfully logged in")
                login_user(user)
                return redirect(url_for('auth.login'))
            flash("Wrong Password Please Check Again")
            return redirect(url_for('auth.login'))

        flash("please try to register")
        return redirect(url_for('auth.login'))

       
        
    
    return render_template('login.html')








# signup 
@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':

        # getting the form input
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm = request.form.get('second-password')
        type = request.form.get('registertype')

        # check if there is still a user present by this email name else regiser a user
        user = User.query.filter_by(email=email).first()
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password != confirm:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif user:
            flash("No need of double registeration")
            return redirect(url_for('auth.signup'))
        else:

            user =  User(email=email,
                          password=generate_password_hash(
                password, method='sha256')
                         ,first_name=first_name,
                         last_name=last_name,
                         type=type)
            # adding to the database
            db.session.add(user)
            db.session.commit() 


            flash("You have succesfully registered as   "+user.type)
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')


@auth.route('/logout')
def log_out():
    flash("You have succesfully logged out")
    logout_user()
    return redirect(url_for('views.home'))