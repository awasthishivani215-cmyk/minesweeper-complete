#!/usr/bin/python3
"""
Test if agent can actually detect mines
"""
from minesweeper_agent import MinesweeperPlayer

def test_mine_detection():
    """Test the agent's mine detection capabilities"""
    
    print("\n" + "="*70)
    print("🔬 TESTING MINE DETECTION")
    print("="*70)
    
    player = MinesweeperPlayer()
    
    # Test 1: Board with obvious safe move
    print("\n📋 TEST 1: Safe cell detection")
    game1 = {
        "board": [
            ["1", ".", "."],
            [".", ".", "."],
            [".", ".", "."]
        ],
        "rows": 3, "cols": 3, "mines": 2
    }
    
    print("Board:")
    for row in game1["board"]:
        print("  " + " ".join(str(c) for c in row))
    
    action1, _, _ = player.play_action(game1, tgps_show=True)
    print(f"🤖 Agent chooses: {action1}")
    
    # Test 2: Board with obvious mine
    print("\n📋 TEST 2: Mine detection (should flag)")
    game2 = {
        "board": [
            ["1", "1", "1"],
            ["1", ".", "1"],
            ["1", "1", "1"]
        ],
        "rows": 3, "cols": 3, "mines": 1
    }
    
    print("Board (center is likely a mine):")
    for row in game2["board"]:
        print("  " + " ".join(str(c) for c in row))
    
    action2, _, _ = player.play_action(game2, tgps_show=True)
    print(f"🤖 Agent chooses: {action2}")
    
    # Test 3: Multiple moves
    print("\n📋 TEST 3: 5 moves analysis")
    game3 = {
        "board": [
            [".", ".", ".", "."],
            [".", "2", "1", "."],
            [".", ".", ".", "."],
            [".", ".", ".", "."]
        ],
        "rows": 4, "cols": 4, "mines": 3
    }
    
    for i in range(5):
        action, _, _ = player.play_action(game3, tgps_show=False)
        print(f"Move {i+1}: {action}")

if __name__ == "__main__":
    test_mine_detection()