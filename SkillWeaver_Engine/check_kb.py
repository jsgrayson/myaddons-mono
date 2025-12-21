import hid
for d in hid.enumerate():
    if d['vendor_id'] == 0x05ac:
        print(f"Device: {d['product_string']} | ID: {hex(d['vendor_id'])}:{hex(d['product_id'])} | Path: {d['path']}")
