from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


TAG_RE = re.compile(r"<\|([^|]+)\|>")
EMOTION_TAGS = {"HAPPY", "SAD", "ANGRY", "NEUTRAL", "FEARFUL", "DISGUSTED", "SURPRISED"}


def clean_sentence(sentence: str) -> str:
    return TAG_RE.sub("", sentence).strip()


def format_time(ms: int | float | None) -> str:
    if ms is None:
        return "??:??.???"
    seconds = float(ms) / 1000
    minutes = int(seconds // 60)
    rest = seconds - minutes * 60
    return f"{minutes:02d}:{rest:06.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create speaker and SenseVoice emotion labeled transcripts.")
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("outputs") / "labeled")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    payload = json.loads(args.json_file.read_text(encoding="utf-8"))
    items = payload if isinstance(payload, list) else [payload]
    summary = []

    for item in items:
        audio = Path(item["audio"])
        sentences = item["raw"][0].get("sentence_info", [])
        speakers = Counter()
        emotions = Counter()
        lines = []
        for sentence in sentences:
            raw = sentence.get("sentence") or sentence.get("text") or ""
            tags = TAG_RE.findall(raw)
            emotion = next((tag for tag in tags if tag in EMOTION_TAGS), "UNKNOWN")
            speaker = sentence.get("spk", "UNKNOWN")
            speakers[str(speaker)] += 1
            emotions[emotion] += 1
            lines.append(
                f"[{format_time(sentence.get('start'))}-{format_time(sentence.get('end'))}] "
                f"Speaker {speaker} | {emotion}: {clean_sentence(raw)}"
            )
        out_path = args.out_dir / f"{audio.stem}.labeled.txt"
        out_path.write_text("\n".join(lines), encoding="utf-8")
        summary.append(
            {
                "audio": str(audio),
                "segments": len(sentences),
                "speakers": dict(sorted(speakers.items())),
                "sentiments": dict(sorted(emotions.items())),
                "labeled_text": str(out_path),
            }
        )

    summary_path = args.out_dir / "label_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved labeled transcripts to {args.out_dir}")
    print(f"Saved label summary to {summary_path}")


if __name__ == "__main__":
    main()
