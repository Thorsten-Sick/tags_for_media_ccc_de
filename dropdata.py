#!/usr/bin/env python3

import json
import requests

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

# Detailed Tags (let's find out if there are more than 3 talks deserving those tags)

## Anonymisation networks
I2P = "i2p"
FREENET = "freenet"
GNUNET = "gnunet"
JONDONYM = "jondonym"
LOOPIX = "loopix"
VUVUZELA = "vuvuzela"

## Hadware hacking tools
CHIPWHISPERER = "chipwhisperer"
GLITCHKIT = "glitchkit"


#SERIES
SECURITY_NIGHTMARES = "security nightmares"
METHODISCH_INKORREKT = "methodisch inkorrekt"


talks = [{
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

#print(dump(talks, Dumper=Dumper))
print(json.dumps(talks, indent=4))
