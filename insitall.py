import urllib.request
from platform import system
from os.path import expanduser
import shutil
import os
import ast
import webbrowser

os.chdir(".")
if os.path.exists("./tmp"):
    for z in os.listdir("./tmp"):
        os.remove(f"./tmp/{z}")
else:
    os.mkdir("./tmp")

def yn(bool):
    if bool == True:
        return "yes"
    if bool == False:
        return "no"
    return "no"

def download(name, url):
    urllib.request.urlretrieve(url, name)

def mcdir(os):
    if os == "Windows":
        return f"{str(expanduser('~'))}\\AppData\\Roaming\\.minecraft".replace("\\","/")
    if os == "Darwin":
        return f"{str(expanduser('~'))}/Library/Application Support/minecraft"
    if os == "Linux":
        return f"{str(expanduser('~'))}/.minecraft"

def select():
    print("""
    1: mc.unixtm.dev
    2: Bring back old mods
    3: Nevermind
    No others yet
    """)
    selection = input("[1,2,3]: ")
    if selection in ["1","2","3"]:
        return int(selection)
    else:
        return int(select())

sel = select()
fabricmc_win = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.1/fabric-installer-0.11.1.exe"
prefix = "https://raw.githubusercontent.com/UnixPNG/script-wget/main/"
fabricmc_java = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.1/fabric-installer-0.11.1.jar"
javadownloadlink = "https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html"
unixtm_mods = ast.literal_eval(urllib.request.urlopen("https://raw.githubusercontent.com/UnixPNG/script-wget/main/mods.txt").read(20000).decode("utf-8").replace("\n",""))

try:
    if sel == 3:
        print("ok")

    if sel == 2:
        print("Restoring old mods and removing new ones...")
        theList = os.listdir(mcdir(system())+'/mods')

        try:
            theList.remove("unixtmOldMods")
        except:
            raise Exception("Old mods folder not found! Cannot continue!")
        for x in theList:
            os.remove(mcdir(system())+'/mods/'+x)

        for x in os.listdir(mcdir(system())+'/mods/unixtmOldMods'):
            shutil.move(mcdir(system())+'/mods/unixtmOldMods/'+x, mcdir(system())+'/mods/'+x)

        print("Done!")

    if sel == 1:
        print("Downloading mods for \"mc.unixtm.dev\"")
        for x in unixtm_mods:
            download(f"./tmp/{x[1]}",f"{prefix}{x[0]}")
            print(f"Downloaded \"{x[1]}\"")

        if system() not in ["Darwin","Windows","Linux"]:
            print("Fatal error: We cannot detect your OS.")
            raise Exception("Fatal error: We cannot detect your OS.")

        print(f"OS: {system()}")
        print(f"Minecraft directory: {mcdir(system())}")
        print(f"Mods directory exists: {yn(os.path.exists(mcdir(system())+'/mods'))}")
        print("Installing mods for \"mc.unixtm.dev\"")

        if not os.path.exists(mcdir(system())+'/mods'):
            os.mkdir(mcdir(system())+'/mods')

        if not os.path.exists(mcdir(system())+'/mods/unixtmOldMods'):
            os.mkdir(mcdir(system())+'/mods/unixtmOldMods')

        else:
            for x in os.listdir(mcdir(system())+'/mods/unixtmOldMods'):
                os.remove(mcdir(system())+f'/mods/unixtmOldMods/{x}')

        for x in os.listdir(mcdir(system())+'/mods'):
            try:
                shutil.move(mcdir(system())+f'/mods/{x}',mcdir(system())+f'/mods/unixtmOldMods/{x}')
            except:
                continue

        for x in os.listdir("./tmp"):
            shutil.move(f"./tmp/{x}", mcdir(system())+f'/mods/{x}')

        if system() == "Windows":
            download("tmp/fabric.exe", fabricmc_win)
            print("Select the newest loader version and Minecraft version 1.19.")
            print("Then check \"Create Profile\" and click \"Install\".")
            print("Then make sure to close all windows of the program.")
            print("If you can't see any new windows, look in the taskbar or whatever (next line)")
            print("for a sheet of paper, and click it.")
            print()
            os.chdir("./tmp")
            os.system("fabric")
            os.chdir("../")
        if system() in ["Darwin","Linux"]:
            if os.system("which java") == 0: 
                download("tmp/fabric.jar", fabricmc_java)
                print("Select the newest loader version and Minecraft version 1.19.")
                print("Then check \"Create Profile\" and click \"Install\".")
                print("Then make sure to close all windows of the program.")
                print("If you can't see any new windows, look in the taskbar or whatever (next line)")
                print("for a sheet of paper, and click it.")
                print()
                os.chdir("./tmp")
                os.system("java -jar fabric.jar")
                os.chdir("../")
            else:
                print("Java not installed on your OS. Please install it.")
                webbrowser.open_new(javadownloadlink)

        print("Done!")
except:
    raise Exception("There was an error installing/removing the mods. Try again later")

for x in os.listdir("./tmp"):
    os.remove(f"./tmp/{x}") 