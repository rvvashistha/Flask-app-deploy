from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
import uuid
import pymysql
from werkzeug.utils import secure_filename

app = Flask(__name__)
 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Rohit2798@localhost/session_feedback_store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    learner = db.Column(db.String(200), unique=True)
    mentor = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, learner, mentor, rating, comments):
        self.learner = learner
        self.mentor = mentor
        self.rating = rating
        self.comments = comments


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])  # type: ignore
def submit():
    if request.method == 'POST':
        learner = request.form['learner']
        mentor = request.form['mentor']
        rating = request.form['rating']         
        comments = request.form['comments']
        # print(learner, mentor, rating, comments)
        if learner == '' or mentor == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.learner == learner).count() == 0:
            data = Feedback(learner, mentor, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('thanku.html')
        return render_template('index.html', message='You have already submitted feedback')
    
   
if __name__ == "__main__":
    app.run()
