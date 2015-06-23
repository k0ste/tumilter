#!/usr/bin/python2

import Milter
import string
import time
import sys
from optparse import OptionParser

def main():
  parser = OptionParser()
  parser.add_option('-s', '--socket', dest='socket', help='Socket to listen (e.g. inet:8890@localhost)')
  parser.add_option('-t', '--timeout', type='int', dest='timeout', default='10', help='MTA timeout (default is 10 sec)')
  (options, args) = parser.parse_args()
  if not options.socket:
    parser.print_help()
    sys.exit(0)
    
  Milter.factory = TuMilter
  print "%s TuMilter startup" % time.strftime('%Y %b %d %H:%M:%S')
  sys.stdout.flush()
  Milter.runmilter("tumilter",options.socket,options.timeout)
  
class TuMilter(Milter.Milter):
  "Milter to limit the numer of To and Cc recipients"

  def __init__(self):
    self.tocc = 0
    self.id = Milter.uniqueID()
    self.recipients = 2

  def header(self,name,val):
    
    sv = self.getsymval('{auth_authen}')
    if sv==None or sv=="":
      return Milter.CONTINUE

    lname = name.lower()
    if lname == 'to' or lname=='cc':
      mails = string.split(val, ',')
      self.tocc=self.tocc+len(mails)

    if self.tocc >= self.recipients:
      self.setreply('550', '5.5.3', 'Sorry, your message has too many recipients')
      return Milter.REJECT
   
    return Milter.CONTINUE
    
if __name__ == "__main__":
  main()
  