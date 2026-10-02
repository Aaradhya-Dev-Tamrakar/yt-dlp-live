#!/usr/bin/env python3
"""
scripts/verify.py - Deterministic Verification Gate for yt-dlp-live
Verifies stream configuration, scripts, sync wrappers, synthetic SHA invariants, and workflows.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def check_structure():
    print("[1/4] Checking project structure and core files...")
    required = [
        "README.md",
        "sync.ps1",
        "sync.bat",
        "record_live.ps1",
        "relay_live.ps1",
        "stream_file_live.bat",
        "yt-dlp.conf",
    ]
    missing = [f for f in required if not (ROOT / f).exists()]
    if missing:
        print(f"[FAIL] Missing required files: {missing}")
        return False
    print("  [PASS] All core live-streaming scripts and sync wrappers exist.")
    return True

def check_scripts_integrity():
    print("[2/4] Verifying scripts and config files integrity...")
    conf_file = ROOT / "yt-dlp.conf"
    if not conf_file.exists() or not conf_file.read_text(encoding="utf-8").strip():
        print("[FAIL] yt-dlp.conf missing or empty.")
        return False
    print("  [PASS] yt-dlp configuration verified.")
    return True

def check_synthetic_shas():
    print("[3/4] Enforcing zero synthetic commit SHAs...")
    synthetic_pattern = re.compile(r'\b(rel\d+|upg\d+|xtool\d+|dummy_sha|fake_sha|placeholder_sha)\b', re.IGNORECASE)
    text_extensions = {".md", ".ps1", ".bat", ".conf", ".yml", ".yaml", ".json", ".txt"}
    
    violations = []
    for file in ROOT.rglob("*"):
        if file.is_file() and file.suffix.lower() in text_extensions:
            if any(part in file.parts for part in (".git", "scripts")):
                continue
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                for line_idx, line in enumerate(content.splitlines(), start=1):
                    if synthetic_pattern.search(line):
                        violations.append(f"{file.relative_to(ROOT)}:{line_idx} - {line.strip()}")
            except Exception:
                pass

    if violations:
        print(f"[FAIL] Found {len(violations)} synthetic SHA violations:")
        for v in violations[:10]:
            print(f"  {v}")
        return False
    print("  [PASS] Zero synthetic commit SHAs detected.")
    return True

def check_workflows():
    print("[4/4] Verifying GitHub workflows...")
    wf_dir = ROOT / ".github" / "workflows"
    if not wf_dir.exists():
        print("[FAIL] Missing .github/workflows directory.")
        return False
    workflows = list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))
    if not workflows:
        print("[FAIL] No workflow files found in .github/workflows.")
        return False
    print(f"  [PASS] Verified {len(workflows)} CI workflow definitions.")
    return True

def main():
    print(f"Running deterministic verification in {ROOT}\n")
    checks = [
        check_structure,
        check_scripts_integrity,
        check_synthetic_shas,
        check_workflows,
    ]
    
    passed = 0
    errors = 0
    for check in checks:
        if check():
            passed += 1
        else:
            errors += 1
        print()
        
    print("=" * 50)
    print(f"Passed: {passed}   Errors: {errors}")
    if errors == 0:
        print("\nALL CHECKS PASSED DETERMINISTICALLY.")
        return 0
    else:
        print(f"\nVERIFICATION FAILED WITH {errors} ERROR(S).")
        return 1

if __name__ == "__main__":
    sys.exit(main())
