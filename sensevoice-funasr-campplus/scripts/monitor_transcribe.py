from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

import psutil


def process_tree(root: psutil.Process) -> list[psutil.Process]:
    try:
        return [root, *root.children(recursive=True)]
    except psutil.Error:
        return [root]


def sample(root: psutil.Process, cpu_state: dict[int, tuple[float, float]]) -> dict:
    cpu = 0.0
    rss = vms = read_bytes = write_bytes = 0
    procs = process_tree(root)
    now = time.time()
    for proc in procs:
        try:
            times = proc.cpu_times()
            cpu_time = times.user + times.system
            previous = cpu_state.get(proc.pid)
            if previous:
                previous_wall, previous_cpu = previous
                wall_delta = max(now - previous_wall, 1e-6)
                cpu += max(cpu_time - previous_cpu, 0.0) / wall_delta * 100.0
            cpu_state[proc.pid] = (now, cpu_time)
            mem = proc.memory_info()
            rss += mem.rss
            vms += mem.vms
            try:
                io = proc.io_counters()
                read_bytes += io.read_bytes
                write_bytes += io.write_bytes
            except (psutil.AccessDenied, AttributeError):
                pass
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    live_pids = {proc.pid for proc in procs}
    for pid in list(cpu_state):
        if pid not in live_pids:
            del cpu_state[pid]
    return {
        "timestamp": now,
        "process_count": len(procs),
        "cpu_percent": round(cpu, 2),
        "rss_mb": round(rss / 1024 / 1024, 2),
        "vms_mb": round(vms / 1024 / 1024, 2),
        "read_mb": round(read_bytes / 1024 / 1024, 2),
        "write_mb": round(write_bytes / 1024 / 1024, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SenseVoice transcription and record resource usage.")
    parser.add_argument("audio", nargs="+", type=Path)
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--script", type=Path, default=Path(__file__).with_name("transcribe_sensevoice.py"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs") / "monitored")
    parser.add_argument("--sample-interval-s", type=float, default=5.0)
    parser.add_argument("--offline", action="store_true", help="Use local cached model directories only.")
    parser.add_argument("--preview-chars", type=int, default=1000, help="Transcript characters to print into transcribe.log; use 0 for private logs.")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    project_dir = args.project_dir.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(args.script.resolve()),
        "--project-dir",
        str(project_dir),
        "--speaker",
        "--out-dir",
        str(out_dir),
        "--preview-chars",
        str(args.preview_chars),
    ]
    if args.offline:
        command.append("--offline")
    command.extend(str(path.resolve()) for path in args.audio)

    started = time.time()
    rows = []
    cpu_state = {}
    log_path = out_dir / "transcribe.log"
    with log_path.open("w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            command,
            cwd=str(project_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        root = psutil.Process(proc.pid)
        for child in process_tree(root):
            try:
                child.cpu_percent(interval=None)
            except psutil.Error:
                pass
        next_sample = 0.0
        while proc.poll() is None:
            line = proc.stdout.readline() if proc.stdout else ""
            if line:
                print(line, end="")
                log_file.write(line)
                log_file.flush()
            now = time.time()
            if now >= next_sample:
                row = sample(root, cpu_state)
                row["elapsed_s"] = round(now - started, 2)
                rows.append(row)
                next_sample = now + args.sample_interval_s
        if proc.stdout:
            for line in proc.stdout:
                print(line, end="")
                log_file.write(line)

    samples_path = out_dir / "resource_samples.csv"
    if rows:
        with samples_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    ended = time.time()
    summary = {
        "command": command,
        "returncode": proc.returncode,
        "started_at": started,
        "ended_at": ended,
        "wall_s": round(ended - started, 3),
        "sample_interval_s": args.sample_interval_s,
        "samples": len(rows),
        "peak_cpu_percent": max((row["cpu_percent"] for row in rows), default=0),
        "avg_cpu_percent": round(sum(row["cpu_percent"] for row in rows) / len(rows), 2) if rows else 0,
        "peak_rss_mb": max((row["rss_mb"] for row in rows), default=0),
        "peak_vms_mb": max((row["vms_mb"] for row in rows), default=0),
        "final_read_mb": rows[-1]["read_mb"] if rows else 0,
        "final_write_mb": rows[-1]["write_mb"] if rows else 0,
        "samples_csv": str(samples_path),
        "transcribe_log": str(log_path),
    }
    (out_dir / "resource_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResource summary saved to {out_dir / 'resource_summary.json'}")
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
