import os
import shutil

# class : control
# writer : huang, wei
# zid : 5119435
class control:
    number = 0
    online_user = dict()

    def __init__(cls):
        super(control, cls).__init__()
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(control, cls).__call__(*args, **kw)

        return cls._instance

    # class : verify
    # writer : huang, wei
    # zid : 5119435
    def verify(email, password):
        u = control.getuser(email)
        # print(u)
        try:
            print(email,password)
            if (password == u['password']):
                control.online(email, password)
                return True
        except:
            return False

    # class : is_online
    # writer : huang, wei
    # zid : 5119435
    def is_online(email):
        try:
            control.online_user[email]
            return True
        except:
            return False

    # class : online
    # writer : huang, wei
    # zid : 5119435
    def online(email, password):
        control.number += 1
        control.online_user[email] = password
        return True

    # class : offline
    # writer : huang, wei
    # zid : 5119435
    def offline(email, password):
        if (control.verify(email, password)):
            control.number -= 1
            control.online_user.pop(email)
            return True
        else:
            return False

    # class : getuser
    # writer : huang, wei
    # zid : 5119435
    def getuser(email):
        user = dict()
        with open('./data/user/' + email + '.txt') as f:
            for line in f:
                key, value = line.split(':')
                if (key in {'property','deleted_post','collect'} ):
                    if(value.strip()):
                        user[key.strip()] = value.strip().split(',')
                    else:
                        user[key.strip()] = []
                else:
                    user[key.strip()] = value.strip()
        if('property' not in user.keys()):
            user['property']=[]
        if ('deleted_post' not in user.keys()):
            user['deleted_post'] = []
        if ('collect' not in user.keys()):
            user['collect'] = []
        return user

    # class : remove_user
    # writer : huang, wei
    # zid : 5119435
    def remove_user(email):
        try:
            shutil.move('data/user/' + str(email)+'.txt', 'data/user_del/' + str(email)+'.txt')
            return True
        except:
            return False

    # class : remove_house_permanent
    # writer : huang, wei
    # zid : 5119435
    def remove_house_permanent(houseid):
        try:
            os.rmdir('data/house_del/'+houseid)
            return True
        except:
            return False

    def putuser(email,username,birthday,password,phone_number,address,property=None,deleted_post=None,collect=None):
        user_txt = 'data/user/' + email + '.txt'
        user=dict()
        try:
            user=control.getuser(email)
        except:
            pass
        if(property == None):
            try:
                property = user['property']
            except:
                property = []
        if (deleted_post == None):
            try:
                deleted_post = user['deleted_post']
            except:
                pass
        if (collect == None):
            try:
                collect = user['collect']
            except:
                pass

        try:
            control.remove_user(email)
        except:
            pass
        if os.path.exists(user_txt) == False:  # 没有就创建
            with open(user_txt, 'w') as f:
                f.write('user_name:' + username + '\n'
                        + 'birthday:' + birthday + '\n'
                        + 'password:' + password + '\n'
                        + 'email:' + email + '\n'
                        + 'phone number:' + phone_number + '\n'
                        + 'address:' + str(address) + '\n'
                        +'property:'+','.join(property) + '\n'
                        +'deleted_post:'+','.join(deleted_post)+'\n'
                        +'collect:'+','.join(collect))

        else:
            return False

    # function : result_list_content
    # writer : fan xiaoyu, huangwei,peng cheng wen
    # 获取当前已经存到第几个房源了
    def puthouse(email,password ,picname=None, title=None,
                guest=None, bedroom=None, bed=None, bath=None,
                price=None, options1=None, options2=None, policy=None,
                 content=None,address=None,latitude=None,longitude=None):
        user=dict()
        if(control.verify(email,password)):
            user=control.getuser(email)
        else:
            print('invalid user')
            return
        max_index = (max([int(i) for i in os.listdir(r'data/house/')])) + 1
        path = "data/house/" + str(max_index)
        os.mkdir(path)
        try:
            # 将文件保存在目录下
            # print('picname=',picname)
            for i in picname:
                # print('i=',i)
                for m in i:
                    # print('m=',m)
                    file_path = path + '/' + m.filename
                    if m:
                        m.save(file_path)
        except:
            pass
        data_txt = path + '/' + 'data' + '.txt'
        with open(data_txt, 'a') as f:
            f.write('title:' + title + '\n')
            f.write('\nconfiguration: ')
            try:
                f.write(guest + ' guests')
            except:
                pass
            try:
                f.write(',' + bedroom + ' bedrooms')
            except:
                pass
            try:
                f.write(',' + bed + ' beds')
            except:
                pass
            try:
                f.write(',' + bath + ' baths')
            except:
                pass
            f.write('\n\nbelonging:' + email+'\n')

            f.write('\nHost:' + user['user_name'] +'\n')
            f.write('\nprice: $' + price + '\n')
            f.write('\n\naddress:'+address+'\n')
            f.write('\n\nlatitude:'+str(latitude)+'\n')
            f.write('\n\nlongitude:'+str(longitude)+'\n')
            try:
                f.write('\nAmenities: ' + '\n')
                for i in options1:
                    f.write(i)
                    f.write('\n')
                for i in options2:
                    f.write(i)
                    f.write('\n')
            except:
                pass
            f.write('\nPolicies: ' + '\n' + policy + '\n')
        with open(path + '/content.txt', 'a') as f:
            try:
                f.write(content + '\n')
            except:
                pass
        return max_index

    # class : print_user
    # writer : huang, wei
    # zid : 5119435
    def print_user(user):
        for u in user:
            print(u, end=' : ')
            print(user[u])


    #class feedback_write_file:
    #pengchengwen
    def feedback_write_file(email,title,nowtime,content):
        user_txt = 'data/feedback/' + email + '.txt'
        if os.path.exists(user_txt) == False:  # 没有就创建
            with open(user_txt, 'w') as f:
                f.write('title:' + title + '\n')
                f.write('time:' + nowtime + '\n')
                f.write('content:' + content)

        else:
            f = open(user_txt, 'a')
            f.write('\n'+'\n')
            f.write('title:' + title + '\n')
            f.write('time:'+ nowtime + '\n')
            f.write('content:' + content)
            f.close()
    #remove folder and create empty folder with same name
    #pengchengwen
    def empty_folder(houseid):
        path = 'data/house/'+houseid
        shutil.rmtree(path)
        os.mkdir(path)

    def edit_house_info(email, password,houseid, picname=None, title=None,
                     guest=None, bedroom=None, bed=None, bath=None,
                     price=None, options1=None, options2=None, policy=None, content=None, address=None,latitude=None,longitude=None):

        user = dict()
        if (control.verify(email, password)):
            user = control.getuser(email)
        else:
            print('invalid user')
            return

        path = "data/house/" + str(houseid)
        #os.mkdir(path)
        try:
            # 将文件保存在目录下
            for i in picname:
                for m in i:
                    file_path = path + '/' + m.filename
                    if m:
                        m.save(file_path)
        except:
            pass
        data_txt = path + '/' + 'data' + '.txt'
        with open(data_txt, 'a') as f:
            f.write('title:' + title + '\n')
            f.write('\nconfiguration: ')
            try:
                f.write(guest + ' guests')
            except:
                pass
            try:
                f.write(',' + bedroom + ' bedrooms')
            except:
                pass
            try:
                f.write(',' + bed + ' beds')
            except:
                pass
            try:
                f.write(',' + bath + ' baths')
            except:
                pass
            f.write('\n\nbelonging:' + email+'\n')
            f.write('\nHost:' + user['user_name'] + '\n')
            f.write('\nprice: $' + price + '\n')
            f.write('\naddress: '+address+'\n')
            f.write('\nlatitude: ' + str(latitude) + '\n')
            f.write('\nlongitude: ' + str(longitude) + '\n')
            try:
                f.write('\nAmenities: ' + '\n')
                for i in options1:
                    f.write(i)
                    f.write('\n')
                for i in options2:
                    f.write(i)
                    f.write('\n')
            except:
                pass
            # print(policy)
            f.write('\nPolicies: ' + '\n' )
            f.write(policy)
            f.write('\n')
        with open(path + '/content.txt', 'a') as f:
            try:
                f.write(content + '\n')
            except:
                pass