#! /usr/bin/python
# coding=utf-8
"""Another gsm lookup class.  This one should actually work"""
b=      [u"@∆ 0¡P¿p"]
b.append(u"£_!1AQaq")
b.append(u'$Φ"2BRbr')
b.append(u"¥Γ#3CScs")
b.append(u"èΛ¤4DTdt")
b.append(u"éΩ%5EUeu")
b.append(u"ùΠ&6FVfv")
b.append(u"ìΨ'7GWgw")
b.append(u"òΣ(8HXhx")
b.append(u"ÇΘ)9IYiy")
b.append(u"\nΞ*:JZjz")
b.append(u"Ø +;KÄkä") #no character here, it's an escape
b.append(u"øÆ,<LÖlö")
b.append(u"\ræ-=MÑmñ")
b.append(u"Åß.>NÜnü")
b.append(u"åÉ/?O§oà")


class Gsm7(object):
    def __init__(self):
        pass


    def look(self, codepoint):
        row = codepoint & 0b0001111
        col = codepoint >> 4
        #print "%d:%d"% (row, col)
        if row == 11 and col == 1:
            raise Exception("gsm escape char found")
        try:
            return b[row][col]
        except IndexError(e):
            print e
            exit(1)


if __name__ == "__main__":
    mygsm = Gsm7()
    for x in range(0,3):
      print mygsm.look(x)
      print b[7][6]
