#!/usr/bin/env python3
"""Run all synchronous example scripts in order"""

import subprocess
import sys
import time
from pathlib import Path


def main():
    # Get the examples directory
    examples_dir = Path(__file__).parent

    # Find all Python files, excluding this script and async variants
    example_files = sorted(
        [
            f
            for f in examples_dir.glob("*.py")
            if f.name not in ["00_run_all.py", "00_run_all.py"]
            and not f.name.endswith("_async.py")
        ]
    )

    if not example_files:
        print("No example files found to run")
        return 0

    print(f"Found {len(example_files)} example(s) to run\n")
    print("=" * 70)

    total_start = time.time()
    results = []

    for example_file in example_files:
        example_name = example_file.name
        print(f"\n▶ Running: {example_name}")
        print("-" * 70)

        start_time = time.time()

        try:
            # Run the example script
            result = subprocess.run(
                [sys.executable, str(example_file)],
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout per script
            )

            elapsed_time = time.time() - start_time

            # Print output
            if result.stdout:
                print(result.stdout)

            # Check for errors
            if result.returncode != 0:
                print(f"\n❌ ERROR in {example_name}")
                if result.stderr:
                    print("STDERR:")
                    print(result.stderr)

                results.append(
                    {
                        "name": example_name,
                        "status": "FAILED",
                        "time": elapsed_time,
                        "error": result.stderr or "Non-zero exit code",
                    }
                )

                # Break on error
                print("\n" + "=" * 70)
                print("STOPPING: Error encountered")
                print("=" * 70)
                print_summary(results, time.time() - total_start)
                return 1
            else:
                results.append(
                    {"name": example_name, "status": "PASSED", "time": elapsed_time}
                )
                print(f"✓ Completed in {elapsed_time:.2f}s")

        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            print(f"\n❌ TIMEOUT in {example_name} after {elapsed_time:.2f}s")

            results.append(
                {
                    "name": example_name,
                    "status": "TIMEOUT",
                    "time": elapsed_time,
                    "error": "Script exceeded 60 second timeout",
                }
            )

            # Break on timeout
            print("\n" + "=" * 70)
            print("STOPPING: Timeout encountered")
            print("=" * 70)
            print_summary(results, time.time() - total_start)
            return 1

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"\n❌ EXCEPTION in {example_name}: {e}")

            results.append(
                {
                    "name": example_name,
                    "status": "ERROR",
                    "time": elapsed_time,
                    "error": str(e),
                }
            )

            # Break on exception
            print("\n" + "=" * 70)
            print("STOPPING: Exception encountered")
            print("=" * 70)
            print_summary(results, time.time() - total_start)
            return 1

    total_time = time.time() - total_start

    # Print summary
    print("\n" + "=" * 70)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print_summary(results, total_time)

    return 0


def print_summary(results, total_time):
    """Print execution summary"""
    print("\n📊 EXECUTION SUMMARY")
    print("-" * 70)

    for result in results:
        status_symbol = {
            "PASSED": "✓",
            "FAILED": "❌",
            "TIMEOUT": "⏱",
            "ERROR": "❌",
        }.get(result["status"], "?")

        print(
            f"{status_symbol} {result['name']:40s} {result['time']:>6.2f}s  {result['status']}"
        )

        if "error" in result:
            error_preview = result["error"].split("\n")[0][:50]
            print(f"   Error: {error_preview}")

    print("-" * 70)
    print(f"Total execution time: {total_time:.2f}s")

    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    print(f"Results: {passed}/{total} passed")


if __name__ == "__main__":
    sys.exit(main())
