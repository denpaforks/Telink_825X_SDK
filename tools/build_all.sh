#!/usr/bin/env bash

set -u

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TOOLCHAIN_BIN=${TC32_TOOLCHAIN_BIN:-}

if [ -n "$TOOLCHAIN_BIN" ]; then
    PATH="$TOOLCHAIN_BIN:$PATH"
fi

for command in make tc32-elf-gcc tc32-elf-readelf sha256sum; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "Missing required command: $command" >&2
        exit 2
    fi
done

total=0
passed=0
failed=0
total_warnings=0

while IFS= read -r project_dir; do
    total=$((total + 1))
    relative=${project_dir#"$ROOT"/}
    log_file=$(mktemp)

    if (cd "$project_dir" && make clean >/dev/null 2>&1 && make) >"$log_file" 2>&1; then
        passed=$((passed + 1))
        warnings=$(grep -Eic 'warning:' "$log_file" || true)
        total_warnings=$((total_warnings + warnings))
        elf=$(find "$project_dir/out" -maxdepth 1 -type f -name '*.elf' -print -quit)
        binary=$(find "$project_dir/out" -maxdepth 1 -type f -name '*.bin' -print -quit)
        entry=$(tc32-elf-readelf -h "$elf" | awk -F: '/Entry point address/{gsub(/^[[:space:]]+/, "", $2); print $2}')
        binary_hash=$(sha256sum "$binary" | awk '{print $1}')
        printf 'PASS|%s|warnings=%s|elf=%s|bin=%s|entry=%s|sha256=%s\n' \
            "$relative" "$warnings" "$(stat -c %s "$elf")" "$(stat -c %s "$binary")" \
            "$entry" "$binary_hash"
    else
        failed=$((failed + 1))
        warnings=$(grep -Eic 'warning:' "$log_file" || true)
        total_warnings=$((total_warnings + warnings))
        errors=$(grep -Eic 'error:|undefined reference|No rule to make target|not found' "$log_file" || true)
        printf 'FAIL|%s|warnings=%s|errors=%s\n' "$relative" "$warnings" "$errors"
        tail -n 20 "$log_file" | sed 's/^/  /'
    fi

    rm -f "$log_file"
done < <(find "$ROOT/example" "$ROOT/study" -type f -iname makefile -printf '%h\n' | sort)

printf 'SUMMARY|total=%s|passed=%s|failed=%s|warnings=%s\n' \
    "$total" "$passed" "$failed" "$total_warnings"
[ "$failed" -eq 0 ]
