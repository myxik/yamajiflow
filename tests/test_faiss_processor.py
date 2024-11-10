import os

import faiss
import numpy as np
import pytest

from jyflow.processors.index_processor import FAISSIndexProcessor


@pytest.fixture
def sample_vectors():
    # Create sample vectors for testing
    return np.random.rand(10, 1536).astype(np.float32)

def test_init_with_default_params():
    processor = FAISSIndexProcessor()
    assert processor.dimension == 1536
    assert processor.index_type == "flat"
    assert isinstance(processor.index, faiss.IndexFlatL2)

def test_init_with_custom_params():
    processor = FAISSIndexProcessor(dimension=512, index_type="hnsw")
    assert processor.dimension == 512
    assert processor.index_type == "hnsw"
    assert isinstance(processor.index, faiss.IndexHNSWFlat)

def test_invalid_index_type():
    with pytest.raises(ValueError, match="Unsupported index type"):
        FAISSIndexProcessor(index_type="invalid")

def test_add_and_search_vectors(sample_vectors):
    processor = FAISSIndexProcessor()
    processor.add_vectors(sample_vectors)

    # Test search with single query vector
    query = sample_vectors[0:1]  # Take first vector as query
    distances, indices = processor.search(query, k=3)

    assert distances.shape == (1, 3)
    assert indices.shape == (1, 3)
    assert indices[0][0] == 0  # First result should be the query vector itself

def test_add_vectors_wrong_dimension():
    processor = FAISSIndexProcessor(dimension=1536)
    wrong_dim_vectors = np.random.rand(10, 512).astype(np.float32)

    with pytest.raises(ValueError, match="Expected vectors of dimension"):
        processor.add_vectors(wrong_dim_vectors)

def test_search_wrong_dimension():
    processor = FAISSIndexProcessor(dimension=1536)
    wrong_dim_query = np.random.rand(1, 512).astype(np.float32)

    with pytest.raises(ValueError, match="Expected vectors of dimension"):
        processor.search(wrong_dim_query)

def test_save_and_load_index(sample_vectors, tmp_path):
    # Create temporary file path
    index_path = os.path.join(tmp_path, "test_index.faiss")

    # Create and populate first processor
    processor1 = FAISSIndexProcessor()
    processor1.add_vectors(sample_vectors)
    processor1.save_index(index_path)

    # Create second processor and load index
    processor2 = FAISSIndexProcessor()
    processor2.load_index(index_path)

    # Compare search results from both processors
    query = sample_vectors[0:1]
    distances1, indices1 = processor1.search(query)
    distances2, indices2 = processor2.search(query)

    np.testing.assert_array_almost_equal(distances1, distances2)
    np.testing.assert_array_equal(indices1, indices2)

def test_ivf_index():
    processor = FAISSIndexProcessor(index_type="ivf")
    vectors = np.random.rand(100, 1536).astype(np.float32)

    # Test that adding vectors trains the index
    processor.add_vectors(vectors)
    assert processor.index.is_trained

    # Test search functionality
    query = vectors[0:1]
    distances, indices = processor.search(query, k=3)
    assert distances.shape == (1, 3)
    assert indices.shape == (1, 3)
