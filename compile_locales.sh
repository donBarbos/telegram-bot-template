#!/bin/bash

# Extract messages
pybabel extract --input-dirs=. -o bot/locales/messages.pot --project=messages

# Iterate over directories in ./bot/locales to initialize languages
for lang_dir in ./bot/locales/*; do
    if [ -d "$lang_dir" ]; then
        lang=$(basename "$lang_dir")
        # Skip if not a language directory
        if [[ "$lang" =~ ^(en|ru|uk)$ ]]; then
            echo "Initializing language: $lang"
            pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l "$lang"
        fi
    fi
done

# Compile and update messages
pybabel compile -d bot/locales -D messages --statistics
pybabel update -i bot/locales/messages.pot -d bot/locales -D messages
