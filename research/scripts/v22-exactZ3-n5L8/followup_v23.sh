#!/bin/bash
# followup_v23.sh — the v23 follow-up commit: carry the completed n=5 L=8
# rung into the manuscript chain as NEW files (v21/v22 untouched), refresh
# the certificate, commit and push.  Idempotent via the marker
# /home/z/.v23_rung_done.  Run from anywhere (it cds to its own dir).
#
# Preconditions (checked, loud failures):
#   * results/v22-exactZ3-n5L8/v22_n5_L8_rung.json exists (the chain's
#     run phase wrote at least one point);
#   * git credentials already configured (/home/z/.git-credentials, 600).
set -e
cd "$(dirname "$0")"
MARKER=/home/z/.v23_rung_done
if [ -f "$MARKER" ]; then
  echo "v23 follow-up already done (marker $MARKER present)"; exit 0
fi
RES=../../results/v22-exactZ3-n5L8
LOG=../../logs/v22-exactZ3-n5L8
# The run phase still computing: carrying a PARTIAL grid would commit the
# one-shot marker and lock out the complete v23 later.  Wait for it.
if pgrep -f 'v22_n5_L8_block_v1\.py run' >/dev/null 2>&1; then
  echo "SKIP: run phase still in progress (pid $(pgrep -f 'v22_n5_L8_block_v1\.py run' | tr '\n' ' ')) — no follow-up this round"
  exit 0
fi

# ---- driving mode ----------------------------------------------------------
# The cron-era sandbox reaps background processes a few minutes after launch
# (verified 2026-09-21: setsid'd, nohup'd and plain background children all
# die; the original chain only survived because the crons went active hours
# after its launch).  So the run phase is DRIVEN: each call advances the
# resumable (chunk-checkpointed) assembly by one bounded foreground segment.
# A segment that ends in timeout(124) is NORMAL — progress lives in the
# chunk-state file; re-run this script on the next cron firing.
PGRID=0.44,0.46,0.47,0.48,0.50
NPTS=$(python3 -c "import json,os; p='$RES/v22_n5_L8_rung.json'; print(len(json.load(open(p))) if os.path.exists(p) else 0)" 2>/dev/null || echo 0)
if [ "$NPTS" -lt 5 ]; then
  echo "== driving mode: $NPTS/5 grid points done — one 8.7-min window (up to 2 points in parallel, 2 cores) =="
  # the first (up to) two incomplete points of the grid, in order
  MAP=$(python3 -c "
import json, os
grid = [0.44, 0.46, 0.47, 0.48, 0.50]
p = '$RES/v22_n5_L8_rung.json'
done = {round(r['p'], 4) for r in (json.load(open(p)) if os.path.exists(p) else [])}
missing = [g for g in grid if round(g, 4) not in done]
print(' '.join(f'{g:.2f}' for g in missing[:2]))
" 2>/dev/null)
  if [ -z "$MAP" ]; then MAP=0.44; fi
  PIDS=""
  for g in $MAP; do
    echo "   segment: p=$g (log $LOG/v22_n5_L8_block_run_p${g}.log)"
    if command -v timeout >/dev/null 2>&1; then
      timeout 520 python3 -u v22_n5_L8_block_v1.py run --pgrid $g \
        >> $LOG/v22_n5_L8_block_run_p${g}.log 2>&1 &
    else
      python3 -u v22_n5_L8_block_v1.py run --pgrid $g \
        >> $LOG/v22_n5_L8_block_run_p${g}.log 2>&1 &
    fi
    PIDS="$PIDS $!"
  done
  FAIL=0
  for P in $PIDS; do
    r=0; wait $P || r=$?
    if [ "$r" -ne 0 ] && [ "$r" -ne 124 ] && [ "$r" -ne 143 ]; then
      echo "   segment pid $P FAILED (exit $r)"
      FAIL=1
    fi
  done
  NPTS2=$(python3 -c "import json,os; p='$RES/v22_n5_L8_rung.json'; print(len(json.load(open(p))) if os.path.exists(p) else 0)" 2>/dev/null || echo 0)
  echo "   window done; grid now $NPTS2/5 points; last chunk lines:"
  for g in $MAP; do
    tail -1 $LOG/v22_n5_L8_block_run_p${g}.log 2>/dev/null | sed "s/^/   | p=$g /"
  done
  if [ "$FAIL" -eq 0 ]; then
    echo "DRIVING WINDOW DONE: $NPTS2/5 points — run this script again (up to 2-3 windows per firing, 600s Bash timeout) until the grid completes"
    exit 0
  fi
  echo "ERROR: a driving segment crashed — see the per-p run logs; NOT committing"
  exit 1
fi

if [ ! -f "$RES/v22_n5_L8_rung.json" ]; then
  echo "ERROR: $RES/v22_n5_L8_rung.json missing — run phase produced nothing"
  exit 1
fi

echo "== 1/5 patch (builds all v23 files; anchors asserted) =="
python3 patch_v23_rung.py

echo "== 2/5 compile (tectonic) =="
cd ../../versions
tectonic manuscript_revised_v23_rung.tex
tectonic supplement_v6.tex
cd ../scripts/v22-exactZ3-n5L8

echo "== 3/5 certificate v10 =="
python3 make_cert_v10.py

echo "== 4/5 git: add, commit, push =="
cd ../../..
# keep the 830 MB canonical-id array out of the repo (GitHub 100 MB limit)
if ! grep -q 'ids_nb4.npy' .gitignore 2>/dev/null; then
  printf '# the L=8 full canonical-id array (~830 MB, GitHub 100 MB limit)\nresearch/results/v22-exactZ3-n5L8/tmp_n5L8block/ids_nb4.npy\n' >> .gitignore
fi
git add .gitignore \
  research/versions/manuscript_revised_v23_rung.tex \
  research/versions/manuscript_revised_v23_rung.pdf \
  research/versions/supplement_v6.tex \
  research/versions/supplement_v6.pdf \
  research/versions/changelog_v23.md \
  research/versions/README_v23_rung.md \
  research/versions/mipt_numerical_report_v11.md \
  research/versions/certificate_sha256_v10.txt \
  research/results/v22-exactZ3-n5L8/v22_n5_L8_rung.json \
  research/results/v22-exactZ3-n5L8/tmp_n5L8block/reps_nb4.npy \
  research/results/v22-exactZ3-n5L8/tmp_n5L8block/counts_nb4.npy \
  research/logs/v22-exactZ3-n5L8/v22_n5_L8_block_validate.log \
  research/logs/v22-exactZ3-n5L8/v22_n5_L8_block_ids.log \
  research/logs/v22-exactZ3-n5L8/v22_n5_L8_block_run.log \
  research/logs/v22-exactZ3-n5L8/chain.log
# the per-p driven-run logs (all five exist once the grid is complete)
for g in 0.44 0.46 0.47 0.48 0.50; do
  if [ -f "research/logs/v22-exactZ3-n5L8/v22_n5_L8_block_run_p${g}.log" ]; then
    git add "research/logs/v22-exactZ3-n5L8/v22_n5_L8_block_run_p${g}.log"
  fi
done
git add \
  research/scripts/v22-exactZ3-n5L8/patch_v23_rung.py \
  research/scripts/v22-exactZ3-n5L8/make_cert_v10.py \
  research/scripts/v22-exactZ3-n5L8/followup_v23.sh
git commit -F research/scripts/v22-exactZ3-n5L8/commit_msg_v23.txt
git push origin main

echo "== 5/5 marker =="
touch "$MARKER"
echo "V23 FOLLOW-UP COMPLETE: committed and pushed"
