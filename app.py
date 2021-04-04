from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from datetime import datetime

# this is how we always start a flask app
app = Flask(__name__)
# when configuring the database this is what we use
# the test.db is the name of our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# we create a database model that defines the columns and rules we want to use
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DATETIME, default=datetime.utcnow)

# this will return whatever task we put in as a string
    def __repr__(self):
        return '<Task %r>' % self.id


# since we will be communicating with the database, we will need methods
@app.route('/', methods=['POST', 'GET'])
def index():
    #  our if statement here says that if the request method is a POST, we will create
    # a new variable called task_content that takes its data from our form in the html file
    # we will then create a new variable that places the content in the Todo db model we created

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # we will then try by adding the new task in our db by using the session method available
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    # our else function will return our tasks in order of dates added
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# a similar logic applies to our delete function
# here we set the route to the id of the content we want to delete as this is the unique identifier
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"


# we use the methods because an update is going to get the information and later post to our database
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # we use our query here to identify the right task we are supposed to update
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        # passing task=task in our render template affects the html file.
        # it tells it that the task variable mentioned there is the query from our app.py
        return render_template('update.html', task=task)


# this is always at the end of every flask project. The debug=True hot reloads it
if __name__ == "__main__":
    app.run(debug=True)
