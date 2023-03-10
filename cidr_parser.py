import json, ipaddress, requests, argparse

#Requires dnspython to be installed
try: 
    import dns.resolver
except ImportError: 
    print("This script requires dnspython modules")
    print("pip3 install dnspython")
    raise SystemExit

#Pass Hostname Argument through CLI
CLI=argparse.ArgumentParser()
CLI.add_argument('--list', nargs='+', required=True)
args=CLI.parse_args()
hostname_list=[]
hostname_list=args.list

#Return A Record 50 Times. Run a new DNS query every time to avoid cache lookups.
list=[]
for hostname in hostname_list:
    count=0
    print(hostname)
    while count<50:
        print(hostname)
        resolver=dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['1.1.1.1','8.8.8.8']
        answer=resolver.resolve(hostname, 'a')
        for ipval in answer:
            ipaddr=(ipval.to_text())
            list.append(ipaddr)
        count=count+1

#Iterate Through List of IPs, and return Unique IPs
unique_ip_list=[]
for x in list:
    if x not in unique_ip_list:
        unique_ip_list.append(x)
print("")
print("Unique IP's From DNS A Records")
print(unique_ip_list)

# Download Latest OCI JSON file
url = 'https://docs.oracle.com/iaas/tools/public_ip_ranges.json'
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    with open('cidrs.json', 'w') as f:
        f.write(response.text)
    #print('Latest JSON downloaded')
    regions = json.loads(response.text)
    cidrs = (regions["regions"])
else:
    print(f'Error retrieving JSON file: {response.status_code}')

cidr_blocks=[]
for ip_addr in unique_ip_list:
    for region in cidrs:
        for c in region['cidrs']:
            if ipaddress.ip_address(ip_addr) in ipaddress.ip_network(c['cidr']):
                #cidr_found=("{}-{}").format(region['region'], c['cidr'])
                #Uncomment this line if you want to see the region for each prefix.
                cidr_found=("{}").format(c['cidr'])
                cidr_blocks.append(cidr_found)
                cidr_blocks.append(cidr_found)

unique_cidr_blocks=[]
for x in cidr_blocks:
    if x not in unique_cidr_blocks:
        unique_cidr_blocks.append(x)
print("")
print("Unique CIDR BLOCKS matched with OCI JSON file")
print(unique_cidr_blocks)
print("There are {} unique CIDRs in this list.".format(len(unique_cidr_blocks)))
