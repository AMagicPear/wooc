#!/bin/bash
cd frontend
bun install
bun run build
cd ../backend
pip install -r requirements.txt
# python app.py