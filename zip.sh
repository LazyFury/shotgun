#!/bin/bash
zip -r package.zip . --exclude '*mysql*'\
        --exclude '*.git*' --exclude '*.pyc' --exclude '*.DS_Store*'\
        --exclude '*__pycache__*' --exclude '*venv*'\
        --exclude '*package.zip*' --exclude '*requirements.txt*'\
        --exclude '*zip.sh*'\
        --exclude '*.ruff_cache*'
        --exclude '*package*'