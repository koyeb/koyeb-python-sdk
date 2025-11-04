#!/usr/bin/env python3
"""Run all asynchronous example scripts in order"""

import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path


async def run_example(example_file):
    """Run a single example script and return results"""
    example_name = example_file.name
    print(f"\n▶ Running: {example_name}")
    print("-" * 70)
    
    start_time = time.time()
    
    try:
        # Run the example script
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            str(example_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60  # 60 second timeout per script
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            elapsed_time = time.time() - start_time
            print(f"\n❌ TIMEOUT in {example_name} after {elapsed_time:.2f}s")
            return {
                "name": example_name,
                "status": "TIMEOUT",
                "time": elapsed_time,
                "error": "Script exceeded 60 second timeout"
            }
        
        elapsed_time = time.time() - start_time
        
        # Print output
        if stdout:
            print(stdout.decode())
        
        # Check for errors
        if process.returncode != 0:
            print(f"\n❌ ERROR in {example_name}")
            if stderr:
                print("STDERR:")
                print(stderr.decode())
            
            return {
                "name": example_name,
                "status": "FAILED",
                "time": elapsed_time,
                "error": stderr.decode() if stderr else "Non-zero exit code"
            }
        else:
            print(f"✓ Completed in {elapsed_time:.2f}s")
            return {
                "name": example_name,
                "status": "PASSED",
                "time": elapsed_time
            }
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ EXCEPTION in {example_name}: {e}")
        
        return {
            "name": example_name,
            "status": "ERROR",
            "time": elapsed_time,
            "error": str(e)
        }


async def main():
    # Get the examples directory
    examples_dir = Path(__file__).parent
    
    # Find all async Python files, excluding this script
    example_files = sorted([
        f for f in examples_dir.glob("*_async.py")
        if f.name != "00_run_all_async.py"
    ])
    
    if not example_files:
        print("No async example files found to run")
        return 0
    
    print(f"Found {len(example_files)} async example(s) to run\n")
    print("=" * 70)
    
    total_start = time.time()
    results = []
    
    # Run examples sequentially to maintain order and stop on first error
    for example_file in example_files:
        result = await run_example(example_file)
        results.append(result)
        
        # Break on error
        if result["status"] in ["FAILED", "TIMEOUT", "ERROR"]:
            print("\n" + "=" * 70)
            print("STOPPING: Error encountered")
            print("=" * 70)
            print_summary(results, time.time() - total_start)
            return 1
    
    total_time = time.time() - total_start
    
    # Print summary
    print("\n" + "=" * 70)
    print("ALL ASYNC EXAMPLES COMPLETED SUCCESSFULLY")
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
            "ERROR": "❌"
        }.get(result["status"], "?")
        
        print(f"{status_symbol} {result['name']:40s} {result['time']:>6.2f}s  {result['status']}")
        
        if "error" in result:
            error_preview = result["error"].split("\n")[0][:50]
            print(f"   Error: {error_preview}")
    
    print("-" * 70)
    print(f"Total execution time: {total_time:.2f}s")
    
    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    print(f"Results: {passed}/{total} passed")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
