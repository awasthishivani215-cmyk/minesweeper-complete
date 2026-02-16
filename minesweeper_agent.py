#!/usr/bin/python3
"""
Minesweeper Agent - Fixed version
"""
import json
import re
import random
from pathlib import Path
from typing import Dict, Any, Optional

from minesweeper_model import MinesweeperAgent


class MinesweeperPlayer:
    """Minesweeper player with smart logic"""
    
    def __init__(self, model_size: str = "medium", **kwargs):
        print("\n" + "="*70)
        print("🎮 INITIALIZING MINESWEEPER PLAYER")
        print("="*70 + "\n")
        
        self.agent = MinesweeperAgent(model_size=model_size, **kwargs)

    def analyze_board(self, game_state: Dict) -> Dict:
        """Simple board analysis"""
        board = game_state['board']
        rows = game_state['rows']
        cols = game_state['cols']
        
        safe_cells = []
        
        # Find cells adjacent to numbers
        for r in range(rows):
            for c in range(cols):
                if str(board[r][c]).isdigit() and board[r][c] != '0':
                    # Check neighbors for safe cells
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if board[nr][nc] == '.':
                                    safe_cells.append((nr, nc))
        
        return {'safe': list(set(safe_cells))}

    def build_prompt(self, game_state: Dict) -> str:
        """Simple prompt"""
        board_str = ""
        for r in range(game_state['rows']):
            row_str = " ".join(str(game_state['board'][r][c]) for c in range(game_state['cols']))
            board_str += f"Row {r}: {row_str}\n"
        
        return f"""Minesweeper board:
{board_str}

Choose a safe cell. Output row and column numbers only.
Example: 2 3

Your move:"""

    def play_action(self, game_state: Dict, **gen_kwargs) -> tuple:
        """Generate action"""
        
        # Try smart analysis first
        analysis = self.analyze_board(game_state)
        
        if analysis['safe']:
            r, c = random.choice(analysis['safe'])
            print(f"✅ Smart move: ({r},{c})")
            return {"type": "reveal", "row": r, "col": c}, 0, 0
        
        # Use model
        print("🤔 Using AI...")
        prompt = self.build_prompt(game_state)
        response, tl, gt = self.agent.generate_response(prompt, **gen_kwargs)
        
        # Parse response
        action = self.parse_action(response, game_state)
        
        # Fallback
        if not action:
            print("⚠️ Using random move")
            action = self.random_move(game_state)
        
        return action, tl, gt

    def parse_action(self, response: str, game_state: Dict) -> Optional[Dict]:
        """Parse model response"""
        try:
            numbers = re.findall(r'\d+', response)
            if len(numbers) >= 2:
                row = int(numbers[0])
                col = int(numbers[1])
                
                if 0 <= row < game_state['rows'] and 0 <= col < game_state['cols']:
                    if game_state['board'][row][col] == '.':
                        return {"type": "reveal", "row": row, "col": col}
        except:
            pass
        return None

    def random_move(self, game_state: Dict) -> Dict:
        """Safe random move"""
        board = game_state['board']
        rows, cols = game_state['rows'], game_state['cols']
        
        # Try corners first
        corners = [(0,0), (0,cols-1), (rows-1,0), (rows-1,cols-1)]
        for r, c in corners:
            if board[r][c] == '.':
                return {"type": "reveal", "row": r, "col": c}
        
        # Try edges
        for r in range(rows):
            for c in range(cols):
                if (r == 0 or r == rows-1 or c == 0 or c == cols-1) and board[r][c] == '.':
                    return {"type": "reveal", "row": r, "col": c}
        
        # Random unrevealed
        unrevealed = [(r,c) for r in range(rows) for c in range(cols) if board[r][c] == '.']
        if unrevealed:
            r, c = random.choice(unrevealed)
            return {"type": "reveal", "row": r, "col": c}
        
        return {"type": "reveal", "row": 0, "col": 0}

    @staticmethod
    def save_action(action: Dict, file_path: str | Path) -> None:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(action, f, indent=2)


# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--game_state_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, default="outputs/action.json")
    parser.add_argument("--model_size", type=str, default="medium")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print(f"\n📂 Loading: {args.game_state_file}")
    with open(args.game_state_file, "r") as f:
        game_state = json.load(f)

    player = MinesweeperPlayer(model_size=args.model_size)
    action, tl, gt = player.play_action(game_state, tgps_show=args.verbose)

    if action:
        player.save_action(action, args.output_file)
        print(f"\n✅ Action: {action}")
    else:
        print("\n❌ Failed")