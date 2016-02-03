import numpy as np
print np.dot([[1,2],[3,4]], [[5,6],[7,8]])
X = np.array([[1,1], [2, 1], [3, 1.2], [4, 1], [5, 0.8], [6, 1]])
from sklearn.decomposition import NMF
model = NMF(n_components=2, init='random', random_state=0)
print model.fit(X) 
import pdb; pdb.set_trace()
print model.components_
