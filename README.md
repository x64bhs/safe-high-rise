# Safe High-Rise

A risk-aware building guidance web application that helps assess environmental construction risks and provides actionable building recommendations for early-stage planning.

## Features

- 🏗️ **Risk Assessment**: Analyze environmental construction risks for single or multiple locations
- 🤖 **Building Guidance**: Get intelligent architectural recommendations powered by procedural expert systems
- 🎯 **Safety Tips**: Receive clear, actionable safety recommendations
- 💡 **User-Friendly Interface**: Modern, intuitive web interface for non-technical users

## Tech Stack

### Frontend
- React + Vite
- Modern CSS with responsive design
- Interactive UI components

### Backend
- Procedural design engine
- RESTful API architecture

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Vinay6615/StrataMind---Designing_Structures_that_Think_with_the_Earth.git
cd StrataMind---Designing_Structures_that_Think_with_the_Earth/safe-high-rise_final
```

2. Set up the backend:
```bash
cd backend
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



### Running the Application

1. Start the backend server:
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173` (or the port shown in terminal)

## Project Structure

```
StrataMind---Designing_Structures_that_Think_with_the_Earth/
└── safe-high-rise_final/
    ├── backend/           # Python backend with API endpoints
    │   ├── main.py       # Main application entry point
    │   ├── services/     # Business logic and API integrations
    │   └── venv/         # Python virtual environment
    └── frontend/         # React frontend application
        ├── src/          # Source code
        ├── public/       # Static assets
        └── package.json  # Node dependencies
```

## Usage

1. Enter a location to assess construction risks
2. View AI-generated risk analysis and recommendations
3. Compare multiple locations (optional)
4. Review safety tips and building guidance
5. Use insights for early-stage construction planning

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
