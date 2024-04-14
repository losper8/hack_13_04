# TODO, to chromadb and api

import os

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.metrics import adjusted_rand_score, completeness_score, confusion_matrix, homogeneity_score, normalized_mutual_info_score, v_measure_score
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

embeddings_dirs = os.listdir('testing/embeddings_big')
print(embeddings_dirs)

one_big_embedding = []

df = DataFrame(columns=['embedding', 'class', 'cluster'])
embeddings_, classes = [], []

for embedding_dir in embeddings_dirs:
    embeddings = os.listdir(f'testing/embeddings_big/{embedding_dir}')
    print(embeddings)
    for embedding_name in embeddings:
        print(embedding_name)
        embedding = np.load(f'testing/embeddings_big/{embedding_dir}/{embedding_name}')['embedding']
        # one_big_embedding.append(embedding)
        embeddings_.append(embedding)
        classes.append(embedding_dir)
df['embedding'] = embeddings_
df['class'] = classes

# one_big_embedding = np.array(one_big_embedding)
# print(one_big_embedding.shape)
# np.savez_compressed('one_big_embedding.npz', embedding=one_big_embedding)

# embedding = np.load('one_big_embedding.npz')['embedding']
# print(embedding.shape)

matrix = np.vstack(df.embedding.values)
print(matrix.shape)

n_clusters = 11

kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42)
kmeans.fit(matrix)
labels = kmeans.labels_
df["cluster"] = labels

# db = DBSCAN(eps=0.5, min_samples=3)
# df["cluster"] = db.fit_predict(matrix)
# labels = db.labels_
# df["cluster"] = labels

le = LabelEncoder()
true_labels = le.fit_transform(df['class'])

cluster_labels = df['cluster']

cm = confusion_matrix(true_labels, cluster_labels)
print("Confusion Matrix:\n", cm)

ari = adjusted_rand_score(true_labels, cluster_labels)
print("Adjusted Rand Index:", ari)

nmi = normalized_mutual_info_score(true_labels, cluster_labels)
print("Normalized Mutual Information:", nmi)

homogeneity = homogeneity_score(true_labels, cluster_labels)
completeness = completeness_score(true_labels, cluster_labels)
v_measure = v_measure_score(true_labels, cluster_labels)
print("Homogeneity:", homogeneity)
print("Completeness:", completeness)
print("V-measure:", v_measure)

perplexity = 5
tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42, init="random", learning_rate="auto")
vis_dims2 = tsne.fit_transform(matrix)

x = [x for x, y in vis_dims2]
y = [y for x, y in vis_dims2]

for category, color in enumerate(["purple", "green", "red", "blue", "orange", "yellow", "black", "pink", "brown", "gray", "cyan"]):
    xs = np.array(x)[df.cluster == category]
    ys = np.array(y)[df.cluster == category]
    plt.scatter(xs, ys, color=color, alpha=0.3)

    if not xs.size or not ys.size:
        continue

    avg_x = xs.mean()
    avg_y = ys.mean()

    plt.scatter(avg_x, avg_y, marker="x", color=color, s=100)
plt.title(f'{perplexity} perplexity')
plt.show()

# pca = PCA(n_components=2)
# pca_result = pca.fit_transform(matrix)
#
# # Extract the resulting coordinates
# pca_x = pca_result[:, 0]
# pca_y = pca_result[:, 1]
#
# # Create a scatter plot
# plt.figure(figsize=(10, 7))
# colors = ["purple", "green", "red", "blue", "orange", "yellow", "black", "pink", "brown", "gray", "cyan"]
# for i, color in enumerate(colors):
#     # Plot each cluster with different color
#     plt.scatter(pca_x[df.cluster == i], pca_y[df.cluster == i], color=color, alpha=0.5, label=f'Cluster {i}')
#
# # Marking the center of each cluster
# for i, color in enumerate(colors):
#     xs = pca_x[df.cluster == i]
#     ys = pca_y[df.cluster == i]
#     avg_x = xs.mean()
#     avg_y = ys.mean()
#     plt.scatter(avg_x, avg_y, marker='x', color=color, s=100)
#
# plt.title('PCA Projection of Clusters')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend(loc='best')
# plt.show()
