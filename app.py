# Imports
from flask import Flask
from flask import render_template, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask import request
from helpers.data_cleaner import valid_pass
from sqlalchemy import case

# Initialize Flask App
app = Flask(__name__)

# Session Management
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# SQLALCHEMY (SQLITE3)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user_database.db"
db = SQLAlchemy(app)

# Models [Database Tables]
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

# Todo List ( 1 for each user )
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
        backref=db.backref('todo', lazy=True))

# Task 0 or many to each Todo
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    priority = db.Column(db.String(20), nullable = False)
    label = db.Column(db.String(30), nullable = True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    todo = db.relationship('Todo',
        backref=db.backref('task', lazy=True))
    
# ============================================================================

# ROUTES

# HomePage 
@app.route("/")
def main():
    return redirect(url_for('login'))

# Index Page (USER Dashboard)
@app.route("/index")
def index():
    if 'username' not in session:
        flash("Login First!!")
        return redirect(url_for('login'))
    else:
        results = None
        try:
            # Get the Logged IN User 
            username = session["username"].lower()
            user = User.query.filter_by(username=username).first()
            # Get the respective Todo 
            todo = Todo.query.filter_by(user_id=user.id).first()
            # Order By Logic
            order = {'low' : 3, 'medium' : 2, "high" : 1}
            sort_logic = case(value=Task.priority, whens=order).label("priority")
            results = Task.query.filter_by(todo_id=todo.id).order_by(sort_logic).all()
            
            print(results)
            return render_template("index.html", results = results, todo_id = todo.id ) 
                  
        except:
            flash("Error Occured in Query!")
            print("Error Occured")    
  
    return render_template("index.html", results = results, todo_id = todo.id )


# Signup Route
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if "username" in session:
        return redirect(url_for("index"))
    
    elif request.method == "GET":
        return render_template("signup.html")
    
    elif request.method == "POST":
        # Data Extracted from FORM (POST REQ)
        print("POST")
        username = request.form["username"].lower()
        email = request.form["email"].lower()
        password = request.form["password"].lower()
        confirm_pass = request.form["confirm-pass"].lower()
        
        # Check if User Exists Already
        result = User.query.filter_by(username=username).first()
        
        # If result is None, Create new User
        if result is None:
            print("Here")
            # compare password and confirm_pass
            if valid_pass(password, confirm_pass):
                
                # Create User
                user = User(username=username, password=password, email=email)
                db.session.add(user)
                db.session.commit()
                
                # Create Todo For the user
                todo = Todo(user_id=user.id, user=user)
                db.session.add(todo)
                db.session.commit()
                
                # Create Session of user
                session['username'] = username
                session["login"] = True
                
                return redirect(url_for('index'))
                
            else:
                flash("Passwords Don't Match!!")
                return redirect(url_for("signup"))
        
        # User exits
        else:
            # User Exists..!!
            flash("Can't Create The User!")
            return redirect(url_for("signup"))
             
    return render_template('signup.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    # IF logged in, redirect to home
    if "username" in session:
        username = session['username']
        return redirect(url_for("index"))
    
    # GET Request
    if request.method == "GET":
        return render_template("login.html")
    
    # Post request
    elif request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"].lower()
        # Query DB and get the user
        res = User.query.filter_by(username=username).first()
        
        if res is None:
            return redirect(url_for('login'))
        print(res.username)
        if valid_pass(res.password, password ):
            session["username"] = username
            session["login"] = True
            return redirect(url_for("index"))
        else:
            print("Invalid Password")
            
    return redirect(url_for("login"))
        
@app.route("/logout")
def logout():
    if session.get("username"):
        session.pop("username")
        session.pop("login")
    
    return redirect(url_for("login"))

"""
    Tasks 
"""

# Create Task for Particular TODO ID 
@app.route("/create_task/<int:todo_id>", methods=['POST', "GET"])
def create_task(todo_id):
    if request.method == "POST":
        title = request.form["title"].title()
        priority = request.form["priority"].lower()
        label =  request.form["label"].lower()
        
        todo = Todo.query.filter_by(id=todo_id).first()
    
        task = Task(title=title, priority=priority, label=label, todo=todo, todo_id=todo_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("index"))
      
    else:
        return render_template("create_task.html", todo_id = todo_id)

# Delete Task
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        print("Deeleting Task")
        Task.query.filter_by(id=task_id).delete()
        db.session.commit()
        return redirect(url_for('index'))
    except:
        print("Error In Deleting!!")
        return redirect(url_for('index'))

# Update Task
@app.route("/update_task/<int:task_id>", methods=['POST', 'GET'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    
    if request.method == "GET":    
        print(task)
        return render_template("update_task.html", task_data = task)
    elif request.method == "POST":
        title = request.form["title"].title()
        priority = request.form["priority"].lower()
        label =  request.form["label"].lower()

        task.title = title
        task.priority = priority
        task.label = label

        db.session.commit()
        return redirect(url_for("index"))
        
if __name__ == "__main__":
    app.run(debug=True)