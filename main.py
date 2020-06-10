#!/usr/bin/env python
"""request-sim.py: ThermalNet ServiceNow Request Simulator"""

# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, TermalNet ServiceNow Request Simulator'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

import time, random, decimal, configparser, pysnow, names, sys, ast
from colorama import Fore, Back, Style
from texttable import Texttable
from tqdm import tqdm


def temp_check():
    low_temp = config['temp']['low_temp']
    high_temp = config['temp']['high_temp']
    temp_fahrenheit = float(
        decimal.Decimal(
            random.randrange(int(low_temp) * 100,
                             int(high_temp) * 100)) / 100)
    if temp_fahrenheit > 99.5:
        temp_result = 'no'
    elif temp_fahrenheit < 99.5:
        temp_result = 'yes'
    else:
        temp_result = 'na'
    return [temp_fahrenheit, temp_result]


def access_check(temp, ppe):
    if ppe == 'yes' and temp == 'yes':
        access_result = 'true'
    else:
        access_result = 'false'
    return [access_result]


def now(requester, location, temp_fahrenheit, temp_result, ppe_result, access):
    # define a resource
    request = c.resource(api_path='/table/sn_imt_monitoring_request_for_entry')
    # create te payload
    new_record = {
        'ppe_result': ppe_result,
        'location': location,
        'access_granted': access,
        'temp_fahrenheit': temp_fahrenheit,
        'temperature_result': temp_result,
        'requester': requester
    }
    # create a new sevicenow request record
    # result = request.create(payload=new_record)
    print(Fore.GREEN + '\nJSON payload sent to ServiceNow' + Style.RESET_ALL)
    print(new_record)


def main():
    # locations
    locations = ast.literal_eval(config['now_location']['locations'])
    status = ast.literal_eval(config['now_states']['status'])
    # payload creation
    count = 0
    # while (count < int(sys.argv[1])):
    while (count < 10):
        requester = names.get_full_name()
        location = random.choice(locations)
        temp = temp_check()
        ppe = random.choice(status)
        access = access_check(temp[1], ppe)
        print(Fore.YELLOW + '\nThermalNet Simulator Data' + Style.RESET_ALL)
        t = Texttable()
        t.set_cols_width([20, 10, 8, 8, 8, 8])
        t.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c'])
        t.add_rows(
            [['requester', 'location', 'temp', 'temp ok', 'ppe ok', 'access'],
             [requester, location, temp[0], temp[1], ppe, access[0]]])
        print(t.draw())
        now(requester, location, temp[0], temp[1], ppe, access[0])
        # time.sleep(cycle_time)
        print('\n')
        # visual cycle time
        for i in tqdm(range(cycle_time)):
            time.sleep(1)
        count = count + 1


if __name__ == '__main__':
    count = sys.argv[0]
    # read and parse config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    # servicenow client connection
    c = pysnow.Client(
        instance=(config['now_api']['instance']),
        user=(config['now_api']['user']),
        password=(config['now_api']['password']))
    # set cycle time
    cycle_time = int(config['local']['cycle_time'])
    main()
