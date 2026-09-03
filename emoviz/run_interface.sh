#!/bin/bash
# run_interface.sh — start the EmoViz pipeline tester and open it in the browser.
cd "$(dirname "$0")" || exit 1

if [ ! -x .venv/bin/python ]; then
  echo "No .venv found — run:  bash setup.sh"; exit 1
fi

# stop any previous instance on port 5050
if lsof -ti:5050 >/dev/null 2>&1; then
  echo "stopping previous instance on port 5050…"
  lsof -ti:5050 | xargs kill -9 2>/dev/null
  sleep 1
fi

echo "starting EmoViz interface…"
PYTHONUNBUFFERED=1 .venv/bin/python app.py > outputs/app.log 2>&1 &
PID=$!
echo "  server PID $PID  ·  log: outputs/app.log"

# wait for it to answer
for i in $(seq 1 30); do
  if curl -s -o /dev/null http://127.0.0.1:5050/ 2>/dev/null; then
    echo "  ready → http://127.0.0.1:5050"
    command -v open >/dev/null && open http://127.0.0.1:5050
    echo
    echo "  NOTE: models pre-load in the background (float16, ~1.8 GB). First compare may"
    echo "        take ~30 s; after that each run is a few seconds."
    echo "  Stop with:  kill $PID    (or: lsof -ti:5050 | xargs kill)"
    exit 0
  fi
  sleep 1
done
echo "  server did not start — see outputs/app.log"; exit 1
