# NamecheapDDNS

NamecheapDDNS is a Python script which leverages the url that Namecheap provides to update the A record of a domain.
The following url is used (The script uses https):
dynamicdns.park-your-domain.com/update?host=**<Subdomain>**&domain=**<Domain>**&password=**<Dynamic DNS password>**&ip=**[ip. If left blank, public ip is used.]**

## Installation

You can copy the file NamecheapDDNS.py into your /usr/local/bin

## Usage

Usage: updateNCIP <domain> <password> <subdomain> [-a | --ip <specifiedip>] [--help]
Where subdomain is the host you want to assign an ip to (eg. "@", "www").
NOTE: By default, the argument "\*" (wildcard) points to all of the files in a directory. To define a host that is a literal wildcard, use a backslash (eg. "\\*")

## Contributing

Contribute as you would any other GitHub project. 


## License

TODO: Write license
]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>
