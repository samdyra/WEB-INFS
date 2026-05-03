import json

from django.conf import settings


def _check_api_key():
    if not settings.OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY is not configured.')


def get_vectorstore():
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        openai_api_key=settings.OPENAI_API_KEY,
    )
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
    )


def get_llm():
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model="gpt-5.4-mini",
        temperature=0.3,
        openai_api_key=settings.OPENAI_API_KEY,
    )


def generate_suggestions(extracted_metadata):
    """
    Given a dict of extracted technical metadata, return AI-suggested
    title, description, and keywords as a dict.
    """
    _check_api_key()

    vectorstore = get_vectorstore()
    llm = get_llm()

    attr_names = [
        a['name'] for a in extracted_metadata.get('attribute_schema', [])
    ]

    context = (
        f"GeoJSON dataset details:\n"
        f"- CRS: {extracted_metadata.get('crs_epsg', 'Unknown')}\n"
        f"- Geometry type: {extracted_metadata.get('geometry_type', 'Unknown')}\n"
        f"- Feature count: {extracted_metadata.get('feature_count', 'Unknown')}\n"
        f"- Attribute names: {', '.join(attr_names)}\n"
        f"- Bounding box: {extracted_metadata.get('bbox_display', 'Unknown')}\n"
    )

    docs = vectorstore.similarity_search(
        'title description keywords metadata fields STAC item', k=4,
    )
    spec_context = '\n\n'.join([d.page_content for d in docs])

    prompt = f"""
You are a geospatial metadata expert helping fill in STAC 1.0.0
metadata fields.

STAC specification context:
{spec_context}

Dataset information:
{context}

Based on the dataset attribute names and characteristics, suggest:
1. A concise descriptive title (max 10 words)
2. A clear description (2-3 sentences) explaining what the dataset
   contains and its likely purpose
3. 3-5 relevant keywords as a list
4. A license code, chosen from exactly one of:
   CC-BY-4.0, CC-BY-SA-4.0, CC0-1.0, OGL-Australia, proprietary, other.
   If unsure, use "proprietary".
5. A providers array of 1-2 plausible STAC provider objects with
   "name" and "roles" (roles from: producer, licensor, processor, host).
   If you cannot make a reasonable guess from the dataset hints,
   return an empty array.
6. A links array of 0-2 plausible STAC link objects with "href",
   "rel", and "title". Only include a link if you have strong context
   for a real URL. Otherwise return an empty array.

Respond in this exact JSON format with no extra text or markdown:
{{
  "title": "...",
  "description": "...",
  "keywords": ["...", "...", "..."],
  "license": "...",
  "providers": [{{"name": "...", "roles": ["producer"]}}],
  "links": [{{"href": "...", "rel": "...", "title": "..."}}]
}}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    return json.loads(content.strip())


def chat_with_rag(message, conversation_history, metadata_context):
    """
    Answer a user question grounded in the STAC spec, with the current
    metadata draft and recent conversation history as context.
    """
    _check_api_key()

    vectorstore = get_vectorstore()
    llm = get_llm()

    docs = vectorstore.similarity_search(message, k=4)
    spec_context = '\n\n'.join([d.page_content for d in docs])

    history_str = ''
    for msg in conversation_history[-6:]:
        role = 'User' if msg.get('role') == 'user' else 'Assistant'
        history_str += f"{role}: {msg.get('content', '')}\n"

    meta_str = '\n'.join(
        f'- {k}: {v}' for k, v in metadata_context.items() if v
    )

    prompt = f"""
You are a geospatial metadata assistant helping a user complete
STAC 1.0.0 metadata fields. Answer questions clearly and concisely,
referencing the STAC specification where relevant. If the user asks
about a specific field, explain what it means, why it matters, and
give a practical example relevant to their dataset.

STAC specification context:
{spec_context}

Current metadata being edited:
{meta_str if meta_str else 'No fields filled in yet.'}

Conversation history:
{history_str if history_str else 'No previous messages.'}

User: {message}

Assistant: """

    response = llm.invoke(prompt)
    return response.content.strip()
