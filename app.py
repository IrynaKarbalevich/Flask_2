from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Post %r' % self.id


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Post', backref='category')


menu = [{"name": "Информация обо мне", "url": "about"},
        {"name": "Добавить статью", "url": "create_post"},
        {"name": "Главная страница", "url": "/"}]


@app.route("/")
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html', menu=menu, posts=posts)


@app.route("/post/<int:id>")
def show_post(id):
    post = Post.query.get(id)
    return render_template('post.html', menu=menu, post=post)


@app.route("/post/<int:id>/delete")
def delete_post(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except:
        return 'При удалении произошла ошибка'


@app.route("/about")
def about():
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/contact")
def contact():
    return render_template('contact.html', title="Мои контакты", menu=menu)


@app.route("/certificate")
def show_certificate():
    return render_template('сertificate.html', title="Сертификаты", menu=menu)


@app.route("/create_post", methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Post(title=title, intro=intro, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')

        except:
            return "При добавлении произошла ошибка"
    else:
        return render_template('create_post.html', title='Добавить статью', menu=menu)


@app.route("/post/<int:id>/update", methods=['POST', 'GET'])
def update_post(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "При добавлении произошла ошибка"
    else:
        return render_template('update_post.html', title='Редактирование статьи', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
