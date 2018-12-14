import math
import re

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
            return render_template('result_list1.html', search_phrase=search, email=email, password=password)
        except:
            return render_template('search1.html')


# function : change_person_info
# writer : huang, wei
# zid : 5119435
@app.route('/change_person_info', methods=['GET'])
def change_person_info():
    if (request.method == 'GET'):
        try:
            email = request.args.get('email')
            password = request.args.get('password')
            address = request.args.get('address')
            phone_number = request.args.get('phone_number')
            user_name = request.args.get('user_name')
            birthday = request.args.get('birthday')
            user = dict()
            if (control.verify(email, password)):
                control.putuser(email, user_name, birthday, password, phone_number, address)
            return render_template('person_information_page.html',
                                   email=email, password=password,
                                   user_name=user_name, birthday=birthday,
                                   address=address, phone_number=phone_number)
        except:
            return render_template('search1.html')


# function : search0
# writer : huang, wei
# zid : 5119435
# result_list0-->result_list1
@app.route('/result_list_login', methods=['GET'])
def result_list_login():
    if (request.method == 'GET'):
        search = request.args.get('search')
        email = request.args.get('login_email')
        password = request.args.get('login_password')
        if (control.verify(email, password)):
            return render_template('result_list1.html', search_phrase=search, email=email, password=password)
        else:
            return render_template('result_list0.html')


# function : result_list_content
# writer : huang, wei
# zid : 5119435
@app.route('/result_list_content', methods=['GET'])
def result_list_content():
    search_list = []
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
                                   password=password)


# z5104537
#  Xiaoyu Fan, Huang wei
# the post function:
@app.route('/personal_info')
def personal_info():
    email = request.args.get('email')
    password = request.args.get('password')
    # print(email, password)
    user = dict()
    Post = []
    Deleted = []
    if (control.verify(email, password)):
        user = control.getuser(email)
        post = user['property']
        for i in post:
            Post.append(house.readhouse(i))
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
        except:
            pass
    else:
        return
    birthday = '-'.join(user['birthday'].split('/')[::-1])
    return render_template('person_information_page.html',
                           email=email, password=password,
                           user_name=user['user_name'], birthday=birthday,
                           address=user['address'], phone_number=user['phone number'],
                           Post=Post, Deleted=Deleted)


# z5119435
# Huang wei
# the get_comment function:
@app.route('/get_comment')
def get_comment():
    email=request.args.get('email')
    password=request.args.get('password')
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
                           belonging=h1['belonging'],email=email,
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
    print(email,password,house_id,comment_id,comment_content)
    if(control.verify(email,password)):
        comment.add_comment(email,house_id,comment_id,comment_content)
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
    if (control.verify(email, password)):
        user = control.getuser(email)
        user['deleted_post'].remove(str(house_id))
        try:
            user['property'].append(str(house_id))
        except:
            user['property'] = str(house_id)
        house.recover_house(house_id)
        for i in user['property']:
            Post.append(house.readhouse(i))

        for i in user['deleted_post']:
            Deleted.append(house.read_deleted_house(i))
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
                           Post=Post, Deleted=Deleted)


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
    if (control.verify(email, password)):
        user = control.getuser(email)
        user['property'].remove(str(house_id))
        post = user['property']
        print(post)
        house.remove_house(house_id)
        for i in post:
            Post.append(house.readhouse(i))
        try:
            user['deleted_post'].append(str(house_id))
        except:
            user['deleted_post'] = str(house_id)
        try:
            for i in user['deleted_post']:
                Deleted.append(house.read_deleted_house(i))
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
                           Post=Post, Deleted=Deleted)


# the logout function:
@app.route('/log_out')
def log_out():
    email = request.args.get('email')
    password = request.args.get('password')
    if (control.verify(email, password)):
        control.offline(email, password)
    return render_template('search0.html')


@app.route('/person_page', methods=['GET', 'POST'])
def post_house():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        guest = request.values.get('guest')
        bedroom = request.values.get('bedroom')
        bed = request.values.get('bed')
        bath = request.values.get('bath')
        content = request.values.get('content')
        policy = request.values.get('policy')
        options1 = request.values.getlist("options1")
        options2 = request.values.getlist("options2")
        picname = None
        try:
            picname = [request.files['pic']]
        except:
            pass
        control.puthouse(email, password, picname, title, guest, bedroom,
                         bed, bath, price, options1, options2, policy, content)
        return render_template('person_information_page.html', email=email)
    else:
        return render_template('person_information_page.html')


@app.route('/houseinfo', methods=['GET'])
def houseinfo():
    email = request.args.get('email')
    password = request.args.get('password')
    houseid = request.args.get('houseid')
    h = house.readhouse(houseid)
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
    return render_template('house_info.html',
                           email=email, password=password,
                           houseid=houseid, title=h['title'],
                           configuration=h['configuration'],
                           cook=cook, smoke=smoke, pet=pet,
                           bedroom_number=bedroom_number, guests=guests,
                           bed_number=bed_number, toilet_number=toilet_number,
                           price=h['price'], image=h['image'],
                           Amenities=h['Amenities'], host=h['Host'],
                           content=h['content'])


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
        if (control.putuser(email, username, birthday, password, phone_number, address) == False):
            return render_template('search0.html')
        else:
            return render_template('search1.html')


# 2018-10-1 pengchengwen
# help,home,help_login

@app.route('/help', methods=['GET'])
def help():
    if (request.method == 'GET'):

        email = request.args.get('email')
        password = request.args.get('password')
        print(email)
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
        print(email)
        if email == '':

            return render_template('search0.html')
        else:
            return render_template('search1.html', email=email, password=password)


# print(comment.get_comment("1"))
if __name__ == '__main__':
    app.run()
