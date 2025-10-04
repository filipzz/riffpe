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

from pathlib import Path

_bench_ws_path = (Path(__file__).parent / '.bench_ws').absolute()
_bench_ws_path.mkdir(exist_ok=True)

# Ensure go requirements are installed and in the PATH
_sub = subprocess.run(('go', 'install', 'golang.org/x/tools/cmd/goimports@latest'))
_sub.check_returncode()
# gopy is currently (10.2025) broken on current Go (1.25) and needs some manual changes
if False:
    _sub = subprocess.run(('go', 'install', 'github.com/go-python/gopy@latest'))
    _sub.check_returncode()
else:
    _gopy_path = _bench_ws_path / 'gopy'
    _gopy_patch = Path(__file__).parent / 'gopy.patch'
    if _gopy_path.exists():
        _sub = subprocess.run(('git', 'restore', '.'), cwd=_gopy_path)
    else:
        _sub = subprocess.run(('git', 'clone', 'https://github.com/go-python/gopy'), cwd=_bench_ws_path)
    _sub.check_returncode()
    _sub = subprocess.run(('git', 'apply', _gopy_patch), cwd=_gopy_path)
    _sub.check_returncode()
    _sub = subprocess.run(('go', 'build'), cwd=_gopy_path)
    _sub.check_returncode()
    _sub = subprocess.run(('go', 'install'), cwd=_gopy_path)
    _sub.check_returncode()


_sub = subprocess.run(('go', 'env', '-json'), stdout=subprocess.PIPE)
_sub.check_returncode()
_go_env = json.loads(_sub.stdout)
_go_path = _go_env['GOPATH']

_nenv = os.environ.copy()
_nenv['PATH'] += (os.pathsep + os.path.join(_go_path, 'bin'))


# Create a go module (if doesn't exist) for the bindings and build them
_fpe_path = os.path.join(_bench_ws_path, 'gofpe')
os.makedirs(_fpe_path, exist_ok=True)
with open(os.path.join(_fpe_path, 'go.mod'), 'w') as f:
    f.write("module gofpe")

_sub = subprocess.run(('go', 'get', 'github.com/capitalone/fpe'),
                    env=_nenv, cwd=_fpe_path)
_sub.check_returncode()

_sub = subprocess.run(('gopy', 'build', '-vm', sys.executable, '-name', 'fpe', 'github.com/capitalone/fpe/ff1', 'github.com/capitalone/fpe/ff3'),
                    env=_nenv, cwd=_fpe_path)
_sub.check_returncode()
