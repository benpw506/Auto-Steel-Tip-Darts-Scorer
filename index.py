import argparse
from yacs.config import CfgNode as CN
import os.path as osp
import cv2
from Training.dataset.annotate import get_bounding_box
from Application.src.darts import Dart_Manager
from Application.src.board import DartBoard
from Application.src.player import PlayerManager
from Application.src.GUI import App


def predict_test(yolo, cfg) :

    cap = cv2.VideoCapture(0) 
    temp = 'Application/temp.jpg'
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    ret, frame = cap.read()
    print("Waiting...")
    print("Done...")
    cv2.imwrite(temp, frame)
    
    bbox = get_bounding_box(temp)

    pm = PlayerManager()
    board = DartBoard(None)
    dm = Dart_Manager()

    app = App(board, pm, dm, cap, bbox, yolo, cfg)
    app.mainloop()
    cap.release()
    cv2.destroyAllWindows()
        



if __name__ == '__main__' :
    from Training.train import build_model
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cfg', default='bw_darts')
    args = parser.parse_args()

    cfg = CN(new_allowed=True)
    cfg.merge_from_file(osp.join('Training/configs', args.cfg + '.yaml'))
    cfg.model.name = args.cfg

    yolo = build_model(cfg)
    yolo.load_weights(osp.join('Training','models', args.cfg, 'weights'), cfg.model.weights_type)

    predict_test(yolo, cfg)