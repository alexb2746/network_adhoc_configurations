import os
import requests
import concurrent.futures
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

conf_file = 'configuration_set_commands.set'
network_password = os.getenv('NETWORK_PASSWORD')


def diff_check(result):
    if 'fpc' not in result['name']:
        hostname = result['name'] + #cant show what was here
        junos_username = 'python'
        junos_password = network_password
        # open a connection with the device and start a NETCONF session
        try:
            dev = Device(host=hostname, user=junos_username, passwd=junos_password)
            dev.open()
        except ConnectError as err:
            print(red_output("Cannot connect to device: {0}".format(err)))
            return

        dev.bind(cu=Config)

        # Lock the configuration, load configuration changes, and commit
        print(yellow_output ("Locking the configuration"))
        try:
            dev.cu.lock()
        except LockError as err:
            print(red_output("Unable to lock configuration: {0}".format(err)))
            dev.close()
            return

        print(yellow_output ("Loading configuration changes"))
        try:
            dev.cu.load(path=conf_file, format='set', merge=True)
        except (ConfigLoadError, Exception) as err:
            print(red_output ("Unable to load configuration changes: {0}".format(err)))
            print(red_output ("Unlocking the configuration"))
            try:
                dev.cu.unlock()
            except UnlockError:
                print(red_output("Unable to unlock configuration: {0}".format(err)))
            dev.close()
            return

        print(red_output(f"Doing a diff for {hostname}, DIFF Below:"))
        yellow_output(dev.cu.pdiff())
        
        commit_check = dev.cu.commit_check()

        if commit_check == True:
            print(green_output(f"Commit check passed for {hostname}"))
        else:
            print(red_output(f"Commit check failed for {hostname}"))
            dev.cu.unlock()
            dev.close()
            return
            
        print(yellow_output("Unlocking the configuration"))
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print(red_output(f"Unable to unlock configuration: {0}".format(err)))

        # End the NETCONF session and close the connection
        dev.close()

# This will make an API call to netbox using Alex's API token.
# It will return a list of devices that are active and have a platform of junos.
def get_devices():

    url = #secific netbox api link, cant show what was here

    payload = {}
    headers = {
      'Authorization': #'Token: #cant show what was here'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    response = response.json()

    return(response)

def green_output(string):
    """Prints a string in green"""
    return ("\033[32m" + "*" * 50 + "\033[0m\n" +
        "\033[32m" + "*" * 5 + f"\033[0m {string} \033[32m" + "*" * 5 + "\033[0m\n" +
        "\033[32m" + "*" * 50 + "\033[0m")

def red_output(string):
    """Prints a string in red"""
    return ("\033[31m" + "*" * 50 + "\033[0m\n" +
        "\033[31m" + "*" * 5 + f"\033[0m {string} \033[31m" + "*" * 5 + "\033[0m\n" +
        "\033[31m" + "*" * 50 + "\033[0m")

def yellow_output(string):
    """Prints a string in yellow"""
    return ("\033[33m" + "*" * 50 + "\033[0m\n" +
        "\033[33m" + "*" * 5 + f"\033[0m {string} \033[33m" + "*" * 5 + "\033[0m\n" +
        "\033[33m" + "*" * 50 + "\033[0m")

def main():
    print(yellow_output("Getting devices from netbox."))
    devices = get_devices()
    print(green_output("Done getting devices from netbox!"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(diff_check, result) for result in devices['results']]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    
if __name__ == "__main__":
    main()