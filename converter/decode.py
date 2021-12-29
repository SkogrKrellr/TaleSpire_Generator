import base64
import gzip
from struct import unpack_from, unpack 

asset_list_entry_length = 20
asset_position_entry_length = 8

def assemble_bytes(bytes):
    total = 0
    for byte in bytes:
        total = (total << 8) + byte #take old total, shift it to the left by 8 (make space for another byte), add next byte in list
    return total

def decode_asset(asset_data):
    dec_data = unpack_from('IHH8BI', asset_data)
    uuid = (dec_data[0], dec_data[1], dec_data[2], assemble_bytes(dec_data[3:5]), assemble_bytes(dec_data[5:11]))
    uuid_strings = (format(uuid[0], "08X"), format(uuid[1], "04X"), format(uuid[2], "04X"), format(uuid[3], "04X"), format(uuid[4], "012X"))
    instance_count = dec_data[11]
    uuid_string = '-'.join(x for x in uuid_strings)
    return {
        "uuid": uuid_string,
        "instance_count": instance_count,
        "instances": [] #rename to instance_position? or just positions?
    }


#decodes an asset position, returns a tuple of which asset this position belongs to (index from asset list) as well as the position
def decode_asset_position(asset_position_data, assets, dec_asset_count):
    #decode position from blob passed on
    position_blob = unpack("<Q", asset_position_data)[0]  #unpack as little endian. data is stored as 2 bit pad, 8 bit rot, 2 bit pad, 16 bit y, 2 bit pad, 16 bit z, 2 bit pad, 16 bit x
    #x, y and z are 16bit, rot is 8 bit. all have 2 bit padding between each other.
    x = position_blob & 0xFFFF # isolate lowest 16 bits (x position)
    y = (position_blob >> 36) & 0xFFFF # shift away the x and z coord + 2*2 bit padding
    z = (position_blob >> 18) & 0xFFFF # shift away the x coord + 2 bit padding
    rot = position_blob >> 54 #shift away x, y and z coord + 3*2 padding (54 places) to get rotation to LSB

    #figure out which asset this position actually belongs to and store it
    #print_info("info_quiet", "      Keep track of which asset position is being read. Done by iterating through asset list and summing up instance counts until the current number of parsed asset positions is lower or equal to the number of asset instances from the list. This is the asset this position belongs to.", verbose, quiet)
    sub_total = 0
    for i, asset in enumerate(assets['asset_data']):
        sub_total += asset['instance_count']
        if (dec_asset_count < sub_total): #check if the currently iterated through asset in the asset list is the one we are currently decoding the pos of
            return (i, {
                "x": x,
                "y": y,
                "z": z,
                "rot": rot*15
            })

def decode(data):
    out_json = {
        "unique_asset_count": 0,
        "asset_data": []
    }


    #decode base64
    base64_bytes = data.encode('ascii')
    slab_compressed_data = base64.b64decode(base64_bytes)

    #decompress gzip
    slab_data = gzip.decompress(slab_compressed_data)

    header = slab_data[:10]
    out_json["unique_asset_count"] = unpack("I", header[6:])[0]
    asset_list = slab_data[len(header):len(header) + out_json["unique_asset_count"] * asset_list_entry_length]
    asset_position_list = slab_data[len(header) + len(asset_list):]

    #decode asset list
    for i in range(out_json["unique_asset_count"]):
        asset_data = decode_asset(asset_list[i * asset_list_entry_length : (i+1) * asset_list_entry_length])
        out_json["asset_data"].append(asset_data)

    #decode asset positions
    dec_asset_count = 0
    while(len(asset_position_list[dec_asset_count*asset_position_entry_length:]) > asset_position_entry_length):
        position = decode_asset_position(asset_position_list[dec_asset_count * asset_position_entry_length:(dec_asset_count+1) * asset_position_entry_length], out_json, dec_asset_count)
        out_json["asset_data"][position[0]]["instances"].append(position[1])
        dec_asset_count += 1

    return out_json