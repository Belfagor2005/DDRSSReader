# -*- coding: utf-8 -*-

# based on the work from RSS Simmple by DDamir v.0.2
# This Software is Free, use it where you want
# when you want for whatever you want and modify it if you want but don't remove my copyright!
# adapted for py3 and added fhd screens @lululla 20240524
# recode write @lululla 20240906
from . import _, Utils
from .Console import Console as xConsole

from Components.ActionMap import (ActionMap, NumberActionMap)
from Components.ConfigList import ConfigList
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Components.config import (
    ConfigText,
    KEY_0,
    KEY_DELETE,
    KEY_BACKSPACE,
    KEY_LEFT,
    KEY_RIGHT,
    getConfigListEntry,
)
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from enigma import eTimer
import os
import ssl
import json
import sys
from datetime import datetime

global mydatum
global mynaziv
global mydesc
global HALIGN


PY3 = sys.version_info.major >= 3
if PY3:
    PY3 = True
    unidecode = str

currversion = '0.7'
descplugx = 'RSS Simmple by DDamir v.%s\n\nadapted for py3 by @lululla 20240524\n\n' % currversion
inff = 'Import New from /tmp/feeds.xml'
descplug = descplugx + inff
nazrss = ConfigText(fixed_size=False, visible_width=40)
urlrss = ConfigText(fixed_size=False, visible_width=40)
ssl._create_default_https_context = ssl._create_unverified_context
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9ERFJTU1JlYWRlci9tYWluL2luc3RhbGxlci5zaA=='
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvRERSU1NSZWFkZXI='


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
                            <widget name="pyel" position="1369,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
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
                            <widget source="pyel" render="Label" position="1369,1020" size="250,45" zPosition="4" font="Regular; 30" valign="center" halign="center" backgroundColor="#050c101b" transparent="1" foregroundColor="white" />
                            <widget font="Regular; 40" halign="center" position="69,30" render="Label" size="749,70" source="global.CurrentTime" transparent="1">
                                <convert type="ClockToText">Format:%a %d.%m. %Y | %H:%M</convert>
                            </widget>
                            <widget source="session.VideoPicture" render="Pig" position="77,152" zPosition="20" size="739,421" backgroundColor="transparent" transparent="0" />
                        </screen>'''

        Screen.__init__(self, session)
        # self['VKeyIcon'] = Pixmap()
        self['pblue'] = Label(_('Keyboard'))
        self['pyel'] = Label(_('Update'))
        self['pgreen'] = Label(_('Save'))
        self['pred'] = Label(_('Close'))
        self['info'] = Label(_('Select'))
        self['opisi'] = Label(_('Setup RSS FEED v.%s' % currversion))
        self.Update = False
        self['actions'] = NumberActionMap(['SetupActions',
                                           'TextEntryActions',
                                           'WizardActions',
                                           'HelpActions',
                                           'DirectionActions',
                                           'InfobarEPGActions',
                                           'ChannelSelectBaseActions',
                                           'MediaPlayerActions',
                                           'VirtualKeyboardActions',
                                           'HotkeyActions'], {'cancel': self.close,
                                                              'ok': self.Gotovo,
                                                              'left': self.keyLeft,
                                                              'right': self.keyRight,
                                                              'deleteForward': self.keyDelete,
                                                              'deleteBackward': self.keyBackspace,
                                                              'blue': self.openKeyboard,
                                                              'green': self.savem,
                                                              'showVirtualKeyboard': self.openKeyboard,
                                                              'yellow': self.update_me,  # update_me,
                                                              'yellow_long': self.update_dev,
                                                              'info_long': self.update_dev,
                                                              'infolong': self.update_dev,
                                                              'showEventInfoPlugin': self.update_dev,
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

        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.layoutFinished)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
        page = Utils.urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        if float(currversion) < float(remote_version):
            # if currversion < remote_version:
            self.Update = True
            # self['key_yellow'].show()
            # self['key_green'].show()
            self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
        # self.update_me()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

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
            try:
                with open('/var/ddRSS/feeds', 'r') as fp:
                    for line in fp:
                        line = line.strip()  # Rimuove eventuali spazi vuoti
                        if line:  # Controlla che la riga non sia vuota
                            # Dividi la riga in due parti: nome e URL
                            razbi = line.split(':', 1)
                            if len(razbi) == 2:  # Controlla che ci siano esattamente due parti
                                nome_feed = razbi[0].strip()
                                url_feed = razbi[1].strip()
                                # Crea la stringa formattata per la visualizzazione
                                prvi = f'*** {nome_feed} ***'.center(90)
                                # Aggiungi i dati alle rispettive liste
                                self.rsslist.append(prvi)
                                self.ime.append(nome_feed)
                                self.put.append(url_feed)

            except Exception as e:
                print(f'Errore durante la lettura del file: {e}')

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
            try:
                with open('/var/ddRSS/feeds', 'r') as fp:
                    for line in fp:
                        line = line.strip()  # Rimuove spazi in eccesso
                        if line:
                            # Dividi la linea in nome e URL
                            razbi = line.split(':', 1)
                            if len(razbi) == 2:  # Verifica che ci siano due parti
                                nome_feed = razbi[0].strip()
                                url_feed = razbi[1].strip()

                                # Formatta il nome del feed e aggiungilo alla lista
                                primo = f'*** {nome_feed} ***'.center(90)
                                self.rsslist.append(primo)
                                self.ime.append(nome_feed)
                                self.put.append(url_feed)
            except Exception as e:
                print(f'Errore durante la lettura del file: {e}')
                self.session.open(MessageBox, f"Errore nel ricaricamento dei feed: {e}", MessageBox.TYPE_ERROR, timeout=5)
        self.showMenu()

    def Blue(self):
        if os.path.exists('/tmp/feeds.xml'):
            self.rsslist = []
            self.ime = []
            self.put = []
            try:
                # Apri i file in modo sicuro con 'with'
                with open('/tmp/feeds.xml', 'r') as fp, open('/var/ddRSS/feeds', 'w') as fp1:
                    primo = ''
                    # Leggi il file XML linea per linea
                    for line in fp.read().split('\n'):
                        line = line.strip()  # Rimuovi spazi in eccesso
                        # Estrai il nome
                        n0, n1, n2 = trazenje('<name>', '</name>', '', line)
                        if n0 > -1:
                            nome = uzmitekst(n0 + 6, n1, line).strip()
                            linea = nome + ':'
                            primo = nome
                        # Estrai l'URL
                        n0, n1, n2 = trazenje('<url>', '</url>', '', line)
                        if n0 > -1:
                            url = uzmitekst(n0 + 5, n1, line).strip()
                            linea += url
                            fp1.write(linea + '\n')
                            # Divide la riga in nome e URL
                            nome_url = linea.split(':', 1)
                            nome_feed = nome_url[0].strip()
                            url_feed = nome_url[1].strip()
                            # Formatta il nome del feed
                            primo = f'*** {nome_feed} ***'.center(90)
                            self.rsslist.append(primo)
                            self.ime.append(nome_feed)
                            self.put.append(url_feed)
                # Mostra il menu dopo aver caricato i dati
                self.showMenu()
            except Exception as e:
                # In caso di errore, stampa il messaggio
                print(f'Errore: {e}')
                messaggio_errore = 'Errore durante la lettura del file!'
                self.session.open(MessageBox, messaggio_errore, MessageBox.TYPE_INFO, timeout=5)
        else:
            # Se il file XML non esiste, mostra un messaggio di errore
            pporuka = 'Nessun dato disponibile, file XML non valido!'
            self.session.open(MessageBox, pporuka, MessageBox.TYPE_INFO, timeout=5)

    def izlaz(self):
        # Apri il file in modo sicuro
        with open('/var/ddRSS/feeds', 'w') as fp:
            # Usa zip per combinare le liste 'ime' e 'put' e scrivere direttamente
            for nome, url in zip(self.ime, self.put):
                fp.write(f'{nome}:{url}\n')
        # Chiudi l'interfaccia
        self.close()

    '''
    # def izlaz(self):
        # fp = open('/var/ddRSS/feeds', 'w')
        # for ide in range(0, len(self.rsslist)):
            # fp.write(self.ime[ide] + ':' + self.put[ide] + '\n')
        # fp.close()
        # self.close()
    '''

    def showMenu(self):
        self['rsslist'].setList(self.rsslist)

    def okClicked(self):
        global titolo  # Titolo globale
        selindex = self['rsslist'].getSelectedIndex()
        # Scarica il file RSS
        os.system(f'wget -O /tmp/rsstr {self.put[selindex]}')
        os.system('sync')
        # Verifica se il file è stato scaricato correttamente
        if os.path.exists('/tmp/rsstr'):
            titolo = ''
            contenuto_completo = ''
            try:
                # Leggi il file scaricato e rimuovi CDATA e spazi in eccesso
                with open('/tmp/rsstr', 'r') as fp:
                    for riga in fp.read().split('\n'):
                        riga = riga.strip().replace('<![CDATA[', '').replace(']]>', '')
                        contenuto_completo += riga.strip()

                # Scrivi nel file di output
                with open('/tmp/lirss', 'w') as fp1:
                    if contenuto_completo:
                        # Trova encoding e titolo
                        n0, n1, n2 = trazenje('encoding=', '?><', 'title', contenuto_completo)
                        codifica = uzmitekst(n0 + 9, n1, contenuto_completo) if n0 > -1 else ''
                        if n2 > -1:
                            contenuto_completo = skrati(n2 + 6, contenuto_completo)

                        # Trova il titolo del feed
                        n0, n1, n2 = trazenje('</title>', '<item>', '', contenuto_completo)
                        if n0 > -1:
                            titolo = uzmitekst(0, n0, contenuto_completo)
                            contenuto_completo = skrati(n1, contenuto_completo)
                            fp1.write(f'0<DD>{codifica}<DD>{titolo}<DD>nessuno\n')

                        # Estrai gli elementi del feed
                        elementi = contenuto_completo.split('<item>')[1:]  # Rimuovi il primo elemento vuoto
                        itemnas, date, descrizioni = [], [], []

                        for elemento in elementi:
                            # Trova il titolo dell'elemento
                            n0, n1, n2 = trazenje('<title>', '</title>', '', elemento)
                            if n0 > -1:
                                titolo_elemento = uzmitekst(n0 + 7, n1, elemento)
                                itemnas.append(titolo_elemento)

                            # Trova la data di pubblicazione
                            n0, n1, n2 = trazenje('', '<pubDate>', '</pubDate>', elemento)
                            data = uzmitekst(n1 + 9, n2, elemento) if n1 > -1 else 'nessuna data disponibile'
                            date.append(data)

                            # Trova la descrizione e l'immagine
                            n0, n1, n2 = trazenje('<description>', '</description>', "alt='' /&gt;", elemento)
                            immagine = 'nessuna'
                            if n2 > -1:
                                n3, n4, n5 = trazenje('img src=', '', "alt='' /&gt;", elemento)
                                immagine = uzmitekst(n3 + 8, n5 - 1, elemento) if n3 > -1 and n5 > -1 else 'nessuna'
                            else:
                                n3, n4, n5 = trazenje('src=&quot;', '&lt;br', '&quot; alt=&quot;', elemento)
                                immagine = uzmitekst(n3 + 10, n5, elemento) if n3 > -1 and n5 > -1 else 'nessuna'

                            # Trova e pulisci la descrizione
                            descrizione = uzmitekst(n0 + 13, n1, elemento).replace('&amp;nbsp;', '')
                            descrizioni.append(descrizione)

                            # Scrivi nel file
                            fp1.write(f'{titolo_elemento}<DD>{data}<DD>{descrizione}<DD>{immagine}\n')

                # Apri la vista RSS
                self.session.open(PregledRSS)

            except Exception as e:
                print(f'Errore: {e}')
                messaggio_errore = 'Errore durante la connessione!\nRiprova più tardi.'
                self.session.open(MessageBox, messaggio_errore, MessageBox.TYPE_INFO, timeout=5)


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
        if os.path.exists('/tmp/lirss'):
            prvi = 1
            self.rsslist = []
            with open('/tmp/lirss', 'r', encoding='utf-8') as fp:  # Use 'with' for better file handling
                for line in fp.read().split('\n'):
                    if len(line) != 0:
                        razbi = line.split('<DD>')
                        if prvi == 1:
                            prvi = 0
                            naslov = razbi[2]
                        else:
                            self.itemnas.append(razbi[0])
                            self.datum.append(decodeHtml(razbi[1]))
                            self.desc.append(decodeHtml(razbi[2]))
                            self.slika.append(razbi[3])
                            self.rsslist.append(razbi[0])

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
        '''
        # if myslika != 'none':
            # os.system("wget -O /tmp/slika.jpg '" + str(myslika) + "'")
            # if os.patch.exists('/tmp/slika.jpg'):
                # self['slikica'] = Pixmap()
        '''
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
    import re
    import six
    # List of HTML and Unicode entities to replace
    if six.PY2:
        from six.moves import (html_parser)
        h = html_parser.HTMLParser()
        text = h.unescape(text.decode('utf8')).encode('utf8')
    else:
        import html
        text = html.unescape(text)

    charlist = [
        ('&#034;', '"'), ('&#038;', '&'), ('&#039;', "'"), ('&#060;', ' '),
        ('&#062;', ' '), ('&#160;', ' '), ('&#174;', ''), ('&#192;', 'À'),
        ('&#193;', 'Á'), ('&#194;', 'Â'), ('&#196;', 'Ä'), ('&#204;', 'Ì'),
        ('&#205;', 'Í'), ('&#206;', 'Î'), ('&#207;', 'Ï'), ('&#210;', 'Ò'),
        ('&#211;', 'Ó'), ('&#212;', 'Ô'), ('&#214;', 'Ö'), ('&#217;', 'Ù'),
        ('&#218;', 'Ú'), ('&#219;', 'Û'), ('&#220;', 'Ü'), ('&#223;', 'ß'),
        ('&#224;', 'à'), ('&#225;', 'á'), ('&#226;', 'â'), ('&#228;', 'ä'),
        ('&#232;', 'è'), ('&#233;', 'é'), ('&#234;', 'ê'), ('&#235;', 'ë'),
        ('&#236;', 'ì'), ('&#237;', 'í'), ('&#238;', 'î'), ('&#239;', 'ï'),
        ('&#242;', 'ò'), ('&#243;', 'ó'), ('&#244;', 'ô'), ('&#246;', 'ö'),
        ('&#249;', 'ù'), ('&#250;', 'ú'), ('&#251;', 'û'), ('&#252;', 'ü'),
        ('&#8203;', ''), ('&#8211;', '-'), ('&#8212;', '—'), ('&#8216;', "'"),
        ('&#8217;', "'"), ('&#8220;', '"'), ('&#8221;', '"'), ('&#8222;', ','),
        ('&#8230;', '...'), ('&#x21;', '!'), ('&#x26;', '&'), ('&#x27;', "'"),
        ('&#x3f;', '?'), ('&#xB7;', '·'), ('&#xC4;', 'Ä'), ('&#xD6;', 'Ö'),
        ('&#xDC;', 'Ü'), ('&#xDF;', 'ß'), ('&#xE4;', 'ä'), ('&#xE9;', 'é'),
        ('&#xF6;', 'ö'), ('&#xF8;', 'ø'), ('&#xFB;', 'û'), ('&#xFC;', 'ü'),
        ('&8221;', '”'), ('&8482;', '™'), ('&Aacute;', 'Á'), ('&Acirc;', 'Â'),
        ('&Agrave;', 'À'), ('&Auml;', 'Ä'), ('&Iacute;', 'Í'), ('&Icirc;', 'Î'),
        ('&Igrave;', 'Ì'), ('&Iuml;', 'Ï'), ('&Oacute;', 'Ó'), ('&Ocirc;', 'Ô'),
        ('&Ograve;', 'Ò'), ('&Ouml;', 'Ö'), ('&Uacute;', 'Ú'), ('&Ucirc;', 'Û'),
        ('&Ugrave;', 'Ù'), ('&Uuml;', 'Ü'), ('&aacute;', 'á'), ('&acirc;', 'â'),
        ('&acute;', "'"), ('&agrave;', 'à'), ('&amp;', '&'), ('&apos;', "'"),
        ('&auml;', 'ä'), ('&bdquo;', '"'), ('&eacute;', 'é'), ('&ecirc;', 'ê'),
        ('&egrave;', 'è'), ('&euml;', 'ë'), ('&gt;', '>'), ('&hellip;', '...'),
        ('&iacute;', 'í'), ('&icirc;', 'î'), ('&igrave;', 'ì'), ('&iuml;', 'ï'),
        ('&laquo;', '"'), ('&ldquo;', '"'), ('&lsquo;', "'"), ('&lt;', '<'),
        ('&mdash;', '—'), ('&nbsp;', ' '), ('&ndash;', '-'), ('&oacute;', 'ó'),
        ('&ocirc;', 'ô'), ('&ograve;', 'ò'), ('&ouml;', 'ö'), ('&quot;', '"'),
        ('&raquo;', '"'), ('&rsquo;', "'"), ('&szlig;', 'ß'), ('&uacute;', 'ú'),
        ('&ucirc;', 'û'), ('&ugrave;', 'ù'), ('&uuml;', 'ü'), ('&ntilde;', '~'),
        ('&equals;', '='), ('&quest;', '?'), ('&comma;', ','), ('&period;', '.'),
        ('&colon;', ':'), ('&lpar;', '('), ('&rpar;', ')'), ('&excl;', '!'),
        ('&dollar;', '$'), ('&num;', '#'), ('&ast;', '*'), ('&lowbar;', '_'),
        ('&lsqb;', '['), ('&rsqb;', ']'), ('&half;', '1/2'), ('&DiacriticalTilde;', '~'),
        ('&OpenCurlyDoubleQuote;', '"'), ('&CloseCurlyDoubleQuote;', '"'),
    ]
    # Replacing all HTML entities with their respective characters
    for repl in charlist:
        text = text.replace(repl[0], repl[1])
    # Remove any remaining HTML tags
    text = re.sub('<[^>]+>', '', text)
    return text.strip()


def main(session, **kwargs):
    session.open(MojRSS)


def Plugins(**kwargs):
    return [PluginDescriptor(name='RSS by DD', description='RSS Simmple by DDamir ver.%s' % currversion, icon='rss.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main), PluginDescriptor(name='RSS by DD', description='RSS Simple by DDamir ver.%s' % currversion, icon='rss.png', where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]
