from __future__ import annotations

import argparse
from socket import AF_INET, SOCK_STREAM, socket


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args(argv)

    is_open = check_port(args.host, args.port, args.timeout)

    if is_open:
        print(f"Port {args.port} is open")
        return 0
    else:
        print(f"Port {args.port} is not open")
        return 1


def check_port(host: str, port: int, timeout: float) -> bool:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0


if __name__ == "__main__":
    exit(main())
