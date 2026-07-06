from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from time import perf_counter


DEFAULT_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac", ".opus"}


def configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def configure_caches(project_dir: Path) -> None:
    cache_dir = project_dir / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MODELSCOPE_CACHE", str(cache_dir / "modelscope"))
    os.environ.setdefault("MODELSCOPE_HOME", str(cache_dir / "modelscope-home"))
    os.environ.setdefault("HF_HOME", str(cache_dir / "huggingface"))
    os.environ.setdefault("TORCH_HOME", str(cache_dir / "torch"))


def cached_model_dir(project_dir: Path, name: str) -> Path:
    return project_dir / ".cache" / "modelscope" / "iic" / name


def require_model_dir(path: Path, label: str) -> str:
    if not path.exists():
        raise SystemExit(f"Missing {label} model directory for offline mode: {path}")
    return str(path)


def find_audio_files(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_file() and path.suffix.lower() in DEFAULT_AUDIO_EXTENSIONS)


def write_outputs(items: list[dict], out_dir: Path) -> None:
    (out_dir / "sensevoice_results.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    (out_dir / "sensevoice_results.txt").write_text(
        "\n\n".join(f"=== {Path(item['audio']).name} ===\n{item['text']}" for item in items),
        encoding="utf-8",
    )


def transcribe_file(model, audio_path: Path, args: argparse.Namespace) -> dict:
    from funasr.utils.postprocess_utils import rich_transcription_postprocess

    start = perf_counter()
    result = model.generate(
        input=str(audio_path),
        cache={},
        language=args.language,
        use_itn=not args.no_itn,
        batch_size_s=args.batch_size_s,
        merge_vad=True,
        merge_length_s=args.merge_length_s,
    )
    elapsed_s = perf_counter() - start
    raw_text = result[0].get("text", "") if result else ""
    return {
        "audio": str(audio_path),
        "elapsed_s": round(elapsed_s, 3),
        "text": rich_transcription_postprocess(raw_text),
        "raw": result,
    }


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Transcribe audio with SenseVoiceSmall + FunASR.")
    parser.add_argument("audio", nargs="*", type=Path)
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--batch-size-s", type=int, default=60)
    parser.add_argument("--merge-length-s", type=int, default=15)
    parser.add_argument("--max-segment-ms", type=int, default=30000)
    parser.add_argument("--speaker", action="store_true", help="Enable CAM++ speaker diarization.")
    parser.add_argument("--offline", action="store_true", help="Use local cached model directories only; do not ask ModelScope for metadata/downloads.")
    parser.add_argument("--model-dir", type=Path, default=None, help="Local SenseVoiceSmall model directory.")
    parser.add_argument("--vad-model-dir", type=Path, default=None, help="Local FSMN-VAD model directory.")
    parser.add_argument("--spk-model-dir", type=Path, default=None, help="Local CAM++ speaker model directory.")
    parser.add_argument("--preview-chars", type=int, default=1000, help="Transcript characters to print to stdout; use 0 for private logs.")
    parser.add_argument("--no-itn", action="store_true")
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    out_dir = (args.out_dir or project_dir / "outputs").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    configure_caches(project_dir)

    audio_files = [path.resolve() for path in args.audio] or find_audio_files(project_dir)
    if not audio_files:
        raise SystemExit("No audio files found.")

    from funasr import AutoModel

    if args.offline:
        model_value = require_model_dir(args.model_dir or cached_model_dir(project_dir, "SenseVoiceSmall"), "SenseVoiceSmall")
        vad_value = require_model_dir(
            args.vad_model_dir or cached_model_dir(project_dir, "speech_fsmn_vad_zh-cn-16k-common-pytorch"),
            "FSMN-VAD",
        )
        spk_value = require_model_dir(
            args.spk_model_dir or cached_model_dir(project_dir, "speech_campplus_sv_zh-cn_16k-common"),
            "CAM++",
        )
    else:
        model_value = str(args.model_dir.resolve()) if args.model_dir else "iic/SenseVoiceSmall"
        vad_value = str(args.vad_model_dir.resolve()) if args.vad_model_dir else "fsmn-vad"
        spk_value = str(args.spk_model_dir.resolve()) if args.spk_model_dir else "cam++"

    config = {
        "model": model_value,
        "trust_remote_code": True,
        "vad_model": vad_value,
        "vad_kwargs": {"max_single_segment_time": args.max_segment_ms},
        "device": args.device,
        "disable_update": True,
        "check_latest": False,
    }
    if args.speaker:
        config["spk_model"] = spk_value

    model = AutoModel(**config)
    outputs = []
    for audio_path in audio_files:
        item = transcribe_file(model, audio_path, args)
        outputs.append(item)
        stem = audio_path.stem
        (out_dir / f"{stem}.json").write_text(json.dumps(item, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        (out_dir / f"{stem}.txt").write_text(item["text"], encoding="utf-8")
        write_outputs(outputs, out_dir)
        print(f"\n=== {audio_path.name} ({item['elapsed_s']}s) ===")
        if args.preview_chars > 0:
            preview = item["text"][: args.preview_chars]
            print(preview + ("..." if len(item["text"]) > len(preview) else ""))
        print(f"Saved {out_dir / (stem + '.json')} and {out_dir / (stem + '.txt')}")

    print(f"\nSaved {out_dir / 'sensevoice_results.json'} and {out_dir / 'sensevoice_results.txt'}")


if __name__ == "__main__":
    main()
