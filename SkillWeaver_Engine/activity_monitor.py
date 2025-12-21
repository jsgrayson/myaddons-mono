import hid
import time

print("Opening all accessible devices... press your '2' key.")
all_devs = []
for info in hid.enumerate():
    try:
        d = hid.device()
        d.open_path(info['path'])
        d.set_nonblocking(True)
        all_devs.append((d, info['product_string'], info['path']))
        # Optional: Print what we opened successfully
        # print(f"Opened: {info['product_string']}") 
    except:
        pass

print(f"Monitoring {len(all_devs)} devices.")

try:
    while True:
        for d, name, path in all_devs:
            try:
                report = d.read(64)
                if report:
                    print(f"Data from [{name}] at {path}: {list(report)}")
            except:
                pass
        time.sleep(0.01)
except KeyboardInterrupt:
    for d, n, p in all_devs: 
        try: d.close()
        except: pass
