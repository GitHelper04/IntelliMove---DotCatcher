# Dot Catcher Game

A real-time interactive game built with Python, Kafka, and React where players catch randomly appearing dots on a 5x5 grid.

## 🎮 Game Overview

Dot Catcher is an engaging game where dots randomly appear on a 5x5 grid and players must click on them before they disappear. The game features real-time scoring, win/lose conditions, and a sleek user interface.

### Game Mechanics
- Dots appear randomly on a 5x5 grid every 0.5-2 seconds
- Players must click on dots to catch them before they disappear (2 seconds)
- Win condition: Reach 10 points
- Lose condition: Miss 5 dots
- Real-time score tracking and progress visualization

## 🏗️ Architecture

The game follows a microservices architecture with Kafka as the messaging backbone:

```
┌─────────────────┐    Kafka    ┌────────────────┐    WebSocket    ┌──────────────┐
│  Dot Generator  ├───────────►│                │◄───────────────┤              │
│   (Producer)    │            │                │                │   Frontend   │
└─────────────────┘            │                │                │  (React/Vite)│
                               │   Kafka Bus    │                └──────────────┘
┌─────────────────┐    Kafka    │                │    WebSocket         ▲
│ Action Handler  ├───────────►│                │◄───────────────┐     │
│   (Producer)    │            │                │                │     │
└─────────────────┘            │                │                │     │
                               └────────────────┘                │     │
                                      ▲                          │     │
                                      │ Kafka                    │     │
                                      ▼                          │     │
                              ┌────────────────┐               │     │
                              │ Game Tracker   │               │     │
                              │  (Consumer)    │               │     │
                              └────────────────┘               │     │
                                      ▲                        │     │
                                      │ Updates                │     │
                                      ▼                        │     │
                              ┌────────────────┐               │     │
                              │ Backend Server │◄──────────────┘     │
                              │  (Flask)       │                     │
                              └────────────────┘◄────────────────────┘
```

### Components

1. **Dot Generator** (`dot_catcher/backend/dot_generator.py`)
   - Python service that generates random dots on the grid
   - Publishes dot appearance events to Kafka "dots" topic
   - Runs continuously with randomized intervals (0.5-2 seconds)

2. **Game Tracker** (`dot_catcher/backend/game_tracker.py`)
   - Kafka consumer that subscribes to both "dots" and "actions" topics
   - Tracks game state including scores, misses, and timing
   - Outputs game statistics to terminal

3. **Backend Server** (`dot_catcher/backend/server.py`)
   - Flask server with WebSocket support (Socket.IO)
   - Manages game state and win/lose conditions
   - Bridges Kafka events with frontend via WebSocket
   - Handles user actions and broadcasts updates

4. **Frontend** (`frontend/`)
   - React application built with Vite
   - Real-time UI that updates via WebSocket
   - Interactive 5x5 grid with visual feedback
   - Progress bars for score and misses

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Kafka 3.6.0
- Zookeeper (comes with Kafka)

### Installation

1. **Setup Kafka**
   ```bash
   # Download and extract Kafka
   curl -L https://archive.apache.org/dist/kafka/3.6.0/kafka_2.13-3.6.0.tgz -o kafka.tgz
   tar -xzf kafka.tgz
   mv kafka_2.13-3.6.0 ~/kafka
   ```

2. **Install Python dependencies**
   ```bash
   pip install kafka-python flask flask-socketio
   ```

3. **Install Frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Running the Game

#### Option 1: Using Startup Scripts (Recommended)

```bash
# Start all services
./start_game.sh

# Stop all services
./stop_game.sh
```

#### Option 2: Manual Startup

1. **Start Zookeeper**
   ```bash
   ~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties
   ```

2. **Start Kafka**
   ```bash
   ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties
   ```

3. **Create Kafka Topics**
   ```bash
   ~/kafka/bin/kafka-topics.sh --create --topic dots --bootstrap-server localhost:9092
   ~/kafka/bin/kafka-topics.sh --create --topic actions --bootstrap-server localhost:9092
   ```

4. **Start Backend Services** (each in a separate terminal)
   ```bash
   # Terminal 1: Game Tracker
   cd dot_catcher/backend
   python game_tracker.py
   
   # Terminal 2: Backend Server
   cd dot_catcher/backend
   python server.py
   
   # Terminal 3: Dot Generator
   cd dot_catcher/backend
   python dot_generator.py
   ```

5. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

### Accessing the Game

Once all services are running, open your browser and navigate to:
```
http://localhost:5173
```

## 🎯 How to Play

1. Dots will randomly appear on the 5x5 grid as colored circles
2. Click on dots quickly to catch them before they disappear (2 seconds)
3. Track your progress with the score and mistake counters
4. Win by reaching 10 points before missing 5 dots
5. Use the "Reset Game" button to start over

## 📁 Project Structure

```
IntelliMove/
├── dot_catcher/
│   └── backend/
│       ├── dot_generator.py      # Generates random dots
│       ├── game_tracker.py       # Tracks game state
│       ├── server.py             # Main backend server
│       └── action_handler.py     # Handles user actions
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main game component
│   │   ├── App.css               # Game styles
│   │   └── main.jsx              # Entry point
│   ├── package.json              # Frontend dependencies
│   └── vite.config.js            # Vite configuration
├── start_game.sh                 # Start all services script
└── stop_game.sh                  # Stop all services script
```

## ⚙️ Technical Details

### Kafka Topics

- **dots**: Contains dot appearance events
  ```json
  {
    "event_type": "dot_appeared",
    "position": [x, y],
    "timestamp": "ISO_TIMESTAMP"
  }
  ```

- **actions**: Contains user action events
  ```json
  {
    "event_type": "dot_caught"|"dot_missed",
    "position": [x, y],
    "timestamp": "ISO_TIMESTAMP"
  }
  ```

### WebSocket Events

- **`dot_appeared`**: Sent when a new dot appears
- **`game_state_update`**: Sent when game state changes
- **`game_over`**: Sent when win/lose condition is met
- **`game_reset`**: Sent when game is reset

### Ports

- **Zookeeper**: 2181
- **Kafka**: 9092
- **Backend Server**: 5001
- **Frontend**: 5173

## 🛠️ Development

### Backend Development

The backend is built with Python and consists of several microservices:

1. **Adding New Features**
   - Modify the appropriate service in `dot_catcher/backend/`
   - Ensure Kafka event schemas remain compatible
   - Update game state logic in `server.py` as needed

2. **Extending Game Logic**
   - Win/lose conditions are defined in `server.py`
   - Game state is tracked in the global `game_state` variable
   - Add new WebSocket events by creating new handlers

### Frontend Development

The frontend is built with React and Vite:

1. **UI Components**
   - Main game grid in `App.jsx`
   - Styling in `App.css`
   - WebSocket connection management in `App.jsx`

2. **Customization**
   - Adjust grid size by modifying `GRID_SIZE` constant
   - Change timing values in both frontend and backend
   - Update styling in CSS files

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Kafka for reliable event streaming
- React and Vite for a fast frontend development experience
- Flask-SocketIO for real-time WebSocket communication
