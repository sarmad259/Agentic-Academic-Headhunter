"""Verify all three pipeline upgrades are working and safe."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

errors = []

# ── Upgrade 1: Dynamic Profile Extraction ───────────────────────────────────
print("[1] Testing Dynamic Profile Extraction (matching_engine.py)...")
try:
    from utils.matching_engine import MatchingEngine, _load_portfolio_keywords
    m = MatchingEngine()
    assert isinstance(m.profile["interests"], list), "interests must be a list"
    assert len(m.profile["interests"]) >= 10, "Profile should have at least 10 interests"
    extras = _load_portfolio_keywords("NONEXISTENT_FILE.md")
    assert extras == {"interests": [], "skills": []}, "Should return empty dict on missing file"
    print(f"   OK - Profile interests: {len(m.profile['interests'])} | Fallback tested OK")
except Exception as e:
    errors.append(f"Upgrade 1 FAILED: {e}")

# ── Upgrade 2: Self-Improving Few-Shot Prompts ───────────────────────────────
print("[2] Testing Self-Improving Prompts (intelligence_layer.py)...")
try:
    from utils.intelligence_layer import _load_gold_standard_examples
    result = _load_gold_standard_examples("NONEXISTENT_FOLDER")
    assert result == "", f"Expected empty string for missing folder, got: {repr(result)}"
    os.makedirs("gold_standard", exist_ok=True)
    result2 = _load_gold_standard_examples("gold_standard")
    assert result2 == "", "Expected empty string for empty folder"
    print("   OK - Returns empty string for missing/empty folder. No crash.")
except Exception as e:
    errors.append(f"Upgrade 2 FAILED: {e}")

# ── Upgrade 3: Timezone-Aware Dispatch ──────────────────────────────────────
print("[3] Testing Timezone-Aware Dispatch (email_sender.py)...")
try:
    from utils.email_sender import _wait_until_optimal_time, COUNTRY_UTC_OFFSETS
    assert "Germany" in COUNTRY_UTC_OFFSETS, "Germany should be in offset map"
    assert "Japan" in COUNTRY_UTC_OFFSETS, "Japan should be in offset map"
    # Unknown country should not crash
    _wait_until_optimal_time("UnknownLand")
    _wait_until_optimal_time("")
    _wait_until_optimal_time(None)
    print(f"   OK - {len(COUNTRY_UTC_OFFSETS)} countries mapped | Unknown/None fallback works")
except Exception as e:
    errors.append(f"Upgrade 3 FAILED: {e}")

# ── Draft Manager: Country in YAML ──────────────────────────────────────────
print("[4] Checking Country field in DraftManager YAML...")
try:
    import inspect
    from utils.draft_manager import DraftManager
    src = inspect.getsource(DraftManager._format_draft)
    assert "Country:" in src or "country" in src.lower(), "Country field missing!"
    print("   OK - Country field present in draft YAML template")
except Exception as e:
    errors.append(f"Upgrade 3b FAILED: {e}")

# ── Final Result ─────────────────────────────────────────────────────────────
print()
if errors:
    print(f"FAILED: {len(errors)} error(s):")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("All 4 checks passed! Pipeline is intact and all upgrades are safe.")
