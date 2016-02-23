from app import cache, db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    # image = db.Column(db.String(100), nullable=False, server_default='')

    @staticmethod
    @cache.memoize(timeout=50)
    def get_all_movies():
        # import pdb; pdb.set_trace()
        return Movie.query.all()
