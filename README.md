# The Better Credit 💳

**The Better Credit** is an India-focused credit card rewards optimizer. Give it a transaction — merchant, amount, and category — and it tells you which credit card in your wallet earns you the most rewards, showing both points and their INR value.

Unlike a simple "best card" ranking, it surfaces **multiple winners across reward categories** (cashback, points, NeuCoins, fuel, milestones, travel) and shows **every card in your wallet** with its individual reward for that transaction — plus how close each card is to its next milestone.

## Features

- 🏆 **Multi-category winners** — best cashback, points, NeuCoins, fuel, and travel cards shown side by side, not collapsed into one ranking
- 💳 **Full wallet breakdown** — see what every card in your wallet earns on a transaction, not just the winner
- 🎯 **Milestone tracking** — know how close each card is to its next spend milestone
- 🔑 **Simple dev auth** — API key based authentication for fast local development
- 🌐 **Cross-platform** — REST API, web dashboard, Chrome extension, and (in progress) a Flutter mobile app

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, PostgreSQL (via Supabase) |
| Rule Engine | JSON-driven per-card reward rules |
| Web Dashboard | React, TypeScript, Tailwind CSS v4, Vite |
| Chrome Extension | React, TypeScript, Manifest V3 |
| Mobile App | Flutter, Dart, Riverpod, GoRouter |
| Auth | API key (dev), JWT (planned for production) |

## Project Structure

```
The-Better-Credit/
├── backend/
│   ├── main.py            # FastAPI app, custom OpenAPI/Swagger auth setup
│   ├── database.py
│   ├── auth_utils.py
│   ├── routers/
│   │   ├── cards.py
│   │   ├── suggest.py      # core "which card wins" endpoint
│   │   └── auth.py
│   ├── models/
│   └── schemas/
├── rules/                  # JSON reward rules, one file per card
├── docs/
│   └── architecture.md
├── extension/               # Chrome extension (Manifest V3)
├── app/                     # Flutter mobile app
├── website/                 # Web dashboard (React + Vite)
│   └── src/pages/DashboardPage.tsx
├── create_tables.py
├── .env
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.13
- Node.js & npm
- PostgreSQL / Supabase project
- (Optional) Flutter SDK for mobile development

### Backend Setup

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Set up your .env file
# DEV_API_KEY=tbc-dev-2024

# Run the backend
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`. Click **Authorize** in Swagger UI and enter your dev API key to try endpoints.

### Web Dashboard Setup

```bash
cd website
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

## Authentication

During development, the API uses a simple API key scheme:

```
x-api-key: <your-dev-api-key>
```

This header is required on all protected endpoints. Production deployments will move to per-user JWT/session-based authentication.

## Build Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Cards API | ✅ Done |
| 2 | Rule Engine (`/suggest` endpoint) | ✅ Done |
| 3 | Database + SQLAlchemy | ✅ Done |
| 4 | API Key Auth | ✅ Done |
| 5 | Chrome Extension | ✅ Done |
| 6 | Flutter Mobile App | 🔄 In progress |
| 7 | Rule Monitoring Agent | ⬜ Not started |
| 8 | LLM Explanation Layer | ⬜ Not started |
| 9 | Landing Page / Website | ✅ Done (design polish pending) |

## Roadmap

- **Rule Monitoring Agent** — automatically crawl bank websites, detect rule changes, and update reward JSON files using an LLM
- **LLM Explanation Layer** — turn raw rule engine output into plain-English explanations of why a card wins
- **Mobile App** — finish and ship the Flutter app for Android/iOS

## Contributing

This project is currently a personal learning build. Issues and suggestions are welcome via GitHub Issues.

## License

TBD
