# Nistula Guest Message Handler — Technical Assessment

## 🚀 Live Production Instance (Test Now)
The system is containerized and deployed live on a Linux infrastructure managed by PM2. 

**Copy and paste this exact command into your command prompt to test the live API response immediately:**

```cmd
curl -X POST http://82.112.236.54:5050/webhook/message -H "Content-Type: application/json" -d "{\"source\": \"whatsapp\", \"guest_name\": \"Rahul Sharma\", \"message\": \"Is Villa B1 available April 20-24?\", \"property_id\": \"villa-b1\"}"
```

### Quick Links
- **Interactive Swagger Docs:** http://82.112.236.54:5050/docs
- **Internal Developer Documentation:** http://82.112.236.54:5050/

---

## 🏛️ Architecture & Resilience

### 1. Model Rotation Strategy
To ensure 100% demo uptime and bypass individual model rate-limits, the backend implements a rotation logic that cycles through three distinct high-performance LLM engines. If the primary model returns a resource-exhausted error, the system automatically hot-swaps to the next available tier.

### 2. Service-Oriented Design
The project follows a clean service pattern using **FastAPI** and **Pydantic**. Logic is decoupled to ensure strict schema validation and non-blocking asynchronous processing. The application is managed via **PM2** for auto-restart on crashes and persistence across server reboots.

### 3. Fault-Tolerant Fallback
Engineered a **Heuristic Keyword Engine** that maintains classification capabilities even if external AI services are unreachable. This ensures the webhook remains functional and returns valid JSON responses regardless of upstream API availability.

---

## ⚙️ Setup Instructions (Local)

1. **Clone the repository:**
```bash
git clone https://github.com/rohith2989/nistula-technical-assessment.git
cd nistula-technical-assessment
```

2. **Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\activate   # Windows
```

3. **Install dependencies:**
```bash
pip install fastapi uvicorn google-generativeai python-dotenv
```

4. **Environment Configuration:**
Copy `.env.example` to `.env` and add your API key.

5. **Run the server:**
```bash
uvicorn main:app --reload --port 5050
```

---

## 🔬 Confidence Scoring Logic
LLMs do not naturally output deterministic mathematical confidence. To achieve reliable confidence scoring, the system prompt instructs the AI to score based on **contextual proximity**:

- **0.90 - 1.00:** The answer is explicitly written in the provided mock context (e.g., Check-in time, WiFi password). 
  - **Action:** `auto_send`
- **0.60 - 0.89:** The answer is inferred or partially covered, requiring human nuance (e.g., special arrangements). 
  - **Action:** `agent_review`
- **< 0.60:** The answer is completely absent from the context. 
  - **Action:** `escalate`

### Scoring Modifiers (Deterministic Layer)
The score is further refined in the Python backend via a rule-based modifier system:
- **Booking Reference (+0.05):** Boosts confidence if a valid reference is provided.
- **Concise Query (-0.10):** Penalizes messages under 5 words due to inherent ambiguity.
- **Complexity Penalty (-0.05):** Penalizes messages with more than 2 question marks to trigger human review for multi-part requests.

**Override Rule:** Any message classified as a `complaint` automatically triggers an `escalate` action, regardless of the confidence score, to ensure human empathy and immediate intervention.

---

## 📋 Assessment Deliverables
- **Part 2: SQL Schema:** Optimized for Omnichannel Identity Resolution. Located in `schema.sql`.
- **Part 3: Thinking Questions:** Full analysis of the 3 AM crisis and preventative builds. Located in `thinking.md`.
