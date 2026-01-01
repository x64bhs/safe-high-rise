# Safe High-Rise

A risk-aware building guidance web application that helps assess environmental construction risks and provides actionable building recommendations for early-stage planning.

## Features

- 🏗️ **Risk Assessment**: Analyze environmental construction risks for single or multiple locations
- 🤖 **AI-Powered Recommendations**: Get intelligent building guidance using Google Gemini API
- 📊 **Multi-Location Comparison**: Compare risks across different locations
- 🎯 **Safety Tips**: Receive clear, actionable safety recommendations
- 💡 **User-Friendly Interface**: Modern, intuitive web interface for non-technical users

## Tech Stack

### Frontend
- React + Vite
- Modern CSS with responsive design
- Interactive UI components

### Backend
- Python with Flask/FastAPI
- Google Gemini API integration
- RESTful API architecture

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/safe-high-rise.git
cd safe-high-rise
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

4. Configure environment variables:
   - Create a `.env` file in the backend directory
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

### Running the Application

1. Start the backend server:
```bash
cd backend
venv\Scripts\activate
python main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173` (or the port shown in terminal)

## Project Structure

```
safe-high-rise/
├── backend/           # Python backend with API endpoints
│   ├── main.py       # Main application entry point
│   ├── services/     # Business logic and API integrations
│   └── venv/         # Python virtual environment
├── frontend/         # React frontend application
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── package.json  # Node dependencies
└── README.md         # This file
```

## Usage

1. Enter a location to assess construction risks
2. View AI-generated risk analysis and recommendations
3. Compare multiple locations (optional)
4. Review safety tips and building guidance
5. Use insights for early-stage construction planning

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Powered by Google Gemini API
- Built with React and Python
