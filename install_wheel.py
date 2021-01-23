import glob, pip
for path in glob.glob("./dao-wheel/*.whl"):
    pip.main(['install', path])
