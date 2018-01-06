#!/usr/bin/env python3

import json
import argparse
import os
import re

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

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

ANDROID = "android"
IOS = "ios"

# Detailed Tags (let's find out if there are more than 3 talks deserving those tags)

## Anonymisation networks
I2P = "i2p"
FREENET = "freenet"
GNUNET = "gnunet"
JONDONYM = "jondonym"
LOOPIX = "loopix"
VUVUZELA = "vuvuzela"

## Hardware hacking tools
CHIPWHISPERER = "chipwhisperer"
GLITCHKIT = "glitchkit"
FACEDANCER = "facedancer"
HACKRF = "hackrf"
PROXMARK = "proxmark"
UBERTOOTH = "ubertooth"

SHODAN = "shodan"

#SERIES
SECURITY_NIGHTMARES = "security nightmares"
METHODISCH_INKORREKT = "methodisch inkorrekt"  # TODO
ULTIMATE_TALK = "ultimate talks"
INFRASTRUCTURE_REV = "infrastructure review" # TODO

regexes = {r"\Wrfid\W":[RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Wmifare\W":[RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Wmifare\W":[RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Whitag\W":[RFID, ELECTRONICS, WIRELESS, HARDWARE],
           r"\Wgeheimdienste?\W":[BIGBROTHER, POLITICS],
           r"\Wgchq?\W":[BIGBROTHER, POLITICS],
           r"\Wnsa?\W":[BIGBROTHER, POLITICS],
           r"\Wsatellite\W":[SPACE],
           r"\Wlulzsec\W":[ACTIVISM],
           r"\Warab spring\W":[POLITICS, ACTIVISM],
           r"\Wedward snowden\W":[POLITICS, ACTIVISM, PRIVACY],
           r"\Wtor\W":[NETWORK, PRIVACY, TOR, CRYPTO],
           r"\Wdragnet surveillance system\W": [NETWORK, PRIVACY, BIGBROTHER],
           r"\Wquantenphysik\W": [SCIENCE],
           r"\Wrelativitätstheorie\W": [SCIENCE],
           r"\Walbert einstein\W": [SCIENCE],
           r"\Wdigital surveillance\W": [NETWORK, PRIVACY, BIGBROTHER],
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
           r"\Wmri\W": [BIO],
           r"\Weeg\W": [BIO],
           r"\Wtomography\W": [BIO],
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
           r"\Whacking\W": [HACKING],
           r"\Wseawatch\W": [ACTIVISM, POLITICS],
           r"\Wjugend rettet\W": [ACTIVISM, POLITICS],
           r"\Wmsf\W": [ACTIVISM, POLITICS],
           r"\Wchaos macht schule\W": [ACTIVISM, POLITICS],
           r"\Wcaliope\W": [HARDWARE, SOFTWARE],
           r"\Wtcp\W": [NETWORK],
           r"\Wvlan\W": [NETWORK],
           r"\Wpci express\W": [HARDWARE],
           r"\Wnics?\W": [HARDWARE, NETWORK],
           r"\Wnintendo\W": [CONSOLE],
           r"\Wblockchains?\W": [CRYPTO],
           r"\Wopensource\W": [SOFTWARE],
           r"\Wstaatsanwalt\W": [LAW],
           r"\Wanwälte\W": [LAW],
           r"\Wabmahnanwälte\W": [LAW],
           r"\Wreverse engineering\W": [HACKING],
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
           r"\Wsurveillance\W": [BIGBROTHER],
           r"\Wbluetooth\W": [WIFI, BLUETOOTH],
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
           r"\Wgenome\W": [BIO],
           r"\Wdna\W": [BIO],
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
           r"\Wperl\W": [SOFTWARE],
           r"\Wsql\W": [SOFTWARE],
           r"\Wtan\W": [BANKING],
           r"\Wbandwidth\W": [NETWORK],
           r"\Wlasers?\W": [SCIENCE],
           r"\Wiridium\W": [NETWORK, MOBILE, SPACE],
           r"\Wsocial media\W": [SOCIETY],
           r"\Wheart monitor\W": [BIO],
           r"\Wweltall\W": [SPACE],
           r"\Wgrundrechte\W": [POLITICS, LAW],
           r"\Wanonymous communication\W": [PRIVACY],
           r"\Wprofiling\W": [PRIVACY],
           r"\Wdprk\W": [POLITICS],
           r"\Wnsaua\W": [POLITICS],
           r"\Wfreifunk\W": [NETWORK, WIFI, ACTIVISM],
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
           r"\Wfacedancer\W": [HARDWARE, HACKING, SECURITY, FACEDANCER],
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


           }


default_talks = [{
          "title": "Dude, you broke the Future!",
          "url": "https://media.ccc.de/v/34c3-9270-dude_you_broke_the_future",
          "congress": "34c3",
          "id": "9270",
          "language": "English",
          "tags": [KEYNOTE, POLITICS, INSIGHTS, TECHNOLOGY],
          "series": None,
         },
        {
        "title": "Antipatterns und Missverständnisse in der Softwareentwicklung",
        "url": "https://media.ccc.de/v/34c3-9095-antipatterns_und_missverstandnisse_in_der_softwareentwicklung",
        "congress": "34c3",
        "id": "9095",
        "language": "German",
        "tags": [TECHNOLOGY, ENGINEERING],
        "series": None,
        },
        {
        "title": "Die fabelhafte Welt des Mobilebankings",
        "url": "https://media.ccc.de/v/34c3-8805-die_fabelhafte_welt_des_mobilebankings",
        "congress": "34c3",
        "id": "8805",
        "language": "German",
        "tags": [MOBILE, BANKING, ANDROID, SOFTWARE, IOS, HACKING, SECURITY],
        "series": None,
        },
        {
        "title": "Internet of Fails",
        "url": "https://media.ccc.de/v/34c3-9193-internet_of_fails",
        "congress": "34c3",
        "id": "9193",
        "language": "English",
        "tags": [IOT, PRIVACY, SECURITY, HARDWARE, SOFTWARE, HACKING, BLUETOOTH],
        "series": None,
        },
        {
        "title": "How to drift with any car",
        "url": "https://media.ccc.de/v/34c3-8758-how_to_drift_with_any_car",
        "congress": "34c3",
        "id": "8758",
        "language": "English",
        "tags": [AUTOMOTIVE, HACKING, SECURITY, HARDWARE, SOFTWARE, ELECTRONICS],
        "series": None,
        },
        {
        "title": "Ladeinfrastruktur für Elektroautos: Ausbau statt Sicherheit",
        "url": "https://media.ccc.de/v/34c3-9092-ladeinfrastruktur_fur_elektroautos_ausbau_statt_sicherheit",
        "congress": "34c3",
        "id": "9092",
        "language": "German",
        "tags": [AUTOMOTIVE, HACKING, SECURITY, NETWORK, RFID],
        "series": None,
        },
        {
        "title": "The Ultimate Apollo Guidance Computer Talk",
        "url": "https://media.ccc.de/v/34c3-9064-the_ultimate_apollo_guidance_computer_talk",
        "congress": "34c3",
        "id": "9064",
        "language": "English",
        "tags": [HISTORY, SPACE, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "The Ultimate Game Boy Talk",
        "url": "https://media.ccc.de/v/33c3-8029-the_ultimate_game_boy_talk",
        "congress": "33c3",
        "id": "8029",
        "language": "English",
        "tags": [HISTORY, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "The Ultimate Amiga 500 Talk",
        "url": "https://media.ccc.de/v/32c3-7468-the_ultimate_amiga_500_talk",
        "congress": "32c3",
        "id": "7468",
        "language": "English",
        "tags": [HISTORY, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "The ultimate Galaksija talk",
        "url": "https://media.ccc.de/v/29c3-5178-en-the_ultimate_galaksija_talk_h264",
        "congress": "29c3",
        "id": "5178",
        "language": "English",
        "tags": [HISTORY, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "The Atari 2600 Video Computer System: The Ultimate Talk",
        "url": "https://media.ccc.de/v/28c3-4711-en-the_atari_2600_video_computer_system_the_ultimate_talk",
        "congress": "28c3",
        "id": "4711",
        "language": "English",
        "tags": [HISTORY, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "The Ultimate Commodore 64 Talk",
        "url": "https://media.ccc.de/v/25c3-2874-en-the_ultimate_commodore_64_talk",
        "congress": "25c3",
        "id": "2874",
        "language": "English",
        "tags": [HISTORY, HARDWARE, SOFTWARE],
        "series": ULTIMATE_TALK,
        },
        {
        "title": "QualityLand",
        "url": "https://media.ccc.de/v/34c3-9285-qualityland",
        "congress": "34c3",
        "id": "9285",
        "language": "German",
        "tags": [ENTERTAINMENT],
        "series": None,
        },
        {
        "title": "Schnaps Hacking",
        "url": "https://media.ccc.de/v/34c3-8946-schnaps_hacking",
        "congress": "34c3",
        "id": "8946",
        "language": "English",
        "tags": [FOOD, LAW, MAKING],
        "series": None,
        },
        {
        "title": "Home Distilling",
        "url": "https://media.ccc.de/v/34c3-8938-home_distilling",
        "congress": "34c3",
        "id": "8938",
        "language": "English",
        "tags": [FOOD, LAW, BIO],
        "series": None,
        },
        {
        "title": "How Alice and Bob meet if they don't like onions",
        "url": "https://media.ccc.de/v/34c3-9104-how_alice_and_bob_meet_if_they_don_t_like_onions",
        "congress": "34c3",
        "id": "9104",
        "language": "English",
        "tags": [CRYPTO, I2P, FREENET, GNUNET, JONDONYM, TOR, LOOPIX, VUVUZELA, NETWORK],
        "series": None,
        },
        {
        "title": "All Computers Are Beschlagnahmt",
        "url": "https://media.ccc.de/v/34c3-8955-all_computers_are_beschlagnahmt",
        "congress": "34c3",
        "id": "8955",
        "language": "German",
        "tags": [POLITICS, ACTIVISM, LAW, BIGBROTHER],
        "series": None,
        },
        {
        "title": "Opening Closed Systems with GlitchKit",
        "url": "https://media.ccc.de/v/34c3-9207-opening_closed_systems_with_glitchkit",
        "congress": "34c3",
        "id": "9207",
        "language": "English",
        "tags": [HARDWARE, HACKING, CHIPWHISPERER, ELECTRONICS, GLITCHKIT],
        "series": None,
        },
        {
        "title": "Drones of Power: Airborne Wind Energy",
        "url": "https://media.ccc.de/v/34c3-8877-drones_of_power_airborne_wind_energy",
        "congress": "34c3",
        "id": "8877",
        "language": "English",
        "tags": [SCIENCE, MAKING, SOLUTION, ENERGY],
        "series": None,
        },
        {
        "title": "0en & 1en auf dem Acker",
        "url": "https://media.ccc.de/v/34c3-8961-0en_1en_auf_dem_acker",
        "congress": "34c3",
        "id": "8961",
        "language": "German",
        "tags": [BIO, SCIENCE, ROBOTICS],
        "series": None,
        },
        {
        "title": "The making of a chip",
        "url": "https://media.ccc.de/v/34c3-9250-the_making_of_a_chip",
        "congress": "34C3",
        "id": "9250",
        "language": "English",
        "tags": [HARDWARE, ELECTRONICS],
        "series": None,
        },
        {
        "title": "Zamir Transnational Network und Zagreb Dairy",
        "url": "https://media.ccc.de/v/34c3-8842-zamir_transnational_network_und_zagreb_dairy",
        "congress": "34C3",
        "id": "8842",
        "language": "German",
        "tags": [NETWORK, HISTORY, ACTIVISM],
        "series": None,
        },
        {
        "title": "Security Nightmares 0x12",
        "url": "https://media.ccc.de/v/34c3-8888-security_nightmares_0x12",
        "congress": "34C3",
        "id": "8888",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": "Security Nightmares",
        },
        {
        "title": "Security Nightmares 0x11",
        "url": "https://media.ccc.de/v/33c3-8413-security_nightmares_0x11",
        "congress": "33C3",
        "id": "8413",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares 0x10",
        "url": "https://media.ccc.de/v/32c3-7546-security_nightmares_0x10",
        "congress": "32C3",
        "id": "7446",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/31c3_-_6572_-_de_-_saal_1_-_201412301715_-_security_nightmares_-_frank_-_ron",
        "congress": "31C3",
        "id": "6572",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/30C3_-_5413_-_de_-_saal_1_-_201312301715_-_security_nightmares_-_frank_-_ron",
        "congress": "30C3",
        "id": "5413",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/29c3-5244-de-en-security_nightmares2012_h264",
        "congress": "29C3",
        "id": "5244",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/28c3-4898-de-security_nightmares",
        "congress": "28C3",
        "id": "4898",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/27c3-4230-de-security_nightmares",
        "congress": "27C3",
        "id": "4230",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares",
        "url": "https://media.ccc.de/v/26c3-3687-de-security_nightmares",
        "congress": "26C3",
        "id": "3687",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares 2009",
        "url": "https://media.ccc.de/v/25c3-3021-de-security_nightmares_2009",
        "congress": "25C3",
        "id": "3021",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares 2008",
        "url": "https://media.ccc.de/v/24c3-2336-de-security_nightmares",
        "congress": "24C3",
        "id": "2336",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares 2007",
        "url": "https://media.ccc.de/v/23C3-1682-de-security_nightmares",
        "congress": "23C3",
        "id": "1682",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares 2006",
        "url": "https://media.ccc.de/v/22C3-600-de-security_nightmares",
        "congress": "22C3",
        "id": "600",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        # No security nightmares 21C3 ?
        {
        "title": "Security Nightmares III",
        "url": "https://media.ccc.de/v/20C3-609-Security_Nightmares_III",
        "congress": "20C3",
        "id": "609",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        {
        "title": "Security Nightmares III",
        "url": "https://media.ccc.de/v/19C3-434-security-nightmares",
        "congress": "19C3",
        "id": "434",
        "language": "German",
        "tags": [SECURITY, ENTERTAINMENT],
        "series": SECURITY_NIGHTMARES,
        },
        # No security nightmares left...
        ]


def get_congress(filename):
    return filename.split("-")[0]

def get_id(filename):
    return filename.split("-")[1]

def get_tags(filename):
    res = []
    with open(filename, "rt") as fh:
        content = fh.read().lower()
        for akey in regexes.keys():
            if re.search(akey, content, re.MULTILINE):
                res += regexes[akey]
    return list(set(res))

def from_subtitles(directory):
    res = {}

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".srt"):
                fullname = os.path.join(root, name)
                print(fullname)
                tags = get_tags(fullname)
                print(tags)
                talkid = get_id(name)
                if talkid not in res:
                    res[talkid] = tags
                else:
                    res[talkid] = list(set(res[talkid] + tags))
    return res


def simplify_defaults():
    res = {}
    for talk in default_talks:
        res[talk["id"]] = talk["tags"]
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subtitles", help="Process subtitles folder. Output json", default = None, type=str)
    parser.add_argument("--out", help="out filename. Without postfix .json or .yaml. This will be added", default = None, type = str)
    parser.add_argument("--default", help="Load hard coded default talks as well", action="store_true", default = False)
    args = parser.parse_args()

    talks = {}

    # Generate db from subtitles
    # Subtitles are on mirror.selfnet.de/c3subtitles/congress...
    if args.subtitles:
        talks = from_subtitles(args.subtitles)
        print(talks)

    # Load defaults: Defaults override everything else !
    if args.default:
        simple = simplify_defaults()
        print("Defaults:")
        print(simple)
        for akey in simple.keys():
            talks[akey] = simple[akey]

    # output data
    if args.out:
        with open(args.out+".yaml", "wt") as fh:
            fh.write(dump(talks, Dumper=Dumper))

        with open(args.out+".json", "wt") as fh:
            json.dump(talks, fh, indent=4)
