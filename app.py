from flask import Flask, render_template, request, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False,server_default='')
    content = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task %r>' % self.id
    
# @app.route('/', methods=['POST', 'GET'])
# def home():
#     if request.method == 'POST':
#         task_title = request.form['title']
#         new_task = Todo(title=task_title)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return f'There was an error while adding the task: {str(e)}'
#         except Exception as e:
#             return f'An unexpected error occurred: {str(e)}'

#     else:
#         tasks = Todo.query.all()
#         return render_template("index.html", tasks=tasks)


# @app.route('/', methods=['POST', 'GET'])
# def home():
#     if request.method == 'POST':
#         task_title = request.form['title']
        
#         # task_content = request.form['content']
#         # new_task1 = Todo(title=task_title, content=task_content) 
#         new_task = Todo(title=task_title)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except SQLAlchemyError as e:
#             db.session.rollback()
#         except:
#             return 'There was an error while adding the task'

#     else:
#         tasks = Todo.query.all()
#         return render_template("index.html", tasks=tasks)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_title = request.form['title']
        
        task_content = request.form['content']
        # new_task1 = Todo(title=task_title, content=task_content) 
        new_task = Todo(title=task_title,content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task) 


@app.route('/task/<int:task_id>')
def task_details(task_id):
    task = Todo.query.get_or_404(task_id)
    return render_template('task_details.html', task=task)

# Add this block to create database tables within the application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
