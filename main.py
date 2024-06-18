import shodan
from pyExploitDb import PyExploitDb
pEdb = PyExploitDb()
pEdb.debug = False
pEdb.openFile()

api = shodan.Shodan('Your API Key')

try:
    # Search Shodan
    query = input("Enter search query: ")
    results = api.search(query)

    # Show the results
    print('Results found: {}'.format(results['total']))
    for result in results['matches']:
            with open(f"{query}_results.txt", "a") as f:
                result = result['ip_str']
                f.write(str(result)+'\n')
except shodan.APIError as e:
    print('Error: {}'.format(e))

# Get ips from file
with open(f"{query}_results.txt", "r") as f:
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
            with open(filename, "a") as f:
                f.write(str(exploit)+'\n')
        print(f"Found {len(shodan_info['vulns'])} exploitable vulnerabilities on {ip}. All exploits are saved in {filename} file.")
    except shodan.APIError as e:    
        print('Error: {}'.format(e))