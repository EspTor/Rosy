#!/bin/bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
COUNTER="$VAULT/Habits/coffee-counter.md"
HABIT_FILE="$VAULT/Habits/$(date +%Y-%m-%d).md"

# Get current date
TODAY=$(date +%Y-%m-%d)

# Read current count from counter
if [ -f "$COUNTER" ]; then
    CURRENT=$(grep -oP 'Total cups: \K\d+' "$COUNTER" || echo "0")
else
    CURRENT=0
fi

# Increment
NEW_COUNT=$((CURRENT + 1))

# Update coffee counter
sed -i "s/Total cups: [0-9]\+/Total cups: $NEW_COUNT/" "$COUNTER"
sed -i "s/- [0-9]\+ cups/- $NEW_COUNT cups/" "$COUNTER"

# Update habit tracker if it exists
if [ -f "$HABIT_FILE" ]; then
    # Update the checkbox if not already checked
    if ! grep -q "\[x\] Coffee" "$HABIT_FILE"; then
        sed -i "s/\[ \] Coffee (track cups)/\[x\] Coffee (track cups)/" "$HABIT_FILE"
    fi
    # Update the coffee tracking line
    sed -i "s/☕ Cups today: [0-9]\+/☕ Cups today: $NEW_COUNT/" "$HABIT_FILE"
fi

echo "Coffee count updated to $NEW_COUNT"
