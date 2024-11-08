# Purpose: Handles document ingestion and initial processing
# Components:
#   - ingest_documents(): Reads and processes uploaded files
#   - Pipeline steps:
#     1. Document loading
#     2. Text splitting
#     3. Embedding generation
from global_settings import STORAGE_PATH, INDEX_STORAGE, CACHE_FILE
from logging_functions import log_action
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
import os
def ingest_documents():
    documents = SimpleDirectoryReader(
        STORAGE_PATH, 
        filename_as_id = True
    ).load_data()
    for doc in documents:
        print(doc.id_)
        log_action(
            f"File '{doc.id_}' uploaded user", 
            action_type="UPLOAD"
        )
    
    if os.path.exists(CACHE_FILE):
        cached_hashes = IngestionCache.from_persist_path(CACHE_FILE)
    else:
        cached_hashes = ""

    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=1024, 
                chunk_overlap=20
            ),
            OpenAIEmbedding()
        ],
        cache=cached_hashes
    )
   
    nodes = pipeline.run(documents=documents)
    pipeline.cache.persist(CACHE_FILE)
    
    return nodes
 