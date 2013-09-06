## Script (Python) "sendMail"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=recipients=None, recipient=None, sender=None, subject='', message=''
##title=
##

if sender is None:
    raise 'No sender provided.'

if recipients is None:
    recipients = (recipient,)
if recipients is None:
    raise 'No recipient(s) specified.'
    
# recipients = string.join(recipients, ';')

try:
    mailhost=getattr(context, context.superValues('Mail Host')[0].id)
except:
    raise AttributeError, "Cant find a mail host object."

msgbody = """
%s
"""

msg = msgbody % message
mailhost.send(messageText=msg, mto=recipients, mfrom=sender, subject=subject)

return
