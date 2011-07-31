DATAPORT = '/dev/ttyUSB0'
CONTROLPORT = '/dev/ttyUSB3'


class Vineyard():
    def __init__(selfself, gateway):
       Handler.__init__(self, gateway)

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
    gateway.start()
    
if __name__ == "__main__":
    main()
