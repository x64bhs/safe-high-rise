# 🏗️ Safe High-Rise: Risk-Aware Architectural Guidance

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://deepmind.google/technologies/gemini/)

A sophisticated web application designed for early-stage construction planning. It assesses environmental construction risks and provides intelligent, risk-aware architectural recommendations through a combination of procedural expert systems and AI.

---

## 🌟 Key Features

- 🔍 **Intelligent Risk Assessment**: Evaluates seismic zones, flood potential, and wind speeds based on geographical coordinates.
- 🏗️ **Procedural Design Engine**: Generates architectural recommendations (structural systems, materials, geometry) tailored to the local environment.
- ⚡ **Parallel Data Gathering**: Backend uses `asyncio` to gather weather, geocoding, and elevation data simultaneously for high performance.
- 🤖 **AI-Powered Guidance**: Integrated with Google Gemini for context-aware architectural safety tips and conversational support.
- 📊 **Comprehensive Reports**: Provides safety scores, wellness indices, and structural longevity estimates.
- 🗺️ **Interactive Maps**: Visualize locations and risk zones for better planning.

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Services**: 
  - `Seismic Service`: Zone-based risk analysis.
  - `Flood Service`: Elevation and precipitation-based risk calculation.
  - `Weather Service`: Historical and real-time wind/rain data.
  - `Design Generator`: Procedural logic for building geometry and materials.
- **AI Integration**: Google Gemini API.

### Frontend
- **Framework**: [React](https://react.dev/) + [Vite](https://vite.dev/)
- **UI Architecture**: Component-based with responsive layouts.
- **State Management**: React Hooks and Context API.
- **Styling**: Modern CSS with glassmorphism and interactive elements.

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18 or higher
- **Python**: 3.9+
- **API Key**: A Google Gemini API Key (stored in `.env`)

### Installation & Setup

1. **Clone the project:**
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd safe-high-rise_final
   ```

2. **Backend Configuration:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
   Create a `.env` file in the `backend` folder:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Frontend Configuration:**
   ```bash
   cd frontend
   npm install
   ```

### Running Locally

- **Start Backend**: `uvicorn main:app --reload --port 8000` (from `/backend`)
- **Start Frontend**: `npm run dev` (from `/frontend`)
- **Access App**: Navigate to `http://localhost:5173`

---

## 📁 Project Structure

```text
.
├── backend/                # FastAPI Application
│   ├── services/           # Logic for Risk & Design
│   ├── main.py             # API Endpoints
│   └── requirements.txt    # Python Dependencies
├── frontend/               # React Application (Vite)
│   ├── src/
│   │   ├── components/     # Reusable UI Blocks
│   │   ├── pages/          # Main App Views
│   │   └── Layout.jsx      # Navigation & Structure
│   └── package.json        # Node Dependencies
└── docs/                   # Additional Deployment Guides
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created for safe and sustainable urban development.*
