#!/usr/bin/python3
"""
A script that reads stdin line by line and computes metrics.
"""

import re

def process_log(lines):
    """Computes metrics line by line"""
    total_size = 0
    status_counts = {}

    for i, line in enumerate(lines, start=1):
        match = re.match(r'^\d+\.\d+\.\d+\.\d+ - \[.*\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)$', line)
        if match:
            status_code, file_size = int(match.group(1)), int(match.group(2))
            total_size += file_size

            if status_code in status_counts:
                status_counts[status_code] += 1
            else:
                status_counts[status_code] = 1

        if i % 10 == 0:
            print_statistics(total_size, status_counts)

def print_statistics(total_size, status_counts):
    print(f"Total file size: {total_size}")
    for status_code in sorted(status_counts.keys()):
        print(f"{status_code}: {status_counts[status_code]}")
    print()

if __name__ == "__main__":
    log_lines = []
    try:
        while True:
            line = input()
            log_lines.append(line)
            if len(log_lines) % 10 == 0:
                process_log(log_lines)
                log_lines.clear()
    except KeyboardInterrupt:
        if log_lines:
            process_log(log_lines)
