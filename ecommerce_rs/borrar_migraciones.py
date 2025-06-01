import os
import glob

for root, dirs, files in os.walk("."):
    if "migrations" in dirs:
        path = os.path.join(root, "migrations")
        for file in glob.glob(os.path.join(path, "*.py")):
            if not file.endswith("__init__.py"):
                print("Borrando:", file)
                os.remove(file)
        for file in glob.glob(os.path.join(path, "*.pyc")):
            os.remove(file)
