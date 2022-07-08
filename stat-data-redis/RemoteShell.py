from paramiko.client import SSHClient
import atexit

class RemoteShell:
    def __init__(self,remote_connect):
        self.client = SSHClient()
        self.client.load_system_host_keys()
        for ssh_server in remote_connect:
            try:
                self.client.connect(ssh_server["host"],username=ssh_server["user"],timeout=15)
                atexit.register(self.close)
                break
            except:
                print("ERROR::SSH CONNECTION FAILED!! {}".format(ssh_server))
                continue

    def execute(self,command,timeout=15):
        try:
            stdin,stdout,stderr = self.client.exec_command(command,timeout=timeout)
            return stdout.read().decode("utf8")
        except :
            print("ERROR::SSH EXECUTE TIME OUT!! {}".format(config.COMMANDS["nodes_command"]))
            return None

    def close(self):
        self.client.close()

## UNIT TEST
if __name__ == "__main__":
    clien = RemoteShell("localhost","ruomiao")
    client.execute(ls)
