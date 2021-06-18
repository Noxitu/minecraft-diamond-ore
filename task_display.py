import os

import matplotlib.pyplot as plt
import numpy as np


DIRECTORY = 'diamonds'
VERSION = '1.17'

def main():
    H = 20
    ys = np.zeros((H,), dtype=int)

    for filename in os.listdir(DIRECTORY):
        if filename == '0.npz':
            continue
        diamonds = np.load(f'{DIRECTORY}/{filename}')['diamonds']
        np.add.at(ys, diamonds[:, 0], 1)

    print(ys)
    ax = plt.subplot()
    ax.barh(np.arange(H), ys)
    ax.set_yticks(np.arange(H))
    ax.set_yticklabels(np.arange(H))

    ax.set_title(f'Diamond Ore Distribution - Minecraft {VERSION}')
    ax.set_xlabel('Number of Ores')
    ax.set_ylabel('Y level')
    
    # plt.hist([str(y) for y in np.arange(H)], bins=H, weights=ys, orientation="horizontal")
    plt.show()


if __name__ == '__main__':
    main()
