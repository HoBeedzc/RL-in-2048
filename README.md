# RL in 2048 Game - Python GUI Implementation

![Game Screenshot](screenshot.png) <!-- 建议添加实际截图 -->

A classic 2048 game implementation with smooth animations using Python Tkinter.

## ✨ Features
- 🎮 Classic 2048 gameplay mechanics
- 🖥️ Tkinter-based graphical interface
- ✨ Smooth tile movement & merge animations
- 🎨 Color-coded tiles with automatic theme adjustment
- 📊 Real-time score tracking
- ⏳ Automatic game over detection
- ⌨️ Keyboard controls with shortcuts

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- Tkinter library (usually included in Python standard library)

### Installation
```bash
git clone https://github.com/yourusername/RL-in-2048.git
cd RL-in-2048
```

### Running the Game
```bash
python 2048_gui.py
```

## 🕹️ Controls
| Key          | Action         |
|--------------|----------------|
| ↑ ↓ ← →      | Move tiles     |
| Q            | Quit game      |
| **Objective**| Reach 2048!    |

## 🛠️ Implementation Details
- **OOP Architecture**: `Game2048` class manages game state and UI
- **Animation System**:
  - Smooth tile movement (5px/frame)
  - Scale-up effect for new tiles
  - Merge animation with instantiation
- **Color Scheme**: 14-tier color coding (up to 8192)
- **Efficient Algorithms**:
  - Grid movement optimization
  - Game over detection in O(n^2)
  - Direction-aware merge logic

## 📂 Project Structure
```
RL-in-2048/
├── 2048_gui.py     # Main game implementation
├── README.md       # Documentation
└── .gitignore      # Version control config
```

## 🔮 Future Enhancements
- [ ] High score tracking system
- [ ] Undo/Redo functionality
- [ ] Sound effects integration
- [ ] Adaptive grid sizing
- [ ] AI solver implementation

## 📜 License
Distributed under MIT License. See `LICENSE` for more information.
