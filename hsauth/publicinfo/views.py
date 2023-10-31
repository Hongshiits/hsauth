from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse

import json
import base64
import os
import traceback

from hsauth.settings import BASE_DIR
from auth.views import islogin_inter
from auth.views import db_obj,login_select_uuid_sql,chg_select_everything_sql



# Create your views here.
def upload_avatar(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
        }
    }
    if request.method == 'POST':
        req=json.loads(str(request.POST.get('data')))
        try:
            db_obj.ping(reconnect=True)
            if(islogin_inter(request)):
                digested_token_in=json.loads(str(base64.b64decode(req["token"].encode("utf-8")),encoding="utf-8"))
                digested_token_in['uuid']

                print(request.FILES)

                avatar_file=open(os.path.join(BASE_DIR, '../static/avatar/',digested_token_in['uuid']+'.jpg'),'wb')
                avatar_file.write(request.FILES['avatar'].read())
                avatar_file.close()
                res['data']['status'] = 'ok'
                res['data']['msg'] = 'true'
            else:
                res['data']['status'] = 'false'
                res['data']['msg'] = 'unauthorized'
        except Exception as e:
                traceback.print_exc()
                res['data']['status'] ='error'
                res['data']['msg'] =str(Exception)
        
    return JsonResponse(res)

def get_info(request:HttpRequest):
    req=None
    res={
        'data':{
            'status':'',
            'msg':'',
            'nickname':'',
        }
    }
    if request.method == 'POST':
        try:
            db_obj.ping(reconnect=True)
            req=json.loads(str(request.POST.get('data')))
            db_cursor=db_obj.cursor()
            db_cursor.execute(login_select_uuid_sql,(req['uuid']))
            db_data=db_cursor.fetchone() # type: ignore
            res['data']['username']=db_data[3]# type: ignore
            db_cursor.execute(chg_select_everything_sql,('basic_info',req['uuid']))
            db_data=db_cursor.fetchone() # type: ignore
            if db_data is not None:   #2 region 3 nickname 5 bio
                res['data']['region']=db_data[2]# type: ignore
                res['data']['nickname']=db_data[3]# type: ignore
                res['data']['bio']=db_data[5]# type: ignore
                pass

            db_cursor.close()
        except Exception as e:
            traceback.print_exc()
            res['data']['status'] ='error'

    return JsonResponse(res)

        
        
        


