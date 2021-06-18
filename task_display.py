import os

import matplotlib.pyplot as plt
import numpy as np


DIRECTORY = 'diamonds'
VERSION = '1.17'

def main():
    H = 20
    ys = np.zeros((H,), dtype=int)
    ys2 = np.zeros((H,), dtype=int)

    for filename in os.listdir(DIRECTORY):
        if filename == '0.npz':
            continue
        data = np.load(f'{DIRECTORY}/{filename}', allow_pickle=True)
        diamonds = data['diamonds']
        np.add.at(ys, diamonds[:, 0], 1)

        if 'diamonds2' in data:
            diamonds2 = data['diamonds2']
            np.add.at(ys2, diamonds2[:, 0], 1)

    print(ys+ys2)
    print(sum(ys+ys2))

    ax = plt.subplot()

    ax.barh(np.arange(H), ys, color='#888a85', label='Stone')

    if sum(ys2) > 0:
        ax.barh(np.arange(H), ys2, left=ys, color='#2e3436', label='Deepslate')

    ax.set_yticks(np.arange(H))
    ax.set_yticklabels(np.arange(H))

    ax.set_title(f'Diamond Ore Distribution - Minecraft {VERSION}')
    ax.set_xlabel('Number of Ores')
    ax.set_ylabel('Y level')

    # ax.grid(True)
    ax.legend()
    
    # plt.hist([str(y) for y in np.arange(H)], bins=H, weights=ys, orientation="horizontal")
    plt.show()


if __name__ == '__main__':
    main()
