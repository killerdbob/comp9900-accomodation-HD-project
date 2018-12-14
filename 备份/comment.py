import glob
import os
import re
import shutil

# class : comment
# writer : huang, wei
# zid : 5119435
class comment:

    def __init__(cls):
        super(comment, cls).__init__()
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(comment, cls).__call__(*args, **kw)
        return cls._instance

    def del_comment(house_id, comment_id):
        if (not os.path.exists('./data/house/' + str(house_id) + '/comment/del_comment')):
            os.makedirs('./data/house/' + str(house_id) + '/comment/del_comment')
        for filename in glob.glob('./data/house/' + str(house_id) + '/comment/' + comment_id + '*'):
            file = os.path.split(filename)[-1]
            if (re.match(comment_id + '[-.].*', file)):
                shutil.move(filename,
                            './data/house/' + str(house_id) + '/comment/del_comment/' + file)

    def get_comment(house_id, message_id=None):
        result_list = []
        for filename in glob.glob('./data/house/' + str(house_id) + '/comment/*'):
            if (not message_id):
                m = re.match(r'.*?[\\/][0-9]*\.txt$', filename)
            else:
                m = re.match(r'.*?[\\/]' + str(message_id) + '-[0-9]*\.txt$', filename)
            result = dict()
            if (m):
                comment_id = filename.split('\\')[-1][:-4]
                result['comment_id'] = comment_id
                with open(m[0], encoding='utf-8') as f:
                    for line in f:
                        if (re.match('^from: ', line)):
                            result['from'] = line[6:].strip()
                        elif (re.match('^time: ', line)):
                            result['time'] = line[6:].strip()
                        elif (re.match('^message: ', line)):
                            message=line[9:].strip().replace('\\n','<br>')
                            result['message'] = message
                result_list.append(result)
        return result_list

    def add_comment(email,house_id,comment_id,comment_content):
        max_comment_id = 0
        if(comment_id!='-1'):
            for filename in glob.glob('./data/house/' + str(house_id)
                                      + '/comment/' + comment_id + '*'):
                file=os.path.split(filename)[-1]
                if(re.match(comment_id+'-[0-9]*\.txt',file)):
                    max_comment_id=max(int(re.match(comment_id+'-([0-9]*)\.txt',file).groups()[0]),
                        max_comment_id)
            max_comment_id+=1
            with open('./data/house/' + str(house_id)
                      + '/comment/' + str(comment_id)+'-'+str(max_comment_id)+'.txt','w+') as f:
                f.write('from: '+email+'\n')
                f.write('message: '+comment_content+'\n')
        else:
            for filename in glob.glob('./data/house/' + str(house_id)
                                      + '/comment/*'):
                file=os.path.split(filename)[-1]
                if(re.match('[0-9]*\.txt',file)):
                    max_comment_id=max(int(re.match('([0-9]*)\.txt',file).groups()[0]),
                        max_comment_id)
            max_comment_id+=1
            with open('./data/house/' + str(house_id)
                      + '/comment/' + str(max_comment_id)+'.txt','w+') as f:
                f.write('from: '+email+'\n')
                f.write('message: '+comment_content+'\n')

