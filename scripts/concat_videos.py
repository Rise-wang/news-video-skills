#!/usr/bin/env python3
"""Concatenate MP4 clips with ffmpeg.

Default mode uses ffmpeg's concat demuxer with stream copy. If clips have
different codecs, dimensions, or frame rates, pass --reencode.
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    process = subprocess.run(command, text=True, capture_output=True)
    if process.returncode != 0:
        if process.stdout:
            print(process.stdout, file=sys.stderr)
        if process.stderr:
            print(process.stderr, file=sys.stderr)
        raise SystemExit(process.returncode)


def ffprobe_duration(path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    process = subprocess.run(command, text=True, capture_output=True)
    if process.returncode != 0:
        return 0.0
    try:
        return float(process.stdout.strip())
    except ValueError:
        return 0.0


def write_concat_list(clips: list[Path]) -> str:
    handle = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    with handle:
        for clip in clips:
            escaped = str(clip.resolve()).replace("'", "'\\''")
            handle.write(f"file '{escaped}'\n")
    return handle.name


def build_command(list_file: str, out: Path, reencode: bool) -> list[str]:
    base = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file]
    if reencode:
        return base + [
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(out),
        ]
    return base + ["-c", "copy", str(out)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Concatenate ordered MP4 clips.")
    parser.add_argument("--clips", nargs="+", required=True, help="Ordered clip paths.")
    parser.add_argument("--out", required=True, help="Output MP4 path.")
    parser.add_argument(
        "--reencode",
        action="store_true",
        help="Re-encode clips before concatenation for codec/dimension mismatches.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    clips = [Path(p) for p in args.clips]
    missing = [str(p) for p in clips if not p.exists()]
    if missing:
        raise SystemExit("Missing clip(s): " + ", ".join(missing))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    list_file = write_concat_list(clips)
    try:
        run(build_command(list_file, out, args.reencode))
    finally:
        try:
            os.unlink(list_file)
        except OSError:
            pass

    duration = ffprobe_duration(out)
    if not out.exists() or out.stat().st_size == 0 or duration <= 0:
        raise SystemExit(f"Output failed validation: {out}")

    clip_list = ", ".join(shlex.quote(str(p)) for p in clips)
    print(f"Created {out} from {len(clips)} clips ({duration:.2f}s): {clip_list}")


if __name__ == "__main__":
    main()
