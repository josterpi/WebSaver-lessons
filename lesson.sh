#!/usr/bin/env bash

set -e

REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
BRANCH="main"

mapfile -t HASHES   < <(git -C "$REPO" log --reverse --format="%H"  "$BRANCH")
mapfile -t SUBJECTS < <(git -C "$REPO" log --reverse --format="%s" "$BRANCH")
COUNT=${#HASHES[@]}

current_hash=$(git -C "$REPO" rev-parse HEAD)
current_index=0
for i in "${!HASHES[@]}"; do
    if [[ "${HASHES[$i]}" == "$current_hash" ]]; then
        current_index=$((i + 1))
        break
    fi
done

go_to() {
    local n=$1
    local idx=$((n - 1))
    local subject="${SUBJECTS[$idx]}"

    if [[ $n -eq $COUNT ]]; then
        git -C "$REPO" checkout "$BRANCH" -q
    else
        git -C "$REPO" checkout "${HASHES[$idx]}" -q
    fi
    echo "[$n/$COUNT] $subject"
}

cmd="${1:-list}"

case "$cmd" in
    list)
        for i in "${!HASHES[@]}"; do
            n=$((i + 1))
            if [[ $n -eq $current_index ]]; then
                printf "* %2d. %s\n" "$n" "${SUBJECTS[$i]}"
            else
                printf "  %2d. %s\n" "$n" "${SUBJECTS[$i]}"
            fi
        done
        ;;
    next)
        if [[ $current_index -eq 0 ]]; then
            echo "Not on a commit in this series. Run '$(basename "$0") list' to see options." >&2; exit 1
        fi
        if [[ $current_index -ge $COUNT ]]; then
            echo "Already at the last commit ($COUNT/$COUNT)."; exit 0
        fi
        go_to $((current_index + 1))
        ;;
    prev)
        if [[ $current_index -eq 0 ]]; then
            echo "Not on a commit in this series. Run '$(basename "$0") list' to see options." >&2; exit 1
        fi
        if [[ $current_index -le 1 ]]; then
            echo "Already at the first commit (1/$COUNT)."; exit 0
        fi
        go_to $((current_index - 1))
        ;;
    first)  go_to 1 ;;
    last)   go_to "$COUNT" ;;
    show)
        if [[ $current_index -eq 0 ]]; then
            echo "Not on a commit in this series. Run '$(basename "$0") list' to see options." >&2; exit 1
        fi
        echo "[$current_index/$COUNT]"
        git -C "$REPO" log -1 --format="%B" HEAD
        ;;
    *)
        if ! [[ "$cmd" =~ ^[0-9]+$ ]]; then
            echo "Usage: $(basename "$0") [list | show | next | prev | first | last | N]" >&2; exit 1
        fi
        if [[ $cmd -lt 1 || $cmd -gt $COUNT ]]; then
            echo "No commit $cmd. Valid range: 1–$COUNT." >&2; exit 1
        fi
        go_to "$cmd"
        ;;
esac
