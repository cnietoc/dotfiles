#!/usr/bin/env python3

import argparse
import os
import sys
from datetime import datetime

from scapy.all import UDP, Raw, sniff


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor Wake-on-LAN magic packets")
    parser.add_argument("--iface", default="en0", help="Network interface (default: en0)")
    parser.add_argument("--mac", default=None, help="Filter by target MAC address")
    return parser.parse_args()


def format_mac(raw: bytes) -> str:
    return ":".join(f"{b:02x}" for b in raw)


def make_callback(mac_filter: str | None):
    def on_packet(pkt):
        if not pkt.haslayer(UDP) or not pkt.haslayer(Raw):
            return

        payload = bytes(pkt[Raw].load)
        if len(payload) < 102 or payload[:6] != b"\xff" * 6:
            return

        target_mac = format_mac(payload[6:12])

        if mac_filter and target_mac.lower() != mac_filter.lower():
            return

        src_ip = pkt[0].src if hasattr(pkt[0], "src") else "unknown"
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] WOL → {target_mac}  from {src_ip}")

    return on_packet


def main():
    if os.geteuid() != 0:
        print("error: packet capture requires root — run with sudo", file=sys.stderr)
        sys.exit(1)

    args = parse_args()

    mac_label = f"  filter: {args.mac}" if args.mac else ""
    print(f"Listening for WOL packets on {args.iface}{mac_label}  (Ctrl+C to stop)\n")

    try:
        sniff(
            iface=args.iface,
            filter="udp and (port 9 or port 7)",
            prn=make_callback(args.mac),
            store=False,
        )
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
