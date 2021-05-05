from subprocess import check_output

ip = check_output(['hostname', '-I']).decode('ascii')

print(ip)