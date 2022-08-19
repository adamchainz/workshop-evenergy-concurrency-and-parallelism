from __future__ import annotations

import argparse
import time
from threading import Thread

COUNTER = 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=int)
    args = parser.parse_args(argv)

    threads = [Thread(target=increment) for _ in range(args.target)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Counted up to {COUNTER}")

    return 0


def increment() -> None:
    global COUNTER
    current = COUNTER
    time.sleep(0.0001)  # Simulate long calculation or I/O
    COUNTER = current + 1


if __name__ == "__main__":
    exit(main())
