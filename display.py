import matplotlib.pyplot as plt
import numpy as np


def display_chunk_list(chunks):
    chunks = np.array(chunks)
    print(f'Displying {len(chunks)} chunks.')

    x0 = min(chunks[:, 0]) - 2
    z0 = min(chunks[:, 1]) - 2

    w = max(chunks[:, 0]) - x0 + 3
    h = max(chunks[:, 1]) - z0 + 3

    mask = np.zeros((h, w), dtype=int)
    mask[chunks[:, 1]-z0, chunks[:, 0]-x0] = 1

    plt.imshow(mask)
    plt.show()


def display_diamonds(diamonds, ranges, i1, i2):
    canvas = np.zeros((ranges[i1].stop-ranges[i1].start, ranges[i2].stop-ranges[i2].start))

    for p in diamonds:
        canvas[p[i1]-ranges[i1].start, p[i2]-ranges[i2].start] += 1

    import matplotlib.pyplot as plt
    plt.imshow(canvas)
    plt.show()
