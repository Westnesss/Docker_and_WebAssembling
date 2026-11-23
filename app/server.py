"""
Docker Container PoC - FICA UCE
Minimal, zero-dependency Python 3 HTTP server (standard library only).

Routes:
  GET /            -> index.html (dashboard)
  GET /api/status  -> JSON container metadata
  GET /health      -> liveness probe used by the Docker HEALTHCHECK
"""

import json
import os
import platform
import socket
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))


def _os_name() -> str:
    """Return the distro name from /etc/os-release (e.g. 'Alpine Linux v3.20')."""
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip('"')
    except OSError:
        pass
    return platform.system()


def container_status() -> dict:
    return {
        "status": "running",
        "hostname": socket.gethostname(),
        "platform": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "os": _os_name(),
        "runtime": f"Python {platform.python_version()}",
        "in_container": Path("/.dockerenv").exists(),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "DockerPoC/1.0"

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, data: dict) -> None:
        self._send(code, json.dumps(data, indent=2).encode("utf-8"), "application/json")

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, INDEX_FILE.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/status":
            self._json(200, container_status())
        elif path == "/health":
            self._json(200, {"status": "ok"})
        else:
            self._json(404, {"error": "not found", "path": path})

    def log_message(self, fmt: str, *args) -> None:
        # Write access logs to stdout so `docker logs` shows them
        print(f"{self.address_string()} - {fmt % args}", flush=True)


def main() -> None:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Docker PoC server running on http://{HOST}:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
