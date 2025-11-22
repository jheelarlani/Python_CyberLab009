import subprocess
import sys
import platform

def ping_host(host, count=4):

    param = "-n" if platform.system().lower() == "windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", param, str(count), host],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Count replies
            reply_count = result.stdout.lower().count("reply from")
            print(f"[+] Host {host} is reachable. Replies: {reply_count}/{count}")
            return True
        else:
            print(f"[-] Host {host} is unreachable.")
            return False

    except subprocess.TimeoutExpired:
        print("[!] Ping timed out.")
        return False

    except FileNotFoundError:
        print("[!] Ping tool not found on your system.")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    ping_host(host)
