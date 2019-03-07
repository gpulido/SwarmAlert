import argparse
import re
import time

import docker
from pushover import init, Client

__version__ = '0.0.3-dev'
__author__ = 'gpt'

def service_list_to_str(services_list):
    return '\n'.join([s.name for s in services_list])

def monitor_swarm_pushover(docker_client, white_pattern_list, black_list):
    logger.debug("Getting services from docker")
    services = docker_client.services.list()
    if len(white_pattern_list) > 0:
        services = [s for s in services if s.name in white_pattern_list and s.name not in black_list]
    else:
        services = [s for s in services if s.name not in black_list]
    
    services_name = [service.name for service in services]
    logger.debug(str(services_name))  
    not_running_services = [service for service in services if(len(service.tasks({'desired-state':'Running'})) == 0)]
    logger.debug("Not running:" + str([service.name for service in not_running_services]))
    err_msg = ""
    if len(not_running_services) != 0:
        err_msg = "Detected Stopped Services: \n%s\n%s" % (service_list_to_str(not_running_services), err_msg)

    if err_msg == "":
        return "OK", "OK: detect no stopped services"
    else:
        return "ERROR", err_msg


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True, help="Pushover Token.", type=str)
    parser.add_argument('--app_key', required=True, help="Pushover Application key.", type=str)
    parser.add_argument('--whitelist', default='', required=False,
                        help="List of services to monitor. If not provided or empty, all will be monitorized.", type=str)
    parser.add_argument('--blacklist', default='', required=False,
                        help="Skip checking certain services.", type=str)
    parser.add_argument('--check_interval', default='300', required=False, help="Periodical check. By seconds.",
                        type=int)
    parser.add_argument('--msg_prefix', default='', required=False, help="Pushover message prefix.", type=str)
    parser.add_argument('--loglevel', default='DEBUG', choices=['INFO', 'DEBUG'],  required=False, help="Logging level.", type=str)
    l = parser.parse_args()
    #Configure logging
    import logging
    numeric_level = getattr(logging, l.loglevel.upper(), None)
    logging.basicConfig(format= '%(asctime)s %(levelname)s:%(message)s', level=numeric_level)
    logger = logging.getLogger()

    logger.info("Initializing monitor")

    check_interval = l.check_interval
    white_pattern_list = l.whitelist.split(',')    
    if white_pattern_list == ['']:
        white_pattern_list = []
    logger.debug("Whitelist: " + str(white_pattern_list))
    
    black_list = l.blacklist.split(',')    
    if black_list == ['']:
        black_list = []
    logger.debug("BlackList: " + str(black_list))

    pushover_token = l.token
    pushover_key = l.app_key
    msg_prefix = l.msg_prefix

    if pushover_token == '':
        print("Warning: Please provide a valid pushover token.")
    if pushover_key == '':
        print("Warning: Please provide a valid pushover application key.")
    
    logger.info("Registering PushoverClient")
    pushover_client = Client(pushover_key, api_token="pushover_token")
    pushover_client.send_message("Initializing monitoring", title="SwarmAlert")
    logger.info("Registering Docker Client")
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    has_send_error_alert = False
    while True:
        (status, err_msg) = monitor_swarm_pushover(docker_client, white_pattern_list, black_list)
        logger.debug(" Ouput of monitor: " + status + " " + err_msg)
        if msg_prefix != "":    
            err_msg = "%s\n%s" % (msg_prefix, err_msg)                
        
        if status == "OK":
            if has_send_error_alert is True:
                logger.debug("Sending pushover notification:" + err_msg)
                pushover_client.send_message(err_msg, title="SwarmAlert")
                has_send_error_alert = False
        else:
            if has_send_error_alert is False:
                logger.debug("Sending pushover notification:" + err_msg)
                pushover_client.send_message(err_msg, title="SwarmAlert")           
                # avoid send alerts over and over again
                has_send_error_alert = True
        time.sleep(check_interval)
# File : monitor-docker-slack.py ends

