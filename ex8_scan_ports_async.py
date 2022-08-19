from __future__ import annotations

import argparse
import asyncio
import time
from socket import AF_INET, SOCK_STREAM, socket


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("min_port", type=int)
    parser.add_argument("max_port", type=int)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args(argv)
    if args.max_port < args.min_port:
        parser.error("max_port should be greater than or equal to min_port")

    start = time.perf_counter_ns()

    successful_ports: list[int] = []
    tasks = [
        check_port(args.host, port, args.timeout, successful_ports)
        for port in range(args.min_port, args.max_port + 1)
    ]
    await asyncio.gather(*tasks)

    for port in successful_ports:
        print(f"Port {port} is open")

    duration = (time.perf_counter_ns() - start) / 1e9
    print(f"Completed scan in {duration} seconds")

    return 0


async def check_port(
    host: str, port: int, timeout: float, successful_ports: list[int]
) -> None:
    try:
        future = asyncio.open_connection(host=host, port=port)
        read, write = await asyncio.wait_for(future, timeout=timeout)
        successful_ports.append(port)
        write.close()
    except OSError:
        # pass on port closure
        pass
    except asyncio.TimeoutError:
        # Port is closed, skip and continue
        pass


async def check_port_badly(
    host: str, port: int, timeout: float, successful_ports: list[int]
) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            successful_ports.append(port)


if __name__ == "__main__":
    exit(asyncio.run(main()))
