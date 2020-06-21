import mysql.connector
import smtplib
import config as const


class send_mess():
    def __init__(self):
        self.DATABASE = mysql.connector.connect(host='localhost', user='root', password='1234', database='remoque', auth_plugin='mysql_native_password')
        self.MY_CURSOR = self.DATABASE.cursor(buffered=True)
        self.server = ''
        self.table_name = ''
        self.count = ''

    def change_const(self):
        self.table_name = 'remorque'
        self.FROM = const.FROM
        self.TO = const.TO
        self.MAIL_PASSWORD = const.MAIL_PASSWORD

    def send_message(self, messages):
        with smtplib.SMTP('smtp.gmail.com', 587) as self.smtp:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()

            self.smtp.login(self.FROM, self.MAIL_PASSWORD)

            for self.i in messages:
                self.subject = 'New Remoques '
                self.body = self.msg =f'link: {self.i["link"]}\n' \
                                      f'price: {self.i["price"]}'



                self.msg = f'Subject: {self.subject}\n\n{self.body}'

                self.smtp.sendmail(self.FROM, self.TO, self.msg)

    def output(self):
        self.change_const()
        self.MY_CURSOR.execute(f"select * from {self.table_name} where new_=true")
        self.row = self.MY_CURSOR.fetchall()
        self.messages = []
        for self.i in range(len(self.row)):
            self.message = ({
                # f"title": self.row[self.i][1],
                #              f"description": self.row[self.i][4],
                             f"price": self.row[self.i][3],
                             f"link": self.row[self.i][5]})
            self.messages.append(self.message)
        self.send_message(self.messages)




