from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from socket import AF_INET, SOCK_STREAM, socket


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("min_port", type=int)
    parser.add_argument("max_port", type=int)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args(argv)
    if args.max_port < args.min_port:
        parser.error("max_port should be greater than or equal to min_port")

    start = time.perf_counter_ns()

    with ThreadPoolExecutor() as executor:
        future_to_port = {
            executor.submit(check_port, args.host, port, args.timeout): port
            for port in range(args.min_port, args.max_port + 1)
        }

        for future in as_completed(future_to_port):
            port = future_to_port.pop(future)
            if future.result():
                print(f"Port {port} is open")

    duration = (time.perf_counter_ns() - start) / 1e9
    print(f"Completed scan in {duration} seconds")

    return 0


def check_port(host: str, port: int, timeout: float) -> bool:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0


if __name__ == "__main__":
    main()
