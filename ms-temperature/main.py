#!/usr/bin/env python3
import argparse
import json
import urllib.request
import os
import sys
import signal
from http.server import BaseHTTPRequestHandler, HTTPServer

httpd = None

def shutdown_handler(signum, frame):
    if httpd:
        print(f"Received signal {signum}, shutting down HTTP server", flush=True)
        httpd.socket.close()
    sys.exit(0)

class Handler(BaseHTTPRequestHandler):
    def _json_response(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.command == "OPTIONS":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            return

        if self.path == "/health":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return

        if self.path == "/version":
            self._json_response({
                "name": self.server.name,
                "host": self.server.host,
                "version": self.server.version
            })
            return

        if self.path == "/temperature":
            with urllib.request.urlopen(self.server.random_url + "/random") as resp:
                data = json.loads(resp.read().decode("utf-8"))

            rnd = data["random"]
            temperature = round(-10.0 + (rnd / 1000.0) * 35.0, 1)

            self._json_response({
                "name": self.server.name,
                "host": self.server.host,
                "version": self.server.version,
                "temperature": temperature,
                "randomService": {
                    "name": data["name"],
                    "host": data["host"],
                    "version": data["version"]
                }
            })
            return

        self.send_response(404)
        self.end_headers()

def main():
    global httpd
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=False, default=None)
    parser.add_argument("--version", required=False, default=None)
    parser.add_argument("--random", required=False, default='http://ms-random')
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    name = args.name
    if name is None and 'NAME' in os.environ: name = os.environ['NAME']
    if name is None: name = 'ms-temperature'

    version = args.version
    if version is None and 'VERSION' in os.environ: version = os.environ['VERSION']
    if version is None: version = '0.0.1'

    host = os.environ['HOSTNAME'] if 'HOSTNAME' in os.environ else '***'

    print(f"This is '{name}' at version '{version}', listening on port '{args.port}' on '{host}'.")

    httpd = HTTPServer(("", args.port), Handler)
    httpd.name = name
    httpd.version = version
    httpd.host = host
    httpd.random_url = args.random
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    httpd.serve_forever()

if __name__ == "__main__":
    main()
