#!/bin/bash
# strictly sequential heavy jobs (3 GB machine)
cd "$(dirname "$0")"
L=../../logs/v22-exactZ3-n5L8
python3 -u v22_z3_exact_v1.py all            >> $L/v22_z3_exact_v1.log 2>&1
python3 -u v22_tiltvar_uniform_v1.py         > $L/v22_tiltvar_partB.log 2>&1
python3 -u v22_n5_L8_block_v1.py validate    > $L/v22_n5_L8_block_validate.log 2>&1
python3 -u v22_n5_L8_block_v1.py ids         > $L/v22_n5_L8_block_ids.log 2>&1
python3 -u v22_n5_L8_block_v1.py run --pgrid 0.44,0.46,0.47,0.48,0.50 > $L/v22_n5_L8_block_run.log 2>&1
echo CHAIN_DONE
