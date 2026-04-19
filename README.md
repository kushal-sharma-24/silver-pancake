# silver-pancake

## Chess Game

A terminal-based chess game where you play as White against a heuristic bot (Black).

### How to Play

\\ash
python chess.py
\\n
Enter moves in algebraic notation (e.g., \e2e4\, \d7d5\).

### Commands
- Type a move like \e2e4\ to move
- \moves\ - show all legal moves
- \quit\ - exit the game

### Bot Strategy
The bot uses a heuristic evaluation with piece-square tables and material counting. It evaluates each legal move once and picks the best — no brute force, no deep search.
