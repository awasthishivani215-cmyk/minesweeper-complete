#!/usr/bin/python3
"""
Professional Minesweeper Server
"""
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from minesweeper_agent import MinesweeperPlayer

class AgentHandler(BaseHTTPRequestHandler):
    player = None
    
    def do_POST(self):
        if self.path == '/play':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request = json.loads(post_data)
                game_state = request.get('game_state')
                
                if not game_state:
                    self.send_error(400, "Missing game_state")
                    return
                
                print(f"\n🎮 Processing {game_state['rows']}x{game_state['cols']} board...")
                
                # Professional mine analysis
                action, tokens, time_taken = self.player.play_action(game_state, tgps_show=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {
                    'action': action,
                    'analysis_time': time_taken,
                    'status': 'success'
                }
                
                print(f"✅ Move: {action}")
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_error(500, str(e))
        else:
            self.send_error(404)
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'healthy',
                'model': 'Qwen2.5-0.5B',
                'capabilities': ['mine_detection', 'flagging', 'probability_analysis']
            }).encode())

def main():
    parser = argparse.ArgumentParser(description='Professional Minesweeper Server')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    
    print("🚀 Starting Professional Minesweeper Server...")
    AgentHandler.player = MinesweeperPlayer()
    
    server = HTTPServer((args.host, args.port), AgentHandler)
    print(f"✅ Server running at http://{args.host}:{args.port}")
    print(f"📊 Model: Qwen2.5-0.5B (400MB) with mine detection")
    print(f"🎯 Capabilities: Safe cell detection, mine flagging, probability analysis")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == '__main__':
    main()