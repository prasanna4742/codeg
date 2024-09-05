from config import Configuration
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.postprocessor  import MetadataReplacementPostProcessor

def main():
    print(f"Generating the code - start")
    chat_engine = CodeGenerator.get_chat_engine()
    while True:
        question = input("Enter your request (or 'exit()' to quit, reset() to start new conversation): ")
        if question.lower() == "exit()":
            break
        if question.lower() == "reset()":
            chat_engine.reset()
        streaming_response = chat_engine.stream_chat(question)
        for token in streaming_response.response_gen:
            print(token, end="")
        # response = chat_engine.chat(question)
        # print(f"CodeGenerator Response is as below:\n{response}")
    # chat_engine.chat_repl()
    print(f"Generating the code - end")

class CodeGenerator:
    @staticmethod
    def get_chat_engine():
        index = VectorStoreIndex.from_vector_store(vector_store=Configuration.vector_store,embed_model=Configuration.embed_model)
        query_engine = index.as_query_engine(llm=Configuration.llm,similarity_top_k=5,
                node_postprocessors=[
                # rerank,
                MetadataReplacementPostProcessor(target_metadata_key="window")
            ],
            vector_store_kwargs={"ivfflat_probes": 10},
)
        chat_engine = index.as_chat_engine(
            query_engine=query_engine,
            chat_mode=Configuration.chat_mode,
            memory=Configuration.memory,
            llm=Configuration.llm,
            context_prompt= Configuration.context_prompt,
            verbose=True,
            similarity_top_k=5,
            streaming=True,
            response_mode="refine",)
        return chat_engine

if __name__ == "__main__":
    main()