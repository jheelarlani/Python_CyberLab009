import psutil
import time
import csv
import threading
from flask import Flask, render_template_string
import pandas as pd
import plotly
import plotly.express as px
import json
import nmap

# ------------------------------
# Traffic Monitoring
# ------------------------------
CSV_FILE = "traffic_data.csv"
ALERT_FILE = "alerts.csv"
INTERVAL = 5  # seconds

def monitor_traffic(interface="Wi-Fi"):
    stats = []
    while True:
        net_io = psutil.net_io_counters(pernic=True)[interface]
        timestamp = time.time()
        stats.append((timestamp, net_io.bytes_sent, net_io.bytes_recv))

        # Save CSV
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "sent", "recv"])
            writer.writerows(stats)

        # Check for anomalies
        alerts = []
        if len(stats) > 1:
            sent_rates = [s[1] for s in stats[1:]]
            if len(sent_rates) > 1:
                mean_sent = sum(sent_rates)/len(sent_rates)
                std_sent = pd.Series(sent_rates).std()
                for i, rate in enumerate(sent_rates):
                    if rate > mean_sent + 2*std_sent:
                        alerts.append(f"ALERT at {time.strftime('%H:%M:%S', time.localtime(stats[i+1][0]))}: Outbound spike {rate} bytes!")

        # Save alerts
        with open(ALERT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for alert in alerts:
                writer.writerow([alert])

        time.sleep(INTERVAL)

# ------------------------------
# Host Scanning
# ------------------------------
NETWORK_RANGE = "192.168.1.0/24"

def scan_hosts():
    nm = nmap.PortScanner()
    while True:
        live_hosts = []
        try:
            nm.scan(hosts=NETWORK_RANGE, arguments='-sn')  # ping scan
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    live_hosts.append(host)
        except Exception as e:
            print("Nmap scan error:", e)
        # Save live hosts to CSV for dashboard
        with open("hosts.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["host"])
            for h in live_hosts:
                writer.writerow([h])
        time.sleep(60)  # scan every 60 seconds

# ------------------------------
# Flask Dashboard
# ------------------------------
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Live Network Traffic Dashboard</h1>
    <div id="graph"></div>

    <h2>Live Hosts</h2>
    <ul>
    {% for host in hosts %}
        <li>{{ host }}</li>
    {% endfor %}
    </ul>

    <h2>Alerts</h2>
    <ul style="color:red;">
    {% for alert in alerts %}
        <li>{{ alert }}</li>
    {% endfor %}
    </ul>

    <script>
        var graphs = {{ graphJSON | safe }};
        Plotly.newPlot('graph', graphs.data, graphs.layout);
        setInterval(() => { location.reload(); }, 5000); // refresh every 5 sec
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Load traffic CSV
    try:
        df = pd.read_csv(CSV_FILE)
    except:
        df = pd.DataFrame(columns=['time', 'sent', 'recv'])
    
    fig = px.line(df, x="time", y=["sent", "recv"],
                  labels={"value":"Bytes", "time":"Time (s)", "variable":"Direction"},
                  title="Network Traffic Over Time")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Load live hosts
    try:
        hosts_df = pd.read_csv("hosts.csv")
        hosts = hosts_df['host'].tolist()
    except:
        hosts = []

    # Load alerts
    try:
        alerts_df = pd.read_csv(ALERT_FILE, header=None)
        alerts = alerts_df[0].tolist()
    except:
        alerts = []

    return render_template_string(HTML_TEMPLATE, graphJSON=graphJSON, hosts=hosts, alerts=alerts)

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    threading.Thread(target=monitor_traffic, args=("Wi-Fi",), daemon=True).start()
    threading.Thread(target=scan_hosts, daemon=True).start()
    app.run(debug=True)
