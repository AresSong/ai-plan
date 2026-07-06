---
name: sensevoice-funasr-campplus
description: Set up, verify, and run a lean CPU-only SenseVoiceSmall + FunASR + CAM++ transcription workflow for local audio files. Use when the user wants to install or test FunAudioLLM/SenseVoice, transcribe audio on a laptop without GPU, capture resource usage, or export speaker-labeled and SenseVoice emotion/sentiment-labeled transcripts.
---

# SenseVoice + FunASR + CAM++

Use the bundled scripts from this skill directory. They are self-contained and operate on a target project directory; they do not need to be copied.

## Workflow

1. Ensure the environment:

```powershell
python scripts/ensure_env.py --project-dir <project-dir>
```

Prefer an existing usable Python if the user provides `--python`. Otherwise use `--env-kind auto`:
check `<project-dir>/.venv`, then `<project-dir>/.conda`, then create `<project-dir>/.venv` from Python 3.10/3.11. Use `--env-kind conda` only when requested or when a conda env already exists. It installs only missing packages: `torch`, `torchaudio` from the CPU PyTorch wheel index, then `funasr`, `modelscope`, `more-itertools`, `psutil`, and `soundfile`.

Common environment commands:

```powershell
python scripts/ensure_env.py --project-dir <project-dir> --env-kind venv --seed-python C:\Path\To\Python310\python.exe
python scripts/ensure_env.py --project-dir <project-dir> --python <project-dir>\.venv\Scripts\python.exe
python scripts/ensure_env.py --project-dir <project-dir> --env-kind conda
```

2. Run transcription:

```powershell
<project-dir>\.venv\Scripts\python.exe scripts/transcribe_sensevoice.py --project-dir <project-dir> --speaker <audio files>
```

Use `--speaker` to enable CAM++ (`spk_model="cam++"`). Do not add `ct-punc` by default for SenseVoice; it can trigger timestamp/punctuation mismatch failures. SenseVoice emotion tags are already present in `sentence_info` when the model emits them.

For sensitive audio, run once in an approved network environment to populate `<project-dir>/.cache/modelscope`, then use local-only mode:

```powershell
<project-dir>\.venv\Scripts\python.exe scripts/transcribe_sensevoice.py --project-dir <project-dir> --speaker --offline --preview-chars 0 <audio files>
```

`--offline` resolves SenseVoiceSmall, FSMN-VAD, and CAM++ from `<project-dir>/.cache/modelscope/iic` and avoids ModelScope metadata/download checks. `--preview-chars 0` prevents transcript text from being echoed to stdout or captured in monitor logs.

3. Record resource usage when requested:

```powershell
<project-dir>\.venv\Scripts\python.exe scripts/monitor_transcribe.py --project-dir <project-dir> --out-dir <project-dir>\outputs\monitored --offline --preview-chars 0 <audio files>
```

This writes `resource_summary.json`, `resource_samples.csv`, `transcribe.log`, and transcription outputs.

4. Export labeled transcript:

```powershell
<project-dir>\.venv\Scripts\python.exe scripts/label_sensevoice_output.py <project-dir>\outputs\monitored\sensevoice_results.json --out-dir <project-dir>\outputs\monitored\labeled
```

Labels use CAM++ speaker IDs and SenseVoice emotion tags (`HAPPY`, `NEUTRAL`, etc.). Use `UNKNOWN` when SenseVoice did not emit an emotion tag.

## Notes

- Keep ModelScope/HuggingFace/Torch caches inside `<project-dir>/.cache`.
- Prefer Python 3.10 or 3.11 for Windows CPU PyTorch/FunASR reliability.
- Use CPU by default (`--device cpu`) unless the user explicitly asks for GPU.
- Save full raw JSON as well as cleaned text so speaker and emotion labels can be regenerated without rerunning inference.
- Treat `outputs/**/*.txt`, `outputs/**/*.json`, and `transcribe.log` as sensitive because they can contain transcript text, speaker labels, emotion tags, file names, and timing metadata.
- If PowerShell prints profile execution-policy warnings after commands, ignore them unless the Python command itself fails.
