import speedtest
import datetime
import csv
import time
import schedule

def run_speed_test(log_file='speed_log.csv'):
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    server = st.results.server['name']
    jitter = getattr(st.results, 'jitter', 'N/A')
    packet_loss = getattr(st.results, 'packet_loss', 'N/A')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, download, upload, ping, jitter, packet_loss, server])

schedule.every(1).hours.do(run_speed_test)

try:
    with open('speed_log.csv', 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Download (Mbps)', 'Upload (Mbps)',
                         'Ping (ms)', 'Jitter (ms)', 'Packet Loss (%)', 'Server'])
except FileExistsError:
    pass

while True:
    schedule.run_pending()
    time.sleep(1)
