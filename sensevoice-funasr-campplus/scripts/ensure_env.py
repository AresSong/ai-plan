from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


RUNTIME_PACKAGES = ["funasr", "modelscope", "more-itertools", "psutil", "soundfile"]
TORCH_PACKAGES = ["torch==2.5.1+cpu", "torchaudio==2.5.1+cpu"]


def run(command: list[str], cwd: Path) -> None:
    print("+ " + " ".join(command))
    subprocess.check_call(command, cwd=str(cwd))


def conda_python_exe(env_dir: Path) -> Path:
    if os.name == "nt":
        return env_dir / "python.exe"
    return env_dir / "bin" / "python"


def venv_python_exe(env_dir: Path) -> Path:
    if os.name == "nt":
        return env_dir / "Scripts" / "python.exe"
    return env_dir / "bin" / "python"


def env_python_exe(env_dir: Path) -> Path | None:
    for candidate in (venv_python_exe(env_dir), conda_python_exe(env_dir)):
        if candidate.exists():
            return candidate
    return None


def can_import(py: Path, module: str) -> bool:
    result = subprocess.run(
        [str(py), "-c", f"import {module}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def module_name(package: str) -> str:
    return {"more-itertools": "more_itertools"}.get(package, package)


def python_version(py: Path) -> tuple[int, int, int]:
    code = "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    result = subprocess.check_output([str(py), "-c", code], text=True).strip()
    major, minor, micro = result.split(".")
    return int(major), int(minor), int(micro)


def ensure_supported_python(py: Path) -> None:
    major, minor, _ = python_version(py)
    if (major, minor) not in {(3, 10), (3, 11)}:
        raise SystemExit(
            f"{py} is Python {major}.{minor}. Use Python 3.10 or 3.11 for the most reliable "
            "CPU PyTorch/FunASR Windows setup."
        )


def is_supported_python(py: Path) -> bool:
    try:
        ensure_supported_python(py)
        return True
    except (subprocess.SubprocessError, SystemExit):
        return False


def find_python() -> Path | None:
    for name in ("python", "python3"):
        path = shutil.which(name)
        if path:
            candidate = Path(path)
            try:
                ensure_supported_python(candidate)
                return candidate
            except (subprocess.SubprocessError, SystemExit):
                pass
    return None


def ensure_venv_env(project_dir: Path, env_dir: Path, seed_python: Path | None) -> Path:
    py = venv_python_exe(env_dir)
    if py.exists():
        return py

    seed = seed_python or find_python()
    if seed is None:
        raise SystemExit(
            "Could not find Python 3.10/3.11 to create .venv. Install Python 3.10/3.11, "
            "pass --seed-python, pass --python to an existing env, or use --env-kind conda."
        )
    ensure_supported_python(seed)
    run([str(seed), "-m", "venv", str(env_dir)], project_dir)
    return py


def ensure_conda_env(project_dir: Path, env_dir: Path) -> Path:
    py = conda_python_exe(env_dir)
    if py.exists():
        return py

    conda = shutil.which("conda")
    if conda is None:
        candidates = [
            r"D:\ProgramData\anaconda3\Scripts\conda.exe",
            r"C:\ProgramData\anaconda3\Scripts\conda.exe",
            str(Path.home() / "anaconda3" / "Scripts" / "conda.exe"),
            str(Path.home() / "miniconda3" / "Scripts" / "conda.exe"),
        ]
        conda = next((path for path in candidates if Path(path).exists()), None)
    if conda is None:
        raise SystemExit("Could not find conda. Install Anaconda/Miniconda or pass --python to an existing environment.")

    run([conda, "create", "-p", str(env_dir), "python=3.10", "-y"], project_dir)
    return py


def resolve_python(args: argparse.Namespace, project_dir: Path) -> Path:
    if args.python:
        py = args.python.resolve()
        ensure_supported_python(py)
        return py

    if args.env_dir:
        env_dir = args.env_dir.resolve()
        existing = env_python_exe(env_dir)
        if existing:
            ensure_supported_python(existing)
            return existing
        if args.env_kind == "conda":
            return ensure_conda_env(project_dir, env_dir)
        return ensure_venv_env(project_dir, env_dir, args.seed_python.resolve() if args.seed_python else None)

    venv_dir = project_dir / ".venv"
    conda_dir = project_dir / ".conda"
    if args.env_kind in ("auto", "venv"):
        existing = env_python_exe(venv_dir)
        if existing:
            if args.env_kind == "venv":
                ensure_supported_python(existing)
                return existing
            if is_supported_python(existing):
                return existing
            print(f"Skipping unsupported existing venv Python: {existing}")
    if args.env_kind in ("auto", "conda"):
        existing = env_python_exe(conda_dir)
        if existing:
            if args.env_kind == "conda":
                ensure_supported_python(existing)
                return existing
            if is_supported_python(existing):
                return existing
            print(f"Skipping unsupported existing conda Python: {existing}")

    if args.env_kind == "conda":
        return ensure_conda_env(project_dir, conda_dir)
    return ensure_venv_env(project_dir, venv_dir, args.seed_python.resolve() if args.seed_python else None)


def ensure_packages(py: Path, project_dir: Path) -> None:
    run([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], project_dir)

    if not can_import(py, "torch") or not can_import(py, "torchaudio"):
        run(
            [
                str(py),
                "-m",
                "pip",
                "install",
                "--timeout",
                "120",
                *TORCH_PACKAGES,
                "--index-url",
                "https://download.pytorch.org/whl/cpu",
            ],
            project_dir,
        )

    missing = [pkg for pkg in RUNTIME_PACKAGES if not can_import(py, module_name(pkg))]
    if missing:
        run([str(py), "-m", "pip", "install", *missing], project_dir)


def verify(py: Path) -> None:
    code = (
        "import torch, torchaudio; from funasr import AutoModel; "
        "import modelscope, psutil, soundfile; "
        "print('python', __import__('sys').version.split()[0]); "
        "print('torch', torch.__version__, 'cuda?', torch.cuda.is_available()); "
        "print('torchaudio', torchaudio.__version__); "
        "print('funasr AutoModel ok')"
    )
    subprocess.check_call([str(py), "-c", code])


def main() -> None:
    parser = argparse.ArgumentParser(description="Ensure a CPU SenseVoice/FunASR/CAM++ environment.")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--env-dir", type=Path, default=None)
    parser.add_argument("--env-kind", choices=["auto", "venv", "conda"], default="auto")
    parser.add_argument("--seed-python", type=Path, default=None, help="Python 3.10/3.11 executable used to create a venv.")
    parser.add_argument("--python", type=Path, default=None, help="Use an existing Python executable if it has/should get the packages.")
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    py = resolve_python(args, project_dir)
    ensure_packages(py, project_dir)
    verify(py)
    print(f"Ready: {py}")


if __name__ == "__main__":
    main()
