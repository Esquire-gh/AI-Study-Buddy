import pickle
from pathlib import Path
from django.db import models
from django.contrib.auth import get_user_model

from langchain_community.document_loaders import PyPDFLoader
from chat.utils.helpers import get_openai_embeddings, download_file


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    canvas_api_token = models.CharField(max_length=200)


class Course(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    external_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    external_id = models.CharField(unique=False, max_length=20)
    name = models.CharField(max_length=300)
    url = models.URLField()
    pages = models.BinaryField(blank=True, null=True)

    def generate_pages(self):
        if not self.pages:
            file_path = download_file(self.url, self.name)
                
            if Path(file_path).exists():
                loader = PyPDFLoader(file_path, extract_images=True)
                pages = loader.load_and_split()
                self.pages = pickle.dumps(pages)
                self.save(update_fields=['pages'])

    def get_pages(self):
        if self.pages:
            return pickle.loads(self.pages)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    vector_index = models.BinaryField(null=True, blank=True)

    def _create_vector_from_docs(self, documents):
        from langchain_community.vectorstores import FAISS

        return FAISS.from_documents(documents, get_openai_embeddings())

    def create_new_index(self, documents):
        v_index = self._create_vector_from_docs(documents)
        self.vector_index = v_index.serialize_to_bytes()

    def get_vector_index(self):
        from langchain_community.vectorstores import FAISS

        if not self.vector_index:
            return
        
        v_index = FAISS.deserialize_from_bytes(embeddings=get_openai_embeddings(), serialized=self.vector_index)
        return v_index
    
    def udpate_index(self, new_docs):
        new_index = self._create_vector_from_docs(new_docs)

        old_index = self.get_vector_index()

        combined_index = old_index.merge_from(new_index)
        self.vector_index = combined_index
        self.save(udpate_fields=['vector_index'])
        return self.vector_index
    
    def build_index_with_course_files(self, files: list[CourseFile], overwrite=False):
        documents = []
        for course_file in files:
            pages = course_file.get_pages()
            if isinstance(pages, list):
                documents.extend(pages)
            else:
                documents.append(pages)
            
        if not self.vector_index or overwrite:
            self.create_new_index(documents)
        else:
            self.udpate_index(documents)
        
        self.refresh_from_db()
        return self.vector_index


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.CharField(max_length=50000)  # max_length also dictates the limit for tokens in a message
    is_human = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.text

