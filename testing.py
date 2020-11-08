import urllib2;
import os;
import time;

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

rom_whitelist = ["Gameboy", "Gameboy Color", "Gameboy Advance", "Super Nintendo", "Nintendo 64", "Atari 2600", "Atari 5200", "Atari 7800", "Atari 800", "Atari Lynx", "Game Gear", "Sega Genesis", "MAME", "Sega Master System", "Neo Geo Pocket", "Neo Geo Pocket Color", "Neo Geo", "Nintendo", "Sega 32x", "ZX Spectrum"];
cor_folder = ["gb", "gbc", "gba", "snes", "n64", "atari2600", "atari5200", "atari7800", "atari800", "atarilynx", "gamegear", "genesis", "mame-libretro", "mastersystem", "ngp", "ngpc", "neogeo", "nes", "sega32x", "zxspectrum"]

namelist = [];
consolelist = [];
idlist = [];

print("Starting LOVEROMS downloader...");

def main(page, rom):
    global namelist;
    global consolelist;
    global idlist;
    if(rom == ""):
        print("What rom are you looking for? Press q if you want to quit");
        romname = raw_input("> ");
        rom = romname;
        if(romname == "q"):
            exit(0);
    rom = rom.replace(" ", "+");
    find_roms(rom, page);
    for k in range(len(namelist)):
        print(str(k)+") "+namelist[k]+" CONSOLE: "+consolelist[k]);
    print("Do you wish to search on another page? (y/n)")
    yn = "";
    while(True):
        yn = raw_input("> ");
        if(yn.lower() == "y" or yn.lower() == "n"):
            yn = yn.lower();
            break;
    if(yn == "y"):
        print("Please enter page #");
        page = 0;
        while True:
            page = raw_input("> ");
            try:
                int(page);
                break;
            except:
                print("Please enter a valid number");
        namelist = [];
        consoleslist = [];
        idlist = [];
        main(int(page), rom);
        return;
    print("Please select which rom you wish to install or press q to cancel");
    want = "";
    while(True):
        want = raw_input("> ");
        if(want == "q"):
            main(0, "");
            return;
        try:
            namelist[int(want)];
            break;
        except:
            print("Please enter valid option!");
    id = int(want);
    romid = idlist[id];
    name = namelist[id];
    console = consolelist[id];
    print("Preparing to install "+name+"...");
    directory = "/home/pi/RetroPie/roms/"+cor_folder[rom_whitelist.index(console)];
    url =  "https://download.loveroms.com/downloader/rom/"+idlist[id]+"/1/"+namelist[id].replace(" ", "%20")+".zip";
    print("Downloading and extracting "+url+"...");
    os.system('cd '+directory+' && wget "'+url+'" && unzip "'+name+'.zip" && rm "'+name+'.zip"');
    os.system("killall emulationstation && emulationstation");
    print("Done ! Restarting emulationstation...");
    time.sleep(3);
    exit(0);

def find_roms(name, page):
    roms = fetch_roms(name, page);
    for k in range(len(roms)):
        if(k != 0):
            roms[k] = roms[k].split('<td class="rom-thumbnail-col text-center">')[0];
            if(k == 25):
                roms[k] = roms[k].split('<div class="panel-footer">')[0];
            rom_name = roms[k].split("<span>")[1].split("</span>")[0];
            if(rom_name.startswith(" ")):
                rom_name = rom_name.replace(" ", "", 1);
            rom_console = roms[k].split("</strong>")[1].split("<br />")[0].replace(" ", "", 1);
            rom_id = roms[k].split("/")[4].split('"')[0];
            for consoles in rom_whitelist:
                if(rom_console == consoles):
                    consolelist.append(rom_console);
                    namelist.append(rom_name);
                    idlist.append(rom_id);

def fetch_roms(search, page):
    url = "https://www.loveroms.com/roms/?q="+search+"+&page="+str(page);
    #if you are wondering why I added the "+" before "&page" its because of a website bug, not me
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req);
    except(urllib2.HTTPError, e):
        print e.fp.read();
    content = page.read();
    roms = content.split('<td class="vertical-align-middle" valign="middle">');
    return roms;

main(0, "");
