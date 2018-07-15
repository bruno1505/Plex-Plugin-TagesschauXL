# -*- coding: utf-8 -*-
import string
import urllib			# urllib.quote()
import urllib2			# urllib2.Request
import ssl				# HTTPS-Handshake
import os, subprocess 	# u.a. Behandlung von Pfadnamen
import sys				# Plattformerkennung
import re			# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import time
import datetime
import updater

''' 
####################################################################################################
+++++ Plex-Plugin-TagesschauXL +++++

Funktionen: siehe Datei README.md
Versions-Historie: siehe Datei HISTORY
####################################################################################################
'''

VERSION =  '1.0.6'		
VDATE = '15.07.2018'

# 
#	
# (c) 2017 by Roland Scholz, rols1@gmx.de
# 
#     Functions -> README.md
# 
# 	Licensed under MIT License (MIT)
# 	(previously licensed under GPL 3.0)
# 	A copy of the License you find here:
#		https://github.com/rols1/Plex-Plugin-TagesschauXL/blob/master/LICENSE.md

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

####################################################################################################

NAME = 'TagesschauXL'
PREFIX = '/video/tagesschauxl'			
												

ART = 'art.png'								# Tagesschau.de 1280 X 720 
ICON_SEARCH = 'icon-search.png'						

ICON_MAIN = 'tagesschau.png'			
ICON_MAIN_UPDATER = 'plugin-update.png'		
ICON_UPDATER_NEW = 'plugin-update-new.png'

ICON_LIVE = 'tagesschau-Live.png'
ICON_WICHTIG = 'tagesschau-Wichtig.png'
ICON_100sec = 'tagesschau100sec.png'
ICON_LAST =  'tagesschau-letzte-Sendung.png'
ICON_20 =  'tagesschau-20Uhr.png'
ICON_20GEST =  'tagesschau-20Uhr-Gest.png'
ICON_TTHEMEN = 'tagesthemen.png'
ICON_NACHT = 'tagesschau-Nachtmagazin.png'
ICON_BAB = 'tagesschau-BaB.png'
ICON_ARCHIV = 'tagesschau-Sendungsarchiv.png'
ICON_POD = 'tagesschau-Podcasts.png'
ICON_BLOGS = 'tagesschau-Videoblogs.png'
ICON_RADIO = 'tagesschau-Radio.png'
ICON_BILDER = 'tagesschau-Bilder.png'
ICON_KURZ = 'tagesschau-Kurz.png'
ICON_24 = 'tagesschau24.png'


ICON_HOME = "home.png"
ICON_CAL = "icon-calendar.png"
ICON_OK = "icon-ok.png"
ICON_WARNING = "icon-warning.png"
ICON_NEXT = "icon-next.png"
ICON_CANCEL = "icon-error.png"
ICON_MEHR = "icon-mehr.png"
ICON_DOWNL = "icon-downl.png"
ICON_DOWNL_DIR = "icon-downl-dir.png"
ICON_DELETE = "icon-delete.png"


BASE_URL = 'http://www.tagesschau.de'

# ARD_Live = 'https://www.tagesschau.de/multimedia/livestreams/index.html'				# ersetzt durch ARD_m3u8
ARD_m3u8 = 'http://tagesschau-lh.akamaihd.net/i/tagesschau_1@119231/master.m3u8'
# ARD_IMP = 'http://www.tagesschau.de/die_wichtigsten_nachrichten_als_video/index.html' # Inhalt mit ARD_100  identisch
ARD_100 = 'https://www.tagesschau.de/100sekunden/index.html'
ARD_Last = 'https://www.tagesschau.de/sendung/letzte-sendung/index.html'
ARD_20Uhr = 'https://www.tagesschau.de/sendung/tagesschau/index.html'
ARD_Gest = 'https://www.tagesschau.de/sendung/tagesschau_mit_gebaerdensprache/index.html'
ARD_tthemen = 'https://www.tagesschau.de/sendung/tagesthemen/index.html'
ARD_Nacht = 'https://www.tagesschau.de/sendung/nachtmagazin/index.html'
ARD_bab = 'https://www.tagesschau.de/bab/index.html'
ARD_Archiv = 'https://www.tagesschau.de/multimedia/sendung/index.html'
# ARD_Pod = 'https://www.tagesschau.de/multimedia/podcasts/index.html'					# überflüssig ohne Download-Funktion
ARD_Blogs = 'https://www.tagesschau.de/videoblog/startseite/index.html'
ARD_PolitikRadio = 'https://www.tagesschau.de/multimedia/politikimradio/index.html'
ARD_Bilder = 'https://www.tagesschau.de/multimedia/bilder/index.html'
# ARD_kurz = 'https://www.tagesschau.de/multimedia/kurzerklaert/index.html'				# resfresh -> faktenfinder, s.u.
ARD_kurz = 'https://faktenfinder.tagesschau.de/kurzerklaert/index.html'
BASE_FAKT='https://faktenfinder.tagesschau.de'											# s. get_content

REPO_NAME = 'Plex-Plugin-TagesschauXL'
GITHUB_REPOSITORY = 'rols1/' + REPO_NAME

####################################################################################################

def Start():
	#Log.Debug()  	# definiert in Info.plist
	# Problem Voreinstellung Plakate/Details/Liste:
	#	https://forums.plex.tv/discussion/211755/how-do-i-make-my-objectcontainer-display-as-a-gallery-of-thumbnails
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	ObjectContainer.art        = R(ART)
	ObjectContainer.title1     = NAME
	#ObjectContainer.view_group = "InfoList"

	HTTP.CacheTime = CACHE_1HOUR # Debugging: falls Logdaten ausbleiben, Browserdaten löschen

#----------------------------------------------------------------
# handler bindet an das bundle
@route(PREFIX)
@handler(PREFIX, NAME, art = ART, thumb = ICON_MAIN)
def Main():
	Log('Funktion Main'); Log(PREFIX); Log(VERSION); Log(VDATE)
	Log('Client: '); Log(Client.Platform)
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	
																			
	# folgendes DirectoryObject ist Deko für das nicht sichtbare InputDirectoryObject dahinter:
	oc.add(DirectoryObject(key=Callback(Main),title='Suche: im Suchfeld eingeben', 
		summary='', tagline='TV', thumb=R(ICON_SEARCH)))
	oc.add(InputDirectoryObject(key=Callback(Search, s_type='video', title=u'%s' % L('Search Video')),
		title=u'%s' % L('Search'), prompt=u'%s' % L('Search Video'), thumb=R(ICON_SEARCH)))

	title = 'Livestream'
	oc.add(DirectoryObject(key=Callback(Livestream, title=title), title=title,summary=title, tagline='TV', 
		thumb=R(ICON_LIVE)))
	title = 'Tagesschau in 100 Sekunden' 
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_100, ID='ARD_100', img=ICON_100sec), 
		title=title, summary=title, tagline='TV', thumb=R(ICON_100sec)))
	title = 'Letzte Sendung'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Last, ID='ARD_Last', img=ICON_LAST), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_LAST)))
	title = 'Tagesschau 20 Uhr'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_20Uhr, ID='ARD_20Uhr', img=ICON_20), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_20)))
	title = 'Tagesschau 20 Uhr (Gebärdensprache)'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Gest, ID='ARD_Gest', img=ICON_20GEST), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_20GEST)))
	title = 'Tagesthemen'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_tthemen, ID='ARD_tthemen', img=ICON_TTHEMEN), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_TTHEMEN)))
	title = 'Nachtmagazin'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Nacht, ID='ARD_Nacht', img=ICON_NACHT), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_NACHT)))
	title = 'Bericht aus Berlin'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_bab, ID='ARD_bab', img=ICON_BAB), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_BAB)))
	title = 'Sendungsarchiv'
	summary = 'Tagesschau-Sendungen eines Monats'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Archiv, ID='ARD_Archiv', img=ICON_ARCHIV), 
		title=title,summary=summary, tagline='TV', thumb=R(ICON_ARCHIV)))
	#title = 'Podcasts'														# überflüssig ohne Download-Funktion
	#oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Pod, ID='ARD_Pod', img=''), 
	#	title=title,summary=title, tagline='TV', thumb=R(ICON_POD)))
	title = 'Videoblogs'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Blogs, ID='ARD_Blogs', img=ICON_BLOGS), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_BLOGS)))
	title = 'Politik im Radio'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_PolitikRadio, ID='ARD_PolitikRadio', img=ICON_RADIO), 
		title=title,summary=title, tagline='Radio', thumb=R(ICON_RADIO)))
	title = 'Bildergalerien'
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_Bilder, ID='ARD_Bilder', img=ICON_BILDER),
		title=title,summary=title, tagline='Bilder', thumb=R(ICON_BILDER)))
	title = '#kurzerklärt'.decode(encoding="utf-8", errors="ignore")
	oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ARD_kurz, ID='ARD_kurz', img=ICON_KURZ), 
		title=title,summary=title, tagline='TV', thumb=R(ICON_KURZ)))

	repo_url = 'https://github.com/{0}/releases/'.format(GITHUB_REPOSITORY)
	call_update = False
	if Prefs['pref_info_update'] == True:				# Hinweis auf neues Update beim Start des Plugins 
		ret = updater.update_available(VERSION)
		int_lv = ret[0]			# Version Github
		int_lc = ret[1]			# Version aktuell
		latest_version = ret[2]	# Version Github, Format 1.4.1
		
		if int_lv > int_lc:								# Update-Button "installieren" zeigen
			call_update = True
			title = 'neues Update vorhanden - jetzt installieren'
			summary = 'Plugin aktuell: ' + VERSION + ', neu auf Github: ' + latest_version
			url = 'https://github.com/{0}/releases/download/{1}/{2}.bundle.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
			oc.add(DirectoryObject(key=Callback(updater.update, url=url , ver=latest_version), 
				title=title, summary=summary, tagline=cleanhtml(summary), thumb=R(ICON_UPDATER_NEW)))
	if call_update == False:							# Update-Button "Suche" zeigen	
		title = 'Plugin-Update | akt. Version: ' + VERSION + ' vom ' + VDATE	
		summary='Suche nach neuen Updates starten'
		tagline='Bezugsquelle: ' + repo_url			
		oc.add(DirectoryObject(key=Callback(SearchUpdate, title='Plugin-Update'), 
			title=title, summary=summary, tagline=tagline, thumb=R(ICON_MAIN_UPDATER)))
								
		
	return oc

def dummy(title):
	return
	
#---------------------------------------------------------------- 
def home(cont):												# Home-Button, Aufruf: oc = home(cont=oc)	
	title = 'Zurück zum Hauptmenü'
	title = title.decode(encoding="utf-8", errors="ignore")
	summary = title	
	cont.add(DirectoryObject(key=Callback(Main),title=title, summary=summary, tagline=NAME, thumb=R(ICON_HOME)))
	return cont

####################################################################################################
@route(PREFIX + '/SearchUpdate')
def SearchUpdate(title):		#
	oc = ObjectContainer(view_group="InfoList", art=ObjectContainer.art)	

	ret = updater.update_available(VERSION)
	int_lv = ret[0]			# Version Github
	int_lc = ret[1]			# Version aktuell
	latest_version = ret[2]	# Version Github
	summ = ret[3]			# Plugin-Name
	tag = ret[4]			# History (last change)

	url = 'https://github.com/{0}/releases/download/{1}/{2}.bundle.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
	Log(latest_version); Log(int_lv); Log(int_lc); Log(url); 
	
	if int_lv > int_lc:		# zum Testen drehen (akt. Plugin vorher sichern!)
		oc.add(DirectoryObject(
			key = Callback(updater.update, url=url , ver=latest_version), 
			title = 'Update vorhanden - jetzt installieren',
			summary = 'Plugin aktuell: ' + VERSION + ', neu auf Github: ' + latest_version,
			tagline = cleanhtml(summ),
			thumb = R(ICON_UPDATER_NEW)))
			
		oc.add(DirectoryObject(
			key = Callback(Main), 
			title = 'Update abbrechen',
			summary = 'weiter im aktuellen Plugin',
			thumb = R(ICON_UPDATER_NEW)))
	else:	
		oc.add(DirectoryObject(
			#key = Callback(updater.menu, title='Update Plugin'), 
			key = Callback(Main), 
			title = 'Plugin ist aktuell | weiter zum aktuellen Plugin',
			summary = 'Plugin Version ' + VERSION + ' ist aktuell (kein Update vorhanden)',
			tagline = cleanhtml(summ),
			thumb = R(ICON_OK)))
			
	return oc
	
####################################################################################################
@route(PREFIX + '/Search')	# Suche - Verarbeitung der Eingabe
def Search(query=None, title=L('Search'), s_type='video', pagenr='', MaxPage='', **kwargs):
	Log('Search'); Log(query)
	query = query.replace(' ', '+')   # Blanks durch + ersetzen (..suche2.html?query=bilder+des+tages)
	
	name = 'Suchergebnis zu: ' + query
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	next_cbKey = 'SinglePage'	# cbKey = Callback für Container in PageControl
			
	path =  BASE_URL + '/suche2.html?page_number=%s&query=%s&sort_by=date' % (pagenr, query)
	Log(path) 
	page = HTTP.Request(path).content
	Log(len(page))
			
	i = page.find('war leider erfolglos. Bitte überprüfen Sie Ihre Eingabe')
	Log(i)
	if i > 0:
		msg_notfound = 'Leider kein Treffer.'
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")
		summary = 'zurück zu ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main),title=title, summary=summary, tagline=NAME, thumb=R(ICON_MAIN)))
		return oc
		
	searchResult = stringextract('Suchergebnis</h2>', 'Treffer', page)	
	searchResult = stringextract('<strong>', '</strong>', searchResult)
	MaxPage = (int(searchResult) / 10) + 1		# 10 Beiträge/Seite = Vorgabe ARD
	Log(searchResult); Log(MaxPage)
	
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
	name = 'Suchergebnisse zu: %s (Gesamt: %s), Seite %s'  % (urllib.unquote(query), searchResult, pagenr)
	name = name.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=name, art = ObjectContainer.art)
	oc = home(cont=oc)							# Home-Button	
			
	oc = get_content(oc=oc, page=page, ID='Search')
	
	pagenr = int(pagenr) + 1
	if pagenr <= MaxPage:
		path =  BASE_URL + '/suche2.html?page_number=%s&query=%s&sort_by=date' % (pagenr, query)
		Log(pagenr); Log(path)
		title = "Weitere Beiträge".decode(encoding="utf-8", errors="ignore")
		oc.add(DirectoryObject(key=Callback(Search, query=query, s_type=s_type, pagenr=pagenr, MaxPage=MaxPage), 
			title=title, thumb=R(ICON_MEHR), summary=''))			
	 
	return oc
	
#---------------------------------------------------------------- 
@route(PREFIX + '/menu_hub')	# Verteiler - außer für Suche + Livestream
def menu_hub(title, path, ID, img):	
	Log('menu_hub'); Log(title); Log(ID);
	title = title.decode(encoding="utf-8", errors="ignore")					

	if ID=='ARD_Archiv':						# Vorschaltung Kalendertage (1 Monat)
		oc = Archiv(path=path, ID=ID, img=img) 	# Archiv: Callback nach hier, dann weiter zu oc=get_content
		return oc	

	page = HTTP.Request(path).content
	Log(len(page))
		
	# Direktsprünge - der Rest der Seiten enthält vorwiegend gleiche Inhalte aus dem Archiv:
	if ID=='ARD_100' or ID=='ARD_Last' or ID=='ARD_20Uhr' or ID=='ARD_Gest' or ID=='ARD_tthemen' or ID=='ARD_Nacht':
		if ID=='ARD_100': 
			url =  BASE_URL + stringextract('class=\"headline\"><a href=', '>', page)	# href ohne ""
		if ID=='ARD_Last': 
			url =  BASE_URL + stringextract('class=\"headline\"><a href=\"', '>', page)
		if ID=='ARD_tthemen' or ID=='ARD_Nacht': 
			url =  BASE_URL + stringextract('class=\"headline\"><a href=\"', '\">', page)
		if ID=='ARD_20Uhr' or ID=='ARD_Gest': 
			url =  BASE_URL + stringextract('class=\"mediaLink\" href=\"', '\"', page)
		
		url = url.replace('"', '')		# 15.07.2018 Url's mit Endung " gesehen
		Log(title); Log(url); Log(img)
		oc = GetVideoSources(path=url , title=title, summary=title, thumb=R(img), tagline=title)
		return oc
 
	# Seiten mit unterschiedlichen Archiv-Inhalten
	# Inhalt ermitteln:
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title, art = ObjectContainer.art)
	oc = home(cont=oc)							# Home-Button	

	oc = get_content(oc=oc, page=page, ID=ID)
 
	return oc
	
#---------------------------------------------------------------- 
def Archiv(path, ID, img):	# 30 Tage - ähnlich Verpasst 
	Log('Archiv: ' + path)
	title2 = 'Sendungsarchiv'
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title2, art = ObjectContainer.art)
	oc = home(cont=oc)							# Home-Button	
		
	wlist = range(0,30)			# Abstand 1 Tage
	now = datetime.datetime.now()
	for nr in wlist:
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
		SendDate = rdate.strftime("%Y%m%d")		# ARD-Archiv-Format		
		iWeekday =  rdate.strftime("%A")
		punkte = '.'
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)
		
		ipath =  BASE_URL + '/multimedia/video/videoarchiv2~_date-%s.htm' % (SendDate)
		Log(path) 


		# Log(iPath); Log(iDate); Log(iWeekday);
		title =	"%s | %s" % (iDate, iWeekday)
		Log(title)	

		ID = 'ARD_Archiv_Day'
		oc.add(DirectoryObject(key=Callback(menu_hub, title=title, path=ipath, ID=ID, img=img), 
			title=title, thumb=R(ICON_CAL)))
		
	return oc
			
#------------
def transl_wtag(tag):	# Wochentage engl./deutsch wg. Problemen mit locale-Setting 
	wt_engl = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	wt_deutsch = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
	
	wt_ret = tag
	for i in range (len(wt_engl)):
		el = wt_engl[i]
		if el == tag:
			wt_ret = wt_deutsch[i]
			break
	return wt_ret
#---------------------------------------------------------------- 
@route(PREFIX + '/get_content')
def get_content(oc, page, ID):	
	Log('get_content'); Log('ID=' + ID)

	if  ID=='Search':
		content =  blockextract('class=\"teaser\">', '', page)
	if ID=='ARD_bab' or ID=='ARD_Bilder' or ID=='ARD_PolitikRadio':
		content =  blockextract('class=\"teaser\">', '', page)
	if ID=='ARD_Blogs' or ID=='ARD_kurz'  or ID=='ARD_Archiv_Day':
		content =  blockextract('class=\"teaser\" >', '', page)
		base_url = BASE_FAKT
	if ID=='ARD_PolitikRadio':
		content =  blockextract('class=\"teaser\"', '', page)
		
	base_url = BASE_URL
	if ID=='ARD_kurz':
		base_url = BASE_FAKT									# http://faktenfinder.tagesschau.de
						
	Log(len(page)); Log(len(content));
	
	if len(content) == 0:										# kein Ergebnis oder allg. Fehler
		msg_notfound = 'Leider keine Inhalte' 					# z.B. bei A-Z für best. Buchstaben 
			
		s = 'Es ist leider ein Fehler aufgetreten.'				# ZDF-Meldung Server-Problem
		if page.find('\"title\">' + s) >= 0:
			msg_notfound = s + ' Bitte versuchen Sie es später noch einmal.'
						
		title = msg_notfound.decode(encoding="utf-8", errors="ignore")					
		summary = 'zurück zur ' + NAME.decode(encoding="utf-8", errors="ignore")		
		oc.add(DirectoryObject(key=Callback(Main), title=title, 
			summary=summary, tagline='TV', thumb=R(ICON_MAIN)))
		return oc		
		
	cnt = 0
	for rec in content:	
		cnt = cnt +1													# Satz-Zähler						
		teaser_img = ''												
		teaser_img = stringextract('src=\"', '\"', rec) 	
		if teaser_img.find('http://') == -1:							# ohne http://	bei Wetter + gelöschten Seiten		
			teaser_img = base_url + teaser_img
		teaser_url =  base_url + stringextract('href=\"', '\"', rec)	# 1. Stelle <a href=				
			
		Log(teaser_img); Log(teaser_url)
			
		# hier relevante ID-Liste. ID's mit Direktsprüngen (s. menu_hub) haben GetVideoSources als Callback:
		# Search, ARD_bab, ARD_Archiv, ARD_PolitikRadio, ARD_Bilder, ARD_kurz 
		teasertext='';	headline=''; dachzeile=''; teaser_typ=''; teaser_date=''
		gallery_url='';	onlyGallery=False							
		if ID=='Search':
			teasertext = stringextract('class=\"teasertext \">', '</p>', rec).strip()	# Teasertext mit url + Langtext, 
			teasertext = stringextract('html\">', '<strong>', teasertext)		# Text hinter url, nach | folgt typ
			teasertext = teasertext.replace('|', '')			
			dachzeile = stringextract('dachzeile\">', '</p>', rec).strip()		# Dachzeile mit url + Typ + Datum							
			teaser_typ =  stringextract('<strong>', '</strong>', dachzeile)
			teaser_date =  stringextract('</strong>', '</a>', dachzeile)
			tagline = teaser_typ + teaser_date
			headlineclass = stringextract('headline\">', '</h3>', rec).strip()	# Headline mit url + Kurztext
			headline = stringextract('html\">', '</a>', headlineclass)
		if ID=='ARD_bab':
			headline = stringextract('class=\"headline\">', '</h', rec)
			dachzeile = stringextract('dachzeile\">', '</p>', rec)				# fehlt im 1. Satz
			if cnt == 1:
				teasertext = stringextract('class=\"teasertext\">', '|&nbsp', rec)	# 1. Satz mit Leerz. vor ", mit url + Typ
				pos = rec.find('Ganze Sendung:')			# dachzeile im 1. Satz hier mit Datum
				if pos:
					headline = stringextract('>', '|&nbsp', rec[pos-1:])
			else:
				teasertext = stringextract('class=\"teasertext \">', '|&nbsp', rec)
			if dachzeile:
				tagline = dachzeile
			else:
				tagline = headline
		if ID=='ARD_Blogs' or ID=='ARD_kurz':
			if cnt == 1 and ID=='ARD_Blogs':		# allg. Beschreibung in ARD_Blogs, 1. Satz
				continue
			headline = stringextract('class=\"headline\">', '</h4', rec)
			dachzeile = stringextract('dachzeile\">', '</p>', rec)				# fehlt im 1. Satz
			teasertext = stringextract('class=\"teasertext\">', '|&nbsp', rec)	# 1. Satz mit Leerz. vor ", mit url + Typ
			tagline = dachzeile	
			pos = rec.find('class=\"gallerie\">')								# Satz mit zusätzl. Bilderserie?
			if pos > 0:															# wir erzeugen 2. Button, s.u.
				leftpos, leftstring = my_rfind('<a href=', 'class=\"icon galerie\">', rec)		
				gallery_url = base_url + stringextract('href=\"', '\"', leftstring) 
		if ID=='ARD_Bilder': 
			onlyGallery=True													# kein Hybrid-Satz
			gallery_url =  base_url + stringextract('href=\"', '\"', rec)		# 1. Stelle <a href=
			headlineclass = stringextract('headline\">', '</h4>', rec).strip()	# Headline mit url + Kurztext
			headline = stringextract('html\">', '</a>', headlineclass)
			teasertext = stringextract('title=\"', '\"', rec)					# Bildtitel als teasertext
			teaserdate = stringextract('class=\"teasertext\">', '|&nbsp', rec)  # nur Datum
			tagline = teaserdate			
		if ID=='ARD_PolitikRadio': 													# Podcasts
			headlineclass = stringextract('headline\">', '</h4>', rec).strip()	# Headline mit url + Kurztext
			headline = stringextract('html\">', '</a>', headlineclass)
			if cnt == 1:									# url für 1. Satz hier - fieldset hier eingebettet	
				teaser_url = ARD_PolitikRadio	
				headline = stringextract('<h2 class=\"headline\">', '</h2>', page) # außerhalb akt. Satz! 
			teasertext = stringextract('class=\"teasertext\">', '</p>', rec)	# Autor + Sendeanstalt					
			tagline = teasertext.strip()
		if ID=='ARD_Archiv_Day':
			headlineclass = stringextract('headline\">', '</h4>', rec)			# Headline mit url + Kurztext
			headline = stringextract('html\">', '</a>', headlineclass)
			teasertext = stringextract('class=\"teasertext \">', '</p>', rec).strip()	# Teasertext mit url + Langtext, 
			teasertext = stringextract('html\">', '</a>', teasertext)		# Text hinter url, nach | folgt typ
			if teasertext == '':											# leer: tagesschau vor 20 Jahren
				teasertext = headline		
			dachzeile = stringextract('dachzeile\">', '</p>', rec)		
			tagline = dachzeile	
		Log('content-extracts:')
		teasertext = teasertext.decode(encoding="utf-8", errors="ignore")	 # Decod. manchmal für Logausgabe erforderlich 	
		Log(teaser_url); Log(headline); Log(teasertext[:81]);  		
		Log(dachzeile);	Log(teaser_typ); Log(teaser_date);		
			
		title = unescape(headline)
		summary = unescape(teasertext)
		summary = cleanhtml(summary)
		tagline = cleanhtml(tagline)
		Log(Client.Platform)									# für PHT: Austausch Titel / Tagline
		if  Client.Platform == 'Plex Home Theater':
			title, tagline = tagline, title
				
		if title=='' or summary=='':			# z.B. Video</strong> vom 27.09.2004 00:00:01 (leer, Rauschen)
			Log('title/summary leer: skip')
			continue
			
		title = title.decode(encoding="utf-8", errors="ignore")
		summary = summary.decode(encoding="utf-8", errors="ignore")
		tagline = tagline.decode(encoding="utf-8", errors="ignore")
		Log('neuer Satz:')
		Log(teaser_img);Log(teaser_url);Log(title);Log(summary[:80]);Log(tagline);

		if onlyGallery == True:					# reine Bildgalerie
			oc.add(DirectoryObject(key=Callback(Bildgalerie, path=gallery_url, title=title), 
				title=title, thumb=teaser_img, summary=summary, tagline=tagline))
		else:									# Hybrid-Sätze Video/Bilder 
			oc.add(DirectoryObject(key=Callback(GetVideoSources, path=teaser_url, title=title, summary=summary,
				thumb=teaser_img, tagline=tagline), title=title, thumb=teaser_img, summary=summary, tagline=tagline))
			if gallery_url:
				title = 'Bilder: ' + title
				oc.add(DirectoryObject(key=Callback(Bildgalerie, path=gallery_url, title=title), 
					title=title, thumb=teaser_img, summary=summary, tagline=tagline))
			

	return oc
#-------------
###################################################################################################
@route(PREFIX + '/GetVideoSources')	# Einzelsendung - 
# Problem Texte (tagline, summary): hier umfangreicher, aber Verzicht, da mindestens 3 Seitenkonzepte.
# 	Wir übernehmen daher die Texte vom Aufrufer.
def GetVideoSources(path, title, summary, tagline, thumb):
	Log('Funktion GetVideoSources: ' + path)
	title = title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(view_group="InfoList", title1=title, art=ObjectContainer.art)
	
	page, err = get_page(path=path)				# Seite existiert nicht (mehr)?
	if err:
		return err						
	Log(len(page))			
	# Log(page)
	
	if path.find('/multimedia/bilder/') > 0:					# kann nur Bildstrecke sein, kommt z.B. aus Suche
		oc = Bildgalerie(path=path, title=title)
		return oc
	
	Log('<fieldset>' in page)
	if '<fieldset>' not in page:							# Test auf Videos
		if page.find('magnifier_pos-0.html\">') > 0 :	      	# Einzelbild(er) vorhanden
			leftpos, leftstring = my_rfind('href=', 'magnifier_pos-0.html\">', page)	
			Log(leftstring)	
			gallery_url = BASE_URL + stringextract('href=\"', '\"', leftstring) 
			oc = Bildgalerie(path=gallery_url, title=title)
			return oc
		else:												
			error_txt = 'Das Video steht nicht (mehr) zur Verfügung.'	# weder Videos noch Einzelbilder - Abbruch	 			 	 
			msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
			Log(msg)
			msg =  msg.decode(encoding="utf-8", errors="ignore")
			err = ObjectContainer(header=msgH, message=msg)
			return err
		
	oc = home(cont=oc)					# Home-Button

	videoarea = stringextract('<fieldset>', '</fieldset>', page)		# div. Formate: mp3, ogg 
	videoarea = videoarea.strip()
	# Log(videoarea)
	videos = blockextract('<div class=\"button\"', '</div>', videoarea)
	if len(videos) == 0:										# Seite mit fieldset aber ohne Videobuttons
		if page.find('class=\"icon video\"') > 0 :	      		# Verweis auf relevante Videoseite
			leftpos, leftstring = my_rfind('href=', 'class=\"icon video\"', page)	
			Log(leftstring)	
			video_url = BASE_URL + stringextract('href=\"', '\"', leftstring) # damit hierhin zurück
			oc = GetVideoSources(path=video_url,title=title,summary=summary,tagline=tagline, thumb=thumb)
			return oc			
		
	
	for video in videos:
		# Log(video)
		typ = stringextract('title="', '">', video)
		url = stringextract('href="', '"', video)
		pos = video.rfind('\">')		# Bsp.: ..h264.mp4">Klein (h264)</a>
		vtitel = video[pos:]
		vtitel = stringextract('\">', '</a>', vtitel)
		typ = typ + ' | ' + vtitel
		typ = unescape(typ)
		Log(typ); Log(url)
		# if url.find('.mp4') > 0:		# Beschränkung nicht sinnvoll, manchmal nur Audio-Dateien
		if url:
			oc.add(CreateVideoClipObject(url=url, title=title, 
				summary=summary, meta=path, thumb=thumb, tagline=typ, duration='', resolution=''))		
	
	Log(len(oc))					
	return oc

#-------------------------
@route(PREFIX + '/Bildgalerie')
def Bildgalerie(path, title):	
	Log('Bildgalerie'); Log(title); Log(path)
	
	page = HTTP.Request(path).content
	Log(len(page))
	segment =  stringextract('class=\"mod modA modGallery\">', 'class=\"section sectionA\">', page)	
	img_big = False		
	if segment.find('-videowebl.jpg') > 0:		# XL-Format vorhanden?  
		img_big = True		
	content =  blockextract('class=\"mediaLink\" href=\"#\">', '', segment)   					# Bild-Datensätze
	
			
	Log(len(content))
	# neuer Container mit neuem Titel
	title = 'Bildgalerie: ' + title.decode(encoding="utf-8", errors="ignore")
	oc = ObjectContainer(title2=title, view_group="InfoList")
	
	image = 1
	for rec in content:
		# Hinw.: letzter Satz ist durch section sectionA begrenzt
		# Log(rec)  # bei Bedarf
		thumb = BASE_URL + stringextract('class=\"img\" src=\"', '\"', rec)		
		if 	img_big == True:
			img_src = thumb[0:len(thumb)-5] + 'l.jpg'  # klein -> groß
		else:
			img_src = thumb

				
		title = stringextract('<img alt=\"', '\"', rec)
		summ = stringextract('teasertext colCnt\">', '</p>', rec)
						
		title = unescape(title)
		title = title.decode(encoding="utf-8", errors="ignore")
		summ = unescape(summ)
		summ = summ .decode(encoding="utf-8", errors="ignore")
		Log('neu');Log(title);Log(img_src);Log(summ[0:40]);
		oc.add(PhotoObject(
			key=img_src,
			rating_key='%s.%s' % (Plugin.Identifier, 'Bild ' + str(image)),	# rating_key = eindeutige ID
			summary=summ,
			title=title,
			thumb = img_src
			))
		image += 1
		# Variante CreatePhotoObject.py (s. Codestuecke)
		# oc.add(CreatePhotoObject(url=img_src, source_title=title, art=ART, title=summ))  
		
	return oc	
	
#####################################################################################################
@route(PREFIX + '/Livestream')	# Programm Heute + kommende Wochen. Alternative zu Verpasst (bei KIKA nicht verfügbar)
def Livestream(title):	
	Log('Livestream')
	oc = ObjectContainer(view_group="InfoList", title1=NAME, title2=title, art = ObjectContainer.art)
	oc = home(cont=oc)							# Home-Button
	
	url = ARD_m3u8

	thumb = R(ICON_LIVE)
	title = 'Bandbreite und Auflösung automatisch'
	summary = 'automatische Auflösung | Auswahl durch den Player'
	oc.add(CreateVideoStreamObject(url=url, title=title, summary=summary, tagline=title, meta='', thumb=thumb, 			
		rtmp_live='nein', resolution='960x540'))	# resolution ev. anpassen
	oc = Parseplaylist(oc, url, thumb)	# Liste der zusätzlichen einzelnen Auflösungen 
				
	return oc

#------------
@route(PREFIX + '/CreateVideoStreamObject')	# <- LiveListe, SingleSendung (nur m3u8-Dateien)
def CreateVideoStreamObject(url, title, summary, tagline, meta, thumb, rtmp_live, resolution, include_container=False, **kwargs): 
	Log('CreateVideoStreamObject: '); Log(url); Log(rtmp_live) 
	Log('include_container: '); Log(include_container)
	Log(Client.Platform)

#	oc.add(CreateVideoStreamObject(url=url, title=title, summary=summary, tagline=title, meta='', thumb=thumb, 			
#		rtmp_live='nein', resolution='960x540'))	# resolution ev. anpassen

	resolution=[1280,1024,720,540,480]# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
	meta=url						# leer (None) im Webplayer OK, mit PHT:  Server: Had trouble breaking meta
	mo = MediaObject(parts=[PartObject(key=HTTPLiveStreamURL(url=url))]) 
	rating_key = title
	videoclip_obj = VideoClipObject(					# Parameter wie MovieObject
		key = Callback(CreateVideoStreamObject, url=url, title=title, summary=summary,tagline=title,
		meta=meta, thumb=thumb, rtmp_live='nein', resolution=resolution, include_container=True), 
		rating_key=title,
		title=title,
		summary=summary,
		thumb=thumb,)
			
	videoclip_obj.add(mo)

	Log(url); Log(title); Log(summary); 
	Log(meta); Log(thumb); Log(rating_key); 
	
	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

#-----------------------------
@route(PREFIX + '/PlayVideo')  
def PlayVideo(url, **kwargs):	# resolution übergeben, falls im  videoclip_obj verwendet
	Log('PlayVideo: ' + url); 		# Log('PlayVideo: ' + resolution)
	return Redirect(url)
	
#-----------------------------
@route(PREFIX + '/CreateVideoClipObject')	#
def CreateVideoClipObject(url, title, summary, tagline, meta, thumb, duration, resolution, include_container=False, **kwargs):
	title = title.encode("utf-8")		# ev. für alle ausgelesenen Details erforderlich
	Log('CreateVideoClipObject')
	Log(url); Log(duration); Log(tagline)
	Log(Client.Platform)
	resolution=[1280,1024,720,540,480]	# wie VideoClipObject: Vorgabe für Webplayer entbehrlich, für PHT erforderlich
	if not duration:
		duration = 'duration'			# für PHT (leer nicht akzeptiert)

	videoclip_obj = VideoClipObject(
	key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, tagline=tagline,
		meta=meta, thumb=thumb, duration=duration, resolution=resolution, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		tagline = tagline,
		thumb = thumb,
		items = [
			MediaObject(
				parts = [
					# PartObject(key=url)						# reicht für Webplayer
					PartObject(key=Callback(PlayVideo, url=url)) 
				],
				container = Container.MP4,  	# weitere Video-Details für Chrome nicht erf., aber Firefox 
				video_codec = VideoCodec.H264,	# benötigt VideoCodec + AudioCodec zur Audiowiedergabe
				audio_codec = AudioCodec.AAC,	# 
				
			)  									# for resolution in [720, 540, 480, 240] # (in PlayVideo übergeben), s.o.
	])

	if include_container:						# Abfrage anscheinend verzichtbar, schadet aber auch nicht 
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

####################################################################################################
#									Hilfsfunktionen
#
def get_page(path):		# holt kontrolliert raw-Content
	Log('get_page')
	try:
		# 28.03.2018 Wechsel von HTTP.Request zu urllib2.Request, da der Inhalt von ../sendung/ts-24821.html nicht mehr 
		#	mehr mit dem Chrome-Ergebnis übereinstimmte und 'User-Agent' nicht half. 
		req = urllib2.Request(path)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		gcontext.check_hostname = False
		gcontext.verify_mode = ssl.CERT_NONE
		r = urllib2.urlopen(req, context=gcontext)
		page = r.read()					
		err = ''
	except:
		page = ''
		
	if page == '':	
		error_txt = 'Seite existiert nicht (mehr).'			 			 	 
		msgH = 'Fehler'; msg = error_txt + ' | Seite: ' + path
		Log(msg)
		msg =  msg.decode(encoding="utf-8", errors="ignore")
		err = ObjectContainer(header=msgH, message=msg)

	return page, err
		
#-----------------------------
def Parseplaylist(container, url_m3u8, thumb):		# master.m3u8 auswerten, Url muss komplett sein
#	Besonderheiten s. Plex-Plugin-ARDMediathek2016	

  Log ('Parseplaylist: ' + url_m3u8)
  playlist = ''
  # seit ZDF-Relaunch 28.10.2016 dort nur noch https
  if url_m3u8.find('http://') == 0 or url_m3u8.find('https://') == 0:		# URL oder lokale Datei?	
	try:
		playlist = HTTP.Request(url_m3u8).content  # als Text, nicht als HTML-Element
	except:
		if playlist == '':
			msg = 'Playlist kann nicht geladen werden. URL:\r'
			msg = msg + url_m3u8
			return ObjectContainer(message=msg)	  # header=... ohne Wirkung	(?)			
  else:													
	playlist = Resource.Load(url_m3u8) 
  # Log(playlist)   # bei Bedarf
	 
  lines = playlist.splitlines()
  #Log(lines)
  lines.pop(0)		# 1. Zeile entfernen (#EXTM3U)
  BandwithOld = ''	# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
  i = 0
  #for line in lines[1::2]:	# Start 1. Element, step 2
  for line in lines:	
 	line = lines[i].strip()
 	# Log(line)				bei Bedarf
	if line.startswith('#EXT-X-STREAM-INF'):# tatsächlich m3u8-Datei?
		url = lines[i + 1].strip()	# URL in nächster Zeile
		Log(url)

		Bandwith = GetAttribute(line, 'BANDWIDTH')
		Resolution = GetAttribute(line, 'RESOLUTION')
		if Resolution:	# fehlt manchmal (bei kleinsten Bandbreiten)
			Resolution = 'Auflösung ' + Resolution
		else:
			Resolution = 'Auflösung unbekannt'	# verm. nur Ton? CODECS="mp4a.40.2"
		Codecs = GetAttribute(line, 'CODECS')
		# als Titel wird die  < angezeigt (Sender ist als thumb erkennbar)
		if int(Bandwith) >  64000: 	# < 64000 vermutl. nur Audio, als Video keine Wiedergabe 
			title='Bandbreite ' + Bandwith
			if url.find('#') >= 0:	# Bsp. SR = Saarl. Rundf.: Kennzeichnung für abgeschalteten Link
				Resolution = 'zur Zeit nicht verfügbar!'
			if Bandwith == BandwithOld:	# Zwilling -Test
				title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			if url.startswith('http://') == False:   	# relativer Pfad? 
				pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
				url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
				
			Log(url); Log(title); Log(thumb); Log('Resolution')
			container.add(CreateVideoStreamObject(url=url, title=title, # Einbettung in DirectoryObject zeigt bei
				summary= Resolution, tagline='', meta=Codecs, thumb=thumb, 			# AllConnect trotzdem nur letzten Eintrag
				rtmp_live='nein', resolution=''))
			BandwithOld = Bandwith
			
		if url_m3u8.find('http://') < 0:		# lokale Datei
			if Prefs['pref_tvlive_allbandwith'] == False:	# nur 1. Eintrag
				return container

				
  	i = i + 1	# Index für URL
  #Log (len(container))	# Anzahl Elemente
  if len(container) == 0:	# Fehler, zurück zum Hauptmenü
  		container.add(DirectoryObject(key=Callback(Main),  title='inkompatible m3u8-Datei', 
			tagline='Kennung #EXT-X-STREAM-INF fehlt oder den Pfaden fehlt http:// ', thumb=thumb)) 
	
  return container

#----------------------------------------------------------------  
def GetAttribute(text, attribute, delimiter1 = '=', delimiter2 = ','):
# Bsp.: #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=61000,CODECS="mp4a.40.2"

    if attribute == 'CODECS':	# Trenner = Komma, nur bei CODEC ist Inhalt 'umrahmt' 
    	delimiter1 = '="'
    	delimiter2 = '"'
    x = text.find(attribute)
    if x > -1:
        y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
        z = text.find(delimiter2, y)
        if z == -1:
            z = len(text)
        return unicode(text[y:z].strip())
    else:
        return ''

#----------------------------------------------------------------  
def NotFound(msg):
    return ObjectContainer(
        header=u'%s' % L('Error'),
        message=u'%s' % (msg)
    )

#----------------------------------------------------------------  
def CalculateDuration(timecode):
	milliseconds = 0
	hours        = 0
	minutes      = 0
	seconds      = 0
	d = re.search('([0-9]{1,2}) min', timecode)
	if(None != d):
		minutes = int( d.group(1) )
	else:
		d = re.search('([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).([0-9]{1,3})', timecode)
		if(None != d):
			hours = int ( d.group(1) )
			minutes = int ( d.group(2) )
			seconds = int ( d.group(3) )
			milliseconds = int ( d.group(4) )
	milliseconds += hours * 60 * 60 * 1000
	milliseconds += minutes * 60 * 1000
	milliseconds += seconds * 1000
	return milliseconds
#----------------------------------------------------------------  
def stringextract(mFirstChar, mSecondChar, mString):  	# extrahiert Zeichenkette zwischen 1. + 2. Zeichenkette
	pos1 = mString.find(mFirstChar)						# return '' bei Fehlschlag
	ind = len(mFirstChar)
	#pos2 = mString.find(mSecondChar, pos1 + ind+1)		
	pos2 = mString.find(mSecondChar, pos1 + ind)		# ind+1 beginnt bei Leerstring um 1 Pos. zu weit
	rString = ''

	if pos1 >= 0 and pos2 >= 0:
		rString = mString[pos1+ind:pos2]	# extrahieren 
		
	# Log(mString); Log(mFirstChar); Log(mSecondChar); 	# bei Bedarf
	# Log(pos1); Log(ind); Log(pos2);  Log(rString); 
	return rString
#----------------------------------------------------------------  
def teilstring(zeile, startmarker, endmarker):  		# rfind: endmarker=letzte Fundstelle, return '' bei Fehlschlag
  # die übergebenen Marker bleiben Bestandteile der Rückgabe (werden nicht abgeschnitten)
  pos2 = zeile.find(endmarker, 0)
  pos1 = zeile.rfind(startmarker, 0, pos2)
  if pos1 & pos2:
    teils = zeile[pos1:pos2+len(endmarker)]	# 
  else:
    teils = ''
  #Log(pos1) Log(pos2) 
  return teils 
#----------------------------------------------------------------  
def blockextract(blockmark, blockendmark, mString):  # extrahiert Blöcke begrenzt durch blockmark aus mString
	#   Block wird durch blockendmark begrenzt, falls belegt 
	#	blockmark bleibt Bestandteil der Rückgabe
	#	Verwendung, wenn xpath nicht funktioniert (Bsp. Tabelle EPG-Daten www.dw.com/de/media-center/live-tv/s-100817)
	rlist = []				
	if 	blockmark == '' or 	mString == '':
		Log('blockextract: blockmark or mString leer')
		return rlist
	
	pos = mString.find(blockmark)
	if 	mString.find(blockmark) == -1:
		Log('blockextract: blockmark nicht in mString enthalten')
		# Log(pos); Log(blockmark);Log(len(mString));Log(len(blockmark));
		return rlist
		
	pos2 = 1
	while pos2 > 0:
		pos1 = mString.find(blockmark)						
		ind = len(blockmark)
		pos2 = mString.find(blockmark, pos1 + ind)		
		
		if blockendmark:
			pos3 = mString.find(blockendmark, pos1 + ind)
			ind_end = len(blockendmark)
			block = mString[pos1:pos3+ind_end]	# extrahieren einschl.  blockmark + blockendmark
			# Log(block)			
		else:
			block = mString[pos1:pos2]			# extrahieren einschl.  blockmark
			# Log(block)		
		mString = mString[pos2:]	# Rest von mString, Block entfernt
		rlist.append(block)
		# Log(rlist)
	# Log(rlist)		
	return rlist  
#----------------------------------------------------------------  	
def repl_char(cut_char, line):	# problematische Zeichen in Text entfernen, wenn replace nicht funktioniert
	line_ret = line				# return line bei Fehlschlag
	pos = line_ret.find(cut_char)
	while pos >= 0:
		line_l = line_ret[0:pos]
		line_r = line_ret[pos+len(cut_char):]
		line_ret = line_l + line_r
		pos = line_ret.find(cut_char)
		#Log(cut_char); Log(pos); Log(line_l); Log(line_r); Log(line_ret)	# bei Bedarf	
	return line_ret
#----------------------------------------------------------------  	
def unescape(line):	# HTML-Escapezeichen in Text entfernen, bei Bedarf erweitern. ARD auch &#039; statt richtig &#39;
#	s.a.  ../Framework/api/utilkit.py. 
#	Ersetzung teilweise nicht HTML-konform, sondern darstellungsgerecht.
	line_ret = (line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
		.replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", '"').replace("&#x27;", "'")
		.replace("&ouml;", "ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&szlig;", "ß")
		.replace("&Ouml;", "Ö").replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&apos;", "'")
		.replace("&nbsp;", "").replace("&#10;", " | ").replace("&#8211;", "-"))
		
	# Log(line_ret)		# bei Bedarf
	return line_ret	
#----------------------------------------------------------------  	
def cleanhtml(line): # ersetzt alle HTML-Tags zwischen < und >  mit 1 Leerzeichen
	cleantext = line
	cleanre = re.compile('<.*?>')
	cleantext = re.sub(cleanre, ' ', line)
	return cleantext
#----------------------------------------------------------------  	
def mystrip(line):	# Ersatz für unzuverlässige strip-Funktion
	line_ret = line	
	line_ret = line.replace('\t', '').replace('\n', '').replace('\r', '')
	line_ret = line_ret.strip()	
	# Log(line_ret)		# bei Bedarf
	return line_ret
#----------------------------------------------------------------  	
def my_rfind(left_pattern, start_pattern, line):  # sucht ab start_pattern rückwärts + erweitert 
#	start_pattern nach links bis left_pattern.
#	Rückgabe: Position von left_pattern und String ab left_pattern bis einschl. start_pattern	
#	Mit Python's rfind-Funktion nicht möglich

	# Log(left_pattern); Log(start_pattern); 
	if left_pattern == '' or start_pattern == '' or line.find(start_pattern) == -1:
		return -1, ''
	startpos = line.find(start_pattern)
	# Log(startpos); Log(line[startpos-10:startpos+len(start_pattern)]); 
	i = 1; pos = startpos
	while pos >= 0:
		newline = line[pos-i:startpos+len(start_pattern)]	# newline um 1 Zeichen nach links erweitern
		# Log(newline)
		if newline.find(left_pattern) >= 0:
			leftpos = pos						# Position left_pattern in line
			leftstring = newline
			# Log(leftpos);Log(newline)
			return leftpos, leftstring
		i = i+1				
	return -1, ''								# Fehler, wenn Anfang line erreicht
#----------------------------------------------------------------  	


