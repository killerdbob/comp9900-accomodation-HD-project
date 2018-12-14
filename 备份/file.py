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
        try:
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
        with open('data/user/' + email + '.txt') as f:
            for line in f:
                key, value = line.split(':')
                if (key in {'property','deleted_post'} ):
                    if(value.strip()):
                        user[key.strip()] = value.strip().split(',')
                    else:
                        user[key.strip()] = []
                else:
                    user[key.strip()] = value.strip()
        return user

    def remove_user(email):
        try:
            shutil.move('data/user/' + str(email)+'.txt', 'data/user_del/' + str(email)+'.txt')
            return True
        except:
            return False
    def putuser(email,username,birthday,password,phone_number,address,property=None,deleted_post=None):
        user_txt = 'data/user/' + email + '.txt'
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
                        +'deleted_post:'+','.join(deleted_post))

        else:
            return False

    # function : result_list_content
    # writer : fan xiaoyu, huangwei
    # 获取当前已经存到第几个房源了
    def puthouse(email,password ,picname=None, title=None,
                guest=None, bedroom=None, bed=None, bath=None,
                price=None, options1=None, options2=None, policy=None,content=None):
        user=dict()
        if(control.verify(email,password)):
            user=control.getuser(email)
        else:
            print('invalid user')
            return
        max_index = (max([int(i) for i in os.listdir(r'data/house/')]))
        path = "data/house/" + str(max_index + 1)
        os.mkdir(path)
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
                f.write(', ' + bedroom + ' bedrooms')
            except:
                pass
            try:
                f.write(', ' + bed + ' beds')
            except:
                pass
            try:
                f.write(', ' + bath + ' baths')
            except:
                pass
            f.write('\n\nbelonging:' + email)
            f.write('\nHost:' + user['user_name'] +'\n')
            f.write('\nprice: $' + price + '\n')
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
            f.write('\nPolicies:' + '\n' + policy + '\n')
        with open(path + '/content.txt', 'a') as f:
            try:
                f.write(content + '\n')
            except:
                pass

    # class : print_user
    # writer : huang, wei
    # zid : 5119435
    def print_user(user):
        for u in user:
            print(u, end=' : ')
            print(user[u])
