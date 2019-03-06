import argparse
import re
import time

import docker
from pushover import init, Client

def service_list_to_str(services_list):
    msg = ""
    for service in services_list:
        msg = f"{service.name}\n{msg}"
    return msg

def monitor_swarm_pushover(docker_client, white_pattern_list):
    services = [docker_client.inspect_service(service=service_name) for service_name in white_pattern_list]
    not_running_services = [service for service in services if len(services.tasks(desired_state='Running')) == 0]
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
                        help="Skip checking certain containers. A list of regexp separated by comma.", type=str)
    parser.add_argument('--check_interval', default='300', required=False, help="Periodical check. By seconds.",
                        type=int)
    parser.add_argument('--msg_prefix', default='', required=False, help="Pushover message prefix.", type=str)
    l = parser.parse_args()
    check_interval = l.check_interval
    white_pattern_list = l.whitelist.split(',')

    if white_pattern_list == ['']:
        white_pattern_list = []

    pushover_token = l.token
    pushover_key = l.app_key
    msg_prefix = l.msg_prefix

    if pushover_token == '':
        print("Warning: Please provide a valid pushover token.")
    if pushover_key == '':
        print("Warning: Please provide a valid pushover application key.")

    pushover_client = Client(pushover_key, api_token="pushover_token")
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    has_send_error_alert = False
    while True:
        (status, err_msg) = monitor_swarm_pushover(docker_client, white_pattern_list)
        if msg_prefix != "":
            err_msg = "%s\n%s" % (msg_prefix, err_msg)
        print("%s: %s" % (status, err_msg))
        if status == "OK":
            if has_send_error_alert is True:
                pushover_client.send_message(err_msg, title="SwarmAlert")
                has_send_error_alert = False
        else:
            if has_send_error_alert is False:
                pushover_client.send_message(err_msg, title="SwarmAlert")
           
                # avoid send alerts over and over again
                has_send_error_alert = True
        time.sleep(check_interval)
# File : monitor-docker-slack.py ends

