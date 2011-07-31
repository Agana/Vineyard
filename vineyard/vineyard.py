DATAPORT = '/dev/ttyUSB0'
CONTROLPORT = '/dev/ttyUSB3'

from simplesms import Handler

class Vineyard(Handler):
    def __init__(self, gateway):
       Handler.__init__(self, gateway)
       
    def handle_sms(self, message):
        print 'We have received message from %s that says [%s]' % \
        (message.sender, message.text)
        

from simplesms import Modem
from simplesms import Gateway
   
def bootstrap(options = None):
    modems = connect_modems(options)
    gateway = Gateway(modems)
    return (modems, gateway)

def connect_modems(options=None):
    modem = Modem(port=DATAPORT, control_port=CONTROLPORT)
    modem.boot()
    return {'MTN':modem}
    
def main():
    modems, gateway = bootstrap()
    vineyard = Vineyard(gateway)
    gateway.start()
    
if __name__ == "__main__":
    main()
