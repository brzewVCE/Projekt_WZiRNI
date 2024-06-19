import shodan
from pyExploitDb import PyExploitDb
import os
pEdb = PyExploitDb()
pEdb.debug = False
pEdb.openFile()

# Get API key from file
try:
    with open("api_key.txt", "r") as f:
        api_key = f.read()
        api_key = api_key.strip()
except FileNotFoundError:
    print("File not found. Please create a file named api_key.txt and paste your Shodan API key in it.")
    exit()
api = shodan.Shodan(api_key)

try:
    # Search Shodan
    query = input("Enter search query: ")
    results = api.search(query)

    # Show the results
    print('Results found: {}'.format(results['total']))
    if results['total'] == 0:
        print("No results found.")
        exit()
    if not os.path.exists(query):
        os.makedirs(query)
    for result in results['matches']:
            with open(f"{query}/{query}_results.txt", "a") as f:
                result = result['ip_str']
                f.write(str(result)+'\n')
except shodan.APIError as e:
    print('Error: {}'.format(e))

# Get ips from file
with open(f"{query}/{query}_results.txt", "r") as f:
    ips = f.readlines()
    ips = [x.strip() for x in ips]

# Search for exploits and save them to file
for ip in ips:
    try:
        shodan_info = api.host(ip)
        filename = ip + ".txt"
        if 'vulns' not in shodan_info:
            continue
        for vuln in shodan_info['vulns']:
            exploit = pEdb.searchCve(vuln)
            if exploit == []:
                continue
            with open(f"{query}/{filename}", "a") as f:
                f.write(str(exploit)+'\n')
        print(f"Found {len(shodan_info['vulns'])} exploitable vulnerabilities on {ip}. All exploits are saved in {filename} file.")
    except shodan.APIError as e:    
        print('Error: {}'.format(e))