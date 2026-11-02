# block_puzzle.py
🧩 Block Puzzle Game

An addictive grid-based Block Puzzle game built with Python. Fit geometric block shapes onto the board, complete full rows or columns to clear them, and score as many points as possible before you run out of space!

✨ Features

🎮 Classic Gameplay: Strategic placement of block shapes onto a grid.

💥 Line Clearing Mechanics: Clear full rows and columns simultaneously to score combo points.

🎨 Visual Aesthetics: Clean, colorful design with distinct block shapes.

🏆 Score & High Score Tracking: Live tracking of current score and local high score.

🚫 Game Over Detection: Automatic detection when no legal moves remain.

🔊 Sound Effects: Audio feedback for block placements, line clears, and game over screens.

🛠️ Built With

Python 3.x - Core programming language and logic.

Pygame - Game engine for rendering graphics, handling events, and audio.

🚀 Getting Started

Prerequisites

Make sure you have Python 3.8+ installed on your machine. Check your installation by running:

python --version


Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/block-puzzle-game.git
cd block-puzzle-game


Create a virtual environment (optional but recommended):

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


(Or manually install Pygame: pip install pygame)

🕹️ Running the Game

Execute the main script to start playing:

python main.py


📖 How to Play

Drag and Drop / Place Blocks: Drag available shapes from the bottom panel onto the grid board.

Complete Lines: Fill an entire horizontal row or vertical column with blocks to clear it.

Earn Combos: Clear multiple lines at once to gain exponential bonus points.

Avoid Getting Stuck: Plan your moves ahead! The game ends when no available blocks can fit onto the remaining board space.

🗺️ Roadmap & Upcoming Features

[ ] Add multiple difficulty levels (Easy, Medium, Hard).

[ ] Add power-ups (e.g., Hammer to clear single blocks, Bomb to clear 3x3 areas).

[ ] Global Leaderboard support via a web API.

[ ] Customizable theme styles (Dark Mode, Neon, Classic Wood).

🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated!

If you want to contribute:

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

Reporting Bugs & Requesting Features

Feel free to open an issue on the Issues Page to report bugs or suggest new features.
