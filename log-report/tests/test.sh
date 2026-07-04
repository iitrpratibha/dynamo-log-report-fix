#!/bin/bash
# pytest is already installed in the image (see environment/Dockerfile).
# No set -e here: a failing test must still fall through and write the reward.

mkdir -p /logs/verifier

pytest /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json
code=$?

if [ "$code" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
