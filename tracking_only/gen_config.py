import os
import json
import numpy as np
import cv2
from glob import glob

def gen_config(args):

    if args.seq != '':
        # generate config from a sequence name

        '''
        注意：
        1.一个路径由三个参数构成：seq_home + seq_name + 'left'
        2.这里只支持图片，并且需要正确的后缀，*.png
        '''

        seq_home = '../data'
        result_home = 'results'

        seq_name = args.seq
        img_dir = os.path.join(seq_home, seq_name, 'left')

        img_list = glob(os.path.join(img_dir, '*.png'))
        img_list = sorted(img_list, key=lambda x: int(x.split('/')[-1].split('.')[0]))

        gt = None
        '''
        Select ROI
        参考：http://www.1zlab.com/wiki/python-opencv-tutorial/opencv-image-cut-select-roi/
        '''
        # 设定文件路径
        img_path = img_list[0]
        print(img_path)
        # Read image
        img = cv2.imread(img_path)
        # 创建一个窗口
        cv2.namedWindow("image")
        cv2.imshow("image", img)
        # 是否显示网格
        showCrosshair = True
        # 如果为Ture的话 , 则鼠标的其实位置就作为了roi的中心
        # False: 从左上角到右下角选中区域
        fromCenter = False
        # Select ROI
        rect = cv2.selectROI("image", img, showCrosshair, fromCenter)
        print("已选中矩形区域")
        # 销毁所有窗口
        cv2.destroyAllWindows()
        ###################
        init_bbox = rect

        result_dir = os.path.join(result_home, seq_name)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        savefig_dir = os.path.join(result_dir, 'figs')
        result_path = os.path.join(result_dir, 'result.json')

    elif args.json != '':
        # load config from a json file

        param = json.load(open(args.json, 'r'))
        seq_name = param['seq_name']
        img_list = param['img_list']
        init_bbox = param['init_bbox']
        savefig_dir = param['savefig_dir']
        result_path = param['result_path']
        gt = None

    if args.savefig:
        if not os.path.exists(savefig_dir):
            os.makedirs(savefig_dir)
    else:
        savefig_dir = ''

    return img_list, init_bbox, gt, savefig_dir, args.display, result_path
