# AI Usage — GeoMetaAssist

## Tools Used
- **Claude (claude.ai)** — design document drafting, architecture planning, code review, deployment guidance
- **Claude Code** — code generation, CSS and responsive layout implementation

---

## Usage Log

### 1. Project Overview & Key Features
**Tool:** Claude (claude.ai)
**Prompt goal:** Draft the project overview, problem domain, target audience, and key features for GeoMetaAssist.
**What I learned:** How to frame a SaaS product description clearly, separating problem domain, audience, and feature scope.

---

### 2. Database Schema Design
**Tool:** Claude (claude.ai)
**Prompt goal:** Design a normalised database schema in DBML for a Django SaaS application supporting users, subscriptions, projects, GeoJSON uploads, metadata, and AI chat sessions.
**What I learned:** DBML syntax, AbstractUser field inheritance in Django, BCNF design principles, surrogate key patterns, and how to model SaaS subscription tiers relationally.

---

### 3. HTML Mockups
**Tool:** Claude Code
**Prompt goal:** Initialise a Django project and generate HTML mockup templates for all pages using Bootstrap 5 with a white and dark green colour scheme and sidebar navigation layout.
**What I learned:** Django project and app structure, Bootstrap 5 grid and component usage. HTML structure was written manually; Claude Code was used to assist with CSS and responsive layout implementation.

---

### 4. Technology Research
**Tool:** Claude (claude.ai)
**Prompt goal:** Compare STAC 1.0.0 vs ISO 19115 and client-side (Turf.js) vs server-side (GeoPandas) GeoJSON metadata extraction and produce a justified decision for each.
**What I learned:** The technical and architectural trade-offs between client-side and server-side extraction, and the differences between STAC and ISO 19115 in a web-native SaaS context.

---

### 5. Accessibility Section
**Tool:** Claude (claude.ai)
**Prompt goal:** Draft the WCAG 2.1 Level AA accessibility section, select the 10 most relevant criteria for GeoMetaAssist, and map each to a specific UI component with an implementation approach.
**What I learned:** WCAG 2.1 structure, the POUR principles, and how specific criteria such as ARIA live regions, skip links, and colour contrast apply to a real application interface.

---

### 6. Security Section
**Tool:** Claude (claude.ai)
**Prompt goal:** Draft the security section covering authentication, RBAC with three user roles, object-level permission enforcement, CSRF, XSS, SQL injection, file upload security, and production security headers.
**What I learned:** Web application security concepts including brute-force protection strategies, the distinction between role-level and object-level permission enforcement, HSTS and SSL stripping prevention, and why returning 404 instead of 403 on unauthorised access avoids confirming resource existence.

---

### 7. Django Project Setup and Authentication
**Tool:** Claude Code
**Prompt goal:** Initialise the real Django project with the custom User model using email as USERNAME_FIELD, implement register, login, and logout views, and wire up all URL patterns.
**What I learned:** Custom user model creation with AbstractUser, UserManager override for email-based authentication, Django form validation patterns, and session-based authentication flow.

---

### 8. Geo Data Projects CRUD
**Tool:** Claude Code
**Prompt goal:** Create the projects app with GeoDataProject model, implement full CRUD views with soft delete and object-level ownership enforcement.
**What I learned:** Soft delete pattern using is_deleted and deleted_at fields, object-level ownership enforcement using get_object_or_404 with user filter, and why 404 is preferable to 403 for unauthorised object access.

---

### 9. User Profile and Settings Page
**Tool:** Claude Code
**Prompt goal:** Build a settings page where users can update their name and change their password, with two separate forms on the same page.
**What I learned:** Handling multiple forms on one page using a hidden action field, update_session_auth_hash to keep users logged in after a password change, and Django's built-in password validation.

---

### 10. GeoJSON File Upload
**Tool:** Claude Code
**Prompt goal:** Implement GeoJSON file upload with server-side validation (extension, MIME type, size), UUID-based storage path, and upload status tracking.
**What I learned:** Django FileField and file upload handling, server-side file validation, UUID-based filename generation to prevent path traversal, and Django's MEDIA_ROOT and MEDIA_URL configuration.

---

### 11. Subscription Model and Staff Portal
**Tool:** Claude Code
**Prompt goal:** Build the subscription plans model, auto-assign Free plan on registration, implement quota enforcement, and create a custom staff portal for managing subscriptions.
**What I learned:** Data migrations for seeding default records, quota enforcement at the view layer, custom decorators for role-based access control, and Django's Paginator class.

---

### 12. Technical Metadata Extraction
**Tool:** Claude Code
**Prompt goal:** Implement automatic GeoJSON metadata extraction using GeoPandas, triggered synchronously after upload, saving results to ExtractedTechnicalMetadata.
**What I learned:** GeoPandas API for reading GeoJSON files and extracting CRS, bounding box, geometry type, feature count, and attribute schema. Error handling patterns for extraction pipelines.

---

### 13. STAC Metadata Editor and Export
**Tool:** Claude Code
**Prompt goal:** Build the metadata editor form with STAC field groups, assemble the full STAC 1.0.0 Item JSON from form data and extracted metadata, and implement export and download.
**What I learned:** STAC 1.0.0 Item structure including required fields (type, stac_version, id, geometry, bbox, properties, links, assets), datetime handling per spec, and serving file downloads via HttpResponse with Content-Disposition header.

---

### 14. RAG Pipeline and AI Chatbot
**Tool:** Claude Code
**Prompt goal:** Implement a RAG pipeline using LangChain and ChromaDB over the STAC specification markdown files, with an AI suggestions button and a chatbot panel in the metadata editor.
**What I learned:** How RAG works: ingesting documents into a vector store using text-embedding-3-small, retrieving relevant chunks via semantic similarity search on each query, and passing those chunks as context to gpt-5.4-mini to generate grounded responses. The distinction between the embedding model (retrieval) and the chat model (generation).

---

### 15. Deployment to UQCloud Zone
**Tool:** Claude (claude.ai)
**Prompt goal:** Guide step-by-step deployment of the Django app to UQCloud Zone including Gunicorn systemd service, Nginx reverse proxy configuration, static file collection, and production environment setup.
**What I learned:** Gunicorn systemd service configuration, Nginx reverse proxy setup for Django, the role of SECURE_PROXY_SSL_HEADER on a load-balanced server, why SECURE_SSL_REDIRECT must not be set on UQCloud Zone, and production security header configuration.

---

*Note: prompts listed above represent the main goal of each interaction. Each section involved multiple follow-up exchanges to refine, correct, and adjust the output before it was incorporated into the project.*