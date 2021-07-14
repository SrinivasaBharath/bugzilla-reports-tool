# -*- coding: utf-8
import sys
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sys.path.append("cephQeInfra")


from cephQeInfra import docOnQa
from cephQeInfra import htmlPrep
from cephQeInfra import needInfo_class


htmlPrep_obj= htmlPrep.htmlPrep()
docOnQa_Obj= docOnQa.DocOnQaCls()
needInfo_Obj=needInfo_class.needInfoCls()


start_time=time.strftime("%d %b %Y %H:%M")

needInfoBugs=needInfo_Obj.get_NeedInfo_bugs()
doc_OnQA_bugs=docOnQa_Obj.get_Doc_bugs()




sender = "ceph-qe-infra@redhat.com"
recipients = ["ceph-qe@redhat.com"]


msg = MIMEMultipart('mixed')
msg["Subject"] = "Bugzilla action items on QE -Auto generated at "\
                    + start_time +"[IST]"
msg["From"] = sender
msg["To"] = ", ".join(recipients)
part1 = MIMEText(needInfoBugs, "html")
part2 = MIMEText(doc_OnQA_bugs, "html")


msg.attach(part1)
msg.attach(part2)
        

try:
    s = smtplib.SMTP("localhost")
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()
    print(
        "Results have been emailed to {recipients}".format(
         recipients=recipients
         )
        )

except Exception as e:
            print("\n")
            #log.exception(e)