from __future__ import annotations

import argparse
import time
from multiprocessing import Process, Queue
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

    # Start one process per port
    processes: list[Process] = []
    successful_ports: Queue[int] = Queue()
    for port in range(args.min_port, args.max_port + 1):
        # TODO
        port

    # Wait for all processes to finish
    for process in processes:
        # TODO
        process

    # Output results
    while not successful_ports.empty():
        port = successful_ports.get()
        print(f"Port {port} is open")

    duration = (time.perf_counter_ns() - start) / 1e9
    print(f"Completed scan in {duration} seconds")
    return 0


def check_port(
    host: str, port: int, timeout: float, successful_ports: Queue[int]
) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            successful_ports.put(port)


if __name__ == "__main__":
    exit(main())
