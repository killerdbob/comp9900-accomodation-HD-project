import os
import math
import shutil



# class : Searcher house
# writer : huang, wei
# zid : 5119435

class house:
    word2index = dict()
    index2house = dict()

    def __init__(self):
        super(house, self).__init__()
        self._instance = None

    def __call__(self, *args, **kwargs):
        if (self._instance is None):
            self._instance = super(house, self).__call__(*args, **kwargs)
        return self._instance

    # class : readhouse
    # writer : huang, wei
    # zid : 5119435
    def readhouse(house_id):
        house = dict()
        flag = True
        with open('data/house/' + str(house_id) + '/data.txt', encoding='UTF-8') as f:
            key = ''
            value = ''
            for line in f:
                if (not line.strip()):
                    try:
                        house[key]
                    except:
                        house[key] = value
                    flag = True
                    continue
                if (flag):
                    key, value = line.split(':')
                    key = key.strip()
                    value = value.strip()
                    if (key == 'configuration'):
                        value = value.split(',')
                    elif (key in ['Amenities', 'Policies']):
                        if (value):
                            value = [value]
                        else:
                            value = []
                    elif (key == 'price'):
                        value = int(value[1:])
                    flag = False
                else:
                    if (key in ['Amenities', 'Policies']):
                        value.append(line.strip())
                    else:
                        value += line.strip()
            try:
                house[key]
            except:
                house[key] = value
        try:
            with open('data/house/' + str(house_id) + '/content.txt', encoding='UTF-8') as f:
                value = ''
                for line in f:
                    value += line.strip()
                house['content'] = value
        except:
            house['content'] = ''
        house['image'] = []
        for item in os.listdir('data/house/' + str(house_id)):
            if (item == 'head.jpg'):
                continue
            if (item.endswith('.jpg') or item.endswith('.webp')):
                house['image'].append(item)
        house['house_id']=house_id
        return house

    def read_deleted_house(house_id):
        house = dict()
        flag = True
        with open('data/house_del/' + str(house_id) + '/data.txt', encoding='UTF-8') as f:
            key = ''
            value = ''
            for line in f:
                if (not line.strip()):
                    try:
                        house[key]
                    except:
                        house[key] = value
                    flag = True
                    continue
                if (flag):
                    key, value = line.split(':')
                    key = key.strip()
                    value = value.strip()
                    if (key == 'configuration'):
                        value = value.split(',')
                    elif (key in ['Amenities', 'Policies']):
                        if (value):
                            value = [value]
                        else:
                            value = []
                    elif (key == 'price'):
                        value = int(value[1:])
                    flag = False
                else:
                    if (key in ['Amenities', 'Policies']):
                        value.append(line.strip())
                    else:
                        value += line.strip()
            try:
                house[key]
            except:
                house[key] = value
        try:
            with open('data/house_del/' + str(house_id) + '/content.txt', encoding='UTF-8') as f:
                value = ''
                for line in f:
                    value += line.strip()
                house['content'] = value
        except:
            house['content'] = ''
        house['image'] = []
        for item in os.listdir('data/house_del/' + str(house_id)):
            if (item == 'head.jpg'):
                continue
            if (item.endswith('.jpg') or item.endswith('.webp')):
                house['image'].append(item)
        house['house_id']=house_id
        return house

    # class : savehouse
    # writer : huang, wei
    # zid : 5119435
    def savehouse(house, belongto):
        try:
            number = max([int(i) for i in os.listdir('data/house/')]) + 1
            directory = 'data/house/' + str(number)
            os.mkdir(directory)
            with open(directory + '/data.txt', 'w', encoding='UTF-8') as f:
                for key in house.keys():
                    if (key in ['content', 'image']):
                        continue
                    if (key in ['Amenities', 'Policies', 'configuration']):
                        print(key, end=':', file=f)
                        print('\n'.join(house[key]), file=f)
                        print(file=f)
                    else:
                        print(key, end=':', file=f)
                        print(house[key], file=f)
                        print(file=f)
                print('belonging:', end='', file=f)
                print(belongto, file=f)
                print(file=f)
            with open(directory + '/content.txt', 'w', encoding='UTF-8') as f:
                print(house['Content'], file=f)
            #########
            # 存入 经纬
            ##########
            return True
        except:
            os.rmdir(directory)
            return False

    # class : remove_house
    # writer : huang, wei
    # zid : 5119435
    def remove_house(house_id):
        try:
            shutil.move('data/house/' + str(house_id), 'data/house_del/' + str(house_id))
            return True
        except:
            return False

    # class : recover_house
    # writer : huang, wei
    # zid : 5119435
    def recover_house(house_id):
        try:
            shutil.move('data/house_del/' + str(house_id), 'data/house/' + str(house_id))
            return True
        except:
            return False

    # class : get_index
    # writer : huang, wei
    # zid : 5119435
    def get_index(place):
        index = dict()
        result=[]
        del_index = set(os.listdir('data/house_del'))
        # del_index=set([ os.path.split(i)[-1] for i in pathDir])
        for i in place:
            print(i)
            tmp_set=[]
            with open('data/index/' + i) as f:
                for line in f:
                    tmp_set=line.split(',')
            for j in tmp_set:
                try:
                    index[j]+=1
                except:
                    index[j]=1
        average=sum([i for i in index.values()])/len(index.keys())
        for i in index.keys():
            if(index[i]>=average-1):
                result.append(i)
        result=list(set(result).difference(del_index))
        return result
        # place = place.lower()
        # ind = -1
        # pla = ''
        # with open('data/index/' + place + '.txt') as f:
        #     for line in f:
        #         if (not line.strip()):
        #             continue
        #         if (line.startswith('\t')):
        #             lng, lat = line.strip().split(',')
        #             lng = float(lng)
        #             lat = float(lat)
        #             index[ind].append([lng, lat])
        #         elif (line.strip()):
        #             ind, pla = line.strip().split('\t')
        #             index[ind] = [pla.lower()]


    # class : get_content
    # writer : huang, wei
    # zid : 5119435
    def get_content(search_list,page=1):  # 输入房子id数组 页数从1开始
        result = []
        total_page=math.ceil(len(search_list)/12.0)
        if(page>=total_page):
            search_list=search_list[(page-1)*12:]
        else:
            search_list=search_list[(page-1)*12:page*12]
        for i in search_list:
            result.append(house.readhouse(i))
        return result

    # class : get_content
    # writer : Jingjie Jin
    # zid : 5085901
    def eachFile(filepath):  # scan all txt file
        pathDir = os.listdir(filepath)
        result=[]
        for s in pathDir:
            newDir = os.path.join(filepath, s)
            if os.path.isfile(newDir):
                if (os.path.split(newDir)[1] == 'data.txt'):
                    result.append(newDir)
                    pass
            else:
                house.eachFile(newDir)
        return result

    # class : keyword_index
    # writer : Jingjie Jin
    # zid : 5085901
    def keyword_index(word):
        h = house.eachFile('data/house')  # 选择数据在的主目录
        number = []
        for i in h:
            with open(i) as f1:
                txt = f1.read().lower()
                if (word.lower() in txt):
                   number.append(int(os.path.split(os.path.split(i)[0])[1]))
        number.sort()
        with open('data/index/' + word, 'w+') as f2:
            f2.write(','.join(number))