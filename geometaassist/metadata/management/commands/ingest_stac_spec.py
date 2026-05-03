import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ingest STAC spec markdown files into ChromaDB vector store'

    def handle(self, *args, **options):
        from langchain_community.document_loaders import TextLoader
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        if not settings.OPENAI_API_KEY:
            self.stderr.write(self.style.ERROR(
                'OPENAI_API_KEY is not set. Add it to .env before running this command.'
            ))
            return

        spec_dir = os.path.join(settings.BASE_DIR, 'rag')
        persist_dir = settings.CHROMA_PERSIST_DIR

        if not os.path.exists(spec_dir):
            self.stderr.write(self.style.ERROR(
                f'rag/ directory not found at {spec_dir}. '
                'Place STAC spec markdown files (e.g. item-spec.md, '
                'common-metadata.md) inside rag/ first.'
            ))
            return

        md_files = [
            p for p in glob.glob(os.path.join(spec_dir, '**', '*.md'), recursive=True)
            if os.path.abspath(persist_dir) not in os.path.abspath(p)
        ]

        if not md_files:
            self.stderr.write(self.style.ERROR(
                'No .md files found under rag/. Check the directory contents.'
            ))
            return

        self.stdout.write(f'Found {len(md_files)} markdown files. Loading...')

        docs = []
        for path in md_files:
            try:
                loader = TextLoader(path, encoding='utf-8')
                docs.extend(loader.load())
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipping {path}: {e}'))

        self.stdout.write(f'Loaded {len(docs)} documents. Splitting...')

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        self.stdout.write(f'Created {len(chunks)} chunks. Embedding and storing...')

        embeddings = OpenAIEmbeddings(
            model='text-embedding-3-small',
            openai_api_key=settings.OPENAI_API_KEY,
        )

        os.makedirs(persist_dir, exist_ok=True)

        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir,
        )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully ingested {len(chunks)} chunks into ChromaDB at {persist_dir}'
        ))
