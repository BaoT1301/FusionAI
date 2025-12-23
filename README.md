# FusionAI - AI Research Assistant

An AI-powered research tool that fuses knowledge from Wikipedia, web search, and Claude AI to generate comprehensive research summaries.

![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)
![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204-purple)

## Features

- 🤖 AI-powered research summaries (300-500 words)
- 🔍 Multi-source integration (Wikipedia + Web Search + Claude AI)
- ⚡ Fast results (7-10 seconds)
- 🎨 Modern dark-themed UI
- 📊 Structured output with sources

## Tech Stack

**Frontend:** React, Vite, Axios  
**Backend:** Python, Flask, LangChain, Claude AI (Anthropic)  
**APIs:** Anthropic, Wikipedia, DuckDuckGo

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API key to .env: ANTHROPIC_API_KEY=your_key_here

python app.py
```

Backend runs on `http://localhost:5001`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## Project Structure
```
FusionAI/
├── backend/
│   ├── app.py              # Flask API
│   ├── tools.py            # LangChain tools
│   ├── requirements.txt    # Python dependencies
│   └── .env                # API keys (DO NOT COMMIT)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   └── App.css         # Styles
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite config
└── README.md
```

## API Endpoints

**Health Check:**
```http
GET /api/health
```

**Research:**
```http
POST /api/research
Content-Type: application/json

{
  "query": "artificial intelligence"
}
```

## Environment Variables

Create `backend/.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
PORT=5001
```

**⚠️ Never commit your `.env` file to GitHub!**

## Deployment

**Backend:** Deploy to Render/Heroku (set `ANTHROPIC_API_KEY` in environment variables)  
**Frontend:** Deploy to Vercel/Netlify (build command: `npm run build`, output: `dist`)

## Cost Note

Claude Sonnet 4 costs approximately **$0.03-0.05 per query**. New users get free trial credits.

## Troubleshooting

**Port in use:** Change `PORT` in `.env` or port in `vite.config.js`  
**API errors:** Verify API key in `.env` file  
**Module errors:** Reinstall dependencies with `pip install -r requirements.txt` or `npm install`

## Author

**Bao Tran** - George Mason University  