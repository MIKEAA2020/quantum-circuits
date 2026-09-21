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
  research/logs/v22-exactZ3-n5L8/chain.log \
  research/scripts/v22-exactZ3-n5L8/patch_v23_rung.py \
  research/scripts/v22-exactZ3-n5L8/make_cert_v10.py \
  research/scripts/v22-exactZ3-n5L8/followup_v23.sh
git commit -F research/scripts/v22-exactZ3-n5L8/commit_msg_v23.txt
git push origin main

echo "== 5/5 marker =="
touch "$MARKER"
echo "V23 FOLLOW-UP COMPLETE: committed and pushed"
