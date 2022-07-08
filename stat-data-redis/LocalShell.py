import subprocess

class LocalShell:
    def execute(self,command):
        ret =  subprocess.check_output(command, shell=True,close_fds=True)
        return ret.decode(encoding="ISO-8859-1").strip()
