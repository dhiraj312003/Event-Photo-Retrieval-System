import numpy as np
import pickle
import os
import sys

class FaceDatabase:
    def __init__(self, embedding_dim=512):
        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata = []
        
        # Try to import FAISS
        try:
            import faiss
            self.faiss = faiss
            self.index = faiss.IndexFlatIP(embedding_dim)
            print("FAISS initialized successfully")
        except ImportError:
            self.faiss = None
            print("Warning: FAISS not available. Using simple cosine similarity.")
    
    def add_embeddings(self, embeddings, image_path, boxes):
        """Add face embeddings to database"""
        try:
            if len(embeddings) == 0:
                return
            
            # Ensure embeddings is 2D array
            if len(embeddings.shape) == 1:
                embeddings = embeddings.reshape(1, -1)
            
            # Normalize embeddings for cosine similarity
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1  # Avoid division by zero
            embeddings_normalized = embeddings / norms
            
            # Add to FAISS index if available
            if self.faiss is not None and self.index is not None:
                self.index.add(embeddings_normalized.astype('float32'))
            
            # Store metadata
            start_idx = len(self.metadata)
            for i in range(len(embeddings)):
                metadata_entry = {
                    'image_path': image_path,
                    'box': boxes[i] if i < len(boxes) else None,
                    'embedding': embeddings_normalized[i] if self.faiss is None else None,
                    'embedding_id': start_idx + i
                }
                self.metadata.append(metadata_entry)
                
        except Exception as e:
            print(f"Error adding embeddings: {str(e)}")
    
    def search(self, query_embedding, k=10, threshold=0.6):
        """Search for similar faces"""
        try:
            # Normalize query embedding
            query_norm = np.linalg.norm(query_embedding)
            if query_norm == 0:
                return []
            
            query_normalized = query_embedding / query_norm
            query_normalized = query_normalized.reshape(1, -1).astype('float32')
            
            results = []
            
            # Use FAISS if available
            if self.faiss is not None and self.index is not None:
                distances, indices = self.index.search(query_normalized, min(k, len(self.metadata)))
                
                for i in range(len(indices[0])):
                    idx = indices[0][i]
                    distance = distances[0][i]
                    
                    if distance >= threshold and idx < len(self.metadata):
                        metadata = self.metadata[idx].copy()
                        metadata['similarity'] = float(distance)
                        results.append(metadata)
            
            # Fallback: simple cosine similarity
            else:
                for metadata in self.metadata:
                    if metadata['embedding'] is not None:
                        # Calculate cosine similarity
                        similarity = np.dot(query_normalized.flatten(), metadata['embedding'])
                        
                        if similarity >= threshold:
                            result = metadata.copy()
                            result['similarity'] = float(similarity)
                            results.append(result)
                
                # Sort by similarity
                results.sort(key=lambda x: x['similarity'], reverse=True)
                results = results[:k]
            
            return results
            
        except Exception as e:
            print(f"Error in search: {str(e)}")
            return []
    
    def save(self, index_path, metadata_path):
        """Save database to disk"""
        try:
            # Save FAISS index
            if self.faiss is not None and self.index is not None:
                self.faiss.write_index(self.index, index_path)
            
            # Save metadata
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            print(f"Database saved to {index_path} and {metadata_path}")
            
        except Exception as e:
            print(f"Error saving database: {str(e)}")
    
    def load(self, index_path, metadata_path):
        """Load database from disk"""
        try:
            # Load FAISS index
            if self.faiss is not None and os.path.exists(index_path):
                self.index = self.faiss.read_index(index_path)
            
            # Load metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                
                print(f"Database loaded: {len(self.metadata)} faces")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error loading database: {str(e)}")
            return False
    
    def __len__(self):
        return len(self.metadata)