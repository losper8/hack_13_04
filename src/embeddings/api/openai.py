from io import BytesIO
from typing import Dict, List

import aiohttp
import numpy as np
import pandas as pd
from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, completeness_score, confusion_matrix, davies_bouldin_score, homogeneity_score, normalized_mutual_info_score, silhouette_score, v_measure_score
from sklearn.preprocessing import LabelEncoder
from starlette.responses import FileResponse, StreamingResponse

from embeddings.api.schema import EmbeddingRequest, SearchRequest
from embeddings.domain.embeddings import domain_save_embeddings, openai_collection_clean_big, openai_collection_raw_big, openai_embedding_function
from embeddings.infrastructure.chroma_db_config import chroma_db_config

openai_router = APIRouter(
    prefix="/openai",
    tags=["openai"],
)


@openai_router.post(
    "/embeddings",
)
async def save_embedding(
    request: List[EmbeddingRequest],
):
    await domain_save_embeddings(request)
    return {"message": "Embeddings saved"}


@openai_router.post(
    "/search",
)
async def search(
    request: SearchRequest,
    dataset: str = Query(),
    n_results: int = Query(100),
    include_embeddings: bool = Query(False),
    raw: bool = Query(False),
    first: bool = Query(True),
):
    collection_raw = openai_collection_raw_big
    collection_clean = openai_collection_clean_big

    if first:
        where = {"$and": [{"dataset": {"$eq": dataset}}, {"part_index": {"$eq": 0}}]}
    else:
        where = {"dataset": {"$eq": dataset}}
    include = ["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else [])

    if raw:
        return collection_raw.query(
            query_embeddings=openai_embedding_function([request.text]),
            n_results=n_results,
            include=include,
            where=where
        )
    return collection_clean.query(
        query_embeddings=openai_embedding_function([request.text]),
        n_results=n_results,
        include=include,
        where=where
    )


@openai_router.get(
    "/get_embeddings_npz",
)
async def search(
    dataset: str = Query(),
    raw: bool = Query(False),
    first: bool = Query(True),
):
    collection_raw = openai_collection_raw_big
    collection_clean = openai_collection_clean_big
    collection = collection_raw if raw else collection_clean

    embeddings_all = []
    labels_all = []

    async with aiohttp.ClientSession() as session:
        if first:
            where = {"$and": [{"dataset": {"$eq": dataset}}, {"part_index": {"$eq": 0}}]}
        else:
            where = {"dataset": {"$eq": dataset}}
        include = ["metadatas", "embeddings"]

        async with session.post(
            f'http://{chroma_db_config.HOST}:{chroma_db_config.PORT}/api/v1/collections/{collection.id}/get',
            json={
                'where': where,
                'include': include,
            }
        ) as response:
            result = await response.json()
            embeddings_all.extend([np.array(embedding) for embedding in result['embeddings']])
            labels_all.extend([metadata['class'] for metadata in result['metadatas']])
    embeddings_numpy_all = np.vstack(embeddings_all)
    labels_numpy_all = np.array(labels_all)

    buffer = BytesIO()
    np.savez_compressed(buffer, embeddings=embeddings_numpy_all, labels=labels_numpy_all)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/octet-stream", headers={
        "Content-Disposition": "attachment; filename=embeddings_labels.npz"
    })


@openai_router.get(
    "/train_metrics",
)
async def search(
    dataset: str = Query(),
    n_clusters: int = Query(),
    raw: bool = Query(False),
    first: bool = Query(True),
):
    collection_raw = openai_collection_raw_big
    collection_clean = openai_collection_clean_big
    collection = collection_raw if raw else collection_clean

    embeddings_all = []
    labels_all = []

    async with aiohttp.ClientSession() as session:
        if first:
            where = {"$and":
                [
                    {"dataset": {"$eq": dataset}},
                    {"part_index": {"$eq": 0}},
                    {"class": {"$ne": "test"}}
                ]
            }
        else:
            where = {"$and":
                [
                    {"dataset": {"$eq": dataset}},
                    {"class": {"$ne": "test"}}
                ]
            }

        include = ["metadatas", "embeddings"]

        async with session.post(
            f'http://{chroma_db_config.HOST}:{chroma_db_config.PORT}/api/v1/collections/{collection.id}/get',
            json={
                'where': where,
                'include': include,
            }
        ) as response:
            result = await response.json()
            embeddings_all.extend([np.array(embedding) for embedding in result['embeddings']])
            labels_all.extend([metadata['class'] for metadata in result['metadatas']])
    embeddings_numpy_all = np.vstack(embeddings_all)
    labels_numpy_all = np.array(labels_all)

    df = pd.DataFrame({
        'embedding': list(embeddings_numpy_all),
        'class': labels_numpy_all
    })

    matrix = np.vstack(df.embedding.values)
    print(matrix.shape)

    n_clusters = n_clusters

    kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42, n_init="auto", max_iter=1000)
    kmeans.fit(matrix)
    labels = kmeans.labels_
    df["cluster"] = labels

    le = LabelEncoder()
    true_labels = le.fit_transform(df['class'])

    cluster_labels = df['cluster']

    cm = confusion_matrix(true_labels, cluster_labels)
    ari = adjusted_rand_score(true_labels, cluster_labels)
    nmi = normalized_mutual_info_score(true_labels, cluster_labels)

    homogeneity = homogeneity_score(true_labels, cluster_labels)
    completeness = completeness_score(true_labels, cluster_labels)
    v_measure = v_measure_score(true_labels, cluster_labels)
    silhouette = silhouette_score(matrix, cluster_labels)
    calinski_harabasz = calinski_harabasz_score(matrix, cluster_labels)
    davies_bouldin = davies_bouldin_score(matrix, cluster_labels)

    return {
        'confusion_matrix': cm.tolist(),
        'adjusted_rand_index': ari,
        'normalized_mutual_information': nmi,
        'homogeneity': homogeneity,
        'completeness': completeness,
        'v_measure': v_measure,
        'silhouette_score': silhouette,
        'calinski_harabasz_index': calinski_harabasz,
        'davies_bouldin_index': davies_bouldin,
    }


class TestInferenceRequest(BaseModel):
    cluster_to_class_mapping: Dict[int, str] = Field(default={
        0: 'proxy',
        1: 'contract',
        2: 'act',
        3: 'application',
        4: 'order',
        5: 'invoice',
        6: 'bill',
        7: 'arrangement',
        8: 'contract offer',
        9: 'statute',
        10: 'determination'
    })


@openai_router.post("/test_inference")
async def test_search(
    dataset: str = Query(),
    raw: bool = Query(False),
    first: bool = Query(True),
    n_clusters: int = Query(),
    request: TestInferenceRequest = Body(...),
):
    class_to_cluster_mapping = {v: k for k, v in request.cluster_to_class_mapping.items()}
    collection_raw = openai_collection_raw_big
    collection_clean = openai_collection_clean_big
    collection = collection_raw if raw else collection_clean

    embeddings_all = []
    labels_all = []

    async with aiohttp.ClientSession() as session:
        if first:
            where = {"$and":
                [
                    {"dataset": {"$eq": dataset}},
                    {"part_index": {"$eq": 0}},
                    {"class": {"$ne": "test"}}
                ]
            }
        else:
            where = {"$and":
                [
                    {"dataset": {"$eq": dataset}},
                    {"class": {"$ne": "test"}}
                ]
            }

        include = ["metadatas", "embeddings"]

        async with session.post(
            f'http://{chroma_db_config.HOST}:{chroma_db_config.PORT}/api/v1/collections/{collection.id}/get',
            json={
                'where': where,
                'include': include,
            }
        ) as response:
            result = await response.json()
            embeddings_all.extend([np.array(embedding) for embedding in result['embeddings']])
            labels_all.extend([class_to_cluster_mapping[metadata['class']] for metadata in result['metadatas']])
    embeddings_numpy_all = np.vstack(embeddings_all)
    labels_numpy_all = np.array(labels_all)

    df = pd.DataFrame({
        'embedding': list(embeddings_numpy_all),
        'class': labels_numpy_all
    })

    matrix = np.vstack(df.embedding.values)

    n_clusters = n_clusters

    kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42, n_init="auto", max_iter=1000)
    kmeans.fit(matrix)

    test_embeddings = []
    test_document_ids = []

    async with aiohttp.ClientSession() as session:
        where = {"$and":
            [
                {"dataset": {"$eq": dataset}},
                {"class": {"$eq": "test"}}
            ]
        }

        include = ["metadatas", "embeddings"]

        async with session.post(
            f'http://{chroma_db_config.HOST}:{chroma_db_config.PORT}/api/v1/collections/{collection.id}/get',
            json={
                'where': where,
                'include': include,
            }
        ) as response:
            result = await response.json()
            test_embeddings.extend([np.array(embedding) for embedding in result['embeddings']])
            test_document_ids.extend([metadata['document_id'] for metadata in result['metadatas']])

    test_embeddings_numpy = np.vstack(test_embeddings)
    test_labels = kmeans.predict(test_embeddings_numpy)

    result_data = {
        "document_id": test_document_ids,
        "class_id": test_labels.tolist()
    }
    df = pd.DataFrame(result_data)

    df.to_csv("submission.csv", index=False, sep=';')

    return FileResponse("submission.csv")
