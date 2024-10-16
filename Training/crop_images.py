import argparse
import multiprocessing as mp
import os
import os.path as osp
import cv2
import pandas as pd
from   Training.dataset.annotate import crop_board


def crop(img_path, write_path, bbox, size=800, overwrite=False):
    if osp.exists(write_path) and not overwrite:
        print(write_path, 'already exists')
        return
    
    os.makedirs(osp.join(osp.dirname(write_path)), exist_ok=True)

    crop, _ = crop_board(img_path, bbox)
    if size != 'full':
        crop = cv2.resize(crop, (size, size))
    cv2.imwrite(write_path, crop)
    print('Wrote', write_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-lp', '--labels-path', default='dataset/annotations/bw_dataset_2.pkl')
    parser.add_argument('-ip', '--image-path', default='dataset/images/')
    parser.add_argument('-s', '--size', nargs='+', default=['800'])
    args = parser.parse_args()

    for size in args.size:
        if size != 'full':
            size = int(size)

        data = pd.read_pickle(args.labels_path)

        read_prefix = args.image_path
        write_prefix = osp.join(*args.image_path.split('/')[:-1], 'cropped_images', str(size))

        print('Read path:', read_prefix)
        print('Write path:', write_prefix)

        img_paths = [osp.join(read_prefix, folder, name) for (folder, name) in zip(data.img_folder, data.img_name)]
        write_paths = [osp.join(write_prefix, folder, name) for (folder, name) in zip(data.img_folder, data.img_name)]
        bboxes = data.bbox.values
        sizes = [size for _ in range(len(bboxes))]

        p = mp.Pool(mp.cpu_count())
        p.starmap(crop, list(zip(img_paths, write_paths, bboxes, sizes)))












