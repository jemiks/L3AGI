from pathlib import Path
from typing import List
from pathlib import Path
import time
from uuid import uuid4
from llama_index import SummaryIndex, SimpleDirectoryReader, ServiceContext
from llama_index import load_index_from_storage, StorageContext
from llama_index.llms import LangChainLLM
from langchain.chat_models import ChatOpenAI
from services.aws_s3 import AWSS3Service
from typings.config import AccountSettings

class FileDatasourceRetriever:
    datasource_id = None
    index: SummaryIndex
    index_path: Path = Path("tmp/index")
    datasource_path: Path
    service_context: ServiceContext

    def __init__(self, settings: AccountSettings, datasource_id: str) -> None:
        self.datasource_id = datasource_id
        self.datasource_path = Path(f"tmp/datasources/{self.datasource_id}")

        llm = LangChainLLM(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=settings.openai_api_key))
        self.service_context = ServiceContext.from_defaults(llm=llm)

    def save_documents(self, file_urls: List[str]):
        self.datasource_path.mkdir(parents=True, exist_ok=True)

        for file_url in file_urls:
            key = AWSS3Service.get_key_from_public_url(file_url)
            _, ext = key.rsplit('.', 1)
            name = f"{uuid4()}.{ext}"
            absolute_path = self.datasource_path.joinpath(name).resolve()
            AWSS3Service.download_file(key, absolute_path)


    def load_documents(self):
        try:
            storage_context = StorageContext.from_defaults(persist_dir=self.index_path)
            self.index = load_index_from_storage(storage_context, self.datasource_id)
        except (ValueError, FileNotFoundError):
            documents = SimpleDirectoryReader(self.datasource_path.resolve()).load_data()
            self.index = SummaryIndex.from_documents(documents, service_context=self.service_context)
            self.index.set_index_id(self.datasource_id)
            self.index.storage_context.persist(persist_dir=self.index_path)
        
    def query(self, query_str):
        query_engine = self.index.as_query_engine(response_mode="tree_summarize", service_context=self.service_context)
        result = query_engine.query(query_str)
        return result
    