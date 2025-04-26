import time
from scapy.all import sr1, ICMP, IP
import matplotlib.pyplot as plt

class NetworkLatencyTool:
    def __init__(self, targets, count=10, interval=1):
        self.targets = targets
        self.count = count
        self.interval = interval
        self.results = {target: [] for target in targets}

    def ping(self, target):
        pkt = IP(dst=target)/ICMP()
        start_time = time.time()
        reply = sr1(pkt, timeout=1, verbose=0)
        end_time = time.time()
        if reply:
            rtt = (end_time - start_time) * 1000  # Convert to ms
            return rtt
        else:
            return None

    def run(self):
        for _ in range(self.count):
            for target in self.targets:
                rtt = self.ping(target)
                if rtt:
                    self.results[target].append(rtt)
                time.sleep(self.interval)
        self.display_results()

    def display_results(self):
        for target, rtts in self.results.items():
            if rtts:
                print(f"Results for {target}: Min: {min(rtts):.2f} ms, Max: {max(rtts):.2f} ms, Avg: {sum(rtts)/len(rtts):.2f} ms")
                jitter = self.calculate_jitter(rtts)
                print(f"Jitter: {jitter:.2f} ms")
                loss = self.calculate_packet_loss(self.count, len(rtts))
                print(f"Packet Loss: {loss:.2f}%")
                self.plot_rtt(target, rtts)
            else:
                print(f"No responses from {target}")

    def calculate_jitter(self, rtts):
        jitter = sum(abs(rtts[i] - rtts[i-1]) for i in range(1, len(rtts)))
        return jitter / (len(rtts) - 1) if len(rtts) > 1 else 0

    def calculate_packet_loss(self, sent, received):
        return ((sent - received) / sent) * 100

    def plot_rtt(self, target, rtts):
        plt.plot(rtts, marker='o')
        plt.title(f"RTT Over Time for {target}")
        plt.xlabel("Ping #")
        plt.ylabel("RTT (ms)")
        plt.grid(True)
        plt.show()

if __name__ == "__main__": 
    targets=[input("Enter 1st IP address: "),input("Enter 2nd IP address: ")]
    # targets = ["208.67.222.222", "9.9.9.9"]  # Example targets (Google DNS, Cloudflare DNS)
    tool = NetworkLatencyTool(targets=targets, count=10, interval=1)
    tool.run()
