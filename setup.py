"""One-shot setup: install deps, create .env, generate samples, init DB."""
import os
import shutil
import subprocess
import sys


def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"  ✗ Command failed (exit {result.returncode})")
    else:
        print("  ✓ Done")


if __name__ == "__main__":
    print("=" * 60)
    print("  Atos Contract Helper Agent — Setup")
    print("=" * 60)

    # 1. .env file
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("\n✓ Created .env from .env.example")
        print("  ⚠  Add your ANTHROPIC_API_KEY to .env before running the app.")
    else:
        print("\n✓ .env already exists")

    # 2. Install Python deps FIRST (must happen before any local imports)
    print("\n▶ Installing dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
        check=True
    )
    print("  ✓ Done")

    # 3. Generate sample contracts
    run(f"{sys.executable} sample_contracts/generate_samples.py")

    # 4. Initialize DB schema (import only after deps are installed)
    os.makedirs("data", exist_ok=True)
    from utils.database import initialize_schema
    initialize_schema()
    print("\n✓ Database schema initialized")

    print("\n" + "=" * 60)
    print("  Setup complete!")
    print("  Run with: streamlit run app.py")
    print("=" * 60)
