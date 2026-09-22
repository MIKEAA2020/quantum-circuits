"""Sandbox kill/resume test for the patched orbit_table checkpoint logic.

Modes:
  clean  - wipe sandbox, run the full nb=3 table in one shot (no state),
           record md5 of reps/counts/ids
  kill   - wipe sandbox, start the same pass WITH state_path, SIGKILL after
           ~6 s, assert the state file exists and reps_nb3.npy does NOT
           (incomplete pass must not be mistaken for a completed one)
  resume - rerun the same call to completion; must log the RESUMED line and
           produce byte-identical reps/counts/ids vs the clean run
"""
import hashlib, json, os, signal, subprocess, sys, time

SB = '/home/z/my-project/scripts/test_v22_sandbox'
RES = os.path.join(SB, 'sb_results', 'tmp_n5L8block')
SCRIPT = os.path.join(SB, 'sb_script.py')
STATE = os.path.join(RES, 'ids_nb3_state.npz')

DRIVER = r'''
import sys, os
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts/v22-exactZ3-n5L8')
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts')
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts/v18-n4n5-smc')
sys.path.insert(0, {script_dir!r})
import importlib.util
spec = importlib.util.spec_from_file_location('sbmod', {script!r})
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
kw = dict(chunk=50_000)
if sys.argv[1] in ('state', 'resume'):
    kw.update(state_path={state!r}, save_every=2)
m.orbit_table(3, **kw)
'''


def wipe():
    subprocess.run(['rm', '-rf', os.path.join(SB, 'sb_results')])


def md5s():
    out = {}
    for f in ('reps_nb3.npy', 'counts_nb3.npy', 'ids_nb3.npy'):
        p = os.path.join(RES, f)
        out[f] = hashlib.md5(open(p, 'rb').read()).hexdigest() \
            if os.path.exists(p) else 'ABSENT'
    return out


def run(mode, timeout=300):
    drv = os.path.join(SB, f'drv_{mode}.py')
    open(drv, 'w').write(DRIVER.format(script_dir=SB, script=SCRIPT,
                                       state=STATE))
    t0 = time.time()
    if mode == 'kill':
        proc = subprocess.Popen([sys.executable, drv, 'state'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        time.sleep(1.2)
        alive = proc.poll() is None
        proc.send_signal(signal.SIGKILL)
        out, _ = proc.communicate()
        print(f'  kill: alive_after_1.2s={alive}, rc={proc.returncode}')
        open(os.path.join(SB, f'log_{mode}.txt'), 'w').write(out)
        return
    p = subprocess.run([sys.executable, drv, mode], capture_output=True,
                       text=True, timeout=timeout)
    open(os.path.join(SB, f'log_{mode}.txt'), 'w').write(p.stdout + p.stderr)
    print(f'  {mode}: rc={p.returncode} ({time.time()-t0:.0f}s)')


mode = sys.argv[1]
if mode == 'clean':
    wipe()
    run('clean')
    print(json.dumps(md5s(), indent=1))
elif mode == 'kill':
    wipe()
    run('kill')
    st_ok = os.path.exists(STATE)
    reps_absent = not os.path.exists(os.path.join(RES, 'reps_nb3.npy'))
    ids_partial = os.path.exists(os.path.join(RES, 'ids_nb3.npy'))
    print(f'  kill asserts: state_exists={st_ok}, reps_absent={reps_absent}, '
          f'ids_partial={ids_partial}')
    assert st_ok and reps_absent and ids_partial, 'KILL-MODE ASSERTS FAILED'
    print('  KILL MODE OK')
elif mode == 'resume':
    run('resume')
    log = open(os.path.join(SB, 'log_resume.txt')).read()
    assert 'RESUMED' in log, 'NO RESUMED LINE — resume path not exercised!'
    print('  RESUMED line present:', [l for l in log.splitlines()
                                      if 'RESUMED' in l][0].strip())
    print(json.dumps(md5s(), indent=1))
elif mode == 'compare':
    a = json.load(open(os.path.join(SB, 'md5_clean.json')))
    b = json.load(open(os.path.join(SB, 'md5_resume.json')))
    print('  clean vs resume:', 'IDENTICAL' if a == b else f'MISMATCH {a} {b}')
    assert a == b, 'MISMATCH'
