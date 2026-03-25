# School Library Website

A modern web application for managing a school library built with Flask, Vue.js, and Tailwind CSS.

## Project Structure

```
biblioteca/
├── backend/           # Flask API server
│   ├── app/
│   │   ├── routes/    # API endpoints
│   │   └── models/    # Database models
│   ├── config.py      # Configuration
│   ├── run.py         # Entry point
│   └── requirements.txt
├── frontend/          # Vue.js application
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── pages/       # Page components
│   │   ├── App.vue      # Root component
│   │   └── main.js      # Entry point
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Run the Flask server:
```bash
python run.py
```

The backend will start at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

## Available Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Backend
- `python run.py` - Start Flask development server

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/` - API information

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Vue 3, Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## Features to Implement

- [ ] Book management system
- [ ] User authentication
- [ ] Book borrowing/returning
- [ ] User profiles
- [ ] Search functionality
- [ ] Admin panel
