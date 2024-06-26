import shodan
from pyExploitDb import PyExploitDb
import os
import re
pEdb = PyExploitDb()
pEdb.debug = False
pEdb.openFile()

# Function to validate folder name for Windows
def valid_windows_folder_name(s):
    return re.sub(r'[^a-zA-Z0-9 ]', '_', s)



def main():
    # Get API key from file
    try:
        with open("api_key.txt", "r") as f:
            api_key = f.read()
            api_key = api_key.strip()
    except FileNotFoundError:
        return print("File not found. Please create a file named api_key.txt and paste your Shodan API key in it.")
    api = shodan.Shodan(api_key)

    try:
        # Search Shodan
        query = input("Enter search query: ")
        results = api.search(query)

        # Show the results
        print('Results found: {}'.format(results['total']))
        if results['total'] == 0:
            return print("No results found.")
        folder_name = valid_windows_folder_name(query)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for result in results['matches']:
                with open(f"{folder_name}/{folder_name}_results.txt", "a") as f:
                    result = result['ip_str']
                    f.write(str(result)+'\n')
    except shodan.APIError as e:
        print('Error: {}'.format(e))

    # Get ips from file
    with open(f"{folder_name}/{folder_name}_results.txt", "r") as f:
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
                try:
                # Check if file exists and exploit is already in file
                    with open(f"{folder_name}/{filename}", "r") as f:
                        if exploit['id'] in f.read():
                            continue
                except:
                    pass
                with open(f"{folder_name}/{filename}", "a") as f:
                    # Check if exploit is already in file
                    f.write(str(exploit)+'\n')
            print(f"Found {len(shodan_info['vulns'])} exploitable vulnerabilities on {ip}. All exploits are saved in {filename} file.")
        except shodan.APIError as e:    
            return print('Error: {}'.format(e))

if __name__ == "__main__":
    main()