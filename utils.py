# coding=utf8

with open('inception/imagenet_synset_to_human_label_map.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\t', ' ')
        l = line.split('\n')
        l.pop()
        ll = l[0].split(' ')
        number = ll.pop(0)
        label = ' '.join(ll)
        label_list = label.split(',')
        print(label_list)
        # print(l)