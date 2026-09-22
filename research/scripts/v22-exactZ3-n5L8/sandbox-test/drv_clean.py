
import sys, os
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts/v22-exactZ3-n5L8')
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts')
sys.path.insert(0, '/home/z/my-project/quantum-circuits/research/scripts/v18-n4n5-smc')
sys.path.insert(0, '/home/z/my-project/scripts/test_v22_sandbox')
import importlib.util
spec = importlib.util.spec_from_file_location('sbmod', '/home/z/my-project/scripts/test_v22_sandbox/sb_script.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
kw = dict(chunk=50_000)
if sys.argv[1] == 'state':
    kw.update(state_path='/home/z/my-project/scripts/test_v22_sandbox/sb_results/tmp_n5L8block/ids_nb3_state.npz', save_every=2)
m.orbit_table(3, **kw)
