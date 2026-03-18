#!/bin/bash
set -e
echo "Starting AI-Powered Personal Health Dashboard..."
uvicorn app:app --host 0.0.0.0 --port 9017 --workers 1
