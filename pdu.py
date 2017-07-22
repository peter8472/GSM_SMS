"""read pdu sms format and return timestamp at least... probably more stuff"""
import sys
import pdb
import time
import re
import binascii
import StringIO
import gsm7
test_message = []
# sorry.. these were private.  append your own text messages instead
"""
bitoff	hshift	lshift
1	0	N/A
2	<<1	>>7
3	<<2	>>6
4	<<3	>>5
5	<<4	>>4
"""
def semi_octet_decode(semi):
    newp = []
    pairs = re.findall("..", semi)
    newp = [i[::-1] for i in pairs]
    return "".join(newp)

    
    

class Sms(object):
    def __init__(self,source):
        self.source = source
        self.gsm7 = gsm7.Gsm7()
    def bit_offset(self,septet):
        return septet % 8 + 1
    def byte_offset(self, septet):
        return septet - septet / 8

    def seven_from_eight(self):
        """grab and code message.  This is not easy.   the high bit of
septet 1 is offset by 1

"""

        bitstring = ""
        outstring = ""
        bitlen = self.message_len * 7
        if bitlen % 8 > 0:
            add_byte = True
        bytelen = bitlen / 8
        if add_byte:
            bytelen += 1
        messstring = self.source.read(bytelen*2)
        byteray = [int(i, 16) for i in re.findall("..", messstring)]
        print "ray len is %d" % (len(byteray))
        for x in xrange(0, self.message_len):
            char = byteray[self.byte_offset(x)]
            if self.bit_offset(x) > 1:
                char = char << (self.bit_offset(x) -1)
                low_bits = byteray[self.byte_offset(x) -1] >> (9- self.bit_offset(x))
                char = char | low_bits
            elif self.bit_offset == 0:
                char = char >> 1
            
            char = char &~ (-1<< 7) # mask high bit always
            print  hex(char)
            gsm_char = self.gsm7.look(char)
            outstring = outstring + gsm_char
        return outstring

    def get_message(self):
        answer = self.seven_from_eight()
        print len(answer)
        print answer
        
    def get_ts(self):
        year = self.source.read(2)[::-1]
        month = self.source.read(2)[::-1]
        day = self.source.read(2)[::-1]
        hour = self.source.read(2)[::-1]
        minute = self.source.read(2)[::-1]
        second = self.source.read(2)[::-1]
        tz = self.source.read(2)[::-1]
        return "20%s/%s/%s %s:%s:%s %s" % (year, month,day,hour,minute,second,tz)

        

        
    def read_pdu(self):
        smsclen = self.source.read(2)
        self.smsclen =  int(smsclen, 16)
        
        self.addrtype = self.source.read(2)
        self.smsc = self.source.read(self.smsclen* 2-2) # hex-octets are 2 bytes each
        
        self.smsc_phone =semi_octet_decode(self.smsc) #smsc phone number, plus trailing "F"
        self.tpdu_flags = self.source.read(2)
        
        sender_len = ord(binascii.unhexlify(self.source.read(2)))
        
        self.sender_addrtype = self.source.read(2)
        if sender_len % 2 == 1:
            sender_len=sender_len + 1
        sender = self.source.read(sender_len)
        
        
        self.sender_addr = semi_octet_decode(sender)
        self.protocol_id = self.source.read(2)
        self.data_encoding = self.source.read(2)
        print "data encoding: %s" % (self.data_encoding)
        tmp = self.get_ts()
        self.timestamp = tmp
        self.message_len = int(self.source.read(2), 16)
        print "raw mess len %d" % (self.message_len)
        self.message = self.get_message()
        
        
    
    
if __name__ == "__main__":
    thefile = r"c:\users\pmg\my cubby\text_messages\text_backup1.txt"
    f  = open(thefile)
    f = test_message
    for g in f:
        if len(g) > 3 and g[0].isdigit():
            mysm = Sms(StringIO.StringIO(g))
            print mysm.read_pdu()
            for i in xrange(0,20):
                numlist = [i,mysm.bit_offset(i),mysm.byte_offset(i)]
                if numlist[1] > 1:
                    numlist.append("low bits at %d" % (numlist[2] -1))
                print numlist


    
