import csv
import time
import speedtest
import schedule
import logging
import requests
from datetime import datetime
import socket

logging.basicConfig(filename='speedtest.log', level=logging.INFO, format='%(asctime)s %(message)s')


def ping_server(server: str, port: int, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except OSError:
        return False
    else:
        s.close()
        return True


def run_connectiontest():
    logging.info('Running connection test')
    connected = ping_server("www.google.com", 443)
    with open('connectiontest_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(['Datetime', 'Connected'])

        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M:%S')

        writer.writerow([date + " " + current_time, str(connected)])
        logging.info('Internet connection available: %s', connected)


def run_speedtest():
    logging.info('Running speedtest')
    s = speedtest.Speedtest(secure=True)
    with open('speedtest_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(['Datetime', 'Download Speed (Mbps)', 'Upload Speed (Mbps)'])

        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M:%S')

        download_speed = round(s.download() / 1e6)
        upload_speed = round(s.upload() / 1e6)

        writer.writerow([date + " " + current_time, download_speed, upload_speed])
        logging.info('Download Speed: %s Mbps, Upload Speed: %s Mbps', download_speed, upload_speed)


# run_speedtest()
# check_internet()

schedule.every(30).minutes.do(run_speedtest)
schedule.every(1).minutes.do(run_connectiontest)

while True:
    schedule.run_pending()
    time.sleep(1)
