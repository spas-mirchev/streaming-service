from joblib import PrintTime
import pandas as pd
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


interactions_df = pd.read_csv(
    "/home/evgeniya/Documents/code/streaming service/streamapp/static/csv/lastfm_user_scrobbles.csv")
titles_df = pd.read_csv(
    "/home/evgeniya/Documents/code/streaming service/streamapp/static/csv/lastfm_artist_list.csv")


# artist names
titles_df.index = titles_df["artist_id"]
titles_dict = titles_df["artist_name"].to_dict()

# matrix Users Artists
rows, r_pos = np.unique(interactions_df.values[:, 0], return_inverse=True)
cols, c_pos = np.unique(interactions_df.values[:, 1], return_inverse=True)

interactions_sparse = sparse.csr_matrix(
    (interactions_df.values[:, 2], (r_pos, c_pos)))

# Normalize
Pui = normalize(interactions_sparse, norm='l2', axis=0)
sim = Pui.T * Pui

sim_artists = [titles_dict[i+1]
               for i in sim[13303].toarray().argsort()[0][-20:]]
#print(sim_artists)

fit = Pui * Pui.T * Pui

# beginning

initial_set = set([titles_dict[i+1]for i in np.nonzero(interactions_sparse[2])[1].tolist()])
#print(initial_set)

predicted_set = set([titles_dict[i+1]
                 for i in fit[2].toarray().argsort()[0][-70:].tolist()])
#print(predicted_set)

print(len(predicted_set - initial_set))