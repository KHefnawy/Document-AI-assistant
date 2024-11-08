from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from global_settings import INDEX_STORAGE
from document_uploader import ingest_documents

# Purpose: Creates a searchable vector index from processed documents
# Components:
#   - build_indexes(): Creates/loads vector index
#   - Storage handling: Persists index for future use
#   - Error handling: Manages index loading failures
def build_indexes(nodes):
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
    vector_index = load_index_from_storage(storage_context, index_id="vector")    
    if vector_index is not None:
        vector_index.insert_nodes(nodes)
    else:
        # If no existing vector index, create a new one
        storage_context = StorageContext.from_defaults()
        
        vector_index = VectorStoreIndex(
            nodes, 
            storage_context=storage_context,
            show_progress=True
        )
        vector_index.set_index_id("vector")

    # Persist the updated/new vector index
    storage_context.persist(
        persist_dir=INDEX_STORAGE
    )
    
    return vector_index
