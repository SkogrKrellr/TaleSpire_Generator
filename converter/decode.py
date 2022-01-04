import base64
import gzip
from struct import unpack_from, unpack

LEL = 20  # list_entry_length
PEL = 8  # position_entry_length


def assemble_bytes(bytes):
    total = 0
    for byte in bytes:
        total = (total << 8) + byte
    return total


def decode_asset(asset_data):
    """
    Function to decode an asset header.

    Parameters:
        asset_data (str): containing asset header bytes

    Returns:
        dict: decoded asset header
    """

    dec_data = unpack_from('IHH8BI', asset_data)
    uuid = (
        dec_data[0],
        dec_data[1],
        dec_data[2],
        assemble_bytes(dec_data[3:5]),
        assemble_bytes(dec_data[5:11])
        )
    uuid_strings = (
        format(uuid[0], "08X"),
        format(uuid[1], "04X"),
        format(uuid[2], "04X"),
        format(uuid[3], "04X"),
        format(uuid[4], "012X")
        )
    instance_count = dec_data[11]
    uuid_string = '-'.join(x for x in uuid_strings)
    return {
        "uuid": uuid_string,
        "instance_count": instance_count,
        "instances": []
    }


def decode_asset_position(
    asset_position_data,
    assets,
    dec_asset_count
):
    """
    Function that decodes an asset position, returns a tuple of which asset
    this position belongs to (index from asset list) as well as the position

    Parameters:
        asset_position_data (str): containing asset header bytes
        assets (dict): dictionary of asset and its positions
        dec_asset_count (int): instance count

    Returns:
        dict: decoded asset header
    """
    # decode position from blob passed on
    # unpack as little endian. data is stored as
    # 2 bit pad,
    # 8 bit rot, 2 bit pad,
    # 16 bit y, 2 bit pad,
    # 16 bit z, 2 bit pad,
    # 16 bit x
    position_blob = unpack("<Q", asset_position_data)[0]
    # x, y and z are 16bit, rot is 8 bit.
    # All have 2 bit padding between each other.
    x = position_blob & 0xFFFF  # isolate lowest 16 bits (x position)
    y = (position_blob >> 36) & 0xFFFF  # shift the x and z coord 4 bit padding
    z = (position_blob >> 18) & 0xFFFF  # shift the x coord 2 bit padding
    rot = position_blob >> 54  # shift x, y and z coord 6 padding to get rot

    # figure out which asset this position actually belongs to and store it
    sub_total = 0
    for i, asset in enumerate(assets['asset_data']):
        sub_total += asset['instance_count']
        # check if the currently iterated through asset in the asset list
        # is the one we are currently decoding the pos of
        if (dec_asset_count < sub_total):
            return (i, {
                "x": x,
                "y": y,
                "z": z,
                "rot": rot*15
            })


def decode(data):
    """
    Function that decodes given TaleSpire string into dictionary

    Parameters:
        data (str): TaleSpire string

    Returns:
        json: decoded string
    """

    out_json = {
        "unique_asset_count": 0,
        "asset_data": []
    }

    # decode base64
    base64_bytes = data.encode('ascii')
    slab_compressed_data = base64.b64decode(base64_bytes)

    # decompress gzip
    slab_data = gzip.decompress(slab_compressed_data)

    header = slab_data[:10]
    out_json["unique_asset_count"] = unpack("I", header[6:])[0]
    unique_asset_length = out_json["unique_asset_count"] * LEL
    asset_list = slab_data[len(header):len(header) + unique_asset_length]
    asset_position_list = slab_data[len(header) + len(asset_list):]

    # decode asset list
    for i in range(out_json["unique_asset_count"]):
        asset_data = decode_asset(asset_list[i * LEL: (i+1) * LEL])
        out_json["asset_data"].append(asset_data)

    # decode asset positions
    asset_count = 0
    while(len(asset_position_list[asset_count*PEL:]) > PEL):
        position = decode_asset_position(
            asset_position_list[asset_count * PEL: (asset_count+1) * PEL],
            out_json,
            asset_count
            )
        out_json["asset_data"][position[0]]["instances"].append(position[1])
        asset_count += 1

    return out_json
