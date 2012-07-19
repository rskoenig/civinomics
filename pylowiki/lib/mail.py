import os

def send( send_too, send_from, subject, message ):

    #SENDMAIL = "sendmail" #path to sendmail
    SENDMAIL = "/usr/sbin/sendmail" #path to sendmail
    BR = "\n" # BR types/reads easier

    sub_process = os.popen( "%s -t" % SENDMAIL, "w" )
    sub_process.write( "To: " + send_too + BR )
    sub_process.write( "From: " + send_from + BR )
    sub_process.write( "Subject: " + subject + BR )
    sub_process.write( BR ) #blank line seperates headers from body
    sub_process.write( message + BR )
    status = sub_process.close()
    return True
    #if status = != None:
    #    print "Sendmail exit status", status
