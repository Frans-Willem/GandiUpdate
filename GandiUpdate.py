#!/usr/bin/python
import xmlrpc.client
import sys
import urllib.request as urllib
import re
import itertools

def updateZone(apikey, zonename, records):
	api = xmlrpc.client.ServerProxy("https://rpc.gandi.net/xmlrpc/")
	# Find zone by zonename
	zones = api.domain.zone.list(apikey,{'name':zonename})
	if len(zones) < 1:
		# No such zone :(
		return False
	zone = zones[0]

	# Check to see if we need changes
	need_changes = False
	for record in records:
		records_found = api.domain.zone.record.list(apikey,
			zone['id'],
			zone['version'],
			{'name':record['name'],'type':record['type']}
			)
		# TODO: Check all dictionary keys for equality ?
		if len(records_found) == 0 or records_found[0]['value'] != record['value']:
			need_changes = True

	if not need_changes:
		# No changes needed
		return True

	# Create a new zone version
	new_zone_version = api.domain.zone.version.new(apikey, zone['id'], zone['version'])

	# Update all records
	for record in records:
		records_found = api.domain.zone.record.list(apikey,
			zone['id'],
			new_zone_version,
			{'name':record['name'],'type':record['type']}
			)
		if len(records_found) == 0:
			# Create a new record
			api.domain.zone.record.add(apikey,
				zone['id'],
				new_zone_version,
				record
				)
		else:
			# Change an existing record
			api.domain.zone.record.update(apikey,
				zone['id'],
				new_zone_version,
				{'id': records_found[0]['id']},
				record
				)

	# Set new version as current
	api.domain.zone.version.set(apikey, zone['id'], new_zone_version)
	return True

# records = api.domain.zone.record.list(apikey, zone['id'],zone['version'],{'name':recordname,'type':recordtype});
# print(records)

def fetch_url(url):
	opener = urllib.build_opener()
	opener.addheaders = [('User-agent',
		"Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20120304 Firefox/25.0")]
	conn = opener.open(url, timeout=5)
	content = conn.read()
	content = content.decode('UTF-8')
	return content




def url_re(url, regexp):
	try:
		content = fetch_url(url)
		m = re.search(regexp, content)
		if not m:
			print("No match on", url)
			return None
		result = m.group(0)
		return result if len(result) > 0 else None
	except:
		print("Error while trying",url)
		return None

def most_common(lst):
	return max(set(lst), key=lst.count)

regexp_ipv4 = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'

ipv4_lookups = [
	"http://ip4.me",
	"http://whatismyipaddress.com",
	"http://myexternalip.com/raw",
	"http://ipinfo.io",
	"http://httpbin.org/ip",
	"http://www.google.com"
]

resolved_ips = list(map((lambda server: url_re(server, regexp_ipv4)), ipv4_lookups))
resolved_ips = list(filter((lambda result: not not result and len(result) > 0), resolved_ips))
my_ip = most_common(resolved_ips)

if len(sys.argv) < 4:
	print("Usage:", sys.argv[0], " <apikey> <zonename> <subdomain>")
	exit(0)
	
apikey = sys.argv[1]
zonename = sys.argv[2]
records = [
	{	'name': sys.argv[3],
		'type': 'A',
		'value': my_ip
	}
]
print("Updating", zonename, records)

updateZone(apikey, zonename, records)
