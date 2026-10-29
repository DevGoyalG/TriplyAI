# ✈️ Triply AI — A Multi-Agent Travel Planner with LangGraph

<p align="center">
  Plan smarter trips with AI-powered flight research, hotel discovery, and personalized day-by-day itineraries.
</p>

<p align="center">
  <a href="https://triply-ai.onrender.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-Visit%20TriplyAI-2563EB?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=for-the-badge" alt="LangGraph" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
</p>

<img width="1892" height="863" alt="image" src="https://github.com/user-attachments/assets/15638bb4-6235-4212-a2af-82e02ebd9bc3" />

---

## 🌍 Overview

**TriplyAI** is an open-source, AI-powered travel planning application that transforms natural-language travel requests into personalized travel plans.

Instead of switching between multiple websites to research flights, find hotels, and organize activities, TriplyAI coordinates specialized AI agents in a single workflow to help you plan your journey.

Whether you're planning a weekend getaway or a multi-day international trip, TriplyAI helps bring the essential pieces of your travel plan together.

## ✨ Features

- ✈️ **Flight Research** — Retrieve flight-related information using AviationStack.
- 🏨 **Hotel Discovery** — Research hotel options using Tavily web search.
- 🤖 **Multi-Agent Architecture** — Coordinate specialized agents using LangGraph.
- 🗺️ **Personalized Itineraries** — Generate structured, day-by-day travel plans.
- 💬 **Natural-Language Input** — Describe your destination, trip duration, and preferences in plain English.
- 🧠 **LLM-Powered Planning** — Generate travel recommendations using Groq-hosted language models.
- 💾 **Persistent Checkpointing** — Store workflow state using PostgreSQL and LangGraph's checkpointing integration.
- 🌐 **Web Interface** — Interact with the planner through a FastAPI-powered application.
- 📄 **Export-Friendly Results** — View and use your generated travel plan from the web interface.

## 🖥️ Live Demo

**Try TriplyAI:** https://triply-ai.onrender.com/

> Note: The live demo depends on the availability of the hosted service and its external APIs. Flight information and hotel search results may vary. Always verify bookings, prices, and availability with the relevant provider.

## 🏗️ Architecture

TriplyAI uses a sequential multi-agent workflow orchestrated by LangGraph.

```mermaid
flowchart TD
    A["User Travel Request"] --> B["Flight Agent"]
    B --> C["Hotel Research Agent"]
    C --> D["Itinerary Planning Agent"]
    D --> E["Final Response Agent"]
    E --> F["Personalized Travel Plan"]

    B -.-> G["AviationStack API"]
    C -.-> H["Tavily Web Search"]
    D -.-> I["Groq LLM"]
    E -.-> I

    B -.-> J["PostgreSQL Checkpointer"]
    C -.-> J
    D -.-> J
    E -.-> J
```

### How It Works

1. **User Request:** The user describes their destination, trip duration, budget, and preferences.
2. **Flight Research:** The flight agent retrieves relevant flight information through AviationStack.
3. **Hotel Research:** The hotel agent searches the web for accommodation suggestions.
4. **Itinerary Generation:** The itinerary agent combines the request and collected research to create a day-by-day plan.
5. **Final Response:** The final agent presents the information in a structured, user-friendly format.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | Backend and REST API |
| LangGraph | Multi-agent workflow orchestration |
| LangChain | LLM integration |
| Groq | Language model inference |
| AviationStack | Flight information API |
| Tavily | Web search and hotel research |
| PostgreSQL | Persistent workflow checkpointing |
| Psycopg | PostgreSQL connectivity |
| Jinja2 | HTML template rendering |
| HTML, CSS, JavaScript | Frontend interface |
| Uvicorn | ASGI application server |
| Render | Application hosting |

## 📁 Project Structure

```text
TriplyAI/
├── static/
│   ├── script.js              # Frontend interactions and API requests
│   └── style.css              # UI styling and responsive design
│
├── templates/
│   └── index.html             # Main web interface
│
├── tools/
│   ├── __init__.py            # Tools package initialization
│   ├── flight_tool.py         # Flight research using AviationStack
│   └── tavily_tool.py         # Web search and hotel research using Tavily
│
├── app.py                     # FastAPI application and API endpoints
├── backend.py                 # LangGraph workflow and multi-agent logic
├── requirements.txt           # Python dependencies
│
├── Dockerfile                 # Docker image configuration
├── .dockerignore              # Files excluded from Docker builds
├── .gitignore                 # Files excluded from Git tracking
│
├── test.py                    # Travel agent and tool testing
├── test_db.py                 # PostgreSQL connectivity testing
│
├── TriplyAI-Workflow.pdf      # Multi-agent workflow documentation
├── LICENSE                    # Project license
└── README.md                  # Project documentation
```

*The tree illustrates the main application components. Exact asset filenames and subdirectories may vary.*

## 🚀 Getting Started

Follow these steps to run TriplyAI locally.

### Prerequisites

Make sure you have:

- Python 3.10 or newer
- A PostgreSQL database
- A Groq API key
- A Tavily API key
- An AviationStack API key

### 1. Clone the Repository

```bash
git clone https://github.com/DevGoyalG/TriplyAI.git
cd TriplyAI
```

### 2. Create a Virtual Environment

**Windows — Command Prompt**

```bash
python -m venv venv
venv\Scripts\activate
```

**Windows — PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the following environment variables:

```env
# PostgreSQL Database
DATABASE_URL=postgresql://username:password@host:5432/database_name

# AI Model
GROQ_API_KEY="your_groq_api_key"

# External APIs
AVIATIONSTACK_API_KEY="your_aviationstack_api_key"
TAVILY_API_KEY="your_tavily_api_key"

# Default Flight Origin
DEFAULT_ORIGIN_IATA="DEL"

# LangSmith Tracing
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com/"
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT="TriplyAI"
```

#### Where to Get API Keys

- **Groq:** https://console.groq.com/
- **AviationStack:** https://aviationstack.com/
- **Tavily:** https://tavily.com/
- **LangSmith:** https://smith.langchain.com/

**Security notes:**
- Never commit your `.env` file or real credentials to GitHub.
- Add `.env` to `.gitignore`.
- Configure production secrets in your hosting provider's environment-variable settings.
- Use a secure PostgreSQL connection URL and follow your database provider's SSL requirements.
- LangSmith tracing is optional unless your application configuration requires it.

Replace the placeholder values with your own API credentials and PostgreSQL connection URL.

**Important:**
- Keep your `.env` file private.
- Never commit API keys, passwords, or database credentials to GitHub.
- For a hosted deployment, configure environment variables in your hosting provider's dashboard.
- Use a PostgreSQL connection URL compatible with your database provider's SSL requirements.

### 5. Run the Application

```bash
python app.py
```

Alternatively, start the application with Uvicorn:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open the application in your browser:

**http://127.0.0.1:8000/**

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web interface |
| `POST` | `/api/travel` | Processes a travel planning request |
| `GET` | `/health` | Checks API availability |
| `GET` | `/docs` | Opens interactive Swagger API documentation |

### Example Request

**Endpoint:** `POST /api/travel`

```json
{
  "message": "Plan a 3-day trip to Tokyo with a budget of $1200"
}
```

### Example using cURL

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Plan a 3-day trip to Tokyo with a budget of $1200\"}"
```

The API returns a JSON response containing the generated answer, flight research, hotel research, itinerary, and conversation thread identifier.

## 🔐 Security and Configuration

- Store credentials in environment variables.
- Add `.env` and other secret files to `.gitignore`.
- Avoid returning raw internal exceptions to API clients in production.
- Restrict access to conversation threads appropriately when deploying for multiple users.
- Apply suitable rate limits and input validation before exposing the service publicly.

## ⚠️ Important Limitations

- AviationStack provides flight-related data; it does not automatically guarantee ticket prices or booking availability.
- Hotel suggestions returned through web search may not reflect real-time availability or final prices.
- AI-generated itineraries and budgets are estimates and should be verified before booking.
- Results depend on external API availability, API plan limits, and the selected language model.

TriplyAI is a travel-planning assistant, not a booking or payment platform.

## 🛣️ Future Improvements

Potential directions for extending the project include:

- [ ] Real-time flight fare comparison
- [ ] Hotel price and availability integrations
- [ ] Interactive maps and route visualization
- [ ] User authentication and saved trips
- [ ] Trip budget breakdown and expense tracking
- [ ] More specialized travel agents
- [ ] Automated tests and CI/CD workflows
- [ ] Multilingual travel planning

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome!

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make your changes and test them.
4. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

5. Push your branch and open a Pull Request.

## 🤝 Connect with Me

<a href="https://github.com/DevGoyalG" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</a>
&nbsp;
<a href="https://www.linkedin.com/in/devgoyalg/" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
</a>
&nbsp;
<a href="https://www.instagram.com/dev_goyal_g/" target="_blank">
  <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"/>
</a>
&nbsp;
<a href="https://x.com/dev_goyal_g" target="_blank">
  <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"/>
</a>

---

<p align="center">
  <b>Thank you for visiting! Happy Learning 🚀</b>
</p>
