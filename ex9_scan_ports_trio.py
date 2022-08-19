from __future__ import annotations

import argparse
import time

import trio


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
    async with trio.open_nursery() as nursery:
        for port in range(args.min_port, args.max_port + 1):
            nursery.start_soon(
                check_port, args.host, port, args.timeout, successful_ports
            )

    for port in successful_ports:
        print(f"Port {port} is open")

    duration = (time.perf_counter_ns() - start) / 1e9
    print(f"Completed scan in {duration} seconds")

    return 0


async def check_port(
    host: str, port: int, timeout: float, successful_ports: list[int]
) -> None:
    with trio.move_on_after(timeout):
        await trio.open_tcp_stream(host, port)
        successful_ports.append(port)


if __name__ == "__main__":
    exit(trio.run(main))
