import numpy as np
import numpy.typing as npt
from typing import Dict, Any
from .distance_calculus.cosine_similarity import (
	cosine_similarity_vector_matrix
)

def sort_by_distances(
	user_embedding: npt.NDArray, 
	posts_embeddings: Dict[str, npt.NDArray]
) -> Dict[str, Any]: 
	"""Sort vectors by distances.
	
	:param user_embedding: ndaray: Embedding for the user.
	:param posts_embeddings: dict: Posts ids and their embedding

	return
		Post ids ordered by distance
	"""
	posts_ids = list(posts_embeddings.keys())
	posts_matrix = np.array(list(posts_embeddings.values()))

	cosine_sim_arr = np.zeros(len(posts_ids), dtype=float)
	cosine_similarity_vector_matrix(user_embedding, posts_matrix, cosine_sim_arr)

	top_similar = np.argsort(cosine_sim_arr)[::-1]
	top = [
		{
			"post": posts_ids[i],
			"similarity": cosine_sim_arr[i],
		}
		for i in top_similar
	]
	
	return top
