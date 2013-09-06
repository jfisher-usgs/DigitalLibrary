## Script (Python) "logout"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request  = container.REQUEST
REQUEST  = context.REQUEST
RESPONSE = request.RESPONSE

ROOT = container.root()
rootUrl = ROOT.absolute_url()

RESPONSE.expireCookie('__ac', path='/')
RESPONSE.redirect(rootUrl)
