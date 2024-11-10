import faiss
import numpy as np


class FAISSIndexProcessor:
    """
    A processor class for building and managing FAISS indexes for vector similarity search.
    """

    def __init__(self, dimension: int = 1536, index_type: str = "flat"):
        """
        Initialize the FAISS index processor.

        Args:
            dimension: Dimensionality of the vectors to be indexed. Defaults to 1536.
            index_type: Type of FAISS index to use ('flat', 'ivf', 'hnsw'). Defaults to 'flat'.
        """
        self.dimension = dimension
        self.index_type = index_type
        self.index = self._create_index()

    def _create_index(self) -> faiss.Index:
        """
        Create the appropriate FAISS index based on index_type.

        Returns:
            FAISS index

        Raises:
            ValueError: If the index type is unsupported
        """
        if self.index_type == "flat":
            return faiss.IndexFlatL2(self.dimension)
        elif self.index_type == "ivf":
            quantizer = faiss.IndexFlatL2(self.dimension)
            nlist = 100
            return faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
        elif self.index_type == "hnsw":
            return faiss.IndexHNSWFlat(self.dimension, 32)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")

    def add_vectors(self, vectors: np.ndarray) -> None:
        """
        Add vectors to the index.

        Args:
            vectors: Numpy array of shape (n, dimension) containing n vectors to add

        Raises:
            ValueError: If the vectors are not of the expected dimension
        """
        if vectors.shape[1] != self.dimension:
            raise ValueError(f"Expected vectors of dimension {self.dimension}, got {vectors.shape[1]}")

        if self.index_type == "ivf" and not self.index.is_trained:
            self.index.train(vectors)

        self.index.add(vectors.astype(np.float32))

    def search(self, query_vectors: np.ndarray, k: int = 5) -> tuple[np.ndarray, np.ndarray]:
        """
        Search for the k nearest neighbors of the query vectors.

        Args:
            query_vectors: Numpy array of shape (n, dimension) containing query vectors
            k: Number of nearest neighbors to return

        Returns:
            Tuple of (distances, indices) arrays

        Raises:
            ValueError: If the query vectors are not of the expected dimension
        """
        if query_vectors.shape[1] != self.dimension:
            raise ValueError(f"Expected vectors of dimension {self.dimension}, got {query_vectors.shape[1]}")

        distances, indices = self.index.search(query_vectors.astype(np.float32), k)

        return distances, indices

    def save_index(self, filepath: str) -> None:
        """
        Save the FAISS index to disk.

        Args:
            filepath: Path to save the FAISS index to
        """
        faiss.write_index(self.index, filepath)

    def load_index(self, filepath: str) -> None:
        """
        Load a FAISS index from disk.

        Args:
            filepath: Path to load the FAISS index from
        """
        self.index = faiss.read_index(filepath)
