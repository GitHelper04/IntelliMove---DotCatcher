# Dot Catcher Frontend

This is the frontend component of the Dot Catcher game, built with React and Vite.

## 📁 Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main game component
│   ├── App.css          # Game styles
│   └── main.jsx         # Entry point
├── package.json         # Dependencies
└── vite.config.js       # Vite configuration
```

## 🚀 Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🎮 Game Features

- Real-time dot grid display (5x5)
- Score and miss tracking
- Progress visualization
- Win/lose conditions
- Responsive design

## 🔄 Communication

The frontend communicates with the backend via WebSocket connections on port 5001.