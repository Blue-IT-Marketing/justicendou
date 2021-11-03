from flask import request, redirect

def first_request():
    print('first request called')
    if request.host_url.lower().startswith('https://justice-ndou.herokuapp.com/'):
        redirect(request.host_url.lower().replace('https://justice-ndou.herokuapp.com/', 'https://justice-ndou.site/')), 301
