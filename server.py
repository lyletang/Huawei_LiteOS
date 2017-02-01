# -*- coding:utf-8 -*-
import tensorflow as tf
import numpy as np
import os
import inception
import socket


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
    while True:
        filename = 'received/' + str(num).zfill(2) + '.jpg'
        f = open(filename, 'wb')
        print('listening')
        s.listen(5)
        c, addr = s.accept()
        print('Got connection from ', addr)
        print('Receiving...')
        l = c.recv(1024)
        while l:
            f.write(l)
            l = c.recv(1024)
        f.close()
        print('Done Receiving')

        data = run_inference(model, filename)
        print(data)
        # s.send(data.encode('utf-8'), addr[0])
        num += 1
    model.close()