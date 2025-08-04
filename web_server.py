#!/usr/bin/env python3
"""
Simple web server to serve the User Management UI
"""

import http.server
import socketserver
import webbrowser
import os
from threading import Timer

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow requests to MCP server
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    print(f"🚀 Starting User Management Web Server...")
    print(f"📂 Serving from: {os.getcwd()}")
    print(f"🌐 Access the UI at: http://localhost:{PORT}")
    print(f"🛑 Press Ctrl+C to stop the server")
    print()
    
    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")