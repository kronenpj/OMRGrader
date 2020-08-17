#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]; then
  . venv/bin/activate
fi

QT_AUTO_SCREEN_SCALE_FACTOR=1 python main.py "$@"
