import base64
import gzip
from utils import *
from struct import *

asset_list_entry_length = 20
asset_position_entry_length = 8

#replace with .from_bytes?
def assemble_bytes(bytes):
    total = 0
    for byte in bytes:
        total = (total << 8) + byte
    return total

def decode_asset(asset_data):
    dec_data = unpack('IHH8BI', asset_data)
    uuid = (dec_data[0], dec_data[1], dec_data[2], assemble_bytes(dec_data[3:5]), assemble_bytes(dec_data[5:11]))
    uuid_strings = (format(uuid[0], "08X"), format(uuid[1], "04X"), format(uuid[2], "04X"), format(uuid[3], "04X"), format(uuid[4], "012X"))
    instance_count = dec_data[11]
    uuid_string = '-'.join(x for x in uuid_strings)
    return {
        "uuid": uuid_string,
        "instance_count": instance_count,
        "instances": [] 
    }


def decode_asset_position(asset_position_data, assets, dec_asset_count):
    position_blob = unpack("<Q", asset_position_data)[0] 
    x = position_blob & 0xFFFF 
    y = (position_blob >> 36) & 0xFFFF 
    z = (position_blob >> 18) & 0xFFFF 
    rot = position_blob >> 54
    sub_total = 0
    for i, asset in enumerate(assets['asset_data'].items()):
        sub_total += asset[1]['instance_count']
        if (dec_asset_count < sub_total):
                return (asset[0], {
                "x": x,
                "y": y,
                "z": z,
                "rot": rot*15
            })


def decode(data):
    out_json = {
        "unique_asset_count": 0,
        "asset_data": {}
    }

    base64_bytes = data.encode('ascii')
    slab_compressed_data = base64.b64decode(base64_bytes)
    slab_data = gzip.decompress(slab_compressed_data)

    header = slab_data[:10]
    out_json["unique_asset_count"] = unpack("I", header[6:])[0]
    asset_list = slab_data[len(header):len(header) + out_json["unique_asset_count"] * asset_list_entry_length]
    asset_position_list = slab_data[len(header) + len(asset_list):]

    for i in range(out_json["unique_asset_count"]):
        asset_data = decode_asset(asset_list[i * asset_list_entry_length : (i+1) * asset_list_entry_length])
        out_json["asset_data"][asset_data["uuid"]] = asset_data

    dec_asset_count = 0
    while(len(asset_position_list[dec_asset_count*asset_position_entry_length:]) > asset_position_entry_length):
        position = decode_asset_position(asset_position_list[dec_asset_count * asset_position_entry_length:(dec_asset_count+1) * asset_position_entry_length], out_json, dec_asset_count)
        a = position[1]
        out_json["asset_data"][position[0]]["instances"].append(a)
        dec_asset_count += 1

    return out_json