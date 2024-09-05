from dataclasses import dataclass
import os
import logging
from llama_index.core.llms import LLM
from llama_cpp import Llama
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.lmstudio import LMStudio

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.text_splitter import CodeSplitter
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer

class _Configuration:

    os.environ['OPENAI_API_KEY'] = "lm-studio"
    _text_splitter: CodeSplitter = CodeSplitter(language="java",chunk_lines=60,chunk_lines_overlap=30,max_chars=2000,)
    # _llm_lmstudio: LLM = LMStudio(
    #                         model_name="SanctumAI/Codestral-22B-v0.1-GGUF", base_url="http://host.docker.internal:1234/v1",
    #                         temperature=0.7,request_timeout=6000.0,)
    # _llm_llamacpp: LLM = LlamaCPP(
    #                         model_path='/mnt/c/Users/PKulkarni4/AppData/Local/nomic.ai/GPT4All/SanctumAI/Codestral-22B-v0.1-GGUF/codestral-22b-v0.1.Q3_K_M.gguf',
    #                         temperature=0.7,max_new_tokens=256,context_window=3900,generate_kwargs={},model_kwargs={},verbose=True,)
    _llm: LLM = None
    _use_llamacpp = False
    _embed_model: HuggingFaceEmbedding = HuggingFaceEmbedding(model_name = "neulab/codebert-java", device="cpu")
    _vector_store = PGVectorStore = PGVectorStore.from_params(
        database="postgres",
        host="localhost",
        password="postgres",
        port=5432,
        user="postgres",
        table_name="javacode_embeddings",
        embed_dim=768,  # Ensure this matches your model's output dimensions        
    )
    _code_splitter = CodeSplitter = CodeSplitter(
        language="java",chunk_lines=64,chunk_lines_overlap=32,max_chars=2048,)
    _input_directory = str = "/home/pkulkarni4/work/code/cds/cds-information-model-service-main/cds-information-model-service/src/main/java"
    _chat_mode="condense_plus_context"
    _context_prompt=(
        "You are an expert Java developer. "
        "You will be asked to generate code based on existing java files, that are already embedded."
        "You need to generate concise and complete code with full logic implementation for every generated method."
        "You need to use existing embedded classes and methods as much as possible. Here are the relevant code snippets for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    )
    _memory = ChatMemoryBuffer = ChatMemoryBuffer.from_defaults(token_limit=3900)

    @property
    def memory(self) -> ChatMemoryBuffer:
        return self._memory

    @memory.setter
    def memory(self, memory: ChatMemoryBuffer) -> None:
        self._memory = memory     


    @property
    def context_prompt(self) -> str:
        return self._context_prompt

    @context_prompt.setter
    def context_prompt(self, context_prompt: str) -> None:
        self._context_prompt = context_prompt     

    @property
    def chat_mode(self) -> str:
        return self._chat_mode

    @chat_mode.setter
    def chat_mode(self, chat_mode: str) -> None:
        self._chat_mode = chat_mode     

    @property
    def input_directory(self) -> str:
        return self._input_directory

    @input_directory.setter
    def input_directory(self, input_directory: str) -> None:
        self._input_directory = input_directory     

    @property
    def code_splitter(self) -> CodeSplitter:
        return self._code_splitter

    @code_splitter.setter
    def code_splitter(self, code_splitter: CodeSplitter) -> None:
        self._code_splitter = code_splitter     


    @property
    def embed_model(self) -> HuggingFaceEmbedding:
        return self._embed_model

    @embed_model.setter
    def embed_model(self, embed_model: HuggingFaceEmbedding) -> None:
        self._embed_model = embed_model     

    @property
    def vector_store(self) -> PGVectorStore:
        return self._vector_store

    @vector_store.setter
    def vector_store(self, vector_store: PGVectorStore) -> None:
        self._vector_store = vector_store     

    @property
    def llm(self) -> LLM:
        if self._llm is not None:
            return self._llm
        if self._use_llamacpp == True:
            self._llm = LlamaCPP(
                model_path='/mnt/c/Users/PKulkarni4/AppData/Local/nomic.ai/GPT4All/SanctumAI/Codestral-22B-v0.1-GGUF/codestral-22b-v0.1.Q3_K_M.gguf',
                temperature=0.7,max_new_tokens=256,context_window=3900,generate_kwargs={},model_kwargs={},verbose=True,)
        else:
            self._llm = LMStudio(
                model_name="bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF", base_url="http://host.docker.internal:1234/v1",
                temperature=0.7,request_timeout=6000.0,)
        return self._llm

    @llm.setter
    def llm(self, llm: LLM) -> None:
        self._llm = llm    

#Singleton
Configuration = _Configuration()