import base64
import gzip
import json
from utils import *

HEADER = b'\xCE\xFA\xCE\xD1\x02\x00'
PADDING = b'\x00\x00'

def create_header(unique_asset_count):
    return HEADER + unique_asset_count.to_bytes(4, byteorder='little')

def encode(data):
    slab_data = b'' 
    slab_json = json.loads(data)
    slab_json['unique_asset_count'] = len(slab_json['asset_data']) 
    
    for asset in slab_json['asset_data'].items():
        asset[1]['instance_count'] = len(asset[1]['instances'])
        
    slab_data += create_header(len(slab_json['asset_data']))
    asset_data = create_assets_data(slab_json['asset_data'], )
    slab_data += asset_data[0] + asset_data[1] + PADDING

    slab_compressed_data = gzip.compress(slab_data, compresslevel=9, mtime=0)

    if (len(slab_compressed_data) > 30720):
        print(f"[WARNING] Slab exceeds TaleSpire size limit of 30kB (30720 bytes) binary data! Aborting. ({len(slab_compressed_data)} bytes)")
        return b'``````'

    base64_bytes = base64.b64encode(slab_compressed_data)

    return b'```' + base64_bytes + b'```'

def encode_asset(asset_json):
    uuid_parts = asset_json['uuid'].split("-")

    uuid_bytes = b''
    uuid_bytes += int(uuid_parts[0], 16).to_bytes(4, byteorder='little')
    uuid_bytes += int(uuid_parts[1], 16).to_bytes(2, byteorder='little')
    uuid_bytes += int(uuid_parts[2], 16).to_bytes(2, byteorder='little')
    uuid_bytes += int(uuid_parts[3], 16).to_bytes(2, byteorder='big')
    uuid_bytes += int(uuid_parts[4], 16).to_bytes(6, byteorder='big')
    
    return uuid_bytes + asset_json['instance_count'].to_bytes(4, byteorder='little')

def encode_asset_position(instance_json):
    position = 0
    position |= int(instance_json['x'])
    position |= (int(instance_json['y']) << 36)
    position |= (int(instance_json['z']) << 18)
    position |= (int(instance_json['rot']/15) << 54)

    return position.to_bytes(8, byteorder='little')

def create_assets_data(assets_json):
    asset_list = b''
    position_list = b''

    for asset in assets_json.items(): 
        asset_list += encode_asset(asset[1])
        for instance in asset[1]['instances']:
            position_list += encode_asset_position(instance)

    return ( asset_list, position_list )