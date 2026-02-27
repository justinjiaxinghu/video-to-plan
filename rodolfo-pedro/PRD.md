# Product Requirements Document (PRD): **DealDesk** — AI-Assisted Real Estate Deal Evaluation (Financial + Zoning)

## 1) Executive Summary

Small-to-mid sized real estate developers and analysts like Rodolfo Guerra spend significant time manually extracting data from Offering Memorandums (PDFs), researching market benchmarks in ChatGPT, and copying inputs into Excel models to decide whether a deal is worth pursuing. This fragmented workflow (Excel + Adobe Acrobat + ChatGPT) creates avoidable delays, errors, and limits deal throughput. Rodolfo explicitly calls out the pain: “All this is manual input” (00:09:52) and reiterates the copy/paste bridge between tools (00:16:04–00:16:06, 00:45:15–00:45:21).

**DealDesk** is a web platform (with Excel integration) that ingests an OM PDF, extracts key deal and market data into a structured “Back of the Envelope” model, generates AI-suggested underwriting assumptions (rent, vacancy, opex ratio, cap rate) for a given address/property type, and optionally overlays zoning constraints. The product’s core value proposition is to reduce the “back of the envelope” analysis from **3–4 hours** (00:26:31–00:26:35) to **<30 minutes**, while preserving the analyst’s control via an iterative, editable proforma workflow (“AI provides the first curve, then human adjusts” (00:35:38–00:36:16)).

Initial target users are developers/analysts who already live in Excel and evaluate multiple deals weekly (Rodolfo: **2–3 per week** (00:37:23); other firms up to **10 per week** (00:36:46)). DealDesk focuses on automating the highest-friction steps: document extraction, benchmark generation, and structured model population—without forcing users to abandon Excel.

---

## 2) Problem Statement

### Problem A — Manual extraction + manual input into models (Critical)
Rodolfo’s underwriting workflow requires reading PDFs and manually transferring values into Excel models with many “blue” input cells (visual evidence 09:37–14:02). He states plainly:  
- “**All this is manual input**” (00:09:52)  
- “You download this building, you look, and then you put this data… **all of this manually**.” (00:16:04–00:16:06)

**Impact**
- High time cost and cognitive load
- High risk of transcription errors (wrong rent, wrong cap rate, wrong occupancy)
- Limits deal throughput and slows time-to-decision

### Problem B — Time-to-answer is too slow for early-stage screening (High)
Rodolfo distinguishes between:
- Quick screening: “I don’t want to spend more than **3, 4 hours** doing this thing” (00:26:31–00:26:35)
- Full proforma: “This thing takes easily **a week**” (00:18:39) and “**1, 2 weeks**” (00:26:55–00:27:00)

**Impact**
- Fewer deals evaluated
- Missed opportunities due to slow response time
- Analysts spend time on mechanics rather than judgment

### Problem C — Fragmented workflow across multiple tools (High)
Observed tool switching:
- Excel (09:37)
- Adobe Acrobat (14:02)
- ChatGPT (19:21)

Pedro highlights the inefficiency:  
- “You accessed the GPT chat and then you took this information and put it on the other side.” (00:44:43–00:44:46)  
- “Making this bridge of not leaving a screen, putting it in the GPT chat, copying and returning.” (00:45:15–00:45:21)

**Impact**
- Context switching overhead
- Hard to audit where assumptions came from
- No single “source of truth” for deal inputs

### Problem D — Market data access is expensive and uneven (Medium)
CoStar is described as a “giant company that captures a lot of data” (00:07:34) but is costly: “worth **$2,000 a month**” (00:32:31–00:32:37). Many small developers don’t have access.

**Impact**
- Smaller firms rely on broker OMs or ad-hoc research
- Benchmark quality varies
- Competitive disadvantage vs. larger firms

### Problem E — Underwriting requires “art” + experience; users need guided benchmarks (Medium)
Rodolfo: “You still need a lot of time in the industry… you need to know what you’re doing to underwrite a project.” (00:40:15–00:40:25)  
He uses ChatGPT to get baseline assumptions for unfamiliar property types (office vs multifamily) (19:21–21:33).

**Impact**
- Inconsistent assumptions across analysts
- Harder onboarding for junior analysts
- Increased variance in deal decisions

### Problem F — Zoning complexity blocks feasibility analysis (Medium)
Rodolfo: “Each city has a different zoning code… 60 different types of zones… different restrictions.” (00:41:53–00:42:32)  
He explicitly wants a product that “mixes financial modeling with the zoning part” (00:43:31–00:43:48).

**Impact**
- Feasibility risk discovered late
- Reliance on zoning attorneys (00:42:55)
- Missed constraints (setbacks, FAR, use restrictions)

---

## 3) User Personas

### Persona 1: Rodolfo Guerra — Developer / Underwriter (Primary)
**Role:** Real estate developer responsible for evaluating projects, underwriting, and investment decisions.  
**Goals**
- Screen more deals faster without sacrificing quality
- Build credible assumptions quickly (rent, vacancy, opex, cap rate)
- Reduce manual input and focus on judgment and negotiation

**Frustrations**
- Manual copy/paste from PDFs into Excel (“All this is manual input” 00:09:52)
- Switching between tools (Excel/PDF/ChatGPT) (09:37, 14:02, 19:21)
- Market data access constraints (CoStar cost $2k/mo) (00:32:31–00:32:37)
- Zoning complexity and lack of integrated tooling (00:43:31–00:43:48)

**Technical proficiency**
- Advanced Excel user (multi-tab proformas; structured input cells) (09:37–14:02)
- Comfortable using ChatGPT for benchmarks (19:21–21:33)

**Day-in-the-life scenario**
1. Receives OM PDF from broker (Cushman & Wakefield) (14:02–16:27)
2. Skims market tables (submarket rent/occupancy, comps)
3. Opens Excel “Back of the Envelope” model and begins manual entry (26:16–28:49)
4. Uses ChatGPT to fill knowledge gaps (office underwriting benchmarks) (19:21–21:33)
5. Iterates assumptions until a go/no-go decision (e.g., identifies $11M loss scenario) (00:28:35–00:28:44)

---

### Persona 2: Pedro Judice — AI/Tech Specialist (Secondary / Buyer-Influencer)
**Role:** Technical partner exploring AI automation opportunities in real estate workflows.  
**Goals**
- Build an AI-driven system that “bridges the gap” between intelligence and execution (00:45:07–00:45:21)
- Reduce manual steps and integrate into real workflows (Excel-centric)

**Frustrations**
- AI exists but isn’t operationalized into the user’s workflow
- Copy/paste loops prevent scale adoption (00:45:15–00:45:21)

**Technical proficiency**
- Highly technical; AI model training and evaluation experience

**Day-in-the-life scenario**
1. Observes underwriting workflow and identifies automation points
2. Prototypes extraction + structured outputs
3. Validates with users that outputs map to Excel inputs and decision points

---

### Persona 3: Henrique Cordeiro Guerra — Facilitator / Investor (Tertiary)
**Role:** Connector between real estate and technology; potential sponsor/champion.  
**Goals**
- Enable more efficient deal evaluation
- Identify tech leverage points for investment advantage

**Frustrations**
- Implicit: slow, manual processes reduce competitiveness

**Technical proficiency**
- Moderate; understands value but not hands-on

**Day-in-the-life scenario**
1. Introduces stakeholders
2. Helps validate product-market fit with other investors/developers
3. Supports rollout and adoption

---

## 4) Current Workflow (Step-by-Step) + Friction Points

### Workflow 1: Preliminary Deal Evaluation (“Back of the Envelope”) — 3–4 hours
**Inputs:** OM PDF, address/location, property type, broker assumptions  
**Tools:** Adobe Acrobat, ChatGPT, Excel  
**Steps**
1. **Receive OM PDF** from broker (Cushman & Wakefield) (14:02–16:27)  
   - *Friction:* Unstructured PDF; tables vary by broker/template
2. **Review OM market tables** (land comps, office submarket breakdown: rent, occupancy) (14:02–16:27)  
   - *Friction:* Manual reading; hard to compare across deals
3. **Open Excel “Back of the Envelope”** model and start filling blue input cells (26:16–28:49)  
   - *Friction:* Manual transcription; error-prone
4. **Use ChatGPT for benchmarks** (rent/sf/yr, vacancy, opex ratio, cap rate) for location/property type (19:21–21:33)  
   - *Friction:* Prompting skill required; uncertain provenance; manual copy into Excel
5. **Compute valuation vs costs** and decide go/no-go (example: $50M valuation vs $60M cost → $11M loss) (00:28:35–00:28:44)  
   - *Friction:* Assumptions not traceable; hard to audit later

### Workflow 2: Detailed Financial Modeling (Full Proforma) — 1–2 weeks
**Inputs:** comps, rent rolls, financing terms, development budget, absorption, exit assumptions  
**Tools:** Excel, CoStar (direct or via OM), public records  
**Steps**
1. Gather comps and market data (CoStar) (00:07:24–00:08:22)  
   - *Friction:* Access cost ($2k/mo) (00:32:31–00:32:37)
2. Populate complex Excel proforma tabs (SUMMARY, INPUTS, RENT ANALYSIS, BUDGET, MONTHLY SCHEDULE, ANNUAL PROFORMA) (09:37–14:02)  
   - *Friction:* Heavy manual input; iterative changes ripple across tabs
3. Validate assumptions against OM tables and other sources (00:24:48–00:25:53)  
   - *Friction:* No centralized assumption management; manual comparisons

### Workflow 3: Market Data Validation (Ongoing)
**Tools:** PDF viewer, ChatGPT, Excel  
**Steps**
1. Compare OM cap rates/rents vs ChatGPT suggested ranges (00:25:47–00:25:53)  
2. Adjust assumptions based on judgment (“art”) (00:40:15–00:40:25)  
   - *Friction:* No structured record of why assumptions changed

---

## 5) Proposed Solution

### Product Overview
**DealDesk** is an AI-assisted underwriting workspace that:
1. **Ingests OM PDFs** and extracts key fields into a structured deal record (property details, comps tables, submarket rent/occupancy tables, stated assumptions).
2. **Generates market benchmark assumptions** for a given address + property type (rent, vacancy, opex ratio, cap rate) with citations (source: extracted OM tables + configured data providers + model outputs).
3. **Populates a standardized “Back of the Envelope” model** instantly, with editable assumptions and scenario toggles.
4. **Exports to Excel** (template-compatible) so Excel-native users can continue iterating.
5. **(V1+) Zoning overlay**: given an address/parcel, fetch zoning designation and summarize key constraints; map constraints into feasibility inputs (e.g., max FAR, height, setbacks, allowed uses).

### Differentiation vs current approach
- Eliminates copy/paste between Acrobat ↔ ChatGPT ↔ Excel (00:45:15–00:45:21)
- Converts unstructured PDFs into structured, reusable data
- Provides an “iterative proforma” workflow where AI provides the first curve and the user adjusts (00:35:38–00:36:16)
- Adds zoning + finance in one place (00:43:31–00:43:48)

### Core value proposition
- **Speed:** reduce screening time from **3–4 hours** to **<30 minutes**
- **Consistency:** standardized assumptions and audit trail
- **Coverage:** help users without CoStar access approximate benchmarks credibly
- **Control:** user remains in charge; AI is a starting point, not a black box

---

## 6) User Stories (with Acceptance Criteria)

### P0 (Must Have for MVP)

#### US-P0-1: Create a deal from OM PDF
**Story:** As Rodolfo, I want to upload an OM PDF so that the system extracts key deal and market data automatically.  
**Acceptance Criteria**
- User can upload PDF (up to configurable size, e.g., 50–100MB)
- System extracts at minimum:
  - Property address (if present), city/state
  - Property type (office/multifamily/etc. if present)
  - Key market tables when detectable (e.g., “Office Submarket Breakdown”: avg rent, occupancy)
  - Land sale comps table rows (when present)
- Extraction results are shown in a review UI with confidence indicators and editable fields
- Extraction completes within 2–5 minutes for typical OM

#### US-P0-2: Generate benchmark assumptions for address + property type
**Story:** As Rodolfo, I want AI-generated benchmark ranges (rent, vacancy, opex ratio, cap rate) for my location and property type so that I can underwrite unfamiliar asset classes faster (19:21–21:33).  
**Acceptance Criteria**
- User inputs (or confirms) address/city and property type
- System returns:
  - Rent ($/sf/yr or $/unit/month depending on type)
  - Vacancy %
  - Opex ratio %
  - Cap rate %
  - Each with range + “recommended starting value”
- Each value includes “basis” notes (e.g., “from OM table”, “from configured dataset”, “model estimate”)
- User can override any assumption and see model update

#### US-P0-3: Auto-populate “Back of the Envelope” model
**Story:** As Rodolfo, I want the system to populate a standardized back-of-envelope proforma so that I can reach a go/no-go decision quickly (00:26:31–00:26:35).  
**Acceptance Criteria**
- Model includes at minimum:
  - Revenue inputs (rent, occupancy/vacancy)
  - Operating expenses (opex ratio or $/sf)
  - Cap rate / exit valuation method
  - High-level costs (user-entered: land, hard, soft, financing, contingency)
- Outputs include:
  - Stabilized NOI
  - Exit value
  - Total costs
  - Profit / (loss) and margin
- Updates recalculate in <1 second after edits

#### US-P0-4: Export to Excel
**Story:** As an Excel-centric analyst, I want to export the populated model to an Excel file so that I can continue working in my existing workflow (constraint: reliance on Excel, 00:05:58).  
**Acceptance Criteria**
- Export produces .xlsx with:
  - Inputs in clearly marked cells (mirroring “blue cells” pattern observed)
  - Outputs summary section
  - “Assumptions” tab with provenance notes
- Export includes a stable template version identifier
- No macros required for MVP

#### US-P0-5: Assumption audit trail
**Story:** As Rodolfo, I want to see where each assumption came from so that I can trust and defend the underwriting.  
**Acceptance Criteria**
- Each assumption shows:
  - Source type (OM extraction / user input / AI benchmark)
  - Timestamp
  - Last editor
- User can view change history for key assumptions

---

### P1 (Should Have for V1)

#### US-P1-1: Zoning lookup by address/parcel
**Story:** As Rodolfo, I want the system to identify zoning for an address so that I can quickly assess feasibility (00:45:30–00:45:59).  
**Acceptance Criteria**
- User enters address; system returns:
  - Parcel ID (where available)
  - Zoning designation(s)
  - Jurisdiction (city/county)
- System provides a summarized list of constraints (height, FAR, setbacks, allowed uses) when available
- Clear disclaimer + link to source documents

#### US-P1-2: Zoning-to-model feasibility flags
**Story:** As Rodolfo, I want zoning constraints to flag infeasible assumptions so that I don’t underwrite impossible projects.  
**Acceptance Criteria**
- If user-entered GFA exceeds max FAR * lot area, system flags
- If use type not permitted, system flags
- Flags are explainable and link to zoning source

#### US-P1-3: Scenario comparison (Base / Upside / Downside)
**Story:** As Rodolfo, I want to compare scenarios so that I can quickly see sensitivity to rent/cap/occupancy.  
**Acceptance Criteria**
- At least 3 scenarios with independent assumption sets
- Side-by-side outputs (NOI, value, profit)
- One-click duplicate scenario

#### US-P1-4: OM library + search
**Story:** As a team, I want to store and search uploaded OMs so that we can reuse comps and assumptions across deals.  
**Acceptance Criteria**
- Full-text search over extracted text + metadata
- Filter by city, property type, broker, upload date

---

### P2 (Nice to Have for V2)

#### US-P2-1: Full proforma generation (monthly schedule + financing)
**Story:** As Rodolfo, I want AI to generate a first-pass full proforma so that I can reduce the 1–2 week modeling cycle (00:26:55–00:27:00).  
**Acceptance Criteria**
- Generates multi-tab model (budget, monthly schedule, annual proforma)
- Financing module (interest-only, amortizing, draw schedule)
- Export to Excel with consistent template mapping

#### US-P2-2: Data provider integrations (comps, rents) beyond OMs
**Story:** As a user without CoStar, I want integrated market datasets so that I can benchmark without expensive subscriptions (00:32:31–00:32:37).  
**Acceptance Criteria**
- Pluggable provider framework
- At least one paid + one public dataset integrated (subject to licensing)

#### US-P2-3: Team collaboration + permissions
**Story:** As a manager, I want roles and approvals so that assumptions are governed.  
**Acceptance Criteria**
- Roles: Admin, Analyst, Viewer
- Approval workflow for “final assumptions”

---

## 7) Technical Architecture

### High-level architecture diagram (textual)
1. **Web App (React/Next.js)**  
   ↕ (HTTPS, JWT)  
2. **API Gateway / Backend (Node.js or Python FastAPI)**  
   - Auth, deals, assumptions, exports  
   ↕  
3. **Document Processing Service**  
   - PDF ingestion → OCR (if needed) → layout/table extraction → normalized fields  
   ↕  
4. **AI Orchestration Service**  
   - Prompting + tool calls (extraction validation, benchmark generation, zoning summarization)  
   ↕  
5. **Data Layer**
   - Postgres (core entities)
   - Object storage (S3/GCS) for PDFs and generated exports
   - Vector index (pgvector or managed) for OM retrieval/search (V1)
6. **Integrations**
   - Geocoding (Google/Mapbox)
   - Zoning sources (jurisdiction GIS/APIs where available; fallback to document ingestion)
   - Optional: market datasets (V2)

### Key components & responsibilities
- **Frontend**
  - Deal creation wizard (upload OM, confirm address/type)
  - Extraction review UI (editable fields + confidence)
  - Assumptions panel (ranges, recommended values, provenance)
  - Model view (inputs/outputs, scenarios)
  - Export flow (download .xlsx)
- **Backend API**
  - Deal CRUD, file upload orchestration
  - Assumption versioning + audit trail
  - Model calculation service (deterministic formulas)
  - Excel export generation
- **Document Processing**
  - PDF text extraction (pdfplumber) + OCR (Tesseract/AWS Textract) for scanned docs
  - Table detection and parsing (Textract tables or Camelot/Tabula + heuristics)
  - Field mapping to canonical schema (e.g., “Avg Rent” → `market_rent_psf_yr`)
- **AI Orchestration**
  - Validates extracted fields, suggests mappings
  - Generates benchmark assumptions (with structured JSON output)
  - Produces user-facing explanations and citations
- **Model Engine**
  - Deterministic computation library (no AI in calculations)
  - Supports scenario sets and recalculation
- **Storage**
  - PDFs and exports stored in object storage with signed URLs
  - Postgres stores metadata, extracted fields, assumptions, and results

### Data flow (MVP)
1. User uploads OM → backend stores PDF in S3
2. Backend triggers doc processing job → extracts structured fields + tables
3. AI service normalizes/validates extraction → writes to Postgres
4. User confirms address/type → AI generates benchmark assumptions
5. Model engine computes outputs → UI displays results
6. User exports to Excel → export service generates .xlsx → stored + downloaded

### Third-party integrations required
- **Geocoding:** Google Maps or Mapbox (address normalization)
- **OCR/Table extraction:** AWS Textract (recommended for speed/accuracy) or open-source fallback
- **LLM provider:** OpenAI/Anthropic (structured outputs required)
- **Object storage:** AWS S3 (or GCS/Azure Blob)

---

## 8) Data Model (Schema Description)

### Core entities

#### `users`
- `id` (UUID)
- `email`
- `name`
- `role` (admin/analyst/viewer)
- `created_at`

#### `organizations`
- `id`
- `name`
- `created_at`

#### `deals`
- `id`
- `org_id` (FK)
- `name`
- `address_raw`
- `address_normalized`
- `city`
- `state`
- `lat`, `lng`
- `property_type` (enum: office, multifamily, retail, industrial, land, mixed_use, other)
- `status` (draft, screened, archived)
- `created_by` (FK users)
- `created_at`, `updated_at`

#### `documents`
- `id`
- `deal_id` (FK)
- `type` (om_pdf, zoning_pdf, other)
- `file_url` (S3 key)
- `file_name`
- `uploaded_at`
- `processing_status` (queued, processing, complete, failed)
- `extraction_version`

#### `extracted_fields`
- `id`
- `document_id` (FK)
- `field_key` (canonical key, e.g., `market_rent_psf_yr`)
- `field_label_original` (e.g., “Avg. Asking Rent”)
- `value_text`
- `value_number`
- `unit` (e.g., `USD_PSF_YR`, `%`)
- `confidence` (0–1)
- `source_page`
- `source_bbox` (json)
- `created_at`

#### `market_tables`
- `id`
- `document_id` (FK)
- `table_type` (land_comps, submarket_breakdown, rent_comps, other)
- `headers` (json array)
- `rows` (json array)
- `source_page`
- `confidence`

#### `assumption_sets`
- `id`
- `deal_id` (FK)
- `name` (Base/Upside/Downside)
- `created_at`
- `created_by`

#### `assumptions`
- `id`
- `assumption_set_id` (FK)
- `key` (e.g., `rent_psf_yr`, `vacancy_pct`, `opex_ratio_pct`, `cap_rate_pct`)
- `value_number`
- `unit`
- `range_min`, `range_max` (nullable)
- `source_type` (user, ai_benchmark, om_extraction)
- `source_ref` (document_id/field_id/table_id)
- `notes`
- `updated_at`
- `updated_by`

#### `model_results`
- `id`
- `assumption_set_id` (FK)
- `noi_stabilized`
- `exit_value`
- `total_cost`
- `profit`
- `profit_margin_pct`
- `computed_at`
- `model_version`

#### `exports`
- `id`
- `deal_id` (FK)
- `assumption_set_id` (FK)
- `type` (xlsx)
- `file_url`
- `created_at`

#### (V1+) `zoning_records`
- `id`
- `deal_id` (FK)
- `jurisdiction`
- `zone_code`
- `overlay_codes` (json)
- `constraints` (json: FAR, height, setbacks, uses)
- `source_url`
- `confidence`
- `created_at`

Relationships:
- Organization has many users and deals
- Deal has many documents, assumption sets, exports
- Document has many extracted fields and tables
- Assumption set has many assumptions and one model result (per model version)

---

## 9) API Design (Core Endpoints)

### Auth
- `POST /v1/auth/login`
- `POST /v1/auth/logout`
- `GET /v1/auth/me`

### Deals
- `POST /v1/deals`
  - Req: `{ name, address_raw?, property_type? }`
  - Res: `{ deal }`
- `GET /v1/deals?query=&city=&property_type=&status=`
- `GET /v1/deals/{dealId}`
- `PATCH /v1/deals/{dealId}`

### Document upload + processing
- `POST /v1/deals/{dealId}/documents`
  - Multipart upload: `file`, `type=om_pdf`
  - Res: `{ documentId, processing_status }`
- `GET /v1/documents/{documentId}`
  - Res: `{ status, extracted_summary, tables_detected }`
- `POST /v1/documents/{documentId}/reprocess`
  - Res: `{ status: "queued" }`

### Extraction review
- `GET /v1/documents/{documentId}/extracted-fields`
  - Res: `{ fields: [ {id, field_key, value_number, unit, confidence, source_page} ] }`
- `PATCH /v1/extracted-fields/{fieldId}`
  - Req: `{ value_number?, value_text?, unit? }`
  - Res: `{ field }`

### Assumptions + benchmarks
- `POST /v1/deals/{dealId}/assumption-sets`
  - Req: `{ name }`
  - Res: `{ assumption_set }`
- `POST /v1/deals/{dealId}/benchmarks:generate`
  - Req: `{ assumption_set_id, property_type, location: { city, state, lat?, lng? } }`
  - Res: `{ assumptions: [{ key, range_min, range_max, recommended, unit, notes, source_type }] }`
- `GET /v1/assumption-sets/{id}/assumptions`
- `PUT /v1/assumption-sets/{id}/assumptions`
  - Req: `{ assumptions: [{ key, value_number, unit }] }`
  - Res: `{ assumptions }`

### Model calculation
- `POST /v1/assumption-sets/{id}/compute`
  - Res: `{ results: { noi_stabilized, exit_value, total_cost, profit, profit_margin_pct } }`
- `GET /v1/assumption-sets/{id}/results`

### Export
- `POST /v1/assumption-sets/{id}/export/xlsx`
  - Res: `{ exportId, download_url }`
- `GET /v1/exports/{exportId}`

### (V1+) Zoning
- `POST /v1/deals/{dealId}/zoning:lookup`
  - Req: `{ address_normalized }`
  - Res: `{ zoning_record }`

---

## 10) MVP Scope

### In (MVP: 4–6 weeks)
- Deal creation + OM PDF upload
- Document processing pipeline (text + table extraction) with review UI
- AI benchmark generation for: rent, vacancy, opex ratio, cap rate (structured output)
- Standardized “Back of the Envelope” model (deterministic calculations)
- Assumption editing + audit trail (source + last edited)
- Excel export (.xlsx template)
- Basic deal list + status (draft/screened)

**Why:** Directly targets the highest-severity pains: manual input (00:09:52), fragmented workflow (00:45:15–00:45:21), and 3–4 hour screening time (00:26:31–00:26:35).

### Out (Explicitly not in MVP)
- Full 1–2 week proforma automation (monthly schedules, debt waterfalls)
- Deep CoStar-like comps database (licensing + time)
- Full zoning parsing across all jurisdictions (complexity: 60+ zones per city (00:41:53–00:42:32))
- Multi-user collaboration/permissions beyond basic org/user

### MVP assumptions / constraints
- Users remain Excel-first; we win by pre-populating and exporting
- OM formats vary; MVP targets “good enough extraction” with human review rather than perfect automation

---

## 11) Implementation Phases

### Phase 1 — MVP (4–6 weeks)

**Features**
1. Deal + OM upload
2. Extraction pipeline + review UI
3. Benchmark generation (rent/vacancy/opex/cap)
4. Back-of-envelope model + instant recompute
5. Assumption provenance + change history (basic)
6. Excel export

**Technical tasks**
- Set up Postgres schema + migrations
- S3 storage + signed URL upload/download
- Async job runner (e.g., BullMQ/Celery) for document processing
- Textract (or OCR fallback) integration
- Table extraction + canonical mapping heuristics for:
  - “Office Submarket Breakdown” style tables (rent, occupancy)
  - “Land Sale Comparables” tables
- LLM structured output contracts (JSON schema) for:
  - benchmark generation
  - extraction normalization (optional)
- Model engine library (pure functions + unit tests)
- Excel export generator (e.g., Python openpyxl or Node exceljs) with template mapping
- Observability: job logs, extraction confidence metrics

**Milestones**
- Week 1: Data model + upload + storage + basic UI skeleton
- Week 2: Document processing v0 (text extraction) + extracted fields UI
- Week 3: Table extraction v0 + benchmark generation endpoint
- Week 4: Model engine + assumptions UI + compute
- Week 5: Excel export + end-to-end flows
- Week 6: Hardening, QA with 10–20 OMs, performance + bug fixes

---

### Phase 2 — V1 (8–12 weeks)

**Features**
- OM library search (full-text + filters)
- Scenario comparison (Base/Upside/Downside)
- Zoning lookup by address (jurisdiction-dependent)
- Zoning feasibility flags (FAR/use checks where data available)
- Improved extraction accuracy via feedback loop (user corrections → training set)

**Technical tasks**
- Add vector search (pgvector) for OM retrieval
- Build scenario data model + UI
- Integrate geocoding + parcel lookup (where available)
- Zoning connector framework:
  - GIS endpoints per jurisdiction (starting with Miami/Coral Gables focus)
  - fallback: ingest zoning PDFs and summarize constraints with LLM + citations
- Rule engine for feasibility checks (deterministic)
- Permissioning basics (org-level sharing)

**Milestones**
- Month 1: Search + scenarios
- Month 2: Zoning lookup MVP + feasibility flags
- Month 3: Extraction quality improvements + beta rollout

---

### Phase 3 — V2 (16–24 weeks)

**Features**
- First-pass full proforma generation (multi-tab, monthly schedule)
- Financing module (construction draws, interest reserve)
- Market data provider integrations (licensed/public)
- Team workflows (approvals, comments, roles)
- Advanced analytics: sensitivity tornado charts, Monte Carlo (optional)

**Technical tasks**
- Expand model engine to multi-period cash flows
- Template system for multiple Excel model styles (mapping layer)
- Provider ingestion pipelines + normalization
- Governance: approvals, audit logs, SOC2-ready controls (if targeting enterprise)

**Milestones**
- Quarter 1: Full proforma v0 + export
- Quarter 2: Data integrations + collaboration + scale hardening

---

## 12) Success Metrics

### Primary (quantitative)
1. **Time to complete back-of-envelope screening**
   - Baseline: **3–4 hours** (00:26:31–00:26:35)
   - Target MVP: **<30 minutes** median
2. **Deals screened per week per analyst**
   - Baseline (Rodolfo): **2–3/week** (00:37:23)
   - Target: **6–10/week** (aligning with “companies that do ten per week” (00:36:46))
3. **Manual data entry reduction**
   - Baseline: majority manual (“All this is manual input” (00:09:52))
   - Target: ≥70% of key fields auto-populated (rent, vacancy, opex, cap, address, key OM tables)
4. **Extraction accuracy (field-level)**
   - Target MVP: ≥85% correct after user review for top 20 canonical fields
5. **Export adoption**
   - % of screened deals exported to Excel (target: >60% in MVP, indicating workflow fit)

### Secondary (qualitative)
- User-reported trust in assumptions (provenance clarity)
- Reduced context switching (single workspace vs Acrobat+ChatGPT+Excel)
- Perceived improvement in confidence underwriting unfamiliar property types (office example: rent $50–55, vacancy 9–11%, opex 30–40%, cap 6.5–7.2% (00:20:09–00:20:37, 00:25:47–00:25:53))

---

## 13) Appendix: Visual Evidence (Screen Share Observations)

### Theme A — Fragmented multi-application workflow
**Observed tools**
- Microsoft Excel (09:37–14:02; 26:16–28:49)
- Adobe Acrobat / PDF viewer (14:02–16:27)
- ChatGPT web UI (19:21–21:33)

**Implication for engineering**
- Product must consolidate these steps into one flow and/or integrate with Excel export to avoid forcing behavior change.

---

### Theme B — Manual input patterns in Excel (“blue cells”)
**Observed UI pattern**
- Excel proforma has many designated manual input cells (blue) across multiple tabs (09:37–14:02).
- Back-of-envelope sheet similarly relies on manual entry (26:16–28:49).

**Implication**
- Our model UI should mirror this mental model:
  - clearly separated Inputs vs Outputs
  - editable fields with strong visual affordance
  - fast recalculation

---

### Theme C — Complexity of full proforma models
**Observed tabs/sections (examples)**
- SUMMARY, INPUTS, RENT ANALYSIS, BUDGET, MONTHLY SCHEDULE, ANNUAL PROFORMA (09:37–14:02)
- Sections like Sources & Uses, Proforma Key Assumptions, Returns, Exit Summary, Financing Summary

**Implication**
- MVP should not attempt full parity; instead, focus on the screening model and export compatibility.
- V2 can expand into multi-period modeling once extraction + assumptions are stable.

---

### Theme D — OM PDFs contain critical tables but are unstructured
**Observed content**
- “Land Sale Comparables” and “Office Submarket Breakdown” tables in OM (14:02–16:27)

**Implication**
- Table extraction is a first-class requirement.
- Store extracted tables as structured JSON with page references and confidence.

---

### Theme E — AI used as benchmark generator today (but disconnected)
**Observed**
- ChatGPT response provides structured benchmarks for Coral Gables office underwriting:
  - rent ranges, vacancy, opex ratio, cap rate (19:21–21:33)
- User then manually transfers into Excel (00:44:43–00:44:46)

**Implication**
- Our AI output must be structured (JSON), directly mapped to model inputs, and show provenance to build trust.

---

## Notes / Open Questions (for kickoff)
1. Which “Back of the Envelope” template should we standardize on first (Rodolfo’s current sheet vs a new canonical one)?
2. Initial geographic focus for zoning (Miami / Coral Gables first, per call context)?
3. Data licensing strategy for benchmarks beyond OMs (V2): public datasets vs partnerships.
4. Security/compliance expectations (deal docs are sensitive): encryption at rest, access controls, retention policies.