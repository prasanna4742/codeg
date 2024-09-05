from config import Configuration
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext

def main():
    print(f"Indexing the code - start")
    CodeIndexer.create_and_store_embeddings()
    print(f"Indexing the code - end")

class CodeIndexer:
    @staticmethod
    def create_and_store_embeddings():
        storage_context = StorageContext.from_defaults(vector_store=Configuration.vector_store)
        required_exts = [".java"]
        documents = SimpleDirectoryReader(input_dir=Configuration.input_directory, recursive=True, required_exts=required_exts).load_data()            
        nodes = Configuration.code_splitter.get_nodes_from_documents(documents)
        index = VectorStoreIndex(nodes, storage_context=storage_context,embed_model=Configuration.embed_model)
        print(f"Embeddings for all .java files from {Configuration.input_directory} created, VectorStoreIndex={index}")

if __name__ == "__main__":
    main()