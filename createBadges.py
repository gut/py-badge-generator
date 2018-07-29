#!/usr/bin/env python3
#
# This software is licensed under the MIT License
#
# The MIT License
# 
# Copyright (c) 2007 Siddharta Govindaraj. All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

import os,sys,re
import inspect
from colors import *
from subprocess import call

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except:
    try:
        import Image
        import ImageDraw
        import ImageFont
    except:
        print("Install PIL or Pillow please")
        sys.exit(1)

class BadgeImage(object):
    def __init__(self, filename):
        self.debug = False
        self.img = Image.open(filename)
        self.draw = ImageDraw.Draw(self.img)
        self.width = int(self.img.size[0]*0.9)
        self.ttfFontDir = "fonts"
        self.ttfFont = os.path.join(self.ttfFontDir, "Trebucbd.ttf")

        self.helloLang = {'en':'HELLO my name is',
                          'de':'HALLO mein Name ist',
                          'fr':'SALUT mon nom est',
                          'lu':'MOIEN mäi Numm ass'}
        self.iAmLang   = {'en':"and I'm a ",
                          'de':'und ich bin ',
                          'fr':'et je suis ',
                          'lu':'an ech sinn '}

        self.colorSeperator = "#" + triplet(BLACK)
        self.textColorCompany = "#" + "0099ff"
        self.textColorPerson = "#" + triplet(BLACK)
        self.textColorSoi = "#" + triplet(BLACK)
        self.textColorHello = "#" + triplet(BLACK)
        self.textColorColor = "#" + triplet(BLACK)

    def reColor(self,color, srcFile, dstFile):
        call(["/usr/local/bin/convert", "images/badgeTemplate_bw.png", "+level-colors", color + ",white", srcFile, "-compose", "over", "-composite", dstFile])

    def drawAlignedText(self, pos, text, font_color, xtransform, ytransform):
        (font, color) = font_color
        width,height = font.getsize(text)
        xpos = xtransform(pos[0], width)
        ypos = ytransform(pos[1], height)
        if inspect.stack()[1][3] and self.debug == "drawRightAlignedText":
            print(xpos,ypos)
        self.draw.text((xpos, ypos), text, fill=color, font=font)

    def drawCenteredText(self, pos, text, font):
        self.drawAlignedText(pos, text, font, lambda x,w:x-w/2, lambda y,h:y-h/2)

    def drawLeftAlignedText(self, pos, text, font):
        self.drawAlignedText(pos, text, font, lambda x,w:x, lambda y,h:y-h)

    def drawRightAlignedText(self, pos, text, font):
        self.drawAlignedText(pos, text, font, lambda x,w:w+x, lambda y,h:y-h)

    def getFitSize(self, startsize, text):
        size = startsize
        font = ImageFont.truetype(self.ttfFont, int(size*300/72))
        textwidth, textheight = font.getsize(text)
        while textwidth > self.width:
            size -= 1
            font = ImageFont.truetype(self.ttfFont, int(size*300/72))
            textwidth, textheight = font.getsize(text)
        return size

    def drawPerson(self, name):
        linepos = (self.img.size[0]/2, self.img.size[1]/2)
        line1pos = (self.img.size[0]/2, 300)
        line2pos = (self.img.size[0]/2, int(self.img.size[1]/1.7))
        size = self.getFitSize(45, name)
        if name.find(" ") >= 0:
            firstname, rest = name.split(" ", 1)
        else:
            firstname, rest = (name, "")
        if size < 45 and rest != "":
            personFont = ImageFont.truetype(self.ttfFont, int(self.getFitSize(45, firstname)*300/72))
            self.drawCenteredText(line1pos, firstname, (personFont, self.textColorPerson))
            personFont = ImageFont.truetype(self.ttfFont, int(self.getFitSize(45, rest)*300/72))
            self.drawCenteredText(line2pos, rest, (personFont, self.textColorPerson))
        else:
            personFont = ImageFont.truetype(self.ttfFont, int(self.getFitSize(45, name)*300/72))
            self.drawCenteredText(linepos, name, (personFont, self.textColorPerson))

    def drawHello(self, language):
        pos = (30, 100)
        if self.debug:
            print(pos)
        font = ImageFont.truetype(self.ttfFont, int(self.getFitSize(26, name)*300/72))
        if language == "en":
            hello, rest = self.helloLang["en"].split(" ",1)
            width,height = font.getsize(hello)
        elif language == "de":
            hello, rest = self.helloLang["de"].split(" ",1)
            width,height = font.getsize(hello)
        elif language == "fr":
            hello, rest = self.helloLang["fr"].split(" ",1)
            width,height = font.getsize(rest)
        elif language == "lu":
            hello, rest = self.helloLang["lu"].split(" ",1)
            width,height = font.getsize(hello)
        else:
            print("No language detected!")
            sys.exit(2)

        self.drawLeftAlignedText(pos, hello, (font, self.textColorHello))
        self.drawLeftAlignedText( (pos[0],pos[1]+height+int((height/2)) ), rest, (font, self.textColorHello) )

    def drawSoi(self, language, what):
        pos = (self.img.size[0]/2, 700)
        font = ImageFont.truetype(self.ttfFont, int(self.getFitSize(26, name)*300/72))
        if language == "en":
            iAm = self.iAmLang["en"] + what + "!"
            width,height = font.getsize(iAm)
        if language == "de":
            iAm = self.iAmLang["de"] + what + "!"
            width,height = font.getsize(iAm)
        if language == "fr":
            iAm = self.iAmLang["fr"] + what + "!"
            offset = 10
            width,height = font.getsize(iAm)
            #pos[1] += offset
        if language == "lu":
            iAm = self.iAmLang["lu"] + what + "!"
            width,height = font.getsize(iAm)
        self.drawRightAlignedText((pos[0]-(width*1.3),pos[1]), iAm, (font, self.textColorSoi))

    def drawColor(self, color):
        pos = (self.img.size[0]/2, 700)
        font = ImageFont.truetype(self.ttfFont, int(self.getFitSize(26, name)*300/72))
        width,height = font.getsize(color)
        self.drawLeftAlignedText((pos[0]+200,height-10), color, (font, self.textColorColor))

    def drawCompany(self, name):
        pos = (self.img.size[0]/2, 700)
        font = ImageFont.truetype(self.ttfFont, int(self.getFitSize(26, name)*300/72))
        self.drawCenteredText(pos, name, (font, self.textColorCompany))

    def save(self, filename, doubleSided=True):
        if not doubleSided:
            self.img.save(filename)
            return

        newimg = Image.new("RGB", (self.img.size[0]*2+20, self.img.size[1]), self.colorSeperator)
        newimg.paste(self.img, (0,0))
        newimg.paste(self.img, (self.img.size[0]+20,0))
        newimg.save(filename)

class DataFileReader(object):
    def __init__(self, filename):
        fp = open(filename)
        self.lines = [line[:-1] for line in fp.readlines()]
        fp.close()

    def getData(self):
        for id, line in enumerate(self.lines):
            if re.search('^#', line):
                continue
            if len(line.strip()) != 0:
                name,company,language = line.split("\t")
                name = name.title()
            if not company.startswith("*"):
                company = company.title()
            else:
                company = company[1:]
            yield (id, name.title(), company, language)


if len(sys.argv) > 1:
    filenames = sys.argv[1:]
else:
    filenames = ["people"]

count = 0
for filename in filenames:
    reader = DataFileReader(filename + ".csv")
    if not os.path.exists(filename):
        os.makedirs(filename)
    colorList = []
    colorList = [ "RED", "ORANGE", "BLUE", "YELLOW", "GREEN", "CYAN", "PURPLE", "BROWN", "GRAY", "PINK", "VIOLET", "WHITE" ]
    for id, name, company,language in reader.getData():
        for color in colorList:
            print("Badge ID: {} - Name: {} - What: {} - Color: http://www.colorhexa.com/{}".format(id, name, company, triplet(eval(color))))
            badgeTemplate = "images/badgeTemplate_overlay.png"
            badge = BadgeImage(badgeTemplate)
            confBadge = {'LANG': language,
                        'color': "#" + triplet(eval(color)),
                         'what': company}
            badge.drawHello(confBadge["LANG"])
            badge.drawColor(confBadge["color"].upper())
            badge.drawPerson(name)
            badge.drawSoi(confBadge["LANG"],confBadge["what"])
            badge.save(os.path.join(filename, filename + "_badge_" + str(id) + "_" + confBadge["LANG"] + ".png"), False)
            if badge.debug:
                print(filename + "_badge_" + str(id) + "_" + confBadge["LANG"] + ".png")
            badge.reColor(color,  os.path.join(filename, filename + "_badge_" + str(id) + "_" +  confBadge["LANG"] + ".png"), os.path.join(filename, filename + "_badge_" + str(id) + "_" + confBadge["LANG"] + "_" + confBadge["color"][1:] + ".png"))
        count += 1
print("\n%d badges created" % (count))
