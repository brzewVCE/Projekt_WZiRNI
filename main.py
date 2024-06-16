from shodan import Shodan
from pyExploitDb import PyExploitDb
pEdb = PyExploitDb()
pEdb.debug = False
pEdb.openFile()

api = Shodan('YOUR_API_KEY')

# Lookup an IP
ip = input("Enter IP address: ")
shodan_info = api.host(ip)
filename = ip + ".txt"
for vuln in shodan_info['vulns']:
    exploit = pEdb.searchCve(vuln)
    if exploit == []:
        continue
    with open(filename, "a") as f:
        f.write(str(exploit)+'\n')

print(f"Found {len(shodan_info['vulns'])} vulnerabilities on {ip}. All exploits are saved in {filename} file.")