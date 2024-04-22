import os
import argparse
from urllib.parse import urlparse
import subprocess

class Command:
    def __init__(self, dir, port):
        self.dir = dir
        self.port = port

def set_command(dir, port, type, command):
    if(dir == 'dirsearch'):
        command.dir = 'dirsearch -u {} --exclude-status 404'
        if(type == 'max'):
            command.dir = 'dirsearch -u {} -r --exclude-status 404'
    if(dir == 'gobuster'):
        command.dir = 'gobuster dir -u {} -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -t 30'
    
    if(port == 'rustscan'):
        command.port = 'rustscan -a {} --ulimit 5000 -- -sC -sV'
        if(type == 'min'):
            command.port = 'rustscan -a {} --ulimit 5000'
    if(port == 'nmap'):
        command.port = 'nmap -sC -sV {}'
        if(type == 'min'):
            command.port = 'nmap -sT -T5 {}'
        if(type == 'max'):
            command.port = 'nmap -sC -sV -p0-65535 {}'

def scan_URLs(urls, command, args):
    for url in urls:
        print("Scanning:", url)
        subprocess.run(f'mkdir result/{url}', shell=True)
        try:
            if(os.path.exists(f'result/{url}/{args.directory_scan}')):
                print(f'Skipped {url} {args.directory_scan}')
            else:
                print("Performing directory scan...")
                subprocess.run(f'touch /result/{url}/{args.directory_scan}')
                subprocess.run(command.dir.format(url)+f' -o {os.getcwd()}/result/{url}/{args.directory_scan}', shell=True)
            
            if(os.path.exists(f'result/{url}/{args.port_scan}')):
                print(f'Skipped {url} {args.port_scan}')
            else:
                print("Performing port scan...")
                subprocess.run(command.port.format(url)+f'| tee result/{url}/{args.port_scan}', shell=True)

            if(os.path.exists(f'result/{url}/whatweb')):
                print(f'Skipped {url} whatweb')
            elif(args.scan_type != 'min'):
                print('Performing whatweb...')
                subprocess.run(f'whatweb {url} | tee result/{url}/whatweb', shell=True)
            
            if(os.path.exists(f'result/{url}/nikto')):
                print(f'Skipped {url} nikto')
            elif(args.scan_type == 'max'):
                print('Performing nikto...')
                subprocess.run(f'nikto -host {url} | tee result/{url}/nikto', shell=True)
        
        except Exception as e:
            print("Error accessing url:", e)
    return

def main():
    description = 'A script that scan every url in provided file.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-f', '--file', required=True, help='File containing URLs')
    parser.add_argument('-t', '--scan-type', choices=['min','medium','max'],default='medium'  , help='Specify scan type [min/medium/max] (default: medium)')
    parser.add_argument('-d', '--directory-scan', choices=['dirsearch', 'gobuster'], default='dirsearch', help='Specify directory scan tool [dirsearch/gobuster] (default: dirsearch)')
    parser.add_argument('-p', '--port-scan', choices=['rustscan', 'nmap'], default='rustscan', help='Specify port scan tool [rustscan/nmap] (default: rustscan)')
    args = parser.parse_args()
    
    command = Command('', '')
    set_command(args.directory_scan, args.port_scan, args.scan_type, command)

    if args.file:
        print(f"Scanning URLs from file: {args.file}")
        print(f'Directory scan command: {command.dir}')
        print(f'Port scan command: {command.port}')
        with open(args.file, 'r') as file:
            links = file.readlines()
        urls = [urlparse(link).netloc for link in links]
        subprocess.run('mkdir result',shell=True)
        scan_URLs(urls, command, args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()