# Optional. Not LoT. Logs in as each demo user and asks: may I listen to this topic?
# Install once:  python3 -m pip install paho-mqtt
# Run from this template folder:
#   python3 scripts/probe_access.py --dashboard-pass demo --device-x-pass demo --engineer-pass demo

import argparse
import time

import paho.mqtt.client as mqtt

# who, topic, should the Rules allow it?
CHECKS = [
    ("dashboard", "factory/#", True),
    ("dashboard", "raw/factory/#", False),
    ("dashboard", "#", False),
    ("device_x", "raw/factory/line1/device-x/#", True),
    ("device_x", "raw/#", False),
    ("device_x", "#", False),
    ("engineer", "factory/#", True),
    ("engineer", "raw/factory/#", True),
    ("engineer", "#", False),
]


def can_listen(host, port, user, password, topic):
    answer = {"yes": None}

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            answer["yes"] = False
            client.disconnect()
            return
        client.subscribe(topic)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        code = reason_codes[0]
        answer["yes"] = not code.is_failure
        client.disconnect()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(user, password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.connect(host, port, keepalive=10)
    client.loop_start()
    until = time.time() + 4
    while answer["yes"] is None and time.time() < until:
        time.sleep(0.05)
    client.loop_stop()
    client.disconnect()
    return bool(answer["yes"])


def main():
    p = argparse.ArgumentParser(description="Check the three demo users against the Rules.")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=1883)
    p.add_argument("--dashboard-pass", required=True)
    p.add_argument("--device-x-pass", required=True)
    p.add_argument("--engineer-pass", required=True)
    args = p.parse_args()
    passwords = {
        "dashboard": args.dashboard_pass,
        "device_x": args.device_x_pass,
        "engineer": args.engineer_pass,
    }

    print("Listen checks. Confirm writes in Coreflux HUB Data Viewer.")
    failed = 0
    for user, topic, should_allow in CHECKS:
        got = can_listen(args.host, args.port, user, passwords[user], topic)
        ok = got == should_allow
        if not ok:
            failed += 1
        want = "yes" if should_allow else "no"
        said = "yes" if got else "no"
        print(f"{'OK' if ok else 'FAIL'}  {user} listen {topic}  (want {want}, broker {said})")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
