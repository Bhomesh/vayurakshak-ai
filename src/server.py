"""
VayuRakshak AI - Standalone HTTP REST API & Web Dashboard Server
Runs with zero external dependencies (Python Standard Library http.server).
Exposes the same REST API as AWS Lambda/API Gateway and serves the interactive UI.
Author: Bhomesh Razdan (Lead Architect)
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

from .lambda_handlers import (
    handler_get_stations,
    handler_estimate_hyperlocal,
    handler_get_stubble_fires,
    handler_plan_clean_route,
    handler_get_advisory,
    handler_cedar_authorize
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

class VayuRakshakHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving both REST APIs and frontend assets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Principal-Role")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        params = {k: v[0] for k, v in query.items()}

        if path.startswith("/api/"):
            event = {
                "httpMethod": "GET",
                "path": path,
                "queryStringParameters": params
            }
            if path == "/api/stations":
                res = handler_get_stations(event)
            elif path == "/api/aqi/estimate":
                res = handler_estimate_hyperlocal(event)
            elif path == "/api/stubble/fires":
                res = handler_get_stubble_fires(event)
            elif path == "/api/route/clean":
                res = handler_plan_clean_route(event)
            elif path == "/api/advisory":
                res = handler_get_advisory(event)
            else:
                res = {"statusCode": 404, "body": json.dumps({"error": f"API endpoint {path} not found"})}

            self._send_api_response(res)
            return

        # Serve static frontend files
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"

        event = {
            "httpMethod": "POST",
            "path": path,
            "body": body
        }

        if path == "/api/route/clean":
            res = handler_plan_clean_route(event)
        elif path == "/api/auth/cedar":
            res = handler_cedar_authorize(event)
        else:
            res = {"statusCode": 404, "body": json.dumps({"error": f"API endpoint {path} not found"})}

        self._send_api_response(res)

    def _send_api_response(self, res):
        self.send_response(res.get("statusCode", 200))
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        body = res.get("body", "{}")
        if isinstance(body, str):
            self.wfile.write(body.encode("utf-8"))
        else:
            self.wfile.write(json.dumps(body).encode("utf-8"))

def run_server(port: int = 8080):
    handler = VayuRakshakHandler
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"================================================================")
        print(f" [VayuRakshak AI] Standalone Server Running at http://localhost:{port}")
        print(f" Lead Architect: Bhomesh Razdan")
        print(f" Event: Bharat Builds Tour: Environmental Hacks (WeMakeDevs x AWS)")
        print(f"================================================================")
        print(f" API Endpoints:")
        print(f"  - GET  http://localhost:{port}/api/stations")
        print(f"  - GET  http://localhost:{port}/api/aqi/estimate?lat=28.7499&lon=77.1170")
        print(f"  - GET  http://localhost:{port}/api/stubble/fires")
        print(f"  - GET  http://localhost:{port}/api/route/clean?start_lat=28.7499&start_lon=77.1170&end_lat=28.6139&end_lon=77.2090")
        print(f"  - GET  http://localhost:{port}/api/advisory?group=children_students&aqi=390")
        print(f"  - POST http://localhost:{port}/api/auth/cedar")
        print(f" Frontend Dashboard: http://localhost:{port}/index.html")
        print(f"================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
