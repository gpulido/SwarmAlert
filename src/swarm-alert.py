import argparse
import re
import time

import docker
#from pushover import init, Client
from utils import *
from apprise import NotifyType
import apprise

__version__ = '0.1.0-dev'
__author__ = 'gpt'


def monitor_swarm(docker_client, white_list, black_list):
    """[summary]
    Review the docker_client containers checking for the services on the white list excluding the
    ones that are in the blacklist
    Arguments:
        docker_client {[str]} -- [description]
        white_list {[str]} -- List of services to look after. If empty all services will be monitored
        black_list {[str]} -- List of services to exclude from the monitorization
    
    Returns:
        {[str]} -- List of string of stopped services
    """
    logger.debug("Getting services from docker")
    services = docker_client.services.list()
    if len(white_list) > 0:
        services = [s for s in services if s.name in white_list and s.name not in black_list]
    else:
        services = [s for s in services if s.name not in black_list]
    
    services_name = [service.name for service in services]
    logger.debug(str(services_name))  
    not_running_services = [service for service in services if(len(service.tasks({'desired-state':'Running'})) == 0)]    
    return not_running_services    


def configure_logger(logger_level):
    import logging
    numeric_level = getattr(logging, logger_level, None)
    logging.basicConfig(format= '%(asctime)s %(levelname)s:%(message)s', level=numeric_level)
    return logging.getLogger()
    

def analyse_status(stopped_services, new_stopped):    
    recovered_services = [s for s in stopped_services if s not in stopped_services]    
    new_failing = [s for s in new_stopped if s not in stopped_services]
    keep_failing = [ s for s in stopped_services if s in stopped_services]
    return (recovered_services, new_failing, keep_failing)


def monitor_and_notify(docker_client, apobj):
    logger.info("Starting monitor")    
    stopped_services = []

    while True:        
        new_stopped = monitor_swarm(docker_client, white_pattern_list, black_list)
        (recovered, failing, old_failing) = analyse_status(stopped_services, new_stopped)
        logger.debug(f'Recovered: {str(recovered)}\nFailing: {str(failing)}\nold_failing: {str(old_failing)}') 
        if len(recovered) != 0:                        
            recovered_msg = f'{msg_prefix} Recovered Services: \n {service_list_to_str(recovered)}'   
            logger.debug("Sending notification:" + recovered_msg)
            apobj.notify(body=recovered_msg,
                        title='SwarmAlert',
                        notify_type=NotifyType.INFO)                              
        
        if len(failing) != 0:                        
            failed_msg = f'{msg_prefix} Detected New Stopped Services: \n {service_list_to_str(failing)}'   
            logger.debug("Sending notification:" + failed_msg)
            apobj.notify(body=failed_msg,
                        title='SwarmAlert',
                        notify_type=NotifyType.FAILURE)        
        
        #Only notify old failing services if we are already notifing changes
        if len(old_failing) != 0 and (len(failing) != 0 or len(recovered)!= 0):
            old_failed_msg = f'{msg_prefix} Already Stopped Services: \n {service_list_to_str(old_failing)}'   
            logger.debug("Sending notification:" + old_failed_msg)
            apobj.notify(body=old_failed_msg,
                        title='SwarmAlert',
                        notify_type=NotifyType.FAILURE)        

        stopped_services = new_stopped
        time.sleep(check_interval)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    # parser.add_argument('--user_key', required=True, help="Pushover User Key.", type=str)
    # parser.add_argument('--api_token', required=True, help="Pushover Application token.", type=str)
    parser.add_argument('--config_file', default='src/config.yml', required=False)
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
    logger = configure_logger(l.loglevel.upper())
    
    logger.info("Initializing monitor")

    check_interval = l.check_interval
    white_pattern_list = get_list_from_params(l.whitelist)
    logger.debug("Whitelist: " + str(white_pattern_list))
    
    black_list = get_list_from_params(l.blacklist) 
    logger.debug("BlackList: " + str(black_list))
   
    msg_prefix =  sanitize_str_arg(l.msg_prefix)
        
    logger.info("Registering Apprise service")
    apobj = apprise.Apprise()
    config = apprise.AppriseConfig()
    if not config.add('/src/config.yml'):
         print("Warning: Please provide a valid apprise configuration.")   
    
    apobj.add(config)
    apobj.notify(body='Initializing monitoring',
                 title='SwarmAlert' ) 
    logger.info("Registering Docker Client")

    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    monitor_and_notify(docker_client, apobj)
   

