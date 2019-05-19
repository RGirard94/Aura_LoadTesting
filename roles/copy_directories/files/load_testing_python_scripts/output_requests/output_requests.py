#!/usr/bin/python

import datetime
from influxdb import InfluxDBClient
import configparser
import logging
import time


def change_timestamp(unused_1, unused_2):
    '''unused_1 and what is unused_2.'''
    change_timestamp_time = datetime.datetime.now()
    return change_timestamp_time.timetuple()


logging.Formatter.converter = change_timestamp
logging.basicConfig(
    filename='/home/ansible/personal_logs/influxdb_manual_logs_output-json.log',
    filemode='a',
    format='%(asctime)s.%(msecs)03d : %(message)s',
    level=logging.INFO,
    datefmt="%B %d %Y, %H:%M:%S",
)

DATA_COUNTER_LIST = []


def get_number_output_rrinterval(client):
    r = client.query('select count(*) from RrInterval')
    return list(r.get_points(measurement='RrInterval'))[0]


def get_number_output_motionaccelerometer(client):
    r = client.query('select count(*) from MotionAccelerometer')
    return list(r.get_points(measurement='MotionAccelerometer'))[0]


def get_number_output_motiongyroscope(client):
    r = client.query('select count(*) from MotionGyroscope')
    return list(r.get_points(measurement='MotionGyroscope'))[0]


def check_database_status(client):
    dbs = client.get_list_database()
    return dbs


def check_measurement_status(client):
    mst = client.get_list_measurements()
    return mst


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('/home/ansible/load_testing_python_scripts/output_requests/config.conf')

    influxdb_client_constants = config["Influxdb Client"]

    DB_NAME = influxdb_client_constants["database_name"]
    HOST = influxdb_client_constants["host"]
    PORT = int(influxdb_client_constants["port"])
    USER = influxdb_client_constants["user"]
    PASSWORD = influxdb_client_constants["password"]

    CLIENT = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASSWORD,
                            database=DB_NAME)

    check_physio_signals_exists = False

    while check_physio_signals_exists == False:
        if {'name': 'physio_signals'} in check_database_status(CLIENT):
            check_physio_signals_exists = True

    while check_physio_signals_exists == True:

        if {'name': 'RrInterval'} in check_measurement_status(CLIENT) and 'count_RrInterval' in get_number_output_rrinterval(CLIENT):
            logging.info('monitoring-RrInterval-output : {}'.format(get_number_output_rrinterval(CLIENT)['count_RrInterval']))
        else:
            logging.info('monitoring-RrInterval-output : 0')

        if {'name': 'MotionAccelerometer'} in check_measurement_status(CLIENT) and 'count_x_acm' in get_number_output_motionaccelerometer(CLIENT):
            logging.info('monitoring-MotionAccelerometer-output : {}'.format(get_number_output_motionaccelerometer(CLIENT)['count_x_acm']))
        else:
            logging.info('monitoring-MotionAccelerometer-output : 0')

        if {'name': 'MotionGyroscope'} in check_measurement_status(CLIENT) and 'count_x_gyro' in get_number_output_motiongyroscope(CLIENT):
            logging.info('monitoring-MotionGyroscope-output : {}'.format(get_number_output_motiongyroscope(CLIENT)['count_x_gyro']))
        else:
            logging.info('monitoring-MotionGyroscope-output : 0')

        if {'name': 'physio_signals'} not in check_database_status(CLIENT):
            check_physio_signals_exists = False

        time.sleep(1)
