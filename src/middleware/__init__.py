from flask import request, redirect

def first_request():
    """
        middleware to be run when the very first request is received from the browser
    """
    heroku_url: str = 'https://justice-ndou.herokuapp.com/'
    registered_domain: str = 'https://justice-ndou.herokuapp.com/'

    if request.host_url.lower().startswith(heroku_url):
        return redirect(request.host_url.lower().replace(heroku_url, registered_domain)), 301
