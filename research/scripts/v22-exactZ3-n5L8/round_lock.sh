#!/usr/bin/env bash
# round_lock.sh — round-level lock + structured round log for the v25 completion-sequenced chain.
#
# Trigger model (user directive 2026-10-03 ~00:35+08): the next round is triggered by the
# PREVIOUS round's COMPLETION (a one_time successor job at end + 40s cooldown), never by a
# clock schedule. This script provides the round-level mutual exclusion and the audit log.
#
# Subcommands:
#   acquire
#       Exit 0: lock acquired. stdout: "round_id=<id> start=<epoch> acquired=<epoch>"
#       Exit 2: a fresh lock is held by a live round. stdout: holder info. The caller must
#               append 'event=overlap_skipped ...' to rounds_chain.log, requeue ONE one_time
#               firing at now+30s, and STOP (do not drive).
#       Stale locks are auto-cleaned BEFORE acquiring (events logged to rounds_chain.log):
#         - age >= STALE_TTL  (2640s = 2x max round ~1320s)          -> event=stale_lock_cleaned
#         - age >= ORPHAN_FAST (900s) AND no v25 compute process      -> event=orphan_lock_cleaned
#   release <round_id>
#       Removes the lock iff its round_id matches. stdout: "released=<epoch>".
#       Exit 4 on mismatch (lock kept — it belongs to a newer round).
#   log <round_id> <start> <end> <rc> <lock_released> <next_scheduled> [note]
#       Appends the structured round record (round_id, start, end, duration, rc,
#       lock_acquired, lock_released, next_scheduled) to rounds_chain.log.
#   status
#       Prints lock state: free | held age=<s> py=<0|1> <holder>, with stale/orphan hints.
#
# Lock file: /home/z/.v25_round.lock   (outside the repo; wiped on sandbox rollbacks, which
# is safe: cron jobs live gateway-side and the lock is re-acquired fresh after recovery.)

set -u
LOCK=/home/z/.v25_round.lock
BASE=/home/z/my-project/quantum-circuits
LOGF=$BASE/research/logs/v25-n5L8-ext/rounds_chain.log
STALE_TTL=2640
ORPHAN_FAST=900

now() { date +%s; }
py_running() { pgrep -f 'v25_n5_L8_ext_v1|v22_n5_L8_block_v1|drive_v25_ext' >/dev/null 2>&1 && echo 1 || echo 0; }

cmd=${1:-}
case "$cmd" in
  acquire)
    t=$(now)
    if [ -f "$LOCK" ]; then
      age=$(( t - $(stat -c %Y "$LOCK" 2>/dev/null || echo "$t") ))
      py=$(py_running)
      if [ "$age" -ge "$STALE_TTL" ]; then
        echo "event=stale_lock_cleaned ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) age=${age}s ttl=${STALE_TTL}s" >> "$LOGF"
        rm -f "$LOCK"
      elif [ "$age" -ge "$ORPHAN_FAST" ] && [ "$py" -eq 0 ]; then
        echo "event=orphan_lock_cleaned ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) age=${age}s py=0" >> "$LOGF"
        rm -f "$LOCK"
      else
        echo "HELD age=${age}s py=${py} holder=[$(tr '\n' ' ' < "$LOCK")]"
        exit 2
      fi
    fi
    rid="r$(date -u +%Y%m%dT%H%M%SZ)$$"
    printf 'round_id=%s\nstart=%s\npid=%s\n' "$rid" "$t" "$$" > "$LOCK"
    echo "round_id=$rid start=$t acquired=$t"
    ;;
  release)
    rid=${2:-}
    t=$(now)
    if [ ! -f "$LOCK" ]; then echo "released=$t (lock already absent)"; exit 0; fi
    held=$(sed -n 's/^round_id=//p' "$LOCK" | head -1)
    if [ "$held" = "$rid" ]; then
      rm -f "$LOCK"
      echo "released=$t"
      exit 0
    else
      echo "MISMATCH held=$held tried=$rid — lock kept"
      exit 4
    fi
    ;;
  log)
    rid=${2:?round_id}; st=${3:?start}; en=${4:?end}; rc=${5:-?}; lr=${6:-?}; nx=${7:-?}; note=${8:-}
    dur=$(( en - st ))
    echo "round_id=$rid start=$st end=$en duration=${dur}s rc=$rc lock_acquired=$st lock_released=$lr next_scheduled=$nx${note:+ note=\"$note\"}" >> "$LOGF"
    echo "logged round_id=$rid duration=${dur}s"
    ;;
  status)
    if [ ! -f "$LOCK" ]; then
      echo "free"
    else
      t=$(now); age=$(( t - $(stat -c %Y "$LOCK" 2>/dev/null || echo "$t") )); py=$(py_running)
      echo "held age=${age}s py=${py} holder=[$(tr '\n' ' ' < "$LOCK")]"
      if [ "$age" -ge "$STALE_TTL" ]; then echo "hint: STALE (>= ${STALE_TTL}s) — safe to clean"; fi
      if [ "$age" -ge "$ORPHAN_FAST" ] && [ "$py" -eq 0 ]; then echo "hint: ORPHAN (>= ${ORPHAN_FAST}s, no compute) — safe to clean"; fi
    fi
    ;;
  *)
    echo "usage: round_lock.sh {acquire|release <round_id>|log <round_id> <start> <end> <rc> <lock_released> <next_scheduled> [note]|status}" >&2
    exit 64
    ;;
esac
