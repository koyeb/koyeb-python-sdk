#!/bin/bash
set -e

echo "Applying manual patches after code generation..."

PATCHES=(
  "patches/001-proxy-support.patch"
  "patches/002-api-client-fixes.patch"
)

for patch in "${PATCHES[@]}"; do
  if [ -f "$patch" ]; then
    echo "  Applying $patch..."
    if ! git apply "$patch"; then
      echo "  ERROR: Failed to apply $patch"
      exit 1
    fi
  else
    echo "  WARNING: $patch not found, skipping..."
  fi
done

echo "All patches applied successfully."
