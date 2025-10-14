import sys
import time
import ctypes
from ctypes import wintypes


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


def get_cursor_pos() -> tuple[int, int]:
    point = POINT()
    if not ctypes.windll.user32.GetCursorPos(ctypes.byref(point)):
        raise OSError("GetCursorPos failed")
    return point.x, point.y


def set_cursor_pos(x: int, y: int) -> None:
    if not ctypes.windll.user32.SetCursorPos(x, y):
        raise OSError("SetCursorPos failed")


def jiggle_once(pixels: int = 2) -> None:
    x, y = get_cursor_pos()
    # Small movement right and back to avoid disrupting the user
    set_cursor_pos(x + pixels, y)
    time.sleep(0.05)
    set_cursor_pos(x, y)


def main() -> None:
    if sys.platform != "win32":
        print("This script currently supports Windows only.")
        sys.exit(1)

    interval_seconds = 30
    pixels = 2

    print("Mouse jiggler started. Press Ctrl+C to stop.")
    print(f"Every {interval_seconds}s: move {pixels}px and back to prevent sleep.")

    try:
        while True:
            jiggle_once(pixels)
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()


