import subprocess
import warnings

from setuptools import setup

# There doesn't seem to be a way to import local files from setup.py anymore.
# Ideally, the following would be `from setup_cmake import CMakeExtension, CMakeBuild`
with open("setup_cmake.py") as f:
    code = compile(f.read(), "somefile.py", 'exec')
    exec(code, globals(), locals())


try:
    setup(ext_modules=[CMakeExtension("riffpe._native", "pyriffpe/riffpe")], cmdclass={"build_ext": CMakeBuild})
except (subprocess.CalledProcessError, ImportError):
    warnings.warn("Native build failed, native implementation will not be installed.")
    setup()
