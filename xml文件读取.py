import os
import xml.etree.ElementTree as ET

dirpath = 'C:\\Users\\GW\\Desktop'  # 原来存放xml文件的目录
newdir = 'C:\\Users\\GW\\Desktop'  # 修改label后形成的txt目录

if not os.path.exists(newdir):
    os.makedirs(newdir)

dict_info = {'people': 0, 'bag': 1}  # 有几个 属性 填写几个label names

for fp in os.listdir(dirpath):
    if fp.endswith('.xml'):
        root = ET.parse(os.path.join(dirpath, fp)).getroot()


        sz = root.find('size')
        width = float(sz[0].text)
        height = float(sz[1].text)
        filename = root.find('filename').text
        for child in root.findall('object'):  # 找到图片中的所有框

            sub = child.find('bndbox')  # 找到框的标注值并进行读取
            label = child.find('name').text
            label_ = dict_info.get(label)

            xmin = float(sub[0].text)
            ymin = float(sub[1].text)
            xmax = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
                x_center = (xmin + xmax) / (2 * width)
                x_center = '%.6f' % x_center
                y_center = (ymin + ymax) / (2 * height)
                y_center = '%.6f' % y_center
                w = (xmax - xmin) / width
                w = '%.6f' % w
                h = (ymax - ymin) / height
                h = '%.6f' % h
            except ZeroDivisionError:
                print(filename, '的 width有问题')
            with open(os.path.join(newdir, fp.split('.xml')[0] + '.txt'), 'a+') as f:
                f.write(' '.join([str(label_), str(xmin), str(ymax), str(xmax), str(ymax) + '\n']))
print('ok')

# import xml.etree.ElementTree as ET
# classes = ["people","bag"]
# in_file = open('C:\\Users\\GW\\Desktop\\23.xml',encoding='utf-8')
# out_file = open('C:\\Users\\GW\\Desktop\\23.txt', 'w')
# tree = ET.parse(in_file)
# root = tree.getroot()
# for obj in root.iter('object'):
#     cls = obj.find('name').text
#     if cls not in classes:
#         continue
#     cls_id = classes.index(cls)
#     xmlbox = obj.find('bndbox')
#     xmin=float(xmlbox.find('xmin').text)
#     xmax=float(xmlbox.find('xmax').text)
#     ymin=float(xmlbox.find('ymin').text)
#     ymax=float(xmlbox.find('ymax').text)
#
#     out_file.write(str(cls_id) + " " + str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
