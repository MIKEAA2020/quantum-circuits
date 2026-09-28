#!/bin/bash
# drive_v25_ext.sh -- supervisor/driver for the v25 extension compute
# (the d=3 L=6 locator scan, the d=3 L=8 rung grid, and the finer d=2
# locator grid at L=8, all n=5).  Modeled on the v23 driving mode
# (followup_v23.sh): the cron-era sandbox may reap background processes,
# so all compute advances in BOUNDED, checkpointed foreground segments;
# a segment ending in timeout(124)/SIGTERM(143) is NORMAL -- progress
# lives in the chunk-state files (grids) and the merged results JSONs
# (locator, per-point rung rows).  A supervising instance appends a
# heartbeat line every window so a watcher can detect staleness.
#
# Modes:
#   V25_SUPERVISOR=1  -- loop windows (V25_WINDOW_SECS each, default 3600)
#                        until the config queue is empty, then touch
#                        /home/z/.v25_ext_done and exit.
#   default           -- ONE bounded window, then exit (cron fallback).
#
# The queue: research/results/v22-exactZ3-n5L8/v25_ext_config.json
#   {"queue": [{"kind": "locate", "nb": 3, "plist": [..]},
#              {"kind": "grid", "tag": "d3"|"fine", "p": 0.84}, ...]}
# processed strictly in order, ONE python segment at a time (single-point
# sequential mode, the user-approved OOM-safe profile; a lockfile enforces
# it -- NEVER two python segments at once).
set -u
cd "$(dirname "$0")"
CFG=../../results/v22-exactZ3-n5L8/v25_ext_config.json
LOGD=../../logs/v25-n5L8-ext
MARKER=/home/z/.v25_ext_done
HEART=$LOGD/supervisor_heartbeat.txt
LOCKF=$LOGD/driver.lock
WSECS=${V25_WINDOW_SECS:-3600}
mkdir -p "$LOGD"

exec 9>"$LOCKF"
if ! flock -n 9; then
  echo "another driver holds the lock -- exiting"
  exit 0
fi

if [ ! -f "$CFG" ]; then
  echo "no config $CFG -- nothing to drive"
  exit 0
fi

next_cmd() {
  python3 - "$CFG" <<'EOF'
import json, os, sys
cfg = json.load(open(sys.argv[1]))
RES = os.path.dirname(os.path.abspath(sys.argv[1]))
def rows(name):
    p = os.path.join(RES, name)
    return json.load(open(p)) if os.path.exists(p) else []
loc_done = {(int(r['nb']), round(float(r['p']), 4))
            for r in rows('v25_n5_d3_locator.json')}
d3_done = {round(float(r['p']), 4) for r in rows('v25_n5_L8_rung_d3.json')}
fine_done = {round(float(r['p']), 4) for r in rows('v25_n5_L8_finegrid.json')}
for e in cfg.get('queue', []):
    k = e.get('kind', 'grid')
    if k == 'locate':
        nb = int(e['nb'])
        missing = [p for p in e['plist']
                   if (nb, round(float(p), 4)) not in loc_done]
        if missing:
            print('locate', nb, ','.join(f'{p:g}' for p in missing))
            sys.exit(0)
    else:
        done = d3_done if e['tag'] == 'd3' else fine_done
        if round(float(e['p']), 4) not in done:
            print('grid', e['tag'], f"{e['p']:g}")
            sys.exit(0)
print('EMPTY')
EOF
}

while :; do
  line="$(next_cmd)"
  if [ -z "$line" ]; then
    echo "$(date -u +%FT%TZ) next_cmd failed -- retrying after 60s" >> "$HEART"
    sleep 60
    continue
  fi
  read -r kind a b <<< "$line"
  if [ "$kind" = "EMPTY" ]; then
    [ -f "$MARKER" ] || touch "$MARKER"
    echo "$(date -u +%FT%TZ) queue EMPTY -- campaign complete" >> "$HEART"
    echo "V25 EXTENSION COMPLETE (queue empty)"
    exit 0
  fi
  if [ "$kind" = "locate" ]; then
    echo "$(date -u +%FT%TZ) window: locate nb=$a plist=$b" >> "$HEART"
    timeout "$WSECS" python3 -u v25_n5_L8_ext_v1.py locate-d3 \
      --nb "$a" --plist "$b" >> "$LOGD/locate_nb${a}.log" 2>&1
  else
    echo "$(date -u +%FT%TZ) window: grid tag=$a p=$b" >> "$HEART"
    timeout "$WSECS" python3 -u v25_n5_L8_ext_v1.py run-"$a" \
      --pgrid "$b" >> "$LOGD/run_${a}_p${b}.log" 2>&1
  fi
  rc=$?
  # 124 (timeout) and 143 (SIGTERM) are normal window ends; anything else
  # is logged (checkpointed state survives either way).
  if [ "$rc" -ne 0 ] && [ "$rc" -ne 124 ] && [ "$rc" -ne 143 ]; then
    echo "$(date -u +%FT%TZ) segment rc=$rc (kind=$kind a=$a b=$b) -- check logs" >> "$HEART"
  fi
  if [ "${V25_SUPERVISOR:-0}" != "1" ]; then
    echo "one window done (rc=$rc) -- single-window mode"
    exit 0
  fi
  sleep 5
done
