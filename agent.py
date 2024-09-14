from abc import ABC, abstractmethod
import os
import yaml
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#import sys
#sys.path.append("/data/aisvc_data/NLP/flo/codes/LLM/gemma_sprint/module")
from prompts import *
from langchain_community.llms import LlamaCpp


class Agent(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def summarize(self, content: str) -> str:
        # Implement the logic to summarize the content
        pass


class Gemma(Agent):
    def __init__(self, project_name, model_path, n_batch=8192, n_ctx=8192, n_threads=16, temperature=0):
        super().__init__(model_name=model_path)
        os.environ["LANGCHAIN_TRAICING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = "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"
        os.environ["LANGCHAIN_PROJECT"] = project_name

        self.prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
        
        self.client = LlamaCpp(
            model_path=self.model_name,
            n_threads=n_threads,
            n_batch=n_batch,
            n_ctx=n_ctx,
            n_gpu_layers=-1,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            verbose=True,
            f16_kv=True,
            temperature=temperature,
            top_p=0.9,
            top_k=50
        )

    def summarize(self, article):
        chain = self.prompt | self.client | StrOutputParser()
        result = chain.invoke({'article':article})

        return result