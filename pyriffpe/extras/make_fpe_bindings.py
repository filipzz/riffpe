# This script attempts to build Python bindings for https://github.com/capitalone/fpe
# using gopy, goimports and pybindgen.
#
# Requires `pybindgen` and `go >= 1.15`.
# The remaining tools are pulled automatically
#

import json
import os
import subprocess
import sys


# Ensure go requirements are installed and in the PATH
_sub = subprocess.run(('go', 'install', 'golang.org/x/tools/cmd/goimports@latest'))
_sub.check_returncode()
_sub = subprocess.run(('go', 'install', 'github.com/go-python/gopy@latest'))
_sub.check_returncode()

_sub = subprocess.run(('go', 'env', '-json'), stdout=subprocess.PIPE)
_sub.check_returncode()
_go_env = json.loads(_sub.stdout)
_go_path = _go_env['GOPATH']

_nenv = os.environ.copy()
_nenv['PATH'] += (os.pathsep + os.path.join(_go_path, 'bin'))

_bench_ws_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.bench_ws'))

# Create a go module (if doesn't exist) for the bindings and build them
_fpe_path = os.path.join(_bench_ws_path, f'gofpe')
os.makedirs(_fpe_path, exist_ok=True)
with open(os.path.join(_fpe_path, 'go.mod'), 'w') as f:
    f.write(f"module gofpe")

_sub = subprocess.run(('go', 'get', f'github.com/capitalone/fpe'),
                    env=_nenv, cwd=_fpe_path)
_sub.check_returncode()

_sub = subprocess.run(('gopy', 'build', '-vm', sys.executable, '-name', 'fpe', f'github.com/capitalone/fpe/ff1', f'github.com/capitalone/fpe/ff3'),
                    env=_nenv, cwd=_fpe_path)
_sub.check_returncode()
