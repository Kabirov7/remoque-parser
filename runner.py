from send_mail import send_mess
from parser_kijiji import remorque

def run_parser():
    telegi = remorque()
    telegi.main()

    messages = send_mess()
    messages.output()

run_parser()