# -*- coding: utf-8 -*-

# based on the work from RSS Simmple by DDamir v.0.2
# This Software is Free, use it where you want
# when you want for whatever you want and modify it if you want but don't remove my copyright!
# adapted for py3 and added fhd screens @lululla 20240524
from Components.ActionMap import ActionMap, NumberActionMap
from Components.ConfigList import ConfigList
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Components.config import ConfigText
from Components.config import KEY_0, KEY_DELETE, KEY_BACKSPACE
from Components.config import KEY_LEFT, KEY_RIGHT
from Components.config import getConfigListEntry
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from enigma import eTimer
import os
import ssl
global mydatum
# global myslika
global mynaziv
global mydesc
global HALIGN

version = '0.4'
descplugx = 'RSS Simmple by DDamir v.%s\n\nadapted for py3 by @lululla 20240524\n\n' % version
inff = 'Import New from /tmp/feeds.xml'
descplug = descplugx + inff
nazrss = ConfigText(fixed_size=False, visible_width=40)
urlrss = ConfigText(fixed_size=False, visible_width=40)
ssl._create_default_https_context = ssl._create_unverified_context


def trazenje(t1, t2, t3, tekst):
    n0 = tekst.find(t1)
    n1 = tekst.find(t2)
    n2 = tekst.find(t3)
    return (n0, n1, n2)


def uzmitekst(p0, p1, tekst):
    ut = tekst[p0:p1]
    return ut


def skrati(d0, zl):
    line = zl[d0:len(zl)]
    return line


class UnesiPod(Screen):
    print('class UnesiPod(Screen):')

    def __init__(self, session):
        if os.path.exists('/var/lib/dpkg/status'):
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED" flags="wfNoBorder">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="liste" itemHeight="55" font="Regular; 36" position="920,120" size="930,770" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <!--
                            <widget source="VKeyIcon" conditional="VKeyIcon" render="Pixmap" pixmap="buttons/key_text.png" alphatest="blend" position="1812,996" size="54,34" zPosition="2">
                                <convert type="ConditionalShowHide" />
                            </widget>
                            -->
                            <widget name="pred" position="959,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget name="pgreen" position="1172,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget name="pblue" position="1584,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        </screen>'''
        else:
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED" flags="wfNoBorder">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="liste" itemHeight="55" font="Regular; 36" position="920,120" size="930,770" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <!--
                            <widget source="VKeyIcon" conditional="VKeyIcon" render="Pixmap" pixmap="buttons/key_text.png" alphatest="blend" position="1812,996" size="54,34" zPosition="2">
                                <convert type="ConditionalShowHide" />
                            </widget>
                            -->
                            <widget source="pred" render="Label" position="959,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget source="pgreen" render="Label" position="1172,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget source="pblue" render="Label" position="1584,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                             <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        </screen>'''

        Screen.__init__(self, session)
        self['actions'] = NumberActionMap(['SetupActions',
                                           'TextEntryActions',
                                           'WizardActions',
                                           'HelpActions',
                                           'MediaPlayerActions',
                                           'VirtualKeyboardActions',
                                           'ColorActions'], {'cancel': self.close,
                                                             'ok': self.Gotovo,
                                                             'left': self.keyLeft,
                                                             'right': self.keyRight,
                                                             'deleteForward': self.keyDelete,
                                                             'deleteBackward': self.keyBackspace,
                                                             'blue': self.openKeyboard,
                                                             'green': self.savem,
                                                             'showVirtualKeyboard': self.openKeyboard,
                                                             '0': self.keyNumber,
                                                             '1': self.keyNumber,
                                                             '2': self.keyNumber,
                                                             '3': self.keyNumber,
                                                             '4': self.keyNumber,
                                                             '5': self.keyNumber,
                                                             '6': self.keyNumber,
                                                             '7': self.keyNumber,
                                                             '8': self.keyNumber,
                                                             '9': self.keyNumber}, -1)
        list = []
        self['liste'] = ConfigList(list)
        list.append(getConfigListEntry('RSS name: ', nazrss))
        list.append(getConfigListEntry('URL=>http://: ', urlrss))
        # self['VKeyIcon'] = Pixmap()
        self['pblue'] = Label(_('Keyboard'))
        self['pgreen'] = Label(_('Save'))
        self['pred'] = Label(_('Close'))
        self['info'] = Label(_('Select'))
        self['opisi'] = Label(_('Setup RSS FEED v.%s' % version))
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle('RSS FEED')

    def openKeyboard(self):
        if self['liste'].getCurrent()[1] == nazrss:
            self.session.openWithCallback(self.vrationazad, VirtualKeyBoard, title='RSS name', text=nazrss.value)
        if self['liste'].getCurrent()[1] == urlrss:
            self.session.openWithCallback(self.vrationazad, VirtualKeyBoard, title='URL -> http://', text=urlrss.value)

    def vrationazad(self, callback=None):
        if callback is not None and len(callback):
            if self['liste'].getCurrent()[1] == nazrss:
                nazrss.value = callback
            if self['liste'].getCurrent()[1] == urlrss:
                urlrss.value = callback
        return

    def keyLeft(self):
        self['liste'].handleKey(KEY_LEFT)

    def keyRight(self):
        self['liste'].handleKey(KEY_RIGHT)

    def keyDelete(self):
        self['liste'].handleKey(KEY_DELETE)

    def keyBackspace(self):
        self['liste'].handleKey(KEY_BACKSPACE)

    def keyNumber(self, number):
        self['liste'].handleKey(KEY_0 + number)

    def Gotovo(self):
        self.close()

    def savem(self):
        if os.path.exists('/var/ddRSS/feeds'):
            os.system('rm -rf /tmp/lirss')
            os.system('rm -rf /tmp/rsstr')
            fp1 = open('/var/ddRSS/feeds', 'a')
            title = str(nazrss.value)
            lnk = str(urlrss.value)
            fp1.write(title + ':http://' + lnk + '\n')
            fp1.close()
        self.Gotovo()


class MojRSS(Screen):
    print('class MojRSS(Screen):')

    def __init__(self, session):
        if os.path.exists('/var/lib/dpkg/status'):
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED" flags="wfNoBorder">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="rsslist" itemHeight="55" position="920,120" size="930,770" scrollbarMode="showOnDemand" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <widget name="pred" position="959,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget name="pgreen" position="1172,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget name="pyellow" position="1374,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget name="pblue" position="1584,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        </screen>'''
        else:
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED" flags="wfNoBorder">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="rsslist" itemHeight="55" font="Regular; 36" position="920,120" size="930,770" scrollbarMode="showOnDemand" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <widget source="pred" render="Label" position="959,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget source="pgreen" render="Label" position="1172,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget source="pyellow" render="Label" position="1374,1019" size="250,45" zPosition="4" font="Regular; 28" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget source="pblue" render="Label" position="1584,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        </screen>'''

        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'DirectionActions',
                                     'ColorActions',
                                     'MovieSelectionActions',
                                     'WizardActions',
                                     'EPGSelectActions',
                                     'InputActions',
                                     'NumberActions'], {'ok': self.okClicked,
                                                        'cancel': self.izlaz,
                                                        '0': self.Reload,
                                                        'green': self.Green,
                                                        'red': self.Red,
                                                        'yellow': self.Yellow,
                                                        'blue': self.Blue}, -1)
        self['pred'] = Label(_('Delete'))
        self['pgreen'] = Label(_('Add'))
        self['pyellow'] = Label(_('Edit'))
        self['pblue'] = Label(_('Import'))
        self['info'] = Label(_('Select'))
        self['opisi'] = Label(_(descplug))
        self.ime = []
        self.put = []
        self.rsslist = []
        self['rsslist'] = MenuList([])
        if os.path.exists('/var/ddRSS/feeds'):
            razbi = []
            fp = open('/var/ddRSS/feeds', 'r')
            for line in fp.read().split('\n'):
                if len(line.strip()) != 0:
                    razbi = line.split(':', 1)
                    prvi = '*** ' + razbi[0].strip() + ' ***'
                    prvi = prvi.center(90)
                    self.rsslist.append(prvi)
                    self.ime.append(razbi[0])
                    self.put.append(razbi[1])

            fp.close()
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.showMenu)
        else:
            self.timer.callback.append(self.showMenu)
        self.timer.start(200, True)

    def Red(self):
        sel = self['rsslist'].getCurrent()
        self.rsslist.remove(sel)
        selindex = self['rsslist'].getSelectedIndex()
        del self.ime[selindex]
        del self.put[selindex]
        self.showMenu()

    def Yellow(self):
        selindex = self['rsslist'].getSelectedIndex()
        nazrss.value = self.ime[selindex]
        urlrss.value = self.put[selindex].replace('http://', '')
        self.session.open(UnesiPod)

    def Green(self):
        self.session.openWithCallback(self.Reload, UnesiPod)

    def Reload(self):
        self.ime = []
        self.put = []
        self.rsslist = []
        if os.path.exists('/var/ddRSS/feeds'):
            razbi = []
            fp = open('/var/ddRSS/feeds', 'r')
            for line in fp.read().split('\n'):
                if len(line.strip()) != 0:
                    razbi = line.split(':', 1)
                    prvi = '*** ' + razbi[0].strip() + ' ***'
                    prvi = prvi.center(90)
                    self.rsslist.append(prvi)
                    self.ime.append(razbi[0])
                    self.put.append(razbi[1])
            fp.close()
        self.showMenu()

    def Blue(self):
        prvi = ''
        if os.path.exists('/tmp/feeds.xml') is True:
            self.rsslist = []
            self.ime = []
            self.put = []
            fp1 = open('/var/ddRSS/feeds', 'w')
            fp = open('/tmp/feeds.xml', 'r')
            for line in fp.read().split('\n'):
                n0, n1, n2 = trazenje('<name>', '</name>', '', line)
                if n0 > -1:
                    ut = uzmitekst(n0 + 6, n1, line)
                    linija = ut + ':'
                    prvi = ut
                n0, n1, n2 = trazenje('<url>', '</url>', '', line)
                if n0 > -1:
                    ut = uzmitekst(n0 + 5, n1, line)
                    linija = linija + ut
                    fp1.write(linija + '\n')
                    razbi = []
                    razbi = linija.split(':', 1)
                    prvi = '*** ' + razbi[0].strip() + ' ***'
                    prvi = prvi.center(90)
                    self.rsslist.append(prvi)
                    self.ime.append(razbi[0])
                    self.put.append(razbi[1])

            fp.close()
            fp1.close()
            self.showMenu()
        else:
            pporuka = 'no data, bad xml!'
            self.session.open(MessageBox, pporuka, MessageBox.TYPE_INFO, timeout=5)

    def izlaz(self):
        fp = open('/var/ddRSS/feeds', 'w')
        for ide in range(0, len(self.rsslist)):
            fp.write(self.ime[ide] + ':' + self.put[ide] + '\n')

        fp.close()
        self.close()

    def showMenu(self):
        self['rsslist'].setList(self.rsslist)

    def okClicked(self):
        global naslov
        selindex = self['rsslist'].getSelectedIndex()
        os.system('wget -O /tmp/rsstr ' + self.put[selindex])
        os.system('sync')
        if os.path.exists('/tmp/rsstr') is True:
            line = ''
            naslov = ''
            fp1 = open('/tmp/lirss', 'w')
            fp = open('/tmp/rsstr', 'r')
            linija = ''
            for line in fp.read().split('\n'):
                line = line.strip()
                line = line.replace('<![CDATA[', '')
                line = line.replace(']]>', '')
                linija = linija + line.strip()

            line = linija
            fp.close()
            if len(line) != 0:
                n0, n1, n2 = trazenje('encoding=', '?><', 'title', line)
                if n0 > -1:
                    encod = uzmitekst(n0 + 9, n1, line)
                else:
                    encod = ''
                if n2 > -1:
                    line = skrati(n2 + 6, line)
                n0, n1, n2 = trazenje('</title>', '<item>', '', line)
                if n0 > -1:
                    naslov = uzmitekst(0, n0, line)
                    line = skrati(n1, line)
                    fp1.write('0<DD>' + encod + '<DD>' + naslov + '<DD>none\n')
                razbi = []
                razbi = line.split('<item>')
                del razbi[0]
                itemnas = []
                datum = []
                desc = []
                for ide in range(0, len(razbi)):
                    n0, n1, n2 = trazenje('<title>', '</title>', '', razbi[ide])
                    if n0 > -1:
                        # if encod != '':
                            # proba = uzmitekst(n0 + 7, n1, razbi[ide]).decode(encod).encode('utf8')
                        # else:
                            # proba = uzmitekst(n0 + 7, n1, razbi[ide])
                        proba = uzmitekst(n0 + 7, n1, razbi[ide])  # lululla
                        itemnas.append(proba)
                    n0, n1, n2 = trazenje('', '<pubDate>', '</pubDate>', razbi[ide])
                    if n1 > -1:
                        datum.append(uzmitekst(n1 + 9, n2, razbi[ide]))
                    else:
                        datum.append('no date announced')
                    n0, n1, n2 = trazenje('<description>', '</description>', "alt='' /&gt;", razbi[ide])
                    slika = 'none'
                    if n2 > -1:
                        n0 = n2
                        n3, n4, n5 = trazenje('img src=', '', "alt='' /&gt;", razbi[ide])
                        if n3 > -1 and n5 > -1:
                            slika = uzmitekst(n3 + 8, n5 - 1, razbi[ide])
                    elif slika == 'none':
                        print('ima')
                        n3, n4, n5 = trazenje('src=&quot;', '&lt;br', '&quot; alt=&quot;', razbi[ide])
                        if n3 > -1 and n5 > -1:
                            slika = uzmitekst(n3 + 10, n5, razbi[ide])
                        if n4 > -1:
                            n1 = n4
                    # if encod != '':
                        # proba = uzmitekst(n0 + 13, n1, razbi[ide]).decode(encod).encode('utf8')
                    # else:
                        # proba = uzmitekst(n0 + 13, n1, razbi[ide])
                    proba = uzmitekst(n0 + 13, n1, razbi[ide])  # lululla

                    proba = proba.replace('&amp;nbsp;', '')
                    desc.append(proba)
                    fp1.write(itemnas[ide] + '<DD>' + datum[ide] + '<DD>' + desc[ide] + '<DD>' + slika + '\n')
                self.session.open(PregledRSS)
            else:
                pporuka = 'Gre\xc5\xa1ka prilikom konektiranja!\nPoku\xc5\xa1ajte kasnije.'
                self.session.open(MessageBox, pporuka, MessageBox.TYPE_INFO, timeout=5)
            fp1.close()


class PregledRSS(Screen):
    print('class PregledRSS(Screen):')

    def __init__(self, session):
        global myindex
        global prviput
        if os.path.exists('/var/lib/dpkg/status'):
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="rsspreg" itemHeight="55" position="920,120" size="930,770" scrollbarMode="showOnDemand" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                            <!-- <widget name="slikica" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slika.jpg" position="347,804" zPosition="2" size="200,140" transparent="1" alphatest="on" /> -->
                        </screen>'''
        else:
            self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED">
                            <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                            <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                            <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                            <widget name="rsspreg" itemHeight="55" font="Regular; 36" position="920,120" size="930,770" scrollbarMode="showOnDemand" zPosition="2" transparent="1" />
                            <widget name="opisi" font="Regular; 34" position="61,742" size="773,281" zPosition="2" transparent="1" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                            <!-- <widget name="slikica" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slika.jpg" position="347,804" zPosition="2" size="200,140" transparent="1" alphatest="on" /> -->
                        </screen>'''

        Screen.__init__(self, session)
        self['actions'] = NumberActionMap(['SetupActions',
                                           'DirectionActions',
                                           'ListboxActions'], {
                                          'up': self.keyUp,
                                          'down': self.keyDown,
                                          'left': self.pageUp,
                                          'right': self.pageDown,
                                          'upRepeated': self.keyUp,
                                          'downRepeated': self.keyDown,
                                          'leftRepeated': self.keyUp,
                                          'rightRepeated': self.keyDown,
                                          'pageUp': self.pageUp,
                                          'pageDown': self.pageDown,
                                          'ok': self.OK,
                                          'cancel': self.izlaz}, -2)
        # self['slikica'] = Pixmap()
        self['info'] = Label(_('Select'))
        prviput = 0
        myindex = 0
        self['opisi'] = ScrollLabel()
        self.rsslist = []
        self['rsspreg'] = MenuList([])

        self.brzina = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.brzina_conn = self.brzina.timeout.connect(self.showMenu)
        else:
            self.brzina.callback.append(self.showMenu)
        self.brzina.start(200, True)

    def stvorilistu(self):
        global naslov
        self.itemnas = []
        self.datum = []
        self.desc = []
        self.slika = []
        if os.path.exists('/tmp/lirss') is True:
            prvi = 1
            self.rsslist = []
            fp = open('/tmp/lirss', 'r')
            for line in fp.read().split('\n'):
                if len(line) != 0:
                    razbi = []
                    razbi = line.split('<DD>')
                    if prvi == 1:
                        prvi = 0
                        naslov = razbi[2]
                        # naslov = naslov.center(90)
                    else:
                        self.itemnas.append(razbi[0])
                        self.datum.append(decodeHtml(razbi[1]))
                        self.desc.append(decodeHtml(razbi[2]))
                        self.slika.append(razbi[3])
                        self.rsslist.append(razbi[0])

            fp.close()
        self['rsspreg'].setList(self.rsslist)
        self.showMenu()

    def pageUp(self):
        self['opisi'].pageUp()

    def pageDown(self):
        self['opisi'].pageDown()

    def keyUp(self):
        global myindex
        myindex -= 1
        if myindex < 0:
            myindex = 0
        self['rsspreg'].up()
        self.brzina.start(1500, True)
        self.showMenu()

    def keyDown(self):
        global myindex
        myindex += 1
        if myindex > len(self.rsslist) - 1:
            myindex = len(self.rsslist) - 1
        self['rsspreg'].down()
        self.brzina.start(1500, True)
        self.showMenu()

    def showMenu(self):
        global prviput
        try:
            if prviput == 0:
                prviput = 1
                self.stvorilistu()
            else:
                self.setTitle(naslov)
                self['opisi'].setText(self.datum[myindex] + '\n\n' + self.desc[myindex])
        except Exception as e:
            print('showmenuu aa', e)

    def izlaz(self):
        self.close()

    def OK(self):
        global mydatum
        # global myslika
        global mynaziv
        global mydesc
        mynaziv = self.itemnas[myindex]
        mydatum = self.datum[myindex]
        mydesc = self.desc[myindex]
        # myslika = self.slika[myindex]
        self.session.open(CijeliTekst)


class CijeliTekst(Screen):
    print('class CijeliTekst(Screen):')

    def __init__(self, session):
        # if myslika != 'none':
        self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED">
                        <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                        <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                        <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                        <widget name="opisi" font="Regular; 36" position="920,120" size="930,770" zPosition="2" transparent="1" />
                        <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                            <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                        </widget>
                        <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        <eLabel name="" position="346,652" size="190,52" backgroundColor="#003e4b53" halign="center" valign="center" transparent="0" font="Regular; 17" zPosition="3" text="0 FOR LANGUAGE" />
                        <!-- <widget name="slikica" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slika.jpg" position="347,804" zPosition="2" size="200,140" transparent="1" alphatest="on" /> -->
                    </screen>'''
        # else:
        self.skin = '''<screen position="center,center" size="1920,1080" title="RSS FEED">
                        <widget name="info" position="968,38" zPosition="4" size="870,40" font="Regular;35" backgroundColor="#050c101b" foregroundColor="white" transparent="1" valign="center" />
                        <ePixmap position="188,92" size="500,8" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slider_fhd.png" alphatest="blend" />
                        <ePixmap position="center,center" size="1920,1080" zPosition="-1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/RSS_FEED+1.png" transparent="1" alphatest="blend" />
                        <widget name="opisi" font="Regular; 36" position="920,120" size="930,770" zPosition="2" transparent="1" />
                        <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                            <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                        </widget>
                        <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        <!-- <widget name="slikica" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS/images/slika.jpg" position="347,804" zPosition="2" size="200,140" transparent="1" alphatest="on" /> -->
                    </screen>'''

        Screen.__init__(self, session)
        self['opisi'] = ScrollLabel('Fake start')
        self['info'] = Label(_('Select'))
        self['shortcuts'] = ActionMap(['WizardActions',
                                       'SetupActions'], {'up': self.pageUp,
                                                         'down': self.pageDown,
                                                         'cancel': self.close,
                                                         'ok': self.Gotovo}, -1)
        # if myslika != 'none':
            # os.system("wget -O /tmp/slika.jpg '" + str(myslika) + "'")
            # if os.patch.exists('/tmp/slika.jpg'):
                # self['slikica'] = Pixmap()
        txtxt = mydesc
        self['opisi'] = ScrollLabel()
        self['opisi'].setText(decodeHtml(txtxt))
        self.onLayoutFinish.append(self.showMenu)

    def pageUp(self):
        self['opisi'].pageUp()

    def pageDown(self):
        self['opisi'].pageDown()

    def showMenu(self):
        self.setTitle(mynaziv)

    def Gotovo(self):
        self.close()


def decodeHtml(text):
    charlist = []
    charlist.append(('&#224;', '\xc3\xa0'))
    charlist.append(('&agrave;', '\xc3\xa0'))
    charlist.append(('&#225;', '\xc3\xa1'))
    charlist.append(('&aacute;', '\xc3\xa1'))
    charlist.append(('&#226;', '\xc3\xa2'))
    charlist.append(('&acirc;', '\xc3\xa2'))
    charlist.append(('&#228;', '\xc3\xa4'))
    charlist.append(('&auml;', '\xc3\xa4'))
    charlist.append(('&#249;', '\xc3\xb9'))
    charlist.append(('&ugrave;', '\xc3\xb9'))
    charlist.append(('&#250;', '\xc3\xba'))
    charlist.append(('&uacute;', '\xc3\xba'))
    charlist.append(('&#251;', '\xc3\xbb'))
    charlist.append(('&ucirc;', '\xc3\xbb'))
    charlist.append(('&#252;', '\xc3\xbc'))
    charlist.append(('&uuml;', '\xc3\xbc'))
    charlist.append(('&#242;', '\xc3\xb2'))
    charlist.append(('&ograve;', '\xc3\xb2'))
    charlist.append(('&#243;', '\xc3\xb3'))
    charlist.append(('&oacute;', '\xc3\xb3'))
    charlist.append(('&#244;', '\xc3\xb4'))
    charlist.append(('&ocirc;', '\xc3\xb4'))
    charlist.append(('&#246;', '\xc3\xb6'))
    charlist.append(('&ouml;', '\xc3\xb6'))
    charlist.append(('&#236;', '\xc3\xac'))
    charlist.append(('&igrave;', '\xc3\xac'))
    charlist.append(('&#237;', '\xc3\xad'))
    charlist.append(('&iacute;', '\xc3\xad'))
    charlist.append(('&#238;', '\xc3\xae'))
    charlist.append(('&icirc;', '\xc3\xae'))
    charlist.append(('&#239;', '\xc3\xaf'))
    charlist.append(('&iuml;', '\xc3\xaf'))
    charlist.append(('&#232;', '\xc3\xa8'))
    charlist.append(('&egrave;', '\xc3\xa8'))
    charlist.append(('&#233;', '\xc3\xa9'))
    charlist.append(('&eacute;', '\xc3\xa9'))
    charlist.append(('&#234;', '\xc3\xaa'))
    charlist.append(('&ecirc;', '\xc3\xaa'))
    charlist.append(('&#235;', '\xc3\xab'))
    charlist.append(('&euml;', '\xc3\xab'))
    charlist.append(('&#192;', '\xc3\x80'))
    charlist.append(('&Agrave;', '\xc3\x80'))
    charlist.append(('&#193;', '\xc3\x81'))
    charlist.append(('&Aacute;', '\xc3\x81'))
    charlist.append(('&#194;', '\xc3\x82'))
    charlist.append(('&Acirc;', '\xc3\x82'))
    charlist.append(('&#196;', '\xc3\x84'))
    charlist.append(('&Auml;', '\xc3\x84'))
    charlist.append(('&#217;', '\xc3\x99'))
    charlist.append(('&Ugrave;', '\xc3\x99'))
    charlist.append(('&#218;', '\xc3\x9a'))
    charlist.append(('&Uacute;', '\xc3\x9a'))
    charlist.append(('&#219;', '\xc3\x9b'))
    charlist.append(('&Ucirc;', '\xc3\x9b'))
    charlist.append(('&#220;', '\xc3\x9c'))
    charlist.append(('&Uuml;', '\xc3\x9c'))
    charlist.append(('&#210;', '\xc3\x92'))
    charlist.append(('&Ograve;', '\xc3\x92'))
    charlist.append(('&#211;', '\xc3\x93'))
    charlist.append(('&Oacute;', '\xc3\x93'))
    charlist.append(('&#212;', '\xc3\x94'))
    charlist.append(('&Ocirc;', '\xc3\x94'))
    charlist.append(('&#214;', '\xc3\x96'))
    charlist.append(('&Ouml;', '\xc3\x96'))
    charlist.append(('&#204;', '\xc3\x8c'))
    charlist.append(('&Igrave;', '\xc3\x8c'))
    charlist.append(('&#205;', '\xc3\x8d'))
    charlist.append(('&Iacute;', '\xc3\x8d'))
    charlist.append(('&#206;', '\xc3\x8e'))
    charlist.append(('&Icirc;', '\xc3\x8e'))
    charlist.append(('&#207;', '\xc3\x8f'))
    charlist.append(('&Iuml;', '\xc3\x8f'))
    charlist.append(('&#223;', '\xc3\x9f'))
    charlist.append(('&szlig;', '\xc3\x9f'))
    charlist.append(('&#038;', '&'))
    charlist.append(('&#38;', '&'))
    charlist.append(('&#8230;', '...'))
    charlist.append(('&#8211;', '-'))
    charlist.append(('&#160;', ' '))
    charlist.append(('&#039;', "'"))
    charlist.append(('&#39;', "'"))
    charlist.append(('&#60;', ' '))
    charlist.append(('&#62;', ' '))
    charlist.append(('&lt;', '<'))
    charlist.append(('&gt;', '>'))
    charlist.append(('&nbsp;', ' '))
    charlist.append(('&amp;', '&'))
    charlist.append(('&quot;', '"'))
    charlist.append(('&apos;', "'"))
    charlist.append(('&#8216;', "'"))
    charlist.append(('&#8217;', "'"))
    charlist.append(('&8221;', '\xe2\x80\x9d'))
    charlist.append(('&8482;', '\xe2\x84\xa2'))
    charlist.append(('&#8203;', ''))
    charlist.append(('&#8212;', ''))
    charlist.append(('&#8222;', ''))
    charlist.append(('&#8220;', ''))
    charlist.append(('&raquo;', '"'))
    charlist.append(('&laquo;', '"'))
    charlist.append(('&bdquo;', '"'))
    charlist.append(('&ldquo;', '"'))
    for repl in charlist:
        text = text.replace(repl[0], repl[1])
    from re import sub as re_sub
    text = re_sub('<[^>]+>', '', text)
    return str(text)  # str needed for PLi


def main(session, **kwargs):
    session.open(MojRSS)


def Plugins(**kwargs):
    return [PluginDescriptor(name='RSS by DD', description='RSS Simmple by DDamir ver.%s' % version, icon='rss.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main), PluginDescriptor(name='RSS by DD', description='RSS Simple by DDamir ver.%s' % version, icon='rss.png', where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]
