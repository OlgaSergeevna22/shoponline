from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from base64 import b64encode
from cloudipsp import Api, Checkout

MAX_FILE_SIZE = 1024 * 1024 + 1
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.filters['b64d'] = lambda u: b64encode(u).decode() #add filter for templates
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Item(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.BLOB, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/test_index')
def index_test():
    ds = Item.query.all()
    return render_template('index_test.html',ds=ds)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():

    if request.method == 'POST':
        file = request.files["file"].read()
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        print(request.form)
        item = Item(title=title, price=price, text=text,photo=file)

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