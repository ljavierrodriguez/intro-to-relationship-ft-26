from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


categories_news = db.Table('categories_news', 
    db.Column("news_id", db.Integer, db.ForeignKey('news.id'), nullable=False, primary_key=True),
    db.Column("categories_id", db.Integer, db.ForeignKey('categories.id'), nullable=False, primary_key=True)
)

likes_news = db.Table("likes_news", 
    db.Column("news_id", db.Integer, db.ForeignKey('news.id'), nullable=False, primary_key=True),
    db.Column("users_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
)

friends_users = db.Table("friends_users", 
    db.Column("users_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
    db.Column("friends_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)           
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False)
    likes = db.relationship("New", secondary=likes_news, backref="users")
    news = db.relationship("New", back_populates="user") # [<New 1>, <New 2>]
    friends = db.relationship("User", 
        secondary=friends_users, 
        primaryjoin=(friends_users.c.users_id == id), 
        secondaryjoin=(friends_users.c.friends_id == id),  
        backref=db.backref("friends2", lazy="dynamic")
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "biography": self.profile.biography,
            "count_posts": len(self.news),
            "titles_posts": list(map(lambda new: new.serialize(), self.news)),
            "friends": list(map(lambda user: user.username, self.friends)),
            "likes": len(self.likes)
        }


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.Text, default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class New(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="news")
    comments = db.relationship("Comment", backref="new")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user": self.user.username,
            "comments": len(self.comments)
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    news = db.relationship("New", secondary=categories_news, backref="categorie")


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    date_message = db.Column(db.DateTime, default=datetime.now())
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)