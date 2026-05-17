# AI Usage — GeoMetaAssist

## Design Document

### 1. Project Overview & Key Features
Tool: Claude (claude.ai)
Prompt Goal: Refine the project overview, problem domain, and target audience. Claude also help me draft the list of key features for GeoMetaAssist.
What I Learned: How to frame a SaaS product description clearly, separating problem domain, audience, and feature scope.

### 2. Database Design
Tool: Claude (claude.ai)
Prompt Goal: Help to critically assess the normalization, integrate with the Django user entity, rationale of the entity and relationships, and also making sure my design follow the STAC specification.
What I Learned: DBML syntax, AbstractUser field inheritance in Django, BCNF design principles, and how to model SaaS subscription tiers relationally.

### 3. HTML Mockups
Tool: Claude Code
Prompt Goal: Initialise a Django project and help me build HTML mockups templates for all pages using Bootstrap 5 with realistic placeholder content (mock data).
What I Learned: Django project and app structure, Bootstrap 5 grid and component usage. Claude Code was used heavily to assist with CSS and responsive layout implementation.

### 4. Technology Research
Tool: Claude (claude.ai)
Prompt Goal: Client-side (Turf.js) vs server-side (GeoPandas) GeoJSON metadata extraction across relevant criteria and produce a justified decision for each.
What I Learned: The technical and architectural trade-offs between client-side and server-side extraction.

### 5. Accessibility
Tool: Claude (claude.ai)
Prompt Goal: Criticize the accessibility section, help me assess what 10 most relevant criteria for GeoMetaAssist, and help me map each to a specific UI component with relevant accessibility consideration.
What I Learned: WCAG 2.1 structure, the POUR principles, and how specific criteria such as ARIA live regions, skip links, and colour contrast apply to a real application interface.

### 6. Security
Tool: Claude (claude.ai)
Prompt Goal: Criticize my draft on security key points that I made mostly based on Django docs, and give ideas on what other security consideration other than what Django provides.
What I Learned: Distinction between role-level and object-level permission, HSTS and its role in preventing SSL stripping attacks, and why returning a 404 instead of a 403 on unauthorised object access avoids confirming resource existence to an attacker.

-------

## Code Implementation

### 1. Django Project Setup and Authentication
Tool: Claude
Prompt Goal: Help me init the real Django project with the User model using email as USERNAME_FIELD, then implement register, login, and logout views, and then setup the URL patterns.
What I Learned: We can make a custom user model creation with AbstractUser, and the UserManager override for email-based authentication, I also learn about Django form validation patterns, and session-based authentication flow.

### 2. Soft Deletion
Tool: Claude
Prompt Goal: Give example of how soft deletion is made, and how we can use it instead of hard deletion
What I Learned: Soft delete pattern using is_deleted and deleted_at fields, (archive in subscription)

### 3. User Profile and Settings Page as an Example of how to create a feature end to end
Tool: Claude
Prompt Goal: Help me build the settings page, to help me understand end to end on how to do simple CRUD, and making sure we discuss the best practice in Django
What I Learned: Handling multiple forms on one page, update_session_auth_hash to keep users logged in after a password change, and some good practice in handling CRUD in Django, to help me equip the skills to make the rest of the features

### 4. File upload handling
Tool: Claude
Prompt Goal: Help me Implement GeoJSON file upload with serverside validation (for security), UUID-based storage path, and upload status tracking.
What I Learned: Django FileField and file upload handling, server-side file validation, and Django's MEDIA_ROOT and MEDIA_URL configuration.

### 5. Subscription
Tool: Claude
Prompt Goal: Help me to structure, plan, and build the subscription plans model, and how to enforce the various quota logic
What I Learned:quota enforcement at the view layer, custom decorators for RBAC, and Django's Pagination (for the UI).

### 6. Technical Metadata Extraction
Tool: Claude
Prompt Goal: Help me implement GeoJSON Metadata extraction using geopandas
What I Learned: GeoPandas API for reading GeoJSON files and extracting CRS, bounding box, geometry type, feature count, and attribute schema. Error handling patterns for extraction pipelines.

### 7. STAC Metadata Editor and Export
Tool: Claude
Prompt Goal: Guide me build the metadata editor, especially the client side code (JS), how do we prefill fields based on the AI Suggestion, and how to export/download files
What I Learned: STAC 1.0.0 Item structure including required fields (type, stac_version, id, geometry, bbox, properties, links, assets), datetime handling per spec, and serving file downloads, some 
Client side handling using javascript, and how it wired with the HTML Elements.

### 8. RAG and AI Chatbot
Tool: Claude
Prompt Goal: Help me plan to implement RAG pipeline using LangChain and ChromaDB over the STAC specs documents, with an AI suggestions button and a chatbot panel in the metadata editor
What I Learned: How RAG works from end to end, from ingesting documents to vector store using text-embedding-3-small (provided api), retrieving relevant chunks on each query, and passing those chunks as part of prompot for the gpt-5.4-mini to generate better responses.

### 9. Deployment to UQCloud Zone
Tool: Claude
Prompt Goal: some guidance and help me debug the deployment of the Django app to UQCloud Zone including setup Gunicorn, Nginx, static file collection, and production environment setup.
What I Learned: Gunicorn configuration, Nginx reverse proxy setup for Django, and production security header configuration.

### 10. View, Model, and Template wiring
Tool: Claude
Prompt Goal: I mostly built the UIs based on the mockup design on the first design document submission. In this part, I uses AI to help
me wire up the logics inside views, urls, models, etc to wire it up with the mockup design. 
What I Learned: End to end on how everythings connect in Django, from the first model creation, migration, setting up the urls, forms, admin page, and how it connects with the templates that I have built earlier. 

---

Note: prompts listed above represent the main goal of each interaction. Each section involved multiple follow-up exchanges to refine, correct, and adjust the output before it was incorporated into the project.