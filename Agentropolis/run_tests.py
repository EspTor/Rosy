#!/usr/bin/env python3
"""Task 1 comprehensive test runner."""
import sys
import subprocess
import os

def run_command(cmd, description, check=True):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('-'*60)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if check and result.returncode != 0:
        print(f"❌ FAILED: {description}")
        return False
    else:
        print(f"✅ PASSED: {description}")
        return True

def main():
    base = "/home/ubuntu/Documents/Obsidian Vault/Agentropolis"
    os.chdir(base)

    print("🧪 Task 1 Quality Test Suite")
    print("="*60)

    results = []

    # 1. Structural check
    results.append(run_command(
        [sys.executable, "test_verify.py"],
        "Structural validation (imports)"
    ))

    # 2. Config tests
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_config.py", "-v"],
        "Configuration tests"
    ))

    # 3. Database tests
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_database.py", "-v"],
        "Database connection & table creation"
    ))

    # 4. Model tests
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_models.py", "-v"],
        "Model CRUD tests"
    ))

    # 5. Integration tests
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_models_integration.py", "-v"],
        "Model integration tests"
    ))
    
    # 6. Brain tests
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_brains.py", "-v"],
        "Agent brains tests"
    ))
    
    # 7. E2E test
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/e2e/test_full_flow.py", "-v"],
        "End-to-end pipeline"
    ))

    # 7. Performance benchmarks
    results.append(run_command(
        [sys.executable, "scripts/benchmark.py"],
        "Performance benchmarks"
    ))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    if passed == total:
        print("🎉 ALL TESTS PASSED! Task 1 is HIGH QUALITY and ready for Task 2.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
