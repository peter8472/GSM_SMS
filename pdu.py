"""read pdu sms format and return timestamp at least... probably more stuff"""
import sys
import pdb
import time
import re
import binascii
import StringIO
import gsm7
test_message = []
#test_message.append("0004038127F400006090506134736F9BD9775D0E1287D961F7B80C4ACF41EEF71D1483D962A076DA5DA797E720942006B3B962B5940B149C83C2A0E39B4D0649CBF7B09C3C078DEB73FABB5D9683F2EF3A485E1E97D3F63228562B81DA6F7919D44EBBEBF4F21CF47683C26C36485E36A7D9EC39C804CABFEB7250DD5D9F97C9A076DA5DA797E72076784E07854177F49B5D06E5CB61B90B")
#test_message.append("07911326040000F0040B911346610089F60000208062917314080CC8F71D14969741F977FD07")
#test_message.append("07914150740250F5040B915102446018F300005111701270730006C3309BDD2E03")
#test_message.append("07912160130320F8040B915150899057F300005160426154036F6E5076393C2F83CE653A081E1EAFC3E732284C07B5DFED3908FDAECFCBA0B09B0CA287D76550DA3D4F93CB2010080482B2CBE17919442FE3E9A07619F49683CAED709A0D9ABF4149D0DAFDBE83F2EF3AE8FCA683DAE5F93C7C2E83405474D8BD9E03")
#test_message.append("07912160130300F404038127F400009040607193256F9BD9775D0E1287D961F7B80C4ACF41EEF71D1483C172A076DA5DA797E72094200683B972B1940B149C83C2A0E39B4D0649CBF7B09C3C078DEB73FABB5D9683F2EF3A485E1E97D3F63228562B81DA6F7919D44EBBEBF4F21CF47683C26C36485E36A7D9EC39C804CABFEB7250DD5D9F97C9A076DA5DA797E72076784E07854177F49B5D06E5CB61B90B")
#test_message.append("0581540510F104038154F600110190026171606F704679B90CA2B69A6F719A5D0635E7671D485083B96030103A3C0789CB6537284C2697C920FA1B947FD7E5A0F078FCAEBBE92E50F65D9783DCE53B481C6687DDE332283D07D16C35503BEDAED3CB7317888A0EBBD77390F92D07C9CBE6349B9D769F43")
test_message.append("0581540510F104038154F600112150138040216F704679B90CA2B69A6F719A5D0635E7671D483083B96030103A3C0789CB6537284C2697C920FA1B947FD7E5A0F078FCAEBBE92E50F65D9783DCE53B481C6687DDE332283D07CD6431503BEDAED3CB7317888A0EBBD77390F92D07C9CBE6349B9D769F43")

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
        add_byte = False
        bitlen = self.message_len * 7
        if bitlen % 8 > 0:
            add_byte = True
        bytelen = bitlen / 8
        if add_byte:
            bytelen += 1
        messstring = self.source.read(bytelen*2)
        byteray = [int(i, 16) for i in re.findall("..", messstring)]
        #print "ray len is %d" % (len(byteray))
        for x in xrange(0, self.message_len):
            offset = self.byte_offset(x)
            if len(byteray) == offset: #last char in row is 8 bits offset
                char = 0
            else:
                char = byteray[offset]
            if self.bit_offset(x) > 1:
                char = char << (self.bit_offset(x) -1)
                low_bits = byteray[self.byte_offset(x) -1] >> (9- self.bit_offset(x))
                char = char | low_bits
            elif self.bit_offset == 0:
                char = char >> 1
            
            char = char &~ (-1<< 7) # mask high bit always
            #print  hex(char)
            gsm_char = self.gsm7.look(char)
            outstring = outstring + gsm_char
        return outstring

    def get_message(self):
        self.answer = self.seven_from_eight()
        #print len(self.answer)
        print self.timestamp
        print self.answer
       
    
       
        
    def handle_dcs(self):
        if self.dcs == 0:
            raise Exception("handle_dcs called bbut dcs = 0!")
        self.cg = self.dcs >> 4
        if (self.cg & 0b1100) !=0:
            raise Exception("high bits in DCS CG, not handled")
        elif (self.cg & 0b0010) != 0:
            raise Exception("GSM standard compression not handled!")
        elif (self.cg & 0b0001) != 0: # message class in bits 3..0
            self.low_bits = self.dcs & 0b1111
            #print "low bits: %x" %(self.low_bits)
            

        else:
            exit(1)
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
        if self.smsclen > 0:
            self.addrtype = self.source.read(2)
            self.smsc = self.source.read(self.smsclen* 2-2) # hex-octets are 2 bytes each
            
            self.smsc_phone =semi_octet_decode(self.smsc) #smsc phone number, plus trailing "F"
# this is the end of the smcc header, and the beginning of the real pdu

        self.tpdu_flags = self.source.read(2)
        
        tmp = self.source.read(2)
        sender_len = ord(binascii.unhexlify(tmp))
        
        self.sender_addrtype = self.source.read(2)
        if sender_len % 2 == 1:
            sender_len=sender_len + 1
        sender = self.source.read(sender_len)
        
        
        self.sender_addr = semi_octet_decode(sender)
        self.protocol_id = self.source.read(2)
        self.dcs = int(self.source.read(2), 16)
        #print "data encoding: %x" % (self.dcs)
        if self.dcs != 0:
            self.handle_dcs()
            
            
            
            
        tmp = self.get_ts()
        self.timestamp = tmp
        self.message_len = int(self.source.read(2), 16)
        #print "raw mess len %d" % (self.message_len)
        
        "fix detection of sent merssages"
        self.message = self.get_message()
        
        
    
    
if __name__ == "__main__":
    thefile = r"c:\users\pmg\onedrive\my cubby\phone\text_messages\text_backup3.txt"
    f  = open(thefile)
    f = test_message
    num = 0
    for g in f:
	print "translating: %s" % (g)
        if len(g) > 3 and g[0].isdigit():
            mysm = Sms(StringIO.StringIO(g))
            print mysm.read_pdu()
            for i in xrange(0,20):
                numlist = [i,mysm.bit_offset(i),mysm.byte_offset(i)]
                if numlist[1] > 1:
                    numlist.append("low bits at %d" % (numlist[2] -1))