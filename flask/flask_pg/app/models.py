from . import db

class Book(db.Model):
    __tablename__="books"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    author = db.Column(db.String(120),nullable=False)
    published_date = db.Column(db.Date,nullable=False)

    def to_dict(self):
        return{
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'published_date':self.published_date
        }    