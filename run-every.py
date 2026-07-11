#!/usr/bin/env python3
"""Run a shell command repeatedly every N minutes."""

import argparse
import subprocess
import time
import sys
from datetime import datetime


def tag() -> str:
    return "[run-every]"


def fmt_time(dt: datetime) -> str:
    return dt.strftime("%I:%M %p").lstrip("0").lower()


def run_command(cmd: str, shell: bool) -> int:
    args = cmd if shell else cmd.split()
    result = subprocess.run(args, shell=shell)
    return result.returncode


def countdown(interval_sec: float, run_count: int):
    remaining_sec = interval_sec
    while remaining_sec > 0:
        mins = int(remaining_sec / 60)
        if mins > 0:
            print(f"{tag()} {mins} minute{'s' if mins != 1 else ''} till next run,  completed {run_count}", flush=True)
            # sleep until the next whole-minute boundary
            next_tick = remaining_sec - (mins * 60 - 60) if mins > 1 else remaining_sec
            sleep_secs = min(60, next_tick)
        else:
            # less than a minute left — just wait it out silently
            sleep_secs = remaining_sec

        time.sleep(sleep_secs)
        remaining_sec -= sleep_secs


def main():
    parser = argparse.ArgumentParser(
        description="Run a command every N minutes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  run-every.py 5 'adb logcat -d | grep ERROR'
  run-every.py 1 --count 10 'date'
  run-every.py 0.5 --stop-on-fail 'ping -c1 8.8.8.8'""",
    )
    parser.add_argument("interval", type=float, help="Interval in minutes")
    parser.add_argument("command", help="Command to run (use quotes for complex commands)")
    parser.add_argument("--count", "-n", type=int, default=0, help="Max runs (0 = unlimited)")
    parser.add_argument("--stop-on-fail", "-f", action="store_true", help="Stop if command exits non-zero")
    parser.add_argument("--no-shell", action="store_true", help="Don't use shell (safer, no pipes/globs)")
    args = parser.parse_args()

    interval_sec = args.interval * 60
    use_shell = not args.no_shell
    run_count = 0

    print(f"{tag()} Running every {args.interval}m: {args.command}")
    if args.count:
        print(f"{tag()} Max runs: {args.count}")
    print(f"{tag()} Press Ctrl+C to stop\n")

    try:
        while True:
            run_count += 1
            ts = fmt_time(datetime.now())
            print(f"{tag()} {ts} - starting run #{run_count}", flush=True)
            rc = run_command(args.command, use_shell)

            ts = fmt_time(datetime.now())
            print(f"{tag()} {ts} - job completed with status {rc}", flush=True)

            if args.stop_on_fail and rc != 0:
                print(f"{tag()} Non-zero exit, stopping.")
                sys.exit(rc)

            if args.count and run_count >= args.count:
                print(f"{tag()} Reached {args.count} runs, done.")
                break

            countdown(interval_sec, run_count)

    except KeyboardInterrupt:
        print(f"\n{tag()} Stopped after {run_count} run(s).")


if __name__ == "__main__":
    main()
