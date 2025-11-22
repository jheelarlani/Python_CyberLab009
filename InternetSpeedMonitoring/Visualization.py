import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Load the CSV
df = pd.read_csv('speed_log.csv')

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# ----- Plot 1: Download Speed Over Time -----
plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['Download (Mbps)'], marker='o', linestyle='-', color='blue')
plt.title('Download Speed Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Download Speed (Mbps)')
plt.xticks(rotation=45)
plt.grid(True)

# Optional: format x-axis for better readability
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

plt.tight_layout()
plt.savefig('download_speed_over_time.png')  # Saves the graph as PNG
plt.show()

# ----- Plot 2: Ping Trends Over Time -----
plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['Ping (ms)'], marker='x', linestyle='-', color='green')
plt.title('Ping Trends Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Ping (ms)')
plt.xticks(rotation=45)
plt.grid(True)
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

plt.tight_layout()
plt.savefig('ping_trends_over_time.png')
plt.show()
