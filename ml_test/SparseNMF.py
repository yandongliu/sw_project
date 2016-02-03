"""Sparse Matrix based Non-Negative Matrix Factorization"""
from operator import itemgetter

class SparseMatrix(object):
    def __init__(self, rank):
        self.ratings = []
        self.num_users = 0
        self.num_items = 0
        self.rank = rank
        self.P = []
        self.Q = []

    @staticmethod
    def innerproduct(p, q):
        assert len(p) == len(q)
        prdt = 0.0
        for i in xrange(len(p)):
            prdt += p[i] * q[i]
        return prdt

    def train(self, num_iters):
        """Use stochastic gradient descent to minimize loss"""
        gamma = 0.00005
        lambda_ = 0.0000001
        min_rmse = 10 ** 10
        for loop in xrange(num_iters):
            rmse = 0.0
            for data in self.ratings:
                user_id, item_id, rating = data
                # print user_id, item_id, rating
                p = self.P[user_id - 1]
                q = self.Q[item_id - 1]
                pred = SparseMatrix.innerproduct(p, q)
                err = rating - pred
                rmse += err * err
                for j in xrange(self.rank):
                    q[j] += (gamma * (2.0 * p[j] * err - lambda_ * q[j]))
                    p[j] += (gamma * (2.0 * q[j] * err - lambda_ * p[j]))
            if min_rmse > rmse:
                min_rmse = rmse
            print 'Iteration {} loss {}'.format(loop, min_rmse)

    def predict(self, user_id, item_id):
        return SparseMatrix.innerproduct(self.P[user_id], self.Q[item_id])
                

    @staticmethod
    def loadFromMovielensFile2(fn):
        rank = 20
        matrix = SparseMatrix(rank)
        map_user = {}
        map_item = {}
        cnt_user = 0
        cnt_item = 0
        with open(fn, 'r') as f:
            for l in f:
                user, item, rating, _ = l.rstrip().split('::')
                rating = float(rating)
                if user not in map_user:
                    map_user[user] = cnt_user
                    cnt_user += 1
                if item not in map_item:
                    map_item[item] = cnt_item
                    cnt_item += 1
                user_id = map_user[user]
                item_id = map_item[item]
                matrix.ratings.append((user_id, item_id, rating))
        matrix.num_users = cnt_user
        matrix.num_items = cnt_item
        for i in xrange(cnt_user):
            row = []
            matrix.P.append(row)
            for j in xrange(rank):
                row.append(0.1)
        for i in xrange(cnt_item):
            row = []
            matrix.Q.append(row)
            for j in xrange(rank):
                row.append(0.1)
        return matrix

    @staticmethod
    def loadFromMovielensFile(fn):
        rank = 20
        matrix = SparseMatrix(rank)
        map_user = {}
        map_item = {}
        max_user_id = 0
        max_item_id = 0
        with open(fn, 'r') as f:
            for l in f:
                user_id, item_id, rating, _ = l.rstrip().split('::')
                user_id = int(user_id)
                item_id = int(item_id)
                rating = float(rating)
                matrix.ratings.append((user_id, item_id, rating))
                if max_user_id < user_id:
                    max_user_id = user_id
                if max_item_id < item_id:
                    max_item_id = item_id
        print max_user_id, max_item_id
        matrix.num_users = max_user_id
        matrix.num_items = max_item_id
        for i in xrange(matrix.num_users):
            row = []
            matrix.P.append(row)
            for j in xrange(rank):
                row.append(0.1)
        for i in xrange(matrix.num_items):
            row = []
            matrix.Q.append(row)
            for j in xrange(rank):
                row.append(0.1)
        return matrix

    @staticmethod
    def loadMovieNames(fn):
        map_movie = {}
        with open(fn, 'r') as f:
            for l in f:
                movie_id, name, genre = l.rstrip().split('::')
                map_movie[int(movie_id)] = (name, genre)
        return map_movie

if __name__ == '__main__':
    fn = '../data/ml-1m/ratings_small.dat'
    fn_movie = '../data/ml-1m/movies.dat'
    fn = '../data/ml-1m/ratings.dat'
    movie_names = SparseMatrix.loadMovieNames(fn_movie)
    m = SparseMatrix.loadFromMovielensFile(fn)
    print 'Number of users {}, number of items {}.'.format(len(m.P), len(m.Q))
    m.train(1000)
    scores = []
    user_id = 22
    for item_id in xrange(len(m.Q)):
        score = m.predict(user_id, item_id)
        scores.append((item_id, score)) 
    sorted_scores = sorted(scores, key=itemgetter(1), reverse=True)
    for item in sorted_scores[:5]:
        print 'Movie {}. Score {}'.format(movie_names.get(item[0]), item[1])
