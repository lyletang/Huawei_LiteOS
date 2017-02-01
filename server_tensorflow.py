# -*- coding:utf-8 -*-
import tensorflow as tf
import numpy as np
import os
import inception
import socket
import subprocess

MAX_ACCEPTED_PHOTOS = 10
bundler_command_line = 'C:/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/python.exe F:/osm-bundler-pmvs2-cmvs-full-32-64/osm-bundler/osm-bundlerWin64/RunBundler.py --photos="E:/code/python/Huawei_LiteOS/received"'
pmvs_command_line = 'C:/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/python.exe F:/osm-bundler-pmvs2-cmvs-full-32-64/osm-bundler/osm-bundlerWin64/RunPMVS.py --bundlerOutputPath="F:/workspace/osm-bundler"'


# def reconstruction():
#     print('Start')
#     bundler_return_code = subprocess.call(bundler_command_line)
#     pmvs_return_code = subprocess.call(pmvs_command_line)
#     print('Finish')


def run_inference(model, image_path):
    # Use the Inception model to classify the image.
    pred = model.classify(image_path=image_path)

    # Print the scores and names for the top-1 predictions.
    model.print_scores(pred=pred, k=10, only_first_name=True)
    return model.get_topmost(pred)

if __name__ == '__main__':
    model = inception.Inception()
    # run_inference(model, "images/parrot.jpg")
    s = socket.socket()
    port = 12344
    s.bind(('', port))
    num = 1
    # 硬编码拍摄10张照片
    while num <= MAX_ACCEPTED_PHOTOS:
        filename = 'received/' + str(num).zfill(2) + '.jpg'
        f = open(filename, 'wb')
        print('listening')
        s.listen(11)
        c, addr = s.accept()
        print('Got connection from ', addr)
        print('Receiving...')
        l = c.recv(1024)
        while l:
            f.write(l)
            l = c.recv(1024)
        f.close()
        print('Done Receiving')
        num += 1

    # reconstruction()

    inference_needed = 'received/' + str(5).zfill(2) + '.jpg'
    data = run_inference(model, inference_needed)
    print(data)
    model.close()