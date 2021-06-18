import os
import re
import zlib

import numpy as np
from tqdm import tqdm

import noxitu.minecraft.protocol.nbt as nbt
import noxitu.minecraft.protocol.packet
from noxitu.minecraft.map.global_palette import BLOCKS, GLOBAL_PALETTE

from display import display_diamonds


DIAMOND_ORE_MASK = np.array([name == 'minecraft:diamond_ore' for name in GLOBAL_PALETTE], dtype=bool)


def compute_range(chunks):
    chunks = np.array(chunks)

    x0 = min(chunks[:, 0])
    z0 = min(chunks[:, 1])

    x1 = max(chunks[:, 0]) + 1
    z1 = max(chunks[:, 1]) + 1

    return slice(0, 256), slice(16*z0, 16*z1), slice(16*x0, 16*x1)


def unpack_long(value, bits):
    if value < 0:
        value += 2 ** 64

    mask = 2**bits - 1
    for i in range(0, 64-bits+1, bits):
        yield (value >> i) & mask


def unpack_section(section_data, palette):
    bits_per_block = 4

    while 2 ** bits_per_block < len(palette):
        bits_per_block += 1

    result = [val for packed in section_data for val in unpack_long(packed, bits_per_block)]
    result = result[:16*16*16]
    result = palette[result]
    result = np.array(result).reshape(16, 16, 16).astype(int)
    return result


def extract_diamonds(path, seed=0):
    loaded_chunks = []
    all_diamonds = []

    for chunk_file in tqdm(os.listdir(path)):
        try:
            match = re.match(R'^r\.(-?[0-9]+)\.(-?[0-9]+)\.mca$', chunk_file)
            global_x, global_z = [int(match.group(i)) for i in (1, 2)]
        except:
            tqdm.write(f'\033[31mFailed for {chunk_file}\033[m (wrong filename)')
            raise

        with open(f'{path}/{chunk_file}', 'rb') as fd:
            data = fd.read()

        if len(data) == 0:
            continue

        try:
            chunks = {(i%32, i//32): (4096 * (65536*data[4*i] + 256*data[4*i+1] + data[4*i+2]), 4096*data[4*i+3]) for i in range(1024)}
            chunks = {(x, z): (offset, size) for (x, z), (offset, size) in chunks.items() if size > 0}
        except Exception as ex:
            tqdm.write(f'\033[31mFailed for {chunk_file}\033[m ({ex})')
            tqdm.write(f'len(data) = {len(data)}')
            continue
        
        for (local_x, local_z) in tqdm([(local_x, local_z) for local_x in range(32) for local_z in range(32)], leave=False):
            try:                
                offset, size = chunks[(local_x, local_z)]
            except KeyError:
                continue

            x = 32*global_x + local_x
            z = 32*global_z + local_z

            chunk_data = noxitu.minecraft.protocol.packet.Packet(data[offset:offset+5])
            size = chunk_data.int()
            encryption = chunk_data.ubyte()
            assert encryption == 2

            chunk_data = zlib.decompress(data[offset+5:offset+4+size])
            chunk_data, _ = nbt.parse(chunk_data)

            assert chunk_data[b''][b'Level'][b'xPos'] == x
            assert chunk_data[b''][b'Level'][b'zPos'] == z

            chunk = np.zeros((16, 16, 16, 16), dtype=np.uint16)

            for section in chunk_data[b''][b'Level'][b'Sections']:
                y = section[b'Y']

                if b'BlockStates' in section:
                    palette = []

                    for entry in section[b'Palette']:
                        block = BLOCKS[entry[b'Name'].decode()]
                        if b'Properties' in entry:
                            properties = {key.decode(): value.decode() for key, value in entry[b'Properties'].items()}
                            n = 0
                            for state in block['states']:
                                if all(properties.get(key) == value for key, value in state['properties'].items()):
                                    palette.append(state['id'])
                                    n += 1

                            if n != 1:
                                raise Exception()
                        else:
                            n = 0
                            for state in block['states']:
                                if state['default']:
                                    palette.append(state['id'])
                                    n += 1

                            if n != 1:
                                raise Exception()

                    palette = np.array(palette)
                    chunk[y] = unpack_section(section[b'BlockStates'], palette)

            loaded_chunks.append([x, z])

            diamond_mask = DIAMOND_ORE_MASK[chunk.reshape(256, 16, 16)]
            diamond_list = np.argwhere(diamond_mask) + [0, 16*z, 16*x]

            all_diamonds.extend(diamond_list)

    diamonds = np.array(all_diamonds)
    print(f'Found {len(diamonds)} diamond ores:')

    _, zs, xs = compute_range(loaded_chunks)

    os.makedirs('diamonds', exist_ok=True)
    np.savez(f'diamonds/{seed}.npz',
        diamonds=diamonds,
        xs=xs,
        zs=zs
    )


if __name__ == '__main__':
    extract_diamonds('world_gen/world/region')
