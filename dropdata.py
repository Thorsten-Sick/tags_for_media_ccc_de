#!/usr/bin/env python3

import json
import argparse
import os
import re
import xml.etree.ElementTree
import requests
import pathlib
from concurrent import futures
from collections import defaultdict
from pprint import pprint

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# For concurrent

MAX_WORKERS = 50

# TAGS
KEYNOTE = "keynote"
POLITICS = "politics"
INSIGHTS = "insights"
TECHNOLOGY = "technology"
ENGINEERING = "engineering"
SECURITY = "security"
ENTERTAINMENT = "entertainment"
BIO = "bio"  # hacking plants, people, genes ...
SCIENCE = "science"
BIOMETRICS = "biometrics"
AUTOMOTIVE = "automotive"   # automotive
IOT = "iot"  # internet of things
CRYPTO = "crypto"   # from maths to everything crypto
LAW = "law"
MALWARE = "malware"
HISTORY = "history"  # old computers, events happening loong time ago....
ACTIVISM = "activism"
HARDWARE = "hardware"  # generic hardware focus
SOFTWARE = "software"  # generic software focus
CONSOLE = "console"
AI = "ai"
NETWORK = "network"
WIRELESS = "wireless"  # WIFI BLUETOOTH, ...
WIFI = "wifi"
BLUETOOTH = "bluetooth"
FOOD = "food"   # Food hacking
PRIVACY = "privacy"
SOLUTION = "solution"  # All those proposals that could solve a problem of mankind
MAKING = "making"  # Maker stuff
TOR = "tor"
ROBOTICS = "robotics"
ELECTRONICS = "electronics"
BIGBROTHER = "bigbrother"  # all big-brother style state actions, not only surveillance
HACKING = "hacking"  # Do not attach to all talks....
ENERGY = "energy"  #  global warming, energy generation, ....
SPACE = "space"  # space technology, rockets and satellites
RFID = "rfid"  # RFID/NFC/Mifare
ART = "art"
FORENSIC = "forensic"
BANKING = "banking"
MOBILE = "mobile"
ASSEMBLER = "assembler"
SOCIETY = "society"
AVIATION = "aviation"
CLOUD = "cloud"
LOCKPICKING = "lockpicking"
EDUCATION = "education"
USB = "usb"
RESILIENCE = "resilience"
FREIFUNK = "freifunk"
SURVEILLANCE = "surveillance"
CENSORSHIP = "censorship"
OS = "os"  # Operating system stuff
KERNEL = "kernel"  # OS kernel stuff
ANARCHY = "anarchy"
TRAVEL = "travel"
FUZZING = "fuzzing"
ASAN = "asan"
AFL = "afl"
LIBFUZZER = "libfuzzer"
IFG = "ifg"
LORA = "lora"
VM = "vm"  # virtual machines
SCADA = "scada"
APPLE = "apple"
INTEL = "intel"
MICROSOFT = "microsoft"
OS = "os"  # Operating system
LINUX = "linux"
BSD = "bsd"
CONTAINER = "container"
WEB = "web"
SERVER = "server"
OPENSOURCE = "opensource"
BROWSER = "browser"
SMARTHOME = "smarthome"
DIY = "diy"
DATABASE = "database"
LATEX = "latex"
PYTHON = "python"
RUBY = "ruby"
LISP = "lisp"
CPP = "c++"
JAVA = "java"
INKSCAPE = "inkscape"
GRAPHICS = "graphics"
JAVASCRIPT = "javascript"
PERL = "perl"
OPENSTREETMAP = "openstreetmap"
PODCAST = "podcast"
WEBSERVER = "webserver"
HONEYPOT = "honeypot"
TESTING = "testing"
IMAGEMAGICK = "imagemagick"
MESSENGER = "messenger"
FREIFUNK = "freifunk"
KEYNOTE = "keynote"
OPENING = "opening"
LIGHTNINGTALKS = "lightningtalks"
LEARNING = "learning"
WORDPRESS = "wordpress"
WIKI = "wiki"
ADMINISTRATION = "administration"
MUSIC = "music"
ALGORITHMS = "algorithms"
NAVIGATION = "navigation"
GAMES = "games"

# Detailed Tags (let's find out if there are more than 3 talks deserving those tags)

## Anonymisation networks
I2P = "i2p"
FREENET = "freenet"
GNUNET = "gnunet"
JONDONYM = "jondonym"
LOOPIX = "loopix"
VUVUZELA = "vuvuzela"
SSH = "ssh"

## Hardware hacking tools
CHIPWHISPERER = "chipwhisperer"
GLITCHKIT = "glitchkit"
FACEDANCER = "facedancer"
HACKRF = "hackrf"
PROXMARK = "proxmark"
UBERTOOTH = "ubertooth"
OSMOCOM = "osmocom"

SHODAN = "shodan"

ANDROID = "android"
IOS = "ios"
JTAG = "jtag"
FPGA = "fpga"
EEPROM = "eeprom"
NINTENDO = "nintendo"
ARM = "arm"

#SERIES
SECURITY_NIGHTMARES = "security nightmares"
METHODISCH_INKORREKT = "methodisch inkorrekt"  # TODO
ULTIMATE_TALK = "ultimate talks"
INFRASTRUCTURE_REV = "infrastructure review" # TODO


#################################
# Not all tags are created equal. Topics are common main topics.
# I choose common ones and also use the tracks from the Fahrplan
topics = set([SOFTWARE, HARDWARE, NETWORK, SECURITY, POLITICS, SCIENCE, ART, RESILIENCE])

# There are also subtags and tags
# "tags" are normal tags
# "subtags" are very uncommon tags we will not display but keep around. Maybe they will become common sometimes
SUBTAG_THRESHOLD = 35  # At the moment: The number of congresses so far

# "fulltags" will be the full list of raw tags extracted from the sources





##################################

regexes = {r"\Wrfid\W": [RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Wmifare\W": [RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Whitag\W": [RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Wgeheimdienste?\W": [BIGBROTHER, POLITICS],
           r"\Wgchq?\W": [BIGBROTHER, POLITICS],
           r"\Wnsa?\W": [BIGBROTHER, POLITICS],
           r"\Wsatellite\W": [SPACE],
           r"\Wlulzsec\W": [ACTIVISM],
           r"\Warab spring\W": [POLITICS, ACTIVISM],
           r"\Wedward snowden\W": [POLITICS, ACTIVISM, PRIVACY],
           r"\Wtor\W": [NETWORK, PRIVACY, TOR, CRYPTO],
           r"\Wdragnet surveillance system\W": [NETWORK, PRIVACY, BIGBROTHER, SURVEILLANCE, POLITICS],
           r"\Wquantenphysik\W": [SCIENCE],
           r"\Wrelativitätstheorie\W": [SCIENCE],
           r"\Walbert einstein\W": [SCIENCE],
           r"\Wdigital surveillance\W": [NETWORK, PRIVACY, BIGBROTHER, POLITICS],
           r"\Wactivism\W": [ACTIVISM],
           r"\Wquadraturdunet\W": [ACTIVISM],
           r"\Wngo\W": [ACTIVISM],
           r"\Wlegal issues\W": [LAW, POLITICS],
           r"\Wcryptographic\W": [CRYPTO],
           r"\Wcryptography\W": [CRYPTO],
           r"\Wnetzpolitik\W": [LAW, POLITICS, NETWORK],
           r"\Wbreitbandinternet\W": [LAW, POLITICS, NETWORK],
           r"\Winternetminister\W": [LAW, POLITICS, NETWORK],
           r"\Wpredective policing\W": [LAW, POLITICS, BIGBROTHER],
           r"\Wcreditscoring\W": [LAW, POLITICS, BIGBROTHER],
           r"\Wexploit\W": [HACKING, SECURITY],
           r"\Wbuffer overflow\W": [HACKING, SECURITY],
           r"\Wvulnerability\W": [HACKING, SECURITY],
           r"\Wshellcode\W": [HACKING, SECURITY],
           r"\Wfingerkuppe\W": [BIO],
           r"\Wfingernagel\W": [BIO],
           r"\Wschmuckkunst\W": [ART],
           r"\Wforensic\W": [FORENSIC],
           r"\Wpolice\W": [LAW, POLITICS],
           r"\Wiot\W": [IOT, HARDWARE],
           r"\Wformally verified software\W": [ENGINEERING, SOFTWARE, SECURITY],
           r"\Wpersonal data\W": [PRIVACY],
           r"\Wmobilebanking\W": [MOBILE, BANKING],
           r"\Wonlinebanking\W": [NETWORK, BANKING],
           r"\Wzwei-faktor\W": [SECURITY],
           r"\Wtwo-factor\W": [SECURITY],
           r"\Wzertifikat\W": [SECURITY],
           r"\Wsocial credit system\W": [LAW, POLITICS, BIGBROTHER],
           r"\Wsociety\W": [POLITICS, SOCIETY],
           r"\Wbgp\W": [NETWORK],
           r"\Wandroid\W": [MOBILE],
           r"\Wboot ?loader\W": [SOFTWARE],
           r"\Wida\W": [SOFTWARE, SECURITY, ASSEMBLER],
           r"\Wassembler\W": [SOFTWARE, ASSEMBLER],
           r"\Wamendment\W": [LAW],
           r"\Wreaper drone\W": [POLITICS, AVIATION],
           r"\Wmri\W": [BIO, SCIENCE],
           r"\Weeg\W": [BIO, SCIENCE],
           r"\Wtomography\W": [BIO, SCIENCE],
           r"\Wbiomedical\W": [BIO, SCIENCE],
           r"\Wfitbit\W": [BIO, HARDWARE],
           r"\Wsecurity\W": [SECURITY],
           r"\Wencryption\W": [CRYPTO],
           r"\Wfirmware\W": [HARDWARE, SOFTWARE],
           r"\Wreverse engineering\W": [HACKING, SECURITY],
           r"\Welektroautos?\W": [AUTOMOTIVE],
           r"\Wladeinfrastruktur\W": [AUTOMOTIVE],
           r"\Wdieselgate\W": [AUTOMOTIVE],
           r"\Wcan bus\W": [AUTOMOTIVE],
           r"\Wseawatch\W": [ACTIVISM, POLITICS],
           r"\Wjugend rettet\W": [ACTIVISM, POLITICS],
           r"\Wmsf\W": [ACTIVISM, POLITICS],
           r"\Wchaos macht schule\W": [ACTIVISM, POLITICS, EDUCATION],
           r"\Wcaliope\W": [HARDWARE, SOFTWARE, EDUCATION],
           r"\Wtcp\W": [NETWORK],
           r"\Wvlan\W": [NETWORK],
           r"\Wpci express\W": [HARDWARE],
           r"\Wnics?\W": [HARDWARE, NETWORK],
           r"\Wnintendo\W": [CONSOLE, NINTENDO],
           r"\Wblockchains?\W": [CRYPTO],
           r"\Wopensource\W": [SOFTWARE, OPENSOURCE],
           r"\Wopen-source\W": [SOFTWARE, OPENSOURCE],
           r"\Wopen source\W": [SOFTWARE, OPENSOURCE],
           r"\Wstaatsanwalt\W": [LAW],
           r"\Wanwälte\W": [LAW],
           r"\Wabmahnanwälte\W": [LAW],
           r"\Wfake news\W": [POLITICS, SOCIETY],
           r"\Wlügenpresse\W": [POLITICS, SOCIETY],
           r"\Wdata-science\W": [SCIENCE],
           r"\Wcertificate transparency\W": [CRYPTO],
           r"\Wsha1\W": [CRYPTO],
           r"\Wtls\W": [CRYPTO],
           r"\Wsha256\W": [CRYPTO],
           r"\Wmd5\W": [CRYPTO],
           r"\Wcypher\W": [CRYPTO],
           r"\Wstarttls\W": [CRYPTO],
           r"\Wperfect forward secrecy\W": [CRYPTO],
           r"\Wman-in-the-middle\W": [CRYPTO, HACKING, NETWORK],
           r"\Waktivisten\W": [ACTIVISM],
           r"\Wrouterzwang\W": [NETWORK, WIFI, POLITICS],
           r"\Wcensorship\W": [POLITICS, BIGBROTHER],
           r"\Wfatca\W": [BANKING, POLITICS],
           r"\Wmobile networks?\W": [MOBILE, NETWORK],
           r"\Wmobile phones?\W": [MOBILE],
           r"\Wsurveillance\W": [BIGBROTHER, POLITICS],
           r"\Wbluetooth\W": [WIFI, BLUETOOTH, HARDWARE],
           r"\Wps3\W": [CONSOLE],
           r"\Wgame boy\W": [CONSOLE],
           r"\Waircraft\W": [AVIATION],
           r"\Wpopulisten\W": [SOCIETY],
           r"\Wwhistleblower\W": [SOCIETY, ACTIVISM, POLITICS],
           r"\Wparagrafen\W": [LAW],
           r"\Whdmi\W": [HARDWARE],
           r"\Wamazon aws\W": [CLOUD],
           r"\Ws3\W": [CLOUD],
           r"\Wcloudfront\W": [CLOUD],
           r"\Wgenetic fingerprint\W": [BIO],
           r"\Wgenome\W": [BIO, SCIENCE],
           r"\Wdna\W": [BIO, SCIENCE],
           r"\Wanti-terror-kampf\W": [POLITICS],
           r"\Wurheberrecht\W": [POLITICS, LAW],
           r"\Wspread spectrum technology\W": [WIFI],
           r"\Wlhc\W": [SCIENCE],
           r"\Whiggs\W": [SCIENCE],
           r"\Wcern\W": [SCIENCE],
           r"\Whadron\W": [SCIENCE],
           r"\Wfragdenstaat\W": [ACTIVISM, POLITICS, LAW],
           r"\Winformationsfreiheitsgesetz\W": [ACTIVISM, POLITICS, LAW],
           r"\Wnet neutrality\W": [NETWORK, POLITICS, LAW],
           r"\Wgalaxy\W": [SPACE],
           r"\Wbiochemie\W": [SCIENCE, BIO],
           r"\Wmikroskop\W": [SCIENCE],
           r"\Wecu\W": [AUTOMOTIVE],
           r"\Wvolkswagen\W": [AUTOMOTIVE],
           r"\Wbotnet\W": [MALWARE],
           r"\Wmalware\W": [MALWARE],
           r"\Wtrojaner\W": [MALWARE],
           r"\Wcompiler\W": [SOFTWARE, ASSEMBLER],
           r"\Wmicrocontroller\W": [HARDWARE],
           r"\Wlogjam\W": [CRYPTO],
           r"\Wdiffie-hellman\W": [CRYPTO],
           r"\Wblackout\W": [IOT],
           r"\Wtan\W": [BANKING],
           r"\Wbandwidth\W": [NETWORK],
           r"\Wlasers?\W": [SCIENCE],
           r"\Wiridium\W": [NETWORK, MOBILE, SPACE],
           r"\Wsocial media\W": [SOCIETY],
           r"\Wheart monitor\W": [BIO, SCIENCE],
           r"\Wweltall\W": [SPACE],
           r"\Wgrundrechte\W": [POLITICS, LAW],
           r"\Wanonymous communication\W": [PRIVACY],
           r"\Wprofiling\W": [PRIVACY],
           r"\Wdprk\W": [POLITICS],
           r"\Wnsaua\W": [POLITICS],
           r"\Wfreifunk\W": [NETWORK, WIFI, ACTIVISM, FREIFUNK, RESILIENCE],
           r"\Wgeflüchtete\W": [POLITICS, ACTIVISM],
           r"\Wlandesverrat\W": [POLITICS, ACTIVISM],
           r"\Wbig brother\W": [POLITICS, BIGBROTHER],
           r"\Wuefi\W": [SOFTWARE],
           r"\Wlet's encrypt\W": [SOFTWARE, CRYPTO, NETWORK],
           r"\Weff\W": [ACTIVISM, LAW, POLITICS],
           r"\W3g\W": [NETWORK, MOBILE, WIFI],
           r"\Wgpg\W": [CRYPTO],
           r"\Watm\W": [BANKING],
           r"\Wdatenschutz\W": [POLITICS, LAW, PRIVACY],
           r"\Wi2p\W": [NETWORK, CRYPTO, SECURITY, I2P],
           r"\Wfreenet\W": [NETWORK, CRYPTO, SECURITY, FREENET],
           r"\Wgnunet\W": [NETWORK, CRYPTO, SECURITY, GNUNET],
           r"\Wjondonym\W": [NETWORK, CRYPTO, SECURITY, JONDONYM],
           r"\Wloopix\W": [NETWORK, CRYPTO, SECURITY, LOOPIX],
           r"\Wchipwhisperer\W": [HARDWARE, HACKING, SECURITY, CHIPWHISPERER],
           r"\Wglitchkit\W": [HARDWARE, HACKING, SECURITY, GLITCHKIT],
           r"\Wfacedancer\W": [HARDWARE, HACKING, SECURITY, FACEDANCER, USB],
           r"\Wgoodfet\W": [HARDWARE, HACKING, SECURITY, FACEDANCER],
           r"\Whackrf\W": [HARDWARE, HACKING, SECURITY, HACKRF],
           r"\Wrad1o\W": [HARDWARE, HACKING, SECURITY, HACKRF],
           r"\Wrad10\W": [HARDWARE, HACKING, SECURITY, HACKRF],
           r"\Wproxmark3?\W": [HARDWARE, HACKING, SECURITY, PROXMARK, RFID],
           r"\Wubertooth\W": [HARDWARE, HACKING, SECURITY, UBERTOOTH, BLUETOOTH],
           r"\Wobd-ii\W": [AUTOMOTIVE, HARDWARE],
           r"\Wshodan\W": [NETWORK, HACKING, IOT, HARDWARE],
           r"\Wswift\W": [BANKING],
           r"\Wfingerabdruckscanner\W": [BIOMETRICS],
           r"\Wfingerabdrucksensor\W": [BIOMETRICS],
           r"\Wfingerabdruckdaten\W": [BIOMETRICS, PRIVACY],
           r"\Wfingerprint reader\W": [BIOMETRICS],
           r"\Wbiometrie\W": [BIOMETRICS, SECURITY],
           r"\Wbiometrisch\W": [BIOMETRICS, SECURITY],
           r"\Wvenenerkennung\W": [BIOMETRICS, SECURITY],
           r"\Wpassword\W": [SECURITY],
           r"\Wpasswort\W": [SECURITY],
           r"\Wjtag\W": [JTAG, ELECTRONICS],
           r"\Weeprom\W": [EEPROM, ELECTRONICS],
           r"\Wfpgas?\W": [FPGA, ELECTRONICS],
           r"\Wfuzzing\W": [FUZZING, SECURITY, SOFTWARE, TESTING],
           r"\Wasan\W": [ASAN, SECURITY, SOFTWARE],
           r"\Wafl\W": [FUZZING, SECURITY, SOFTWARE, AFL, TESTING],
           r"\Wlibfuzzer\W": [FUZZING, SECURITY, SOFTWARE, LIBFUZZER, TESTING],
           r"\Wparticle accelerators?\W": [SCIENCE],
           r"\Wembedded systems?\W": [IOT],
           r"\Wgpio\W": [IOT],
           r"\Wlora\W": [LORA],
           r"\Wartist\W": [ART],
           r"\Wvirtual machines?\W": [VM],
           r"\Wkvm\W": [VM],
           r"\Wvirtual box\W": [VM],
           r"\Wqemu\W": [VM],
           r"\Wscada\W": [IOT, SCADA],
           r"\Windustrial control systems?\W": [IOT, SCADA],
           r"\Wmacbooks?\W": [APPLE],
           r"\Wmac\W": [APPLE],
           r"\Wimac\W": [APPLE],
           r"\Wx86\W": [HARDWARE, INTEL],
           r"\Wcpu\W": [HARDWARE],
           r"\Wwindows\W": [MICROSOFT, OS],
           r"\Wwindows drivers?\W": [MICROSOFT, OS],
           r"\Wwindows kernel driver\W": [MICROSOFT, OS],
           r"\Wcable modem\W": [NETWORK],
           r"\Wembedded devices?\W": [IOT],
           r"\Wsystem abuse\W": [SECURITY],
           r"\Wapt\W": [SECURITY, MALWARE, POLITICS],
           r"\Wfiber optic cables?\W": [NETWORK],
           r"\Wplcs?\W": [IOT],
           r"\Whardware design\W": [HARDWARE],
           r"\Wprogramming\W": [SOFTWARE],
           r"\Wamiga 500\W": [HARDWARE, HISTORY],
           r"\Wamiga 1000\W": [HARDWARE, HISTORY],
           r"\Wrobot\W": [HARDWARE],
           r"\Wlinux\W": [OS, LINUX],
           r"\Wnetwork\W": [NETWORK],
           r"\Wnetzwerk\W": [NETWORK],
           r"\Wdocker\W": [CONTAINER],
           r"\Wansible\W": [CONTAINER],
           r"\Wvagrant\W": [CONTAINER],
           r"\Wapache\W": [WEB, SERVER, NETWORK, WEBSERVER],
           r"\Wnginx\W": [WEB, SERVER, NETWORK, WEBSERVER],
           r"\Whttp/2\.0\W": [WEB,  NETWORK],
           r"\Whttp header\.0\W": [WEB,  NETWORK],
           r"\Wrest\W": [WEB,  NETWORK],
           r"\Wpgp\W": [CRYPTO, PRIVACY],
           r"\Wbrowsersecurity\W": [WEB, BROWSER, SECURITY],
           r"\Wbrowser security\W": [WEB, BROWSER, SECURITY],
           r"\Wbrowser\W": [WEB, BROWSER],
           r"\Winternet\W": [NETWORK],
           r"\W802.11\W": [NETWORK, WIFI],
           r"\Wmidi\W": [ART, HARDWARE],
           r"\Wtheater\W": [ART],
           r"\Wios\W": [OS, IOS, APPLE],
           r"\Wspace\W": [SPACE, SCIENCE],
           r"\Winterplanetary\W": [SPACE, SCIENCE],
           r"\Wartificial intelligence\W": [AI],
           r"\Wextraterrestrial\W": [SPACE, SCIENCE],
           r"\Wdnssec\W": [NETWORK, SECURITY],
           r"\Wipsec\W": [NETWORK, SECURITY],
           r"\Wfirewalls?\W": [NETWORK, SECURITY],
           r"\Wipv6\W": [NETWORK],
           r"\Wraspberry pi\W": [HARDWARE],
           r"\Wsmart ?home\W": [SMARTHOME, IOT],
           r"\Warduino\W": [IOT, SOFTWARE, HARDWARE, DIY, ELECTRONICS],
           r"\Wsamba4?\W": [NETWORK],
           r"\Wsql\W": [DATABASE],
           r"\Wmysql\W": [DATABASE],
           r"\Wmongodb\W": [DATABASE],
           r"\Wcouchbase\W": [DATABASE],
           r"\Wcouchdb\W": [DATABASE],
           r"\Wpostgresql\W": [DATABASE],
           r"\Wnosql\W": [DATABASE],
           r"\Whtml5?\W": [WEB, SOFTWARE, BROWSER],
           r"\Wcss\W": [WEB, SOFTWARE, BROWSER],
           r"\Wbsd\W": [BSD, OS],
           r"\Wlatex\W": [LATEX],
           r"\Wpython\W": [PYTHON, SOFTWARE],
           r"\Wruby\W": [RUBY, SOFTWARE],
           r"\Wlisp\W": [LISP, SOFTWARE],
           r"\Wdjango\W": [PYTHON, SOFTWARE, WEB],
           r"\Wfedora\W": [LINUX, OS],
           r"\Winkscape\W": [INKSCAPE, GRAPHICS],
           r"\Wjavascript\W": [JAVASCRIPT, SOFTWARE],
           r"\Wopenstreetmap\W": [OPENSTREETMAP],
           r"\Wosm\W": [OPENSTREETMAP],
           r"\Wpodcast\W": [PODCAST],
           r"\Wpodlove\W": [PODCAST],
           r"\Wkeysigning\W": [CRYPTO, PRIVACY],
           r"\Wwebserver\W": [WEB, WEBSERVER],
           r"\Wdatabase\W": [DATABASE],
           r"\Wlamp\W": [DATABASE, WEBSERVER, WEB],
           r"\Wddos\W": [NETWORK, SECURITY],
           r"\Whoneypots?\W": [SECURITY, HONEYPOT],
           r"\Wcuckoo sandbox\W": [SECURITY, HONEYPOT],
           r"\Wunit testing\W": [TESTING],
           r"\Wterraforming\W": [SCIENCE],
           r"\Whydroponics\W": [SCIENCE],
           r"\Wmusical\W": [ART],
           r"\Wstaatstrojaner\W": [SECURITY, POLITICS, BIGBROTHER],
           r"\Wcarhacking\W": [AUTOMOTIVE, SECURITY, HARDWARE],
           r"\Welectric guitars?\W": [ART],
           r"\Wmoon\W": [SCIENCE, SPACE],
           r"\Wraumfahrt\W": [SCIENCE, SPACE],
           r"\Welectronics\W": [HARDWARE],
           r"\Welektronik\W": [HARDWARE],
           r"\Wunix\W": [LINUX, BSD, OS],
           r"\Wchemie\W": [SCIENCE],
           r"\Wperl\W": [SOFTWARE, PERL],
           r"\Wdemokratie\W": [POLITICS],
           r"\Wc\+\+\W": [CPP, SOFTWARE],
           r"\Wjava\W": [JAVA, SOFTWARE],
           r"\Wscience\W": [SCIENCE],
           r"\Wwar on terror\W": [POLITICS],
           r"\Wdespot\W": [POLITICS],
           r"\Wauthentifizieren\W": [SECURITY],
           r"\Wfiber optics\W": [NETWORK],
           r"\Wpodcasting\W": [PODCAST],
           r"\Wkinkygeeks\W": [SOCIETY],
           r"\Wsticken\W": [HARDWARE, DIY],
           r"\Wstaat\W": [POLITICS],
           r"\Wgesetze?\W": [POLITICS],
           r"\Wdrugs\W": [POLITICS, SCIENCE, BIO],
           r"\Wlockpicking\W": [SECURITY, HARDWARE],
           r"\Wschmuck\W": [ART],
           r"\Wjewellery\W": [POLITICS],
           r"\Wwebsocket\W": [WEB, SOFTWARE, BROWSER],
           r"\Wagile\W": [ENGINEERING],
           r"\Wretrospektive\W": [ENGINEERING],
           r"\Wbioinformatik\W": [SCIENCE, BIO, SOFTWARE],
           r"\Wctf\W": [SECURITY],
           r"\Wimagemagick\W": [GRAPHICS, IMAGEMAGICK],
           r"\Wamnesty international\W": [ACTIVISM, POLITICS],
           r"\Wwahl\W": [POLITICS],
           r"\Wwahlen\W": [POLITICS],
           r"\Welections?\W": [POLITICS],
           r"\Wcyborgs?\W": [BIO, HARDWARE, SCIENCE],
           r"\Wdistilling\W": [DIY, FOOD],
           r"\Wschnaps\W": [DIY, FOOD],
           r"\Wbeer\W": [DIY, FOOD],
           r"\Wmachine learning\W": [AI, SOFTWARE],
           r"\Wparlament\W": [POLITICS],
           r"\Wparlamenten\W": [POLITICS],
           r"\Wjabber\W": [NETWORK, MESSENGER],
           r"\Wxmpp\W": [NETWORK, MESSENGER],
           r"\Wwhatsapp\W": [NETWORK, MESSENGER],
           r"\Wthreema\W": [NETWORK, MESSENGER, PRIVACY],
           r"\Womemo\W": [NETWORK, MESSENGER, PRIVACY],
           r"\Wbsi\W": [POLITICS],
           r"\Wcryptoparties\W": [CRYPTO, SECURITY, PRIVACY],
           r"\Wcrypto partys?\W": [CRYPTO, SECURITY, PRIVACY],
           r"\Wkeynote\W": [KEYNOTE],
           r"\Wglasfasern?\W": [NETWORK],
           r"\Wlightning talks\W": [LIGHTNINGTALKS],
           r"\Wlightning-talks\W": [LIGHTNINGTALKS],
           r"\Wlernen\W": [EDUCATION],
           r"\Wbildung\W": [EDUCATION],
           r"\Wopening\W": [OPENING],
           r"\Wwordpress\W": [WORDPRESS],
           r"\Wwiki\W": [WIKI],
           r"\Wwikipedia\W": [WIKI],
           r"\Wfree software\W": [OPENSOURCE],
           r"\Wowasp\W": [SECURITY, SOFTWARE, WEB],
           r"\Wsysadmin\W": [ADMINISTRATION],
           r"\Wadmin\W": [ADMINISTRATION],
           r"\Wkunst\W": [ART],
           r"\Wart\W": [ART],
           r"\Wgulaschausgabe\W": [FOOD],
           r"\Wdj-set:\W": [MUSIC],
           r"\Wliveset\W": [MUSIC],
           r"\Wdata compression\W": [ALGORITHMS, SOFTWARE],
           r"\Wastrophysik\W": [SPACE, SCIENCE],
           r"\Wgit\W": [ENGINEERING],
           r"\Wbrainfuck\W": [SOFTWARE],
           r"\Walgorithmic\W": [ALGORITHMS, SOFTWARE],
           r"\Wtrojan\W": [MALWARE, SECURITY],
           r"\Wsoftware patent": [POLITICS],
           r"\Wcnc machine\W": [HARDWARE, DIY],
           r"\Wprivacy law": [POLITICS, PRIVACY, LAW],
           r"\Wred cross": [ACTIVISM],
           r"\Wmedicin sans frontier": [ACTIVISM],
           r"\Wchiptune\W": [ART],
           r"\Wnanoloop\W": [ART],
           r"\Wnorth korea\W": [POLITICS],
           r"\Wssh\W": [SSH, NETWORK, SECURITY, PRIVACY],
           r"\Wosmocom\W": [OSMOCOM, NETWORK],
           r"\Wplone\W": [SOFTWARE],
           r"\Wlpi certifica": [LINUX],
           r"\Wgps\W": [NAVIGATION],
           r"\Wgalileo\W": [NAVIGATION],
           r"\Wglonass\W": [NAVIGATION],
           r"\Wminecraft\W": [GAMES],
           r"\Wgeocaching\W": [GAMES, NAVIGATION],
           r"\Wgnome\W": [LINUX, SOFTWARE],
           r"\Wgovernment\W": [POLITICS],
           r"\Wsystemd\W": [LINUX, SOFTWARE],
           r"\Wsnmp\W": [NETWORK],
           r"\Wreproducible build": [SOFTWARE, SECURITY],
           r"\Wcontinuous delivery\W": [SOFTWARE],
           r"\Wkubernetes\W": [SOFTWARE, CLOUD, CONTAINER],
           r"\Wsicherheit\W": [SECURITY],
           r"\Wedri\W": [POLITICS, ACTIVISM],
           r"\Wmethodisch inkorrekt\W": [METHODISCH_INKORREKT, SCIENCE],
           r"\Wsoftwareentwicklung\W": [SOFTWARE],
           r"\Wclimate change\W": [POLITICS, SCIENCE],
           r"\Wtreibhausgas": [POLITICS, SCIENCE],
           r"\Wdrm\W": [POLITICS, CENSORSHIP, SOFTWARE],
           r"\Wkryptographie\W": [SOFTWARE, SECURITY, CRYPTO],

           }

# TODO: create object oriented code

# TODO: extract tags and stuff into db



# See: https://github.com/voc/voctoweb/issues/246
voctoweburl = "https://api.media.ccc.de/public/conferences"


#def get_congress(filename):
#    return filename.split("-")[0]

class MediaTagger():

    def __init__(self):
        pass

    def get_id(self, filename):
        return filename.split("-")[1]


    def text_to_tags(self, text):
        """ Generate tags from a string """

        res = []
        text = text.lower()
        for akey in regexes.keys():
            if re.search(akey, text, re.MULTILINE):
                res += regexes[akey]

        return list(set(res))


    def get_tags(self, filename):
        res = []
        with open(filename, "rt") as fh:
            content = fh.read().lower()
            res = self.text_to_tags(content)
        return res


    def from_subtitles(self, directory):
        # TODO: Can we automatically find more subtitles ?
        res = {}

        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".srt"):
                    fullname = os.path.join(root, name)
                    print(fullname)
                    tags = self.get_tags(fullname)
                    print(tags)
                    talkid = self.get_id(name)
                    if talkid not in res:
                        res[talkid] = tags
                    else:
                        res[talkid] = list(set(res[talkid] + tags))
        return res


    # FRAB

    def from_voctoweb_data(self, data):
        """
        Transfers voctoweb style data into data we can handle
        :param data: voctoweb style json data as dict
        :return:
        """

        res = []
        for entry in data["conferences"]:
            if "acronym" in entry and "schedule_url" in entry and \
                    entry["schedule_url"] and \
                    len(entry.get("acronym", "")) > 0 and \
                    len(entry.get("schedule_url", "")) > 0 and \
                    entry["schedule_url"].startswith("http"):
                res.append((entry["schedule_url"], entry["acronym"]))
        return res

    def from_voctoweb(self):
        """ Use the voctoweb database and extract complete acronym/schedule-url pairs"""

        r = requests.get(voctoweburl)
        res = None
        if r.status_code == requests.codes.ok:
            data = r.json()
            # TODO: Are there any broken entries ?
            # TODO: Use acronym, schedule_url, title, event_last_released_at
            res = self.from_voctoweb_data(data)
        return res


    def download_one(self, entry):
        """ Download one entry in the schedule.xml list """
        url, acronym = entry
        filename = "data/"+acronym+".xml"
        if not pathlib.Path(filename).is_file():
            try:
                r = requests.get(url)
                print(url)
                if r.status_code == requests.codes.ok:
                    with open(filename, "w") as fh:
                        fh.write(r.text)
            except requests.exceptions.MissingSchema:
                print("Error: Broken url: " + url)
            except requests.exceptions.ConnectionError:
                print("Error: Connection error url: " + url)
        else:
            print("Already have file {}".format(filename))

    def from_frabs(self, offline=False):
        """
        offline: Do not download detailed frabs, use existing files only
        """
        collected = {}

        combined_fraps = []
        #with open("manufactured_data/essential_conferences.json") as fh:
        #    data = json.load(fh)
        #    combined_fraps = self.from_voctoweb_data(data)
        combined_fraps += self.from_voctoweb()
        combined_fraps = list(set(combined_fraps))


        # Getting files
        # Todo: optimize

        if not offline:
            workers = min(MAX_WORKERS, len(combined_fraps))
            with futures.ThreadPoolExecutor(workers) as executor:
                res = executor.map(self.download_one, combined_fraps)

        print("# Processing")
        # reading files
        for url, acronym in combined_fraps:
            filename = "data/"+acronym+".xml"
            print(filename)
            try:
                e = xml.etree.ElementTree.parse(filename).getroot()
            except FileNotFoundError:
                print("Error: Missing file {}".format(filename))
            except xml.etree.ElementTree.ParseError:
                print("Error: Broken file {}".format(filename))
            else:
                for days in e.findall('day'):
                    for rooms in days.findall("room"):
                        for event in rooms.findall("event"):
                            e = {}
                            try:
                                e["guid"] = event.attrib["guid"]
                            except KeyError:
                                e["guid"] = None
                            e["id"] = event.attrib["id"]
                            e["title"] = event.find("title").text
                            e["subtitle"] = event.find("subtitle").text
                            e["abstract"] = event.find("abstract").text
                            e["description"] = event.find("description").text
                            try:
                                e["slug"] = event.find("slug").text
                            except AttributeError:
                                e["slug"] = None
                            e["fulltags"] = self.text_to_tags("{title} {subtitle} {abstract} {description}".format(**e))

                            e["acronym"] = acronym
                            if e["guid"]:
                                collected[e["guid"]] = e
        return collected

    # Defaults

    def simplify_defaults(self):
        res = {}
        with open("manufactured_data/talks.json") as fh:
            dt = json.load(fh)
            for talk in dt:
                res[talk["id"]] = talk["fulltags"]
        return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subtitles", help="Process subtitles folder. Output json", default = None, type=str)
    parser.add_argument("--out", help="out filename. Without postfix .json or .yaml. This will be added", default = None, type = str)
    parser.add_argument("--default", help="Load hard coded default talks as well", action="store_true", default = False)
    parser.add_argument("--frab", help="Use frabs to generate data", action="store_true", default = False)
    parser.add_argument("--statistics", help="calculate and write statistics for the tags", action="store_true", default=False)
    parser.add_argument("--offline", help="Do not try to fetch data online. Use existing files", action="store_true", default=False)

    args = parser.parse_args()

    talks = {}
    mt = MediaTagger()

    if args.frab:
        talks = mt.from_frabs(args.offline)

    # Generate db from subtitles
    # Subtitles are on mirror.selfnet.de/c3subtitles/congress...
    if args.subtitles:
        talks = mt.from_subtitles(args.subtitles)
        print(talks)

    # Load defaults: Defaults override everything else !
    if args.default:
        # TODO: data format of json file must be changed and adjusted to new features-it is broken currently
        simple = mt.simplify_defaults()
        print("Defaults:")
        print(simple)
        for akey in simple.keys():
            talks[akey] = simple[akey]

    # Calculate stats to find subtags
    stats = defaultdict(int)
    for anid in talks.keys():
        for atag in talks[anid]["fulltags"]:
            stats[atag] += 1
    stats_sorted_by_value = sorted(stats.items(), key=lambda kv: kv[1])

    subtags = []
    for atag, acount in stats_sorted_by_value:
        if acount < SUBTAG_THRESHOLD and atag not in topics:
            subtags.append(atag)

    # Go through talks. Look into fulltags and extract
    subtags = set(subtags)
    for anid in talks.keys():
        # Calculating subtags, tags and topics
        talks[anid]["subtags"] = list(set(talks[anid]["fulltags"]).intersection(subtags))
        talks[anid]["topics"] = list(set(talks[anid]["fulltags"]).intersection(topics))
        talks[anid]["tags"] = list(set(talks[anid]["fulltags"]) - topics - subtags)


    # output data
    if args.out:
        with open(args.out+".yaml", "wt") as fh:
            fh.write(dump(talks, Dumper=Dumper))

        with open(args.out+".json", "wt") as fh:
            json.dump(talks, fh, indent=4)

    if args.statistics:
        pprint(stats.items())
        pprint(stats_sorted_by_value)

    # TODO: Check that the online frap really works - not only the local DB