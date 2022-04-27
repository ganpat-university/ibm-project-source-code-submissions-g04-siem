import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.25.132', username='kali', password='kali')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("whoami")
print(f'STDOUT: {ssh_stdout.read().decode("utf8")}')


file=open('alert.txt','w')
file.write("Trigger executed successfully!!")
file.close()