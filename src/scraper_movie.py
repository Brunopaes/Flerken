from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import datetime
import requests
import smtplib
import time


class Scraper:
    def __init__(self):
        self.url = [
            'https://www.ingresso.com/sao-paulo/home/busca/resultado?q=vingadores',
            'https://www.ingresso.com/sao-paulo/home/filmes/vingadores-ultimato'
        ]
        self.sess = requests.Session()
        self.content_list = []

    # Used in main
    def accessing_page(self, index):
        return self.sess.get(index)

    # Used in main
    @staticmethod
    def soup(html, page):
        if html.status_code == 200:
            open('../data/log_all.txt', 'a').write('Scraped information at {}, time {}\n'.format(page, datetime.datetime.today()))
            return BeautifulSoup(html.content, 'html.parser')

        else:
            while True:
                if html.content == 200:
                    break
                else:
                    open('../data/log_error.txt', 'a').write('Error Code: {} at {}\n'.format(html.status_code,
                                                                                             datetime.datetime.today()))

    def main(self):
        for page in self.url:
            self.content_list.append(self.soup(self.accessing_page(page), page))

        return self.content_list


class SendMail:
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


class Main:
    def __init__(self):
        self.session = 'Não encontramos nenhuma sessão :('
        self.avengers = 'Vingadores: Ultimato'
        self.is_playing = 'Fora de Cartaz'

    def get_avengers(self, html):
        avengers_html = html.find_all('li', attrs={
            'class': 'ml-it col-xs-12 col-lg-6'
        })

        for i in range(len(avengers_html)):
            if self.avengers in str(avengers_html[i]):
                return self.is_playing not in str(avengers_html[i])

            else:
                pass

    def get_ultimato(self, html):
        try:
            if html.find('strong', attrs={'class': 'tit3 d-block m-b-1'}).text == self.session:
                return False

        except Exception:
            return True

    def __call__(self, *args, **kwargs):
        while True:
            all_avengers = self.get_avengers(Scraper().main()[0])
            ultimato = self.get_ultimato(Scraper().main()[1])

            open('../data/log_boolean.txt', 'a').write('all_avengers: {}, ultimato: {}\n'.format(all_avengers, ultimato))

            if all_avengers is True and ultimato is True:
                SendMail().send_message()
                open('../data/log_mail.txt', 'a').write('email sent at {}'.format(datetime.datetime.today()))
                open('../data/log_release.txt', 'a').write('By the time {} the movie has been released\n'.format(
                    datetime.datetime.today()
                ))
                break

            else:
                open('../data/log_release.txt', 'a').write('By the time {} the movie has not been released\n'.format(
                    datetime.datetime.today()
                ))

            time.sleep(30)


if __name__ == '__main__':
    Main().__call__()
