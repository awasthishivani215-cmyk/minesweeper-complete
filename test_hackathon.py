#!/usr/bin/python3
"""
Quick test for hackathon - FIXED
"""
from minesweeper_agent import MinesweeperPlayer

def quick_test():
    print("\n" + "="*70)
    print("🎯 TESTING MINESWEEPER AGENT")
    print("="*70)
    
    # Initialize player
    player = MinesweeperPlayer(model_size="medium")
    
    # Test different board sizes
    test_sizes = [(5,5), (8,8), (10,10)]
    
    for rows, cols in test_sizes:
        print(f"\n📋 Testing {rows}x{cols} board")
        
        # Create empty board
        board = [["." for _ in range(cols)] for _ in range(rows)]
        game = {
            "board": board,
            "rows": rows,
            "cols": cols,
            "mines": int(rows * cols * 0.2)  # 20% mines
        }
        
        # Get action
        action, _, time_taken = player.play_action(game, tgps_show=True)
        
        if action:
            print(f"✅ Action: {action}")
            print(f"⏱️  Time: {time_taken:.2f}s")
        else:
            print(f"❌ Failed")

if __name__ == "__main__":
    quick_test()