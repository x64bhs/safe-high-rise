# Safe High-Rise

A risk-aware building guidance web application that helps assess environmental construction risks and provides actionable building recommendations for early-stage planning.

## Features

- 🏗️ **Risk Assessment**: Analyze environmental construction risks for single or multiple locations.
- 🤖 **AI-Driven Design**: Intelligent architectural recommendations powered by a procedural expert system.
- 🏢 **3D Visualization**: Interactive building previews based on environmental data.
- 📊 **Resilience Reports**: Comprehensive safety scores and structural recommendations.
- 💡 **User-Friendly Interface**: Modern, intuitive web interface designed for architectural planning.

## Tech Stack

### Frontend
- React + Vite
- Three.js / React Three Fiber (3D Visualization)
- Modern Vanilla CSS

### Backend (API)
- Python + FastAPI
- Serverless-ready for Vercel deployment
- Expert system for structural engineering logic

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- Python 3.10+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/x64bhs/safe-high-rise.git
cd safe-high-rise_final
```

2. Set up the backend (Local):
```bash
cd api
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

### Running the Application Locally

1. Start the API server:
```bash
cd api
uvicorn index:app --reload --port 8000
```

2. Start the React frontend:
```bash
cd frontend
npm run dev
```

3. Open `http://localhost:5173`. The frontend is configured to proxy `/api` requests to `http://localhost:8000`.

## Deployment (Vercel)

This project is optimized for deployment on Vercel as a full-stack application.

1. Connect your GitHub repository to Vercel.
2. Vercel will automatically detect the `vercel.json` configuration.
3. **Deployment Settings**:
   - **Root Directory**: Project Root (leave as default).
   - **Build Command**: Managed by `vercel.json`.
4. Once deployed, verify your API health at `https://your-app.vercel.app/api/health`.

## Project Structure

```
safe-high-rise/
├── api/                # Python backend (FastAPI)
│   ├── index.py        # Main entry point for Vercel
│   ├── services/       # Engineering logic (Seismic, Wind, Flood)
│   └── requirements.txt
├── frontend/           # React frontend
│   ├── src/            # Components, Pages, Assets
│   └── vite.config.js  # Configured with API proxy
└── vercel.json         # Full-stack deployment configuration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
