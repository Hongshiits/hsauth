from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse

import atexit
import hashlib
import json
import base64
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import calendar
import traceback
from threading import Thread
# Create your views here.

################################################################
# tool method
################################################################


cache_counts=1
cache_time=calendar.timegm(time.gmtime())
def generate_uuid(server_num:str,db_num:str):
    global cache_counts,cache_time
    cache_counts+=1
    cache_time_in=calendar.timegm(time.gmtime())
    if (cache_time_in-cache_time)>100:
        cache_time=cache_time_in
        cache_counts=0
    return server_num + db_num + str(cache_time)+str(cache_counts)

signature_key='YmYyNGVjZDI0MWVkYjljNDYwZGY1MDhiYmIyMWI0NDI1MmQ2YWM4OTJhMGE3NjJjMDdmY2MwNTdkZGE4ZTQ5Mg=='
def generate_token(uuid:str,time_in:str,hash:str,add_str:str=""):
    #base64 
    #store structure:
    #hash uuid time signature
    #signature structure:
    #hash method(hash+uuid+time+signature key)
    processed_time=str(calendar.timegm(time.gmtime())+int(time_in))
    data_in_token={
        'hash': hash,
        'uuid': uuid,
        'time': processed_time,
        'signature': hashlib.sha256(str(hash+uuid+processed_time+signature_key+add_str).encode('utf-8')).hexdigest()
    }
    return str(base64.b64encode(str(json.dumps(data_in_token)).encode("utf-8")),encoding="utf-8")

def chktoken(token:str,add_str:str="",digested_token_in=None):
    digested_token=digested_token_in
    if digested_token_in is None:
        digested_token=json.loads(str(base64.b64decode(token.encode("utf-8")),encoding="utf-8"))
    if int(digested_token['time'])>calendar.timegm(time.gmtime()) and hashlib.sha256(str(digested_token['hash']+digested_token['uuid']+digested_token['time']+signature_key+add_str).encode('utf-8')).hexdigest() == digested_token['signature']:#type: ignore
        return True
    else:
        return False 
    
def send_email(email_in:str,host_in=None,add_type=None):
    otp=generate_token(email_in,'600','sha256')
    smtp_obj=smtplib.SMTP('smtp.office365.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login('notifications@inkore.net','iNKOREAuth#PSWD')
    if add_type is None:
        message=MIMEText(mail_template_001%(host_in,otp,email_in),'html','utf-8')
    else:
        message=MIMEText(mail_template_general[add_type]%(host_in,otp,email_in),'html','utf-8')
    message['From']='notifications@inkore.net'
    message['To']=email_in
    message['Subject']=Header('Hongshiite账户验证码','utf-8')
    smtp_obj.sendmail('notifications@inkore.net',email_in,message.as_string())
    smtp_obj.quit()
##################################################################






########################################################################
# 1,register
# 2,login
# 4,chkstatus(abandon)
# 3,islogin
# 5,email_otp





################################################################
#pre
# 1,pymysql(https://zhuanlan.zhihu.com/p/139763027)

# db structure:
#
# user table:
# uuid (primary key)
# email
# password
# username 
# 

db_obj=pymysql.connect(host='localhost',port=3306,user='sql1',passwd='OIglOI08240923**sql1',database='hsauth')

def pre_db_obj():
    db_obj.ping(reconnect=True)
    pass

register_insert_sql='INSERT INTO users (uuid,username,email,password) VALUES (%s,\'%s\',\'%s\',\'%s\')'
register_server_num=1
register_db_num=1

login_select_uuid_sql='SELECT * FROM users WHERE uuid = %s'
login_select_email_sql='SELECT * FROM users WHERE email = \'%s\''
reg_select_reg_email_sql='SELECT * FROM reg_email WHERE email = \'%s\''
reg_insert_reg_email_sql='INSERT INTO reg_email (email,last_act_time) VALUES (\'%s\',%s)'
reg_update_reg_email_sql='UPDATE reg_email SET last_act_time = \'%s\' WHERE email = \'%s\''
chg_update_everything_sql='UPDATE %s SET %s = \'%s\' WHERE uuid = \'%s\''
chg_update_everything_email_sql='UPDATE %s SET %s = \'%s\' WHERE email = \'%s\''
chg_insert_everything_sql='INSERT INTO %s (uuid,%s) VALUES (\'%s\',\'%s\')'
chg_select_everything_sql='SELECT * FROM %s WHERE uuid = %s'

#db_cursor.execute('slquery')
#data=db_cursor.fetchall()
#data=db_cursor.fetchone()

@atexit.register
def close_db_connection():
    db_obj.close()
    pass

################################################################
# 2，smtplib
#



mail_template_001="""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP -->
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <meta
      http-equiv="X-Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <title>Hongshiite OTP</title>
  </head>
  <body>
    <p>您的邮箱验证码是</p>
    <a href='http://%s/static/register.html?otp=%s&email=%s'>注册</a>
    <p>该验证码用于注册Hongshiite账户，十分钟内有效，请勿随意给其他人</p>
  </body>
</html>

"""
mail_template_general={}
mail_template_general['register']=mail_template_001
mail_template_general['reset']="""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP -->
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <meta
      http-equiv="X-Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <title>Hongshiite OTP</title>
  </head>
  <body>
    <p>您的邮箱验证码是</p>
    <a href='http://%s/static/reset_password.html?otp=%s&email=%s'>重置密码</a>
    <p>该验证码用于重置Hongshiite账户密码，十分钟内有效，请勿随意给其他人</p>
  </body>
</html>

"""


########################################################################
# register
# req(data):
# 1,email
# 1,OTP
# 2,username
# 3,password(sha256)
#
# res(data):
# 1,status
# 2,msg


def register(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        },
    }
    if request.method == 'POST':
        try:
            pre_db_obj()
            req=dict(json.loads(str(request.POST.get('data'))))
            if chktoken(req['otp'])!=True:
                raise Exception('otp invailed')
            uuid=generate_uuid(str(register_server_num),str(register_db_num))
            db_cursor=db_obj.cursor()
            db_cursor.execute(register_insert_sql%(uuid,req['username'],req['email'],req['password']))
            db_obj.commit()
            db_cursor.close()
            res['data']['status']='ok'
            res['data']['msg'] ='ok'            
        except Exception:
            res['data']['status']='error'
            res['data']['msg'] =str(Exception)
            db_obj.rollback()
            traceback.print_exc()
            pass
        return JsonResponse(res)
    else:
        return render(request,'auth_pro_register.html')
        pass

    

################################################################
# login
# req:
# 1,email(or uuid)
# 2,password
# 3,is_long_term_login
# 
# res:
# 1,status
# 2,msg
# 3,token
# 4,time
# 5,uuid
def login(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
            'token':'',
            'time':'',
            'uuid':''
        }
    }
    if request.method == 'POST':
        try:
            pre_db_obj()
            req=json.loads(str(request.POST.get('data')))
            db_cursor=db_obj.cursor()
            db_cursor.execute(login_select_email_sql%req['email'])
        
            db_data=db_cursor.fetchone() # type: ignore
            
            if db_data is not None and db_data[2]==req['password']: # type: ignore
                
                res['data']['status'] ='ok'
                res['data']['msg'] ='login successful'
                res['data']['uuid']=str(db_data[0]) # type: ignore
                if req['is_long_term_login']=='True':
                    res['data']['time']='15552000' 
                    res['data']['token'] =generate_token(str(db_data[0]), '15552000','sha256',db_data[2])# type: ignore
                    pass
                else:
                    res['data']['time']='86400' 
                    res['data']['token'] =generate_token(str(db_data[0]), '86400','sha256',db_data[2])# type: ignore
                    pass
                pass
            else: 
                res['data']['status'] ='fail'
                res['data']['msg'] ='Invalid password or email address'
                pass            


            db_cursor.close()

        except Exception:
            traceback.print_exc()
            res['data']['status'] ='error'
            res['data']['msg'] =str(Exception)
            pass

    return JsonResponse(res)

################################################################
# reset
# req:
# 1,email
# 2,otp
# 3,password
# res:
# (general)

def auth_reset(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        },
    }
    if request.method == 'POST':
        try:
            pre_db_obj()
            req=dict(json.loads(str(request.POST.get('data'))))

            digested_token=json.loads(str(base64.b64decode(req["otp"].encode("utf-8")),encoding="utf-8"))
            if chktoken(req['otp'],"",digested_token)!=True:
                raise Exception('otp invailed')
            uuid=digested_token['uuid']
            db_cursor=db_obj.cursor()
            db_cursor.execute(chg_update_everything_email_sql,('users','password',req['password'],req['uuid']))
            db_obj.commit()
            db_cursor.close()
            res['data']['status']='ok'
            res['data']['msg'] ='ok'            
        except Exception:
            res['data']['status']='error'
            res['data']['msg'] =str(Exception)
            db_obj.rollback()
            traceback.print_exc()
            pass
    return JsonResponse(res)
    
    

########################################################################
# islogin
# req:
# 1,token
# res:
# 1,status
# 2,msg
def islogin(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':
        pre_db_obj()
        req=json.loads(str(request.POST.get('data')))

        digested_token=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))

        db_cursor=db_obj.cursor()
        db_cursor.execute(login_select_uuid_sql%digested_token['uuid'])
        db_data=db_cursor.fetchone() # type: ignore



        if chktoken(req['token'],db_data[2],digested_token):# type: ignore
            res['data']['status'] = 'ok'
            res['data']['msg'] = 'true'
        else:
            res['data']['status'] = 'fail'
            res['data']['msg'] = 'false'
            pass


        db_cursor.close()

    return JsonResponse(res)

def islogin_inter(request:HttpRequest):
    req=None
    if request.method == 'POST':
        pre_db_obj()
        req=json.loads(str(request.POST.get('data')))

        digested_token=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))

        db_cursor=db_obj.cursor()
        db_cursor.execute(login_select_uuid_sql%digested_token['uuid'])
        db_data=db_cursor.fetchone() # type: ignore

        if chktoken(req['token'],db_data[2],digested_token):# type: ignore
            db_cursor.close()
            return True
        else:
            db_cursor.close()
            return False
            


        



########################################################################
# email_otp
# req:
# 1,email
# res:
# 1,status
# 2,msg
def email_otp(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':


        try:
            pre_db_obj()
            req=json.loads(str(request.POST.get('data')))

            time_cache_in=calendar.timegm(time.gmtime())

            db_cursor=db_obj.cursor()
            db_cursor.execute(reg_select_reg_email_sql%req['email'])
            db_data=db_cursor.fetchone() # type: ignore

            new_user_flag=0

            if db_data==None:
                db_cursor.execute(reg_insert_reg_email_sql%(req['email'],time_cache_in))
                new_user_flag=1
                db_obj.commit()
                db_cursor.execute(reg_select_reg_email_sql%req['email'])
                db_data=db_cursor.fetchone() # type: ignore
            
            if int(db_data[1])+60<time_cache_in or new_user_flag==1:# type: ignore

                try:
                    if req['type'] is not None:
                        Thread(target=send_email,args=[str(req['email']),req['host'],req['type']]).start()
                    else:
                        Thread(target=send_email,args=[str(req['email']),req['host']]).start()
                    res['data']['status'] ='ok'
                except Exception:
                    res['data']['status'] ='error'
                
            else:
                res['data']['status'] ='fail'
                res['data']['msg'] ='Frequent request'
            db_cursor.execute(reg_update_reg_email_sql%(time_cache_in,req['email']))
            db_obj.commit()

            db_cursor.close()

            pass
        except Exception:
            res['data']['status'] ='error'
            res['data']['msg']=str(Exception)
            traceback.print_exc()
    return JsonResponse(res)

#########################################################
#req
#token
#table
#column
#value
block_table=['reg_mail','logs']
block_column=['uuid','password','email']
block_select_column=['password']


def update_info(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':



        pre_db_obj()
        req=json.loads(str(request.POST.get('data')))

        digested_token=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))

        db_cursor=db_obj.cursor()
        db_cursor.execute(login_select_uuid_sql%digested_token['uuid'])
        db_data=db_cursor.fetchone() # type: ignore
        db_cursor.close()

        if (req['table'] not in block_table) and (req['column'] not in block_column) and chktoken(req['token'],db_data[2],digested_token):# type: ignore
            try:
                db_cursor=db_obj.cursor()
                db_cursor.execute(chg_update_everything_sql%(req['table'],req['column'],req['value'],digested_token['uuid']))
                db_obj.commit()
                res['data']['status'] = 'ok'
                res['data']['msg'] = 'true'
            except Exception:
                res['data']['status'] = 'fail'
                res['data']['msg'] = 'update error.check whether your infomation is in this table.'
            
            
        else:
            res['data']['status'] = 'fail'
            res['data']['msg'] = 'Invalid token'
            pass


        db_cursor.close()

    return JsonResponse(res)

def insert_info(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':



        pre_db_obj()
        req=json.loads(str(request.POST.get('data')))

        digested_token=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))

        db_cursor=db_obj.cursor()
        db_cursor.execute(login_select_uuid_sql%digested_token['uuid'])
        db_data=db_cursor.fetchone() # type: ignore
        db_cursor.close()

        if (req['table'] not in block_table) and (req['column'] not in block_column) and chktoken(req['token'],db_data[2],digested_token):# type: ignore
            
            db_cursor=db_obj.cursor()
            db_cursor.execute(chg_insert_everything_sql%(req['table'],req['column'],digested_token['uuid'],req['value']))
            db_obj.commit()
            res['data']['status'] = 'ok'
            res['data']['msg'] = 'true'
            
        else:
            res['data']['status'] = 'fail'
            res['data']['msg'] = 'Invalid token'
            pass


        db_cursor.close()

    return JsonResponse(res)

def select_info(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':



        pre_db_obj()
        req=json.loads(str(request.POST.get('data')))

        digested_token=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))

        db_cursor=db_obj.cursor()
        db_cursor.execute(login_select_uuid_sql%digested_token['uuid'])
        db_data=db_cursor.fetchone() # type: ignore
        db_cursor.close()

        if (req['table'] not in block_table) and chktoken(req['token'],db_data[2],digested_token):# type: ignore
            
            db_cursor=db_obj.cursor()
            db_cursor.execute(chg_select_everything_sql%(req['table'],digested_token['uuid']))
            db_data=db_cursor.fetchone()
            temp_json_data={}
            temp_count=0
            for column_in in db_cursor.description:
                if column_in not in block_select_column:
                    temp_json_data[column_in[0]]=str(db_data[temp_count])  # type: ignore
                temp_count+=1
                pass
            res['data']['status'] = 'ok'
            res['data']['msg'] = 'true'
            
            res['data']['info']=temp_json_data # type: ignore
            
        else:
            res['data']['status'] = 'fail'
            res['data']['msg'] = 'Invalid token'
            pass


        db_cursor.close()

    return JsonResponse(res)































#test data:
#FD.append('data',
# '{
# \"email\":\"hongshiite@outlook.com\",
# \"otp\":\"eyJoYXNoIjogInNoYTI1NiIsICJ1dWlkIjogImhvbmdzaGlpdGVAb3V0bG9vay5jb20iLCAidGltZSI6ICIxNjkzNjAzMDgwIiwgInNpZ25hdHVyZSI6ICJmZWM1MGMxMWQwNDFhMjE0YTNkYzE2MTM2MTg3YmRmYTFmMWY0NTY5YTNlMDM5MTU5NDVlMWJhYjRmZTRjMzM4In0=\",
# \"username\":\"PtCu\",
# \"password\":\"fghnbvghjhvghjbvghbvfghvfghv\",
# \"token\":\"eyJoYXNoIjogInNoYTI1NiIsICJ1dWlkIjogIjExMTY5MzUwNDQ3NzAiLCAidGltZSI6ICIxNzA5MDkzMDk0IiwgInNpZ25hdHVyZSI6ICJiZmQ3Zjk4ZjdmNjQwNDIyMzNhNjg1NzhlZGMwZDAzYmJhMTI1ZjhhNDlhOWNlN2NhMmNlYWM4N2E0NDkxMmQwIn0=\",
# \"is_long_term_login\":\"True\"
# }')
#
#