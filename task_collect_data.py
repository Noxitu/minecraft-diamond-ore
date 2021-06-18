import os
import task_extract
import task_generate


def main():
    for seed in range(1, 12+1):
        if os.path.exists(f'diamonds/{seed}.npz'):
            continue

        print(f'Generating seed={seed}')
        task_generate.generate_world(seed=seed)
        task_extract.extract_diamonds('world_gen/world/region', seed=seed)


if __name__ == '__main__':
    main()
