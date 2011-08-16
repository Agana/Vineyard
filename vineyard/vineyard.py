# Vineyard - Tending the flock with mobile technology
# Agana Agana-Nsiire, for The Truth for Free Media Ministry
# Bible verses obtained from bible.cc

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
        
#       These are what to look for in a received message
        
#       Request for a pastor's contact
        phrase_pastor = re.match(r'^pastor\s\w+\s\w+.', rec_text, re.IGNORECASE)
#       Prayer request
        phrase_prayer = re.match(r'^prayer.', rec_text, re.IGNORECASE)
#       Bible verse query
        phrase_bible = re.match(r'^\w+\s\d+:\d+', rec_text, re.IGNORECASE)
        phrase_bible_1_2 = re.match(r'^\d+\s\w+\s\d+:\d+', rec_text, re.IGNORECASE)
#       Bible verse explanation request
        phrase_bible_explain = re.match(r'^explain\s\w+\s\d+:\d+', rec_text, re.IGNORECASE)
#       Song request
        phrase_hymn = re.match(r'^hymn|sdah\s\d+.', rec_text, re.IGNORECASE)
        
#       This handles requests for pastors' contacts
        
        if phrase_pastor:
#       TODO: create a webpage with pastors' names and scrape that with regex

            name_tel = {'Emmanuel Gaizer' : '0244444444', 'Nii Lante Thompson' : '0245444545'}
            name_email = {'Emmanuel Gaizer' : 'egaizer@yahoo.com', 'Nii Lante Thompson' : 'niilantethompson@yahoo.com'}
            name_tel.items()
            pastor_call = rec_text.split()[0]
            pastor_name = " ".join(rec_text.split()[1:])
            print pastor_name
            if pastor_name in name_tel:
                pastor_send = pastor_name + " " + name_tel[pastor_name] + " " + name_email[pastor_name]
                text = pastor_send
                print text
                self.send(message.sender, text)
            else:
                text = "Sorry, we don't have this contact. Our list is growing, do check back soon"
                print text
                self.send(message.sender, text)

#       This handles requests for prayer
        elif phrase_prayer:
            text = "A prayer support partner will contact you shortly,"
            +message.sender+"Remember: Blessed is he whose help is the God \n",
            "of Jacob,whose hope is in the LORD his God, who made heaven and \n",
            "earth, the sea, and all that is in them, who keeps faith forever;\n",
            "- Psalm 146:5,6"
            print text
            self.send(message.sender, text)
            
#       This handles requests for Bible verses
        elif phrase_bible:
            my_text = rec_text.strip()
            raw_book, chapter_verse = my_text.split()
            book = raw_book.lower()
            chapter, verse = chapter_verse.split(':')

            print book, chapter, verse
            
            webpage = urllib2.urlopen('http://bible.cc/'+book+'/'+chapter+'-'+verse+'.htm').read()
            stuffToSearch = "".join(webpage)
            search_for = r'<a href="http://kingjbible.com/'+book+'/'+chapter+'.htm">King James Bible</a></span><br>(.*)<p><span class="versiontext"><a href="http://kjv.us/'+book+'/'+chapter+'.htm">'
            search_it = re.search(search_for, stuffToSearch)
            rawest_text = (search_it.group(1))
            
#           Sometimes King James italises words (insertions of translators)
#           This removes the <i> and </i> html tags in such texts
            raw_text = re.sub("<i>", "", rawest_text)
            text = re.sub("</i>", "", raw_text) + " " + "\n<Thanks for using TFF Vineyard! www.thetruthforfree.org/vineyard>"
            print text
            self.send(message.sender, text)
        
        elif phrase_bible_1_2:
            book_ind = rec_text.split()[0]
            book_name = rec_text.split()[1]
            chapter_verse = rec_text.split()[2]
            chapter, verse = chapter_verse.split(':')
            
            
            print book_ind, book_name, chapter, verse
            
            webpage = urllib2.urlopen('http://bible.cc/'+book_ind+'_'+book_name+'/'+chapter+'-'+verse+'.htm').read()
            stuffToSearch = "".join(webpage)
            search_for = r'<a href="http://kingjbible.com/'+book_ind+'_'+book_name+'/'+chapter+'.htm">King James Bible</a></span><br>(.*)<p><span class="versiontext"><a href="http://kjv.us/'+book_ind+'_'+book_name+'/'+chapter+'.htm">'
            search_it = re.search(search_for, stuffToSearch)
            rawest_text = (search_it.group(1))
            
#           Sometimes King James italises words (insertions of translators)
#           This removes the <i> and </i> html tags in such texts
            raw_text = re.sub("<i>", "", rawest_text)
            text = re.sub("</i>", "", raw_text) + " " + "\n<Thanks for using TFF Vineyard! www.thetruthforfree.org/vineyard>"
            print text
            self.send(message.sender, text)
       
#       This handles requests for Bible explanations
        elif phrase_bible_explain:
           book = rec_text.split()[1]
           chapter_verse = rec_text.split()[2]
           chapter, verse = chapter_verse.split(':')

#          The following comments may be implemented later
#          webpage = urllib2.urlopen('http://bible.cc/'+book+'/'+chapter+'-'+verse+'.htm').read()
#          stuffToSearch = "".join(webpage)
#          search_for = r'<a href="http://kingjbible.com/'+book+'/'+chapter+'.htm">King James Bible</a></span><br>(.*)<p><span class="versiontext"><a href="http://kjv.us/'+book+'/'+chapter+'.htm">'
#          search_it = re.search(search_for, stuffToSearch)
           my_set = book, chapter, verse
           text = "One of our staff will soon reach you with an answer to your question on " + book + " " + chapter + ":" + verse + " . Thanks for using Vineyard! www.thetruthforfree.org/vineyard"
           print text
           self.send(message.sender, text) 
#       This handles song requests (hymns for now)
        elif phrase_hymn:
            hymn_id = rec_text.split()[1]
            text = "Thanks for the request. Hymn " + hymn_id + " has been added to the queue."       
            print text
            self.send(message.sender, text)
            
        else:
#           (If the message does not qualify for any of them)
            text = "Sorry, your message is not understood. Please try again. Check for spelling and other errors. Thanks for using Vineyard! www.thetruthforfree.org"
            print text
        
            self.send(message.sender, text)
        
        
            
    def handle_call(self, message, caller, dt):
        print 'We received a call from %s at %s' % (caller, dt)
        number = caller
        text = "Thanks for the call, pastor john on %s" % \
        (caller)
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


# Messages of exhortation delivered everyday
