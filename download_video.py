import sys
from pathlib import Path


def main() -> None:
    try:
        from yt_dlp import YoutubeDL
    except Exception:
        print("yt-dlp is not installed. Run: install-req")
        sys.exit(1)

    # Prefer CLI arg if provided, else prompt
    url = sys.argv[1].strip() if len(sys.argv) > 1 else input("Enter the video URL: ").strip()
    # Allow accidental leading '@' or quotes
    if url.startswith('@'):
        url = url[1:]
    url = url.strip('"\'')
    if not url:
        print("No URL provided.")
        sys.exit(1)

    # Output folder: downloads/
    out_dir = Path("downloads")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Format selection: worstvideo+worstaudio combined when possible; fall back to worst
    ydl_opts = {
        "format": "worstvideo*+worstaudio/worst",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        # Keep it simple and quiet for beginners
        "noprogress": False,
        "quiet": False,
        "restrictfilenames": True,
        "ignoreerrors": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Saved to: {out_dir.resolve()}")
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


