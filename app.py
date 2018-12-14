import datetime
import math
import os
import re
import shutil

from flask import Flask, render_template, request

from comment import comment
from file import control
from searcher import house

app = Flask(__name__, static_folder='', static_url_path='')
app.secret_key = '6666666'


# email = 'z5119435@student.unsw.edu.au'

# function : search
# writer : huang, wei
# zid : 5119435
@app.route('/', methods=['GET'])
def search():
    return render_template('search0.html')


# function : search
# writer : huang, wei
# zid : 5119435
@app.route('/404_not_found', methods=['GET'])
def not_found():
    return render_template('404_not_found.html')


# function : search_login
# writer : huang, wei
# zid : 5119435
# search0-->search1
@app.route('/search_login', methods=['GET'])
def search_login():
    if (request.method == 'GET'):
        email = request.args.get('login_email')
        password = request.args.get('login_password')
        print('email=', email)
        print('password=', password)
        if (control.verify(email, password)):
            return render_template('search1.html', email=email, password=password)
        else:
            return render_template('search0.html')
        # print(username+" "+password)


# function : search0
# writer : huang, wei
# zid : 5119435
# search0-->result_list0
@app.route('/search0', methods=['GET'])
def search0():
    if (request.method == 'GET'):
        try:
            search = request.args.get('search')
            return render_template('result_list0.html', search_phrase=search)
        except:
            return render_template('search0.html')


# function : search1
# writer : huang, wei
# zid : 5119435
# search1-->result_list1
@app.route('/search1', methods=['GET'])
def search1():
    if (request.method == 'GET'):
        try:
            search = request.args.get('search')
            email = request.args.get('email')
            password = request.args.get('password')
            collect=[]
            if(control.verify(email,password)):
                try:
                    collect=control.getuser(email)['collect']
                except:
                    pass
            return render_template('result_list1.html',
                                   search_phrase=search, email=email,
                                   password=password, Collect=collect)
        except:
            return render_template('search1.html')


# function : change_person_info
# writer : huang, wei pengchengwen
# zid : 5119435
@app.route('/change_person_info', methods=['GET'])
def change_person_info():
    if (request.method == 'GET'):
        email = request.values.get('email')
        password = request.values.get('password')
        user = control.getuser(email)

        if (control.verify(email, password)):
            try:

                new_password = request.values.get('new_password')
                address = request.values.get('address')
                phone_number = request.values.get('phone_number')
                user_name = request.values.get('user_name')
                birthday = request.values.get('birthday')
                comfirm_password = request.values.get('comfirm_password')
                try:
                    Post_id = user['property']
                except:
                    Post_id = []
                try:
                    deleted_id = user['deleted_post']
                except:
                    deleted_id = []

                try:
                    collect=[]
                    visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
                    for i in visible_collect:
                        collect.append(house.readhouse(i))
                except:
                    collect = []
                control.putuser(email, user_name, birthday, new_password, phone_number, address, Post_id, deleted_id, collect)
                return render_template('person_information_page.html',
                                       email=email, password=new_password,
                                       user_name=user_name, birthday=birthday,
                                       address=address, phone_number=phone_number)
            except:
                return render_template('search1.html', email=email, password=password)


# function : search0
# writer : huang, wei
# zid : 5119435
# result_list0-->result_list1
# @app.route('/result_list_login', methods=['GET'])
# def result_list_login():
#     if (request.method == 'GET'):
#         print('huangwei')
#         search = request.args.get('search')
#         email = request.args.get('login_email')
#         password = request.args.get('login_password')
#         print(email, password, search)
#         if (control.verify(email, password)):
#             return render_template('result_list1.html', search_phrase=search, email=email, password=password)
#         else:
#             return render_template('result_list0.html')


# function : result_list_content
# writer : huang, wei
# zid : 5119435
@app.route('/result_list_content', methods=['GET'])
def result_list_content():
    search_list = []
    collect = []
    email = ''
    password = ''
    cur_page = 1
    total_page = 1
    if (request.method == 'GET'):
        try:
            email = request.args.get('email')
            password = request.args.get('password')
            search = request.args.get('search')
            cur_page = int(request.args.get('cur_page'))
            search = re.split('[^a-z0-9]*', search.lower())
            search_list = house.get_index(search)
            user=control.getuser(email)
            if('collect' in user.keys()):
                collect = user['collect']
            total_page = math.ceil(len(search_list) / 12.0)
        except:
            cur_page = 1
            total_page = 1
        finally:
            if (1 < cur_page):
                pre_page = cur_page - 1
            else:
                pre_page = 1
            if (cur_page < total_page):
                next_page = cur_page + 1
            else:
                next_page = total_page
            # print(house.get_content(search_list))

            return render_template('result_list_content.html',
                                   contents=house.get_content(search_list, cur_page),
                                   current_page=cur_page,
                                   total_page=total_page,
                                   pre_page=pre_page,
                                   next_page=next_page,
                                   email=email,
                                   password=password,
                                   Collect=collect)


# z5119435
# Huang wei
# the post function:
@app.route('/personal_info')
def personal_info():
    email = request.args.get('email')
    password = request.args.get('password')
    # print(email, password)
    user = dict()
    Post = []
    Deleted = []
    Collect = []
    if (control.verify(email, password)):
        user = control.getuser(email)
        try:
            for i in user['property']:
                Post.append(house.readhouse(i))
        except:
            pass
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
        except:
            pass
        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass
    else:
        return
    birthday = '-'.join(user['birthday'].split('/')[::-1])
    return render_template('person_information_page.html',
                           email=email, password=password,
                           user_name=user['user_name'], birthday=birthday,
                           address=user['address'], phone_number=user['phone number'],
                           Post=Post, Deleted=Deleted, Collect=Collect)


# z5119435
# Huang wei
# the get_comment function:
@app.route('/get_comment')
def get_comment():
    email = request.args.get('email')
    password = request.args.get('password')
    comment_id = request.args.get('comment_id')
    house_id = request.args.get('house_id')
    # print('house_id', house_id, comment_id)
    # print('comment_id:', comment.get_comment(house_id, comment_id))
    cur_page = -1
    try:
        cur_page = int(request.args.get('cur_page'))
    except:
        pass
    if (comment_id == '-1'):
        comment_content = comment.get_comment(house_id)
    else:
        comment_content = comment.get_comment(house_id, comment_id)
    total_page = math.ceil(len(comment_content) / 5)
    if (cur_page != -1):
        if (cur_page <= total_page):
            comment_content = comment_content[(cur_page - 1) * 5:cur_page * 5]
        else:
            comment_content = comment_content[(total_page - 1) * 5:total_page * 5]
    next_page = (cur_page + 1) if cur_page < total_page else total_page
    h1 = house.readhouse(house_id)
    previous_page = (cur_page - 1) if cur_page > 2 else 1
    return render_template('comment.html',
                           comment_content=comment_content,
                           previous_page=previous_page, next_page=next_page,
                           total_page=total_page, cur_page=cur_page,
                           belonging=h1['belonging'], email=email,
                           password=password)


# z5119435
# Huang wei
# the del_comment function:
@app.route('/del_comment')
def del_comment():
    email = request.args.get('email')
    password = request.args.get('password')
    house_id = int(request.args.get('house_id'))
    comment_id = request.args.get('comment_id')
    if (control.verify(email, password)):
        comment.del_comment(house_id, comment_id)
    return ''


# z5119435
# Huang wei
# the reply_comment function:
@app.route('/reply_comment')
def reply_comment():
    email = request.args.get('email')
    password = request.args.get('password')
    house_id = request.args.get('house_id')
    comment_id = request.args.get('comment_id')
    comment_content = request.args.get('comment_content')
    # print(email, password, house_id, comment_id, comment_content)
    if (control.verify(email, password)):
        comment.add_comment(email, house_id, comment_id, comment_content)
    return ''


# z5119435
# Huang wei
# the recover_house function:
@app.route('/recover_house')
def recover_house():
    email = request.args.get('email')
    password = request.args.get('password')
    house_id = int(request.args.get('house_id'))
    Post = []
    Deleted = []
    Collect = []
    if (control.verify(email, password)):
        user = control.getuser(email)
        user['deleted_post'].remove(str(house_id))
        try:
            user['property'].append(str(house_id))
        except:
            user['property'] = str(house_id)
        house.recover_house(house_id)
        try:
            for i in user['property']:
                Post.append(house.readhouse(i))
        except:
            pass
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
        except:
            pass

        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass

        control.putuser(email, user['user_name'], user['birthday'],
                        password, user['phone number'], user['address'],
                        user['property'], user['deleted_post'])
    else:
        return
    birthday = '-'.join(user['birthday'].split('/')[::-1])
    return render_template('person_information_page.html',
                           email=email, password=password,
                           user_name=user['user_name'], birthday=birthday,
                           address=user['address'], phone_number=user['phone number'],
                           Post=Post, Deleted=Deleted, Collect=Collect)


# z5119435
# Huang wei
# the remove_house function:
@app.route('/remove_house')
def remove_house():
    email = request.args.get('email')
    password = request.args.get('password')
    house_id = int(request.args.get('house_id'))
    Post = []
    Deleted = []
    Collect = []
    if (control.verify(email, password)):
        user = control.getuser(email)
        user['property'].remove(str(house_id))
        post = user['property']
        # print(post)
        house.remove_house(house_id)
        try:
            for i in post:
                Post.append(house.readhouse(i))
        except:
            pass

        try:
            user['deleted_post'].append(str(house_id))
        except:
            user['deleted_post'] = [str(house_id)]
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
        except:
            pass

        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass
        control.putuser(email, user['user_name'], user['birthday'],
                        password, user['phone number'], user['address'],
                        user['property'], user['deleted_post'])
    else:
        return
    birthday = '-'.join(user['birthday'].split('/')[::-1])
    return render_template('person_information_page.html',
                           email=email, password=password,
                           user_name=user['user_name'], birthday=birthday,
                           address=user['address'], phone_number=user['phone number'],
                           Post=Post, Deleted=Deleted, Collect=Collect)


# the logout function:
@app.route('/log_out')
def log_out():
    email = request.args.get('email')

    password = request.args.get('password')
    if (control.verify(email, password)):
        control.offline(email, password)
    return render_template('search0.html')


# z5103407
# pengchengwen
# go to post house
@app.route('/to_post_house', methods=['GET'])
def to_post_house():
    email = request.args.get('email')
    password = request.args.get('password')
    # print('post_house',email)
    return render_template('post_house.html', email=email, password=password)


# z5119435
# Huang wei
# the remove_house function:
@app.route('/post_house', methods=['GET', 'POST'])
def post_house():
    email = request.values.get('email')
    password = request.values.get('password')
    if request.method == 'POST':
        title = request.values.get('title')
        price = request.values.get('price')
        address = request.values.get('address')
        latitude = request.values.get('latitude')
        longitude = request.values.get('longitude')
        print('latitude=', latitude)
        print('longitude=', longitude)
        guest = request.values.get('guest')
        bedroom = request.values.get('bedroom')
        bed = request.values.get('bed')
        bath = request.values.get('bath')
        address = request.values.get('address')
        content = request.values.get('content')
        policy = request.values.get('policy')
        options1 = request.values.getlist("options1")
        options2 = request.values.getlist("options2")
        # picname = None
        # try:
        #     picname = [request.files['pic']]
        # except:
        #     pass

        # this part by fanxiaoyu
        picname = []
        try:
            pic = request.files.getlist('pic')
            picname.append(pic)
            print('上传文件', picname)
        except:
            pass

        policy = "\n".join(policy.split('\r\n'))
        max_index = control.puthouse(email, password, picname, title, guest, bedroom,
                                     bed, bath, price, options1, options2, policy, content, address, latitude,
                                     longitude)
        # print('max_index=',max_index)
        Post = []
        Deleted = []
        Collect = []
        if (control.verify(email, password)):
            user = control.getuser(email)
            user['property'].append(str(max_index))
            try:
                control.putuser(email, user['user_name'], user['birthday'], password, user['phone number'],
                                user['address'], user['property'], user['deleted_post'])
            except:
                control.putuser(email, user['user_name'], user['birthday'], password, user['phone number'],
                                user['address'], user['property'])
            try:
                for i in user['property']:
                    Post.append(house.readhouse(i))
            except:
                pass
            # print(Post)
            try:
                for i in user['deleted_post']:
                    Deleted.append(house.read_deleted_house(i))
            except:
                pass

            try:
                visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
                for i in visible_collect:
                    Collect.append(house.readhouse(i))
            except:
                pass
            # print(Deleted)
            birthday = '-'.join(user['birthday'].split('/')[::-1])
            return render_template('person_information_page.html',
                                   email=email, password=password,
                                   user_name=user['user_name'], birthday=birthday,
                                   address=user['address'], phone_number=user['phone number'],
                                   Post=Post, Deleted=Deleted, Collect=Collect)
    else:
        return render_template('person_information_page.html')


# z5119435
# Huang wei
# the removehouse permenant function:
@app.route('/remove_house_permanent', methods=['GET'])
def remove_house_permanent():
    email = request.args.get('email')
    password = request.args.get('password')
    houseid = request.args.get('house_id')
    if (control.verify(email, password)):
        user = control.getuser(email)
        user['deleted_post'].remove(houseid)
        control.remove_house_permanent(houseid)
        control.putuser(email, user['user_name'],
                        user['birthday'], password,
                        user['user_name'], user['address'],
                        user['property'], user['deleted_post'])
        Post = []
        Deleted = []
        Collect = []
        try:
            for i in user['property']:
                Post.append(house.readhouse(i))
        except:
            pass
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
        except:
            pass
        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass

        control.putuser(email, user['user_name'], user['birthday'],
                        password, user['phone number'], user['address'],
                        user['property'], user['deleted_post'])
        birthday = '-'.join(user['birthday'].split('/')[::-1])
        return render_template('person_information_page.html',
                               email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=Post, Deleted=Deleted, Collect=Collect)
    else:
        return


# z5119435
# Huang wei
# the houseinfo function:
# resultlist0->houseinfo0
@app.route('/houseinfo', methods=['GET'])
def houseinfo():
    email = request.args.get('email')
    # print(email)
    password = request.args.get('password')
    houseid = request.args.get('houseid')
    h = house.readhouse(houseid)
    policy = "<br>".join(h['Policies'])
    cook = 'Not' if 'No cooking' in h['Policies'] else ''
    smoke = 'Not' if 'No smoking' in h['Policies'] else ''
    pet = 'Not' if 'No pets' in h['Policies'] else ''
    bedroom_number = 0
    guests = 0
    bed_number = 0
    toilet_number = 0
    for line in h['configuration']:
        if ('guest' in line):
            guests = int(line.split(' ')[0])
        elif ('bedroom' in line):
            bedroom_number = int(line.split(' ')[0])
        elif ('bed' in line):
            bed_number = int(line.split(' ')[0])
        elif ('bath' in line):
            toilet_number = int(line.split(' ')[0])
    # post house owner
    post_email = h['belonging']
    user = control.getuser(post_email)

    return render_template('house_info.html',
                           email=email, password=password,
                           houseid=houseid, title=h['title'],
                           configuration=h['configuration'],
                           cook=cook, smoke=smoke, pet=pet,
                           bedroom_number=bedroom_number, guests=guests,
                           bed_number=bed_number, toilet_number=toilet_number,
                           price=h['price'], image=h['image'],
                           Amenities=h['Amenities'], host=h['Host'],
                           content=h['content'], longitude=h['longitude'],
                           latitude=h['latitude'], policy=policy,
                           post_email=post_email, user_name=user['user_name'],
                           address=user['address'], phone_number=user['phone number']
                           )


# z5119435
# Huang wei
# the houseinfo function:
# resultlist1->houseinfo1
@app.route('/houseinfo1', methods=['GET'])
def houseinfo1():
    email = request.args.get('email')
    password = request.args.get('password')
    houseid = request.args.get('houseid')
    h = house.readhouse(houseid)
    policy = "<br>".join(h['Policies'])
    cook = 'Not' if 'No cooking' in h['Policies'] else ''
    smoke = 'Not' if 'No smoking' in h['Policies'] else ''
    pet = 'Not' if 'No pets' in h['Policies'] else ''
    bedroom_number = 0
    guests = 0
    bed_number = 0
    toilet_number = 0
    for line in h['configuration']:
        if ('guest' in line):
            guests = int(line.split(' ')[0])
        elif ('bedroom' in line):
            bedroom_number = int(line.split(' ')[0])
        elif ('bed' in line):
            bed_number = int(line.split(' ')[0])
        elif ('bath' in line):
            toilet_number = int(line.split(' ')[0])
    # post house owner
    post_email = h['belonging']
    user = control.getuser(post_email)
    user1 = control.getuser(email)
    collect_id=[]
    try:
        collect_id = user1['collect']
    except:
        pass
    return render_template('house_info1.html',
                           email=email, password=password,
                           houseid=houseid, title=h['title'],
                           configuration=h['configuration'],
                           cook=cook, smoke=smoke, pet=pet,
                           bedroom_number=bedroom_number, guests=guests,
                           bed_number=bed_number, toilet_number=toilet_number,
                           price=h['price'], image=h['image'],
                           Amenities=h['Amenities'], host=h['Host'],
                           content=h['content'], longitude=h['longitude'],
                           latitude=h['latitude'], policy=policy,
                           post_email=post_email, user_name=user['user_name'],
                           address=user['address'], phone_number=user['phone number'],
                           Collect=collect_id)


# function : search_register
# writer : chengwen Peng
# zid : 5103407
#
@app.route('/search_register', methods=['GET'])
def search_register():
    if (request.method == 'GET'):
        email = request.args.get('register_email')
        password = request.args.get('register_password')
        username = request.args.get('register_username')
        birthday = request.args.get('register_birthday')
        phone_number = request.args.get('register_phone_number')
        address = request.args.get('register_address')
        srcfile = './data/user/head/default.jpg'
        dstfile = './data/user/head/' + email + '.jpg'
        shutil.copyfile(srcfile, dstfile)
        if (control.putuser(email, username, birthday, password, phone_number, address,[],[],[]) == False):
            return render_template('search0.html')
        else:
            return render_template('search1.html', email=email, password=password)


# 2018-10-1 pengchengwen
# help,home,help_login

@app.route('/help', methods=['GET'])
def help():
    if (request.method == 'GET'):

        email = request.args.get('email')
        password = request.args.get('password')
        # print(email)
        if email == '':

            return render_template('help0.html')
        else:
            return render_template('help1.html', email=email, password=password)


@app.route('/help_login', methods=['GET'])
def help_login():
    if (request.method == 'GET'):
        email = request.args.get('login_email')
        password = request.args.get('login_password')
        if (control.verify(email, password)):
            return render_template('help1.html', email=email, password=password)
        else:
            return render_template('help0.html')


@app.route('/home', methods=['GET'])
def home():
    if (request.method == 'GET'):

        email = request.args.get('email')
        password = request.args.get('password')
        # print(email)
        if email == '':

            return render_template('search0.html')
        else:
            return render_template('search1.html', email=email, password=password)


# function : feedback
# writer : chengwen Peng
# zid : 5103407
@app.route('/feedback', methods=['POST'])
def feedback():
    # if(request.method == 'GET'):
    #
    #     feedback = request.args.get('feedback')

    email = request.form.get('email')
    password = request.form.get('password')
    Deleted = []
    Collect = []
    if request.method == 'POST':
        title = str(request.form.get('title'))
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(nowtime)
        content = request.values.get('content')

        control.feedback_write_file(email, title, nowtime, content)
        user = control.getuser(email)
        try:
            Post = [house.readhouse(_) for _ in user['deleted_post']]
        except:
            Post=[]
        try:
            Deleted = user['deleted_post']
        except:
            pass
        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass
        birthday = '-'.join(user['birthday'].split('/')[::-1])
        return render_template('person_information_page.html', email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=Post, Deleted=Deleted, Collect=Collect)

    else:
        user = control.getuser(email)
        try:
            Post = [house.readhouse(_) for _ in user['deleted_post']]
        except:
            Post=[]
        try:
            Deleted = user['deleted_post']
        except:
            pass
        try:
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            pass
        birthday = '-'.join(user['birthday'].split('/')[::-1])
        return render_template('person_information_page.html', email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=Post, Deleted=Deleted, Collect=Collect)


@app.route('/house_info_login', methods=['GET'])
def house_info_login():
    if (request.method == 'GET'):
        email = request.args.get('login_email')
        password = request.args.get('login_password')
        if (control.verify(email, password)):
            return render_template('house_info1.html', email=email, password=password)
        else:
            return render_template('house_info.html')


# function : map
# writer : huang wei
# zid : 5119435
@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('map.html')


# function: go to edit house page
# pengchengwen
@app.route('/to_edit_house', methods=['GET', 'POST'])
def to_edit_house():
    email = request.args.get('email')
    password = request.args.get('password')
    house_id = request.args.get('house_id')
    print(house_id)
    h = house.readhouse(house_id)
    # bug fix by huang,wei
    try:
        # print('to_edit=',h['Policies'])
        policy = "\n".join(h['Policies'])
    except:
        pass
    #
    # print(h['configuration'])
    for line in h['configuration']:
        if ('guest' in line):
            guests = int(line.split(' ')[0])
            # print('guest=',guests)
        elif ('bedroom' in line):
            bedroom_number = int(line.split(' ')[0])
            # print('bedroom=',bedroom_number)
        elif ('bed' in line):
            bed_number = int(line.split(' ')[0])
        elif ('bath' in line):
            toilet_number = int(line.split(' ')[0])

    return render_template('edit_house.html', email=email, password=password, house_id=house_id,
                           title=h['title'], bedroom_number=bedroom_number,
                           guests=guests, bed_number=bed_number,
                           toilet_number=toilet_number, price=h['price'],
                           host=h['Host'], content=h['content'],
                           address=h['address'], policy=policy,
                           latitude=h['latitude'], longitude=h['longitude'])


# function: edit_house
# chengwen peng
@app.route('/edit_house', methods=['GET', 'POST'])
def edit_house():
    email = request.values.get('email')
    password = request.values.get('password')
    house_id = int(request.values.get('house_id'))
    print(email, password, 'house_id12=', house_id)

    if request.method == 'POST':
        title = request.values.get('title')
        address = request.values.get('address')
        latitude = request.values.get('latitude')
        longitude = request.values.get('longitude')
        print('latitude=', latitude)
        print('longitude=', longitude)
        price = request.values.get('price')
        guest = request.values.get('guest')
        bedroom = request.values.get('bedroom')
        bed = request.values.get('bed')
        bath = request.values.get('bath')
        content = request.values.get('content')
        policy = request.values.get('policy')
        options1 = request.values.getlist("options1")
        options2 = request.values.getlist("options2")
        # picname = None
        # try:
        #     picname = [request.files['pic']]
        # except:
        #     pass
        # this part by fanxiaoyu

        # this is by fanxiaoyu
        picname = []
        try:
            pic = request.files.getlist('pic')
            picname.append(pic)
            print('上传文件', picname)
        except:
            pass

        control.empty_folder(str(house_id))
        policy = "\n".join(policy.split('\r\n'))
        control.edit_house_info(email, password, house_id, picname, title, guest, bedroom,
                                bed, bath, price, options1, options2, policy, content, address, latitude, longitude)

        Post = []
        Deleted = []
        Collect = []
        if (control.verify(email, password)):
            user = control.getuser(email)

            try:
                control.putuser(email, user['user_name'], user['birthday'], password, user['phone number'],
                                user['address'], user['property'], user['deleted_post'])
            except:
                control.putuser(email, user['user_name'], user['birthday'], password, user['phone number'],
                                user['address'], user['property'])
            for i in user['property']:
                Post.append(house.readhouse(i))
            # print(Post)
            try:
                for i in user['deleted_post']:
                    Deleted.append(house.read_deleted_house(i))
            except:
                pass

            try:
                visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
                for i in visible_collect:
                    Collect.append(house.readhouse(i))
            except:
                pass

            birthday = '-'.join(user['birthday'].split('/')[::-1])
            return render_template('person_information_page.html',
                                   email=email, password=password,
                                   user_name=user['user_name'], birthday=birthday,
                                   address=user['address'], phone_number=user['phone number'],
                                   Post=Post, Deleted=Deleted, Collect=Collect)
    else:
        return render_template('person_information_page.html')


# book function
# chengwen peng
# @app.route('/get_owner_info',methods=['GET'])
# def get_owner_info():
#     try:
#         email = request.args.get('email')
#         password = request.args.get('password')
#         user = control.getuser(email)
#         if (control.verify(email, password)):
#             return render_template('house_info1.html', email=email, password =password, user_name=user['user_name'],
#                                    address=user['address'], phone_number=user['phone number'], )
#     except:
#
#         return render_template('house_info.html')

# upload head(判断上传的文件是不是属于允许的类型)
# chengwen peng
@app.route('/upload_head', methods=['POST'])
def upload_head():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST':
        picname = [request.files['pic']]
        # if picname[0] and allowed_file(picname[0]):
        # print(email)
        # print('picname',picname)
        # print('picname[0]',picname[0])
        file_name = "./data/user/head/" + str(email) + ".jpg"
        os.remove(file_name)
        picname[0].save(file_name)
        user = control.getuser(email)
        try:
            Post = [house.readhouse(i) for i in user['property']]
        except:
            Post = []

        try:
            Deleted = [house.readhouse(i) for i in user['deleted_post']]
        except:
            Deleted = []

        try:
            Collect = []
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            Collect = []

        birthday = '-'.join(user['birthday'].split('/')[::-1])
        return render_template('person_information_page.html', email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=Post, Deleted=Deleted, Collect=Collect)
        # else:
        # return render_template('新建文件夹/false.html', email=email, password=password)
    else:
        user = control.getuser(email)
        birthday = '-'.join(user['birthday'].split('/')[::-1])
        try:
            Post = [house.readhouse(i) for i in user['property']]
        except:
            Post = []

        try:
            Deleted = [house.readhouse(i) for i in user['deleted_post']]
        except:
            Deleted = []

        try:
            Collect = []
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            for i in visible_collect:
                Collect.append(house.readhouse(i))
        except:
            Collect = []

        return render_template('person_information_page.html', email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=Post, Deleted=Deleted,Collect=Collect)


@app.route('/colloct', methods=['GET'])
def colloct():
    email = request.values.get('email')
    password = request.values.get('password')
    house_id = request.values.get('house_id')
    if (control.verify(email, password)):
        user = control.getuser(email)
        try:
            post_id = user['property']
        except:
            post_id = []
        try:
            deleted_id = user['deleted_post']
        except:
            deleted_id = []
        try:
            collect = user['collect']
        except:
            collect = []
        collect.append(house_id)
        control.putuser(email, user['user_name'], user['birthday'],
                        password, user['phone number'], user['address'],
                        post_id, deleted_id, collect)
        return 'success'
    else:
        return 'fail'


@app.route('/uncolloct', methods=['GET'])
def uncolloct():
    email = request.values.get('email')
    password = request.values.get('password')
    house_id = request.values.get('house_id')
    if (control.verify(email, password)):
        user = control.getuser(email)
        try:
            post = [house.readhouse(i) for i in user['property']]
            post_id=[i for i in user['property']]
        except:
            post = []
            post_id = []
        try:
            deleted = [house.read_deleted_house(i) for i in user['deleted_post']]
            deleted_id = [i for i in user['deleted_post']]
        except:
            deleted = []
            deleted_id = []
        collect_id=[]
        try:

            collect = []
            visible_collect = set(user['collect']).difference(set(os.listdir('data/house_del')))
            collect_id=[item for item in visible_collect]
            collect_id.remove(house_id)
            for i in collect_id:
                collect.append(house.readhouse(i))

        except:
            pass
        control.putuser(email, user['user_name'], user['birthday'],
                        password, user['phone number'], user['address'],
                        post_id, deleted_id, collect_id)
        user = control.getuser(email)

        birthday = '-'.join(user['birthday'].split('/')[::-1])
        return render_template('person_information_page.html', email=email, password=password,
                               user_name=user['user_name'], birthday=birthday,
                               address=user['address'], phone_number=user['phone number'],
                               Post=post, Deleted=deleted, Collect=collect)
    else:
        return 'fail'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
