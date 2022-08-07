from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        photo = request.form['photo']
        price = request.form['price']
        text = request.form['text']

        item = Item(title=title, price=price, text=text, photo=photo)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка'

    else:
        return render_template('create.html')


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)