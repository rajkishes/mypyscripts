from netmiko import ConnectHandler
from napalm import get_network_driver
import paramiko
from datetime import date
from getpass import getpass
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import pathlib

#Username and password prompts
user = input("Please enter your username: ")
pwd = getpass()

#Reads the commands from the file
with open ("commands_file.txt") as f:
	commands_to_execute = f.read().splitlines()

#Reads the devicelist from the file
with open ("devices_list.txt") as f:
	all_hosts = f.read().splitlines()

print (all_hosts)

#Create a directory to store the log files, if the directory already exits, it will use the same one

config_dir = "Config-Logs"
pathlib.Path(config_dir).mkdir(exist_ok=True)

#Iterates through the device list in the device_list file

for device in all_hosts:
    host_ip = device
    #device_dir = config_dir + "/" + host_ip
    #pathlib.Path(device_dir).mkdir(exist_ok=True)
    print (f'connecting to {host_ip}...')
    iosv_device = {
		'device_type' : 'cisco_ios',
		'ip' : host_ip,
		'username' : user,
		'password' : pwd,
		'secret' : pwd,
	}
	
    try:
	    net_connect = ConnectHandler(**iosv_device)
    except (AuthenticationException):
	    print(f'Authentication to {host_ip} failed')
	    continue
    except (SSHException):
	    print(f'Encountered a time out to {host_ip}')
	    continue
    except (NetMikoTimeoutException):
	    print(f'SSH failed; check if SSH is enabled on {host_ip}')
	    continue
    except Exception as unknown_error:
	    print(f'unknown error logging into {host_ip}')
	    continue
		

    filename = f"" + str(date.today()) + ".txt"
    #Creates a file with the device ip as name inside the folder
    with open(filename, "a+") as f:
        f.write(host_ip)
        f.write("\n")
        f.write("=" * (80 ))
        f.write("\n")
        for command in commands_to_execute:
            f.write("=" * 20)
            f.write(command)
            f.write("=" * (80 - len(command)))
            f.write("\n" * 2)
            cmd_output = net_connect.send_command(command)
            f.write(cmd_output + "\n" *2)

