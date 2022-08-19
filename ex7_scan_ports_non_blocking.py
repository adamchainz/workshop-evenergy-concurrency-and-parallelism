from __future__ import annotations

import argparse
import time
from errno import EINPROGRESS
from fcntl import F_GETFL, F_SETFL, fcntl
from os import O_NONBLOCK
from select import select
from socket import AF_INET, SO_ERROR, SOCK_STREAM, SOL_SOCKET, SocketType, socket


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

    # Open all sockets, and filter out those that immediately errored
    socks: list[SocketType] = [
        s
        for port in range(args.min_port, args.max_port + 1)
        if (s := open_port(args.host, port)) is not None
    ]

    # Wait for the timeout
    time.sleep(args.timeout)

    # Request status of our sockets from the OS
    _readable, writeable, _errored = select([], socks, [], 0)

    # Sockets signaled as writeable have something to report
    for sock in writeable:
        error = sock.getsockopt(SOL_SOCKET, SO_ERROR)
        if error == 0:
            # No error means it connected
            _ip, port = sock.getpeername()
            print(f"Port {port} is open")

    # Close all sockets
    for sock in socks:
        sock.close()

    duration = (time.perf_counter_ns() - start) / 1e9
    print(f"Completed scan in {duration} seconds")

    return 0


def open_port(host: str, port: int) -> SocketType | None:
    sock = socket(AF_INET, SOCK_STREAM)

    # Make socket non-blocking
    flags = fcntl(sock, F_GETFL)
    fcntl(sock, F_SETFL, flags | O_NONBLOCK)

    # Start connecting to destination
    result = sock.connect_ex((host, port))
    # Connecting may instantly fail
    if result not in (0, EINPROGRESS):
        sock.close()
        return None
    return sock


if __name__ == "__main__":
    exit(main())
