import sys, os
virt_binary = "/home/timdobbs/.env/env/34/bin/python"
if sys.executable != virt_binary: os.execl(virt_binary, virt_binary, *sys.argv)
sys.path.append(os.getcwd())
from __init__ import app as application
