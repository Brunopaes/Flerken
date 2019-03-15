from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import datetime
import requests
import smtplib
import time


class Scraper:
    def __init__(self):
        self.url = 'https://www.ingresso.com/sao-paulo/home/filmes/vingadores-ultimato'
        self.sess = requests.Session()

    # Used in main
    def accessing_page(self):
        return self.sess.get(self.url)

    # Used in main
    @staticmethod
    def soup(html):
        if html.status_code == 200:
            open('../data/log_all.txt', 'a').write('Scraped information at {}\n'.format(datetime.datetime.today()))
            return BeautifulSoup(html.content, 'html.parser')

        else:
            while True:
                if html.content == 200:
                    break
                else:
                    open('../data/log_error.txt', 'a').write('Error Code: {} at {}\n'.format(html.status_code,
                                                                                             datetime.datetime.today()))

    def main(self):
        return self.soup(self.accessing_page())


class SendMail(object):
    def __init__(self):
        self.email = 'brunopaes05@gmail.com'
        self.password = 'eulpecyaaazekfot'
        self.server = 'smtp.gmail.com'
        self.port = 587

        self.recipients = open('../data/recipients.txt').read()

        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.login(self.email, self.password)
        self.session = session

    def send_message(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Avengers: End Game"
        message["From"] = self.email
        message["To"] = self.recipients

        message.attach(MIMEText('The Avengers: End game pre-release sales has started!!\n'
                                'You can find the available tickets at: '
                                'https://www.ingresso.com/sao-paulo/home/filmes/vingadores-ultimato\n\n'
                                'Please, certify yourself to warn "Flerken" group (your friends).\n\n'
                                '------------------------\n'
                                'Best Regards, Flerken - The Bot'))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, message['To'].split(','), message.as_string())


if __name__ == '__main__':
    while True:
        try:
            msg = Scraper().main().find('strong', attrs={'class': 'tit3 d-block m-b-1'}).text

        except Exception:
            SendMail().send_message()
            break

        time.sleep(5)
    SendMail().send_message()
