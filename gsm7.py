#! /usr/bin/python
import csv
import pdb
"""This package looks up gsm7 special alphabet
https://en.wikipedia.org/wiki/GSM_03.38
https://en.wikipedia.org/wiki/GSM_03.40#Message_Content
http://www.smartposition.nl/resources/sms_pdu.html
http://www.canarysystems.com/nsupport/CDMA_AT_Commands.pdf
bit format is here:
http://www.etsi.org/deliver/etsi_ts/100900_100999/100900/07.02.00_60/ts_100900v070200p.pdf


"""
alpha = {}    
class Gsm7(object):
    def __init__(self):
        self.alpha = {}
        with open("gsm.csv") as f:
            j = csv.reader(f)
            for i in j:
                self.alpha[int(i[0], 16)] = i[1]

    def write_all(self):
        f = open("gsm.csv", 'a')
        j = csv.writer(f)
        sorted = self.alpha.keys()
        sorted.sort()
        for a in sorted:
            
            j.writerow(["{0:#x}".format(a), self.alpha[a]])
            print ["{0:#x}".format(a), self.alpha[a]]
        f.close()

    def look(self,codepoint):
        if self.alpha.has_key(codepoint):
            return self.alpha[codepoint]
        else:
            self.alpha[codepoint] = ""
            print "in OOKUP"
            f = open("gsm.csv", 'a')
            f.write("{0:#x},\n".format(codepoint))
            f.close()
            return "?"


def blah():
    f = open("gsm.csv", 'w')
    j = csv.writer(f)
    for a in alpha:
        j.writerow(["{0:#x}".format(a), alpha[a]])
    f.close()

def sp(number):
    print "{0:0x} {0:08b}".format(number)

if __name__ == "__main__":
    tstr = [0x44,0x65,0x73,0x69, 0x67, 0x6e,0x00,0x48,0x6f,0x6d,0x65]
    #let's pack that... okay...
    
    tmp = tstr[0]
    sp(tmp)
    tmp = tmp << 1
    sp(tmp)
    tmp = tmp | tstr[1] >> 7
    sp(tmp)
    
