#!/usr/bin/env python

#import the subprocess module
import subprocess
import optparse
import re

#Def arguments
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

#Def change mac address
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#Def get current mac and use regex to check it
def get_current_mac(interface):
    #Check de result van ifconfig + de interface
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    #Regex and search in 'ifconfig_result'
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read the MAC address")

#Get arguments that the user enters
options = get_arguments()
#Get the current mac
current_mac = get_current_mac(options.interface)
#Print the current mac
print("Current MAC = " + str(current_mac)) #casting
#Change the mac address
change_mac(options.interface, options.new_mac)

#Check if the user arguments really got changed
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was succesfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed. ")
