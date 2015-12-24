

### The only things you'll have to edit (unless you're porting this script over to a different language) 
### are at the bottom of this file.

import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
  def write(self, s):
    pass

def submit():   
  print '==\n== [sandbox] Submitting Solutions \n=='
  
  (login, password) = loginPrompt()
  if not login:
    print '!! Submission Cancelled'
    return
  
  print '\n== Connecting to Coursera ... '

  # Part Identifier
  (partIdx, sid) = partPrompt()

  # Get Challenge
  (login, ch, state, ch_aux) = getChallenge(login, sid) #sid is the "part identifier"
  if((not login) or (not ch) or (not state)):
    # Some error occured, error string in first return element.
    print '\n!! Error: %s\n' % login
    return

  # Attempt Submission with Challenge
  ch_resp = challengeResponse(login, password, ch)
  (result, string) = submitSolution(login, ch_resp, sid, output(partIdx), \
                                  source(partIdx), state, ch_aux)

  print '== %s' % string.strip()


# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  (login, password) = basicPrompt()
  return login, password


def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  login = raw_input('Login (Email address): ')
  password = raw_input('One-time Password (from the assignment page. This is NOT your own account\'s password): ')
  return login, password

def partPrompt():
  print 'Hello! These are the assignment parts that you can submit:'
  counter = 0
  for part in partFriendlyNames:
    counter += 1
    print str(counter) + ') ' + partFriendlyNames[counter - 1]
  partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
  return (partIdx, partIds[partIdx])

def getChallenge(email, sid):
  """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
  url = challenge_url()
  values = {'email_address' : email, 'assignment_part_sid' : sid, 'response_encoding' : 'delim'}
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  text = response.read().strip()

  # text is of the form email|ch|signature
  splits = text.split('|')
  if(len(splits) != 9):
    print 'Badly formatted challenge response: %s' % text
    return None
  return (splits[2], splits[4], splits[6], splits[8])

def challengeResponse(email, passwd, challenge):
  sha1 = hashlib.sha1()
  sha1.update("".join([challenge, passwd])) # hash the first elements
  digest = sha1.hexdigest()
  strAnswer = ''
  for i in range(0, len(digest)):
    strAnswer = strAnswer + digest[i]
  return strAnswer 
  
def challenge_url():
  """Returns the challenge url."""
  return "https://class.coursera.org/" + URL + "/assignment/challenge"

def submit_url():
  """Returns the submission url."""
  return "https://class.coursera.org/" + URL + "/assignment/submit"

def submitSolution(email_address, ch_resp, sid, output, source, state, ch_aux):
  """Submits a solution to the server. Returns (result, string)."""
  source_64_msg = email.message.Message()
  source_64_msg.set_payload(source)
  email.encoders.encode_base64(source_64_msg)

  output_64_msg = email.message.Message()
  output_64_msg.set_payload(output)
  email.encoders.encode_base64(output_64_msg)
  values = { 'assignment_part_sid' : sid, \
             'email_address' : email_address, \
             'submission' : output_64_msg.get_payload(), \
             'submission_aux' : source_64_msg.get_payload(), \
             'challenge_response' : ch_resp, \
             'state' : state \
           }
  url = submit_url()  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  string = response.read().strip()
  result = 0
  return result, string

## This collects the source code (just for logging purposes) 
def source(partIdx):
  # open the file, get all lines
  f = open(sourceFiles[partIdx])
  src = f.read() 
  f.close()
  return src



############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

from scipy.io import wavfile
import numpy as np

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'dsp-006'

# the "Identifier" you used when creating the part
partIds = ['ScaledFFTdB','PrototypeFilter',
           'SubbandFiltering','Quantization']
# used to generate readable run-time information for students
partFriendlyNames = ['Scaled FFT [dB]','Prototype Filter Design',
                     'Subband Filtering','Quantization']
# source files to collect (just for our records)
sourceFiles = ['assignment1.py','assignment2.py','assignment3.py','assignment4.py']

def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = ''

  if partIdx == 0: # This is ScaledFFTdB

    from assignment1 import scaled_fft_db

    r,x = wavfile.read('data/a1_submissionInput.wav')
    X = scaled_fft_db(x)

    for val in X:
        outputString += '%.5f ' % (val)


  elif partIdx == 1: # This is PrototypeFilter

    from assignment2 import prototype_filter

    h = prototype_filter()
      
    # test signal
    s = np.loadtxt('data/a2_submissionInput.txt')
    r = np.convolve(h, s)[4*512:5*512]/2

    for val in r:
        outputString += '%.5f ' % val

  elif partIdx == 2: # This is SubbandFiltering

    from assignment3 import subband_filtering

    r,x = wavfile.read('data/a3_submissionInput.wav')

    h = np.hanning(512)
    X = subband_filtering(x, h)

    for val in X:
        outputString += '%.5f ' % (val)

  elif partIdx == 3: # This is Quantization

    from assignment4 import quantization

    from parameters import EncoderParameters
    params = EncoderParameters(44100, 2, 64)

    val_in = np.loadtxt('data/a4_submissionInput.txt')

    for r,row in enumerate(val_in):
        val = row[0]
        scf = row[1]
        ba = int(row[2])
        QCa = params.table.qca[ba-2]
        QCb = params.table.qcb[ba-2]
        val = quantization(val, scf, ba, QCa, QCb)
        outputString += '%d ' % (val)


  return outputString.strip()

submit()
