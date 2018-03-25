

import cv2
import xml.etree.ElementTree as ET
import os
import re


class Space:
    def __init__(self):
        self.id = 0
        self.occupied = 0
        self.rotatedRect = self.rotatedRect()
        self.contour = self.contour()

    def __repr__(self):
        return repr(vars(self))

    class rotatedRect:
        def __init__(self):
            self.center = self.center()
            self.size = self.size()
            self.angle = self.angle()

        def __repr__(self):
            return repr(vars(self))

        class center:
            def __init__(self):
                self.x = 0
                self.y = 0

            def __repr__(self):
                return repr(vars(self))

        class size:
            def __init__(self):
                self.w = 0
                self.h = 0

            def __repr__(self):
                return repr(vars(self))

        class angle:
            def __init__(self):
                self.d = 0

            def __repr__(self):
                return repr(vars(self))

    class contour:
        def __init__(self):
            self.pointArr = []
            self.point = self.point()

        def __repr__(self):
            return repr(vars(self))

        class point:
            def __init__(self):
                self.x = 0
                self.y = 0

            def __repr__(self):
                return repr(vars(self))


class FileInfo:
    #  put the same file together, and sequentially.
    def __init__(self):
        self.name = ""
        self.image_path = ""
        self.xml_path = ""

    def __repr__(self):
        return repr(vars(self))


def create_data_set(image_path, xml_path, file_name, destination_dir_path):
    space_arr = []
    tree = ET.ElementTree(file=xml_path)

    for elem_space in tree.iter(tag='space'):
        new_space = Space()
        new_space.id = int(elem_space.attrib['id'])


        #  because some occupied didn't have the value, so we don't know if there is a car or not, so we crop the image
        #  base on the image has occupied value.
        try:
            new_space.occupied = int(elem_space.attrib['occupied'])
        except:
            print("[Exception] There is no field 'occupied' in xml where space_id = {0} path = {1}".format(new_space.id, xml_path))

        # get each element from xml file
        for elem_rotatedRect in elem_space.iter(tag='rotatedRect'):
            for elem_center in elem_rotatedRect.iter(tag='center'):
                new_space.rotatedRect.center.x = int(elem_center.attrib['x'])
                new_space.rotatedRect.center.y = int(elem_center.attrib['y'])
            for elem_size in elem_rotatedRect.iter(tag='size'):
                new_space.rotatedRect.size.w = int(elem_size.attrib['w'])
                new_space.rotatedRect.size.h = int(elem_size.attrib['h'])
            for elem_angle in elem_rotatedRect.iter(tag='angle'):
                new_space.rotatedRect.angle.d = int(elem_angle.attrib['d'])

        for elem_contour in elem_space.iter(tag='contour'):
            for elem_point in elem_contour.iter(tag='point'):
                new_point = Space.contour.point()
                new_point.x = int(elem_point.attrib['x'])
                new_point.y = int(elem_point.attrib['y'])
                new_space.contour.pointArr.append(new_point)

        space_arr.append(new_space)

    # because we have four x and value, and we want to get them.
    for index, space in enumerate(space_arr):
        min_x = 999999  # set min_x very large to let any point.x smaller than min_x
        max_x = 0  # set max_x equal 0 to let any point.x bigger than max_x
        min_y = 999999
        max_y = 0

        for point in space.contour.pointArr:
            # we want to find the minimum x, y and maximum x, y
            # if point.x smaller than min_x, we replace the min_x
            # For example, in id=4, 1.x="453" y="369" 2.x="543" y="386" 3.x="573" y="334" 4.x="446" y="304"
            if point.x < min_x:
                min_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y

        img = cv2.imread(image_path)
        crop_img = img[min_y:max_y, min_x: max_x]

        if space.occupied == 1:
            new_file_name = destination_dir_path + "positive/{0}_{1}.jpg".format(file_name, str(space.id))
            cv2.imwrite(new_file_name, crop_img)
        elif space.occupied == 0:
            new_file_name = destination_dir_path + "negative/{0}_{1}.jpg".format(file_name, str(space.id))
            cv2.imwrite(new_file_name, crop_img)


def isFileInfoExisted(file_info_arr, new_file_name):
    for file_info in file_info_arr:
        if file_info.name == new_file_name:
            return file_info
    return False

def get_all_file(destination_dir_path, source_dir_path):

    file_info_arr = []

    print("Start traversing file path.")

    print(source_dir_path)

    for file in os.listdir(source_dir_path):
        if file.endswith(".jpg"):
            file_info = isFileInfoExisted(file_info_arr, file.replace(".jpg", ""))
            if file_info:
                file_info.image_path = os.path.join(source_dir_path, file)
            else:
                file_info = FileInfo()
                file_info.name = file.replace(".jpg", "")
                file_info.image_path = os.path.join(source_dir_path, file)
                file_info_arr.append(file_info)
        elif file.endswith(".xml"):
            file_info = isFileInfoExisted(file_info_arr, file.replace(".xml", ""))
            if file_info:
                file_info.xml_path = os.path.join(source_dir_path, file)
            else:
                file_info = FileInfo()
                file_info.name = file.replace(".xml", "")
                file_info.xml_path = os.path.join(source_dir_path, file)
                file_info_arr.append(file_info)

    print("Traversing complete.")

    print("Start creating data set.")

    for file_info in file_info_arr:
        create_data_set(file_info.image_path, file_info.xml_path, file_info.name, destination_dir_path)
        # print(file_info.image_path, file_info.xml_path, file_info.name, destination_dir_path)

    print("Creating complete.")




if __name__ == '__main__':
    destination_dir_path = "/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/"

    #  create output file
    os.makedirs(destination_dir_path + "parking2_positive")
    os.makedirs(destination_dir_path + "parking2_negative")

    source_dir_path = "/Users/laichian/Desktop/Computer_Vision/homework-3-MattLai-master/PKLot/parking2/sunny/"
    dirs = os.listdir(source_dir_path)


    for file in os.listdir(source_dir_path):

        #  use regular expression to prevent some file which we don't want.
        pattern = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        match = pattern.match(file)
        print(match)
        if match:
            get_all_file(destination_dir_path, source_dir_path+file+"/")

