import json
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.request import urlopen, Request


NAZARE_LAT = 39.60
NAZARE_LON = -9.07
TIMEZONE = "Europe/Lisbon"


def fetch_wave_height_m() -> float | None:
    # Open-Meteo Marine API (no key required)
    url = (
        "https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={NAZARE_LAT}&longitude={NAZARE_LON}"
        "&hourly=wave_height"
        f"&timezone={TIMEZONE.replace('/', '%2F')}"
    )
    req = Request(url, headers={"User-Agent": "curl/8"})
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    heights = hourly.get("wave_height", [])
    if not times or not heights:
        return None
    # Take the last available value
    return float(heights[-1]) if heights[-1] is not None else None


def build_html(height_m: float | None) -> str:
    value_text = f"{height_m:.1f} m" if height_m is not None else "N/A"
    status = "Calm" if (height_m is not None and height_m < 1.0) else (
        "Moderate" if (height_m is not None and height_m < 3.0) else "High"
    )
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Nazaré Wave Height</title>
  <meta http-equiv="refresh" content="600"> <!-- refresh every 10 minutes -->
  <style>
    body {{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: linear-gradient(180deg, #0a2540 0%, #102a43 100%);
      color: #fff; display: grid; place-items: center; min-height: 100vh; margin: 0;
    }}
    .card {{
      background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
      border-radius: 16px; padding: 28px 32px; text-align: center; backdrop-filter: blur(6px);
      box-shadow: 0 12px 28px rgba(0,0,0,0.25);
    }}
    .title {{ font-size: 18px; letter-spacing: 0.4px; opacity: 0.9; margin: 0 0 10px; }}
    .value {{ font-size: 56px; font-weight: 700; margin: 8px 0; }}
    .status {{ font-size: 14px; opacity: 0.9; margin-top: 6px; }}
    .note {{ font-size: 12px; opacity: 0.7; margin-top: 16px; }}
  </style>
  <link rel="icon" href="data:," />
  <meta name="description" content="Live wave height in Nazaré (Open-Meteo Marine)." />
  <meta property="og:title" content="Nazaré Wave Height" />
  <meta property="og:description" content="Current wave height at Nazaré, Portugal." />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="en_US" />
  <meta name="theme-color" content="#0a2540" />
  <script>console.log('Generated at', new Date().toISOString())</script>
  <script type="application/ld+json">{{
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "Nazaré Wave Height",
    "description": "Current significant wave height for Nazaré (Open-Meteo Marine).",
    "license": "https://open-meteo.com/",
    "creator": {{"@type": "Organization", "name": "Open-Meteo"}}
  }}</script>
  <meta name="robots" content="noindex" />
  <meta http-equiv="Cache-Control" content="no-store" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script>document.addEventListener('visibilitychange',()=>{{ if(!document.hidden) location.reload(); }});</script>
</head>
<body>
  <div class="card" role="region" aria-label="Nazaré Wave Height">
    <p class="title">Nazaré Wave Height (significant)</p>
    <p class="value" aria-live="polite">{value_text}</p>
    <p class="status">Condition: {status}</p>
    <p class="note">Source: Open-Meteo Marine • Auto-refreshes every 10 minutes</p>
  </div>
</body>
</html>
"""


def write_html(html: str, filename: str = "wave.html") -> Path:
    out = Path(filename)
    out.write_text(html, encoding="utf-8")
    return out


def serve_file(path: Path, port: int = 8000) -> None:
    # Serve current directory so the HTML is accessible at http://localhost:8000/wave.html
    httpd = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
    print(f"Serving {path.name} at http://localhost:{port}/{path.name}")
    webbrowser.open(f"http://localhost:{port}/{path.name}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


def main() -> None:
    try:
        height = fetch_wave_height_m()
    except Exception as e:
        print(f"Failed to fetch wave height: {e}")
        height = None

    html = build_html(height)
    out = write_html(html)
    print(f"Generated {out.resolve()}")

    # Optional: start a tiny local web server to view the page
    serve_file(out, port=8000)


if __name__ == "__main__":
    main()


