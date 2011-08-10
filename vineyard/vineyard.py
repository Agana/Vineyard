DATAPORT = '/dev/ttyUSB0'
CONTROLPORT = '/dev/ttyUSB3'

from simplesms import Handler
import re
import urllib2

class Vineyard(Handler):
    def __init__(self, gateway):
       Handler.__init__(self, gateway)
       
    def handle_sms(self, message):
        print 'We have received message from %s that says [%s]' % \
        (message.sender, message.text)
        rec_text = message.text
        phrase_pastor = re.findall(r'^pastor', rec_text, re.IGNORECASE)
        phrase_prayer = re.findall(r'^prayer', rec_text, re.IGNORECASE)
        phrase_bible = re.match(r'^\w+\s\d+:\d+', rec_text, re.IGNORECASE)
        if phrase_pastor:
            text = "A pastor will be in touch shortly"
        elif phrase_prayer:
            text = "Thank you for reaching us. The Lord hears \n",
            "his children"
        elif phrase_bible:
            my_text = rec_text.strip()
            raw_book = my_text.split()[0]
            book = raw_book.lower()
            chapter_verse = my_text.split()[1]
            chapter = chapter_verse.split(':')[0]
            verse = chapter_verse.split(':')[1]
            print book, chapter, verse
            webpage = urllib2.urlopen('http://bible.cc/'+book+'/'+chapter+'-'+verse+'.htm').read()
            stuffToSearch = ""
            for line in webpage:
                stuffToSearch += line
            search_for = re.compile(r'<a href="http://kingjbible.com/'+book+'/'+chapter+'.htm">King James Bible</a></span><br>(.*)<p><span class="versiontext"><a href="http://kjv.us/'+book+'/'+chapter+'.htm">')
            search_it = re.search(search_for, stuffToSearch)
            text = (search_it.group(1))
            print text
            
        else:
            text = "Thanks for getting in touch"
        
        self.send(message.sender, text)
        
        

            
    def handle_call(self, message, caller, dt):
        print 'We received a call from %s at %s' % (caller, dt)
        number = caller
        text = "Thanks for the call, pastor john on %s" % \
        (caller)
        
        phrase = re.findall(r'pastor', text)
        if phrase:
            print 'yay'
        else:
            print 'nay'
        self.send(number, text)

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
