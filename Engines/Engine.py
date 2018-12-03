"""
Testing testing
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import sys
import configparser

class Engine():
    config = configparser.ConfigParser()
    config.read('/Users/troysmith/Code/AlgorithmicTradingBots/config/config.ini')
    my_email = config['config']['my_email']
    my_email_pw = config['config']['my_email_pw']

    def __init__(self):
        pass

    def EmailTradeDetails(self, trade_details):
        fromaddr = my_email
        toaddr = "troywsmith2016+trading@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        msg['Subject'] = 'Trade Details'
        body = '''
        
        Trade Details: 
        Date: 
        Time: 

        Instrument:
        Units: 
        
        '''

        msg.attach(MIMEText(body, 'plain'))
        # attachment = open(filename, "rb")
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload((attachment).read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition',
        #                 "attachment; filename= %s" % filename)
        # msg.attach(part)
        server.login(fromaddr, my_email_pw)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
