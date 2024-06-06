# Import necessary modules from Flask, SQLAlchemy, and Werkzeug
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database and other app configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Todo', backref='owner')  # Relationship between User and their tasks

# Define Todo model for the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    list_id = db.Column(db.Integer, default=1)  # New column for list ID
    children = db.relationship('Todo', backref=db.backref('parent', remote_side=[id]))  # Relationship for hierarchical tasks

# Helper function to log in a user and store their ID in the session
def login_user(user):
    session['user_id'] = user.id

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        return '<p>Incorrect username or password</p>'
    return render_template('login.html')

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Main route to display the todo list
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    todo_list = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('base.html', todo_list=todo_list)

# Route to add a new task
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    parent_id = request.form.get("parent_id", type=int)
    list_id = request.form.get("list_id", type=int, default=1)  # Capture the list ID
    level = 1
    if parent_id:
        parent_task = Todo.query.get(parent_id)
        if not parent_task or parent_task.level >= 3:
            return "Invalid parent task or maximum depth reached!", 400
        level = parent_task.level + 1
    new_todo = Todo(title=title, user_id=session['user_id'], parent_id=parent_id, level=level, list_id=list_id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

# Route to update the completion status of a task
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=session['user_id']).first()
    if not todo:
        return "Task not found!", 404
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

# Route to delete a task
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=session['user_id']).first()
    if not todo:
        return "Task not found!", 404
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# Route to move a top-level task under another top-level task
@app.route("/move-task", methods=["POST"])
def move_task():
    task_id = request.form.get("task_id", type=int)
    new_parent_id = request.form.get("new_parent_id", type=int)
    task = Todo.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if not task:
        return "Task not found!", 404
    if new_parent_id:
        new_parent = Todo.query.get(new_parent_id)
        if not new_parent or new_parent.level != 1:
            return "Invalid target task!", 400
        # Ensure the task being moved does not have any sub-tasks
        if task.children:
            return "Cannot move a task with sub-tasks!", 400
        task.parent = new_parent
        task.level = 2  # Since it's now a sub-task
    db.session.commit()
    return redirect(url_for("index"))

# Main execution point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)  # Run the Flask app in debug mode
