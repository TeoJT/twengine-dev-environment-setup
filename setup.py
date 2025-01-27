import platform
import os
import urllib.request
import urllib.error
import zipfile
import shutil
import tarfile

PROCESSING_DOWNLOAD_URL_WINDOWS = 'https://github.com/processing/processing4/releases/download/processing-1295-4.3.2/processing-4.3.2-windows-x64.zip'

PROCESSING_DOWNLOAD_URL_LINUX = 'https://github.com/processing/processing4/releases/download/processing-1295-4.3.2/processing-4.3.2-linux-x64.tgz'


# Prompt colors
class color:

    HEADER    = '\033[95m'
    YELLOW    = '\033[93m'
    LRED      = '\033[91m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    GREEN     = '\033[32m'
    GOLD      = '\033[33m'
    RED       = '\033[31m'
    GREY      = '\033[90m'
    BLACK     = '\033[30m'
    NONE      = '\033[0m'
    WHITE     = '\033[29m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

    HRED      = '\033[41m'
    HGREEN    = '\033[42m'
    HYELLOW   = '\033[43m'
    HBLUE     = '\033[44m'
    HPURPLE   = '\033[45m'
    HCYAN     = '\033[46m'
    HWHITE    = '\033[47m'

ERROR_MESSAGE_WIDTH = 40

def generateHeader(headerText):
    display = headerText
    whitespace = "⠀" * (ERROR_MESSAGE_WIDTH-len(display))
    return display+whitespace

def error(message):
    head = color.HRED+color.BOLD+color.GOLD+generateHeader("ERROR!!!")+color.NONE
    print(head)
    endStringBefore = -1
    endString = -1
    for c in range(0, len(message), ERROR_MESSAGE_WIDTH-1):
        endStringBefore = endString
        if (c < len(message)-ERROR_MESSAGE_WIDTH):
            endString = message.rfind(" ", 0, c+ERROR_MESSAGE_WIDTH+1)
        else:
            endString = len(message)
        print(message[endStringBefore+1:endString])


# noColor = False
# if (platform.system() == "Windows"):
#     # No color in windows cmd
#     HEADER    = ''
#     YELLOW    = ''
#     LRED      = ''
#     BLUE      = ''
#     PURPLE    = ''
#     CYAN      = ''
#     GREEN     = ''
#     GOLD      = ''
#     RED       = ''
#     GREY      = ''
#     BLACK     = ''
#     NONE      = ''
#     WHITE     = ''
#     BOLD      = ''
#     UNDERLINE = ''
#     HRED      = ''
#     HGREEN    = ''
#     HYELLOW   = ''
#     HBLUE     = ''
#     HPURPLE   = ''
#     HCYAN     = ''
#     HWHITE    = ''


CORE_DIR = "core"
ICONS_DIR = "icons"
LIB_DIR = "libraries"
THEME_DIR = "theme"
THUMB_DIR = "thumb"
PROCESSING_DIR = "Processing"

print(color.BOLD+color.PURPLE+"TWEngine Development Environment Installer"+color.NONE)

# Perform initial checks
def check_dir(dir):
    if (not os.path.exists(dir)):
        error("Initial check failed: missing "+dir)
        exit(1)

check_dir(CORE_DIR)
check_dir(ICONS_DIR)
check_dir(LIB_DIR)
check_dir(THEME_DIR)
check_dir(THUMB_DIR)

# 1. Get install path
print(color.CYAN+"Select install path (enter nothing for "+os.getcwd()+"):"+color.NONE)
install_path = input()
while (not os.path.exists(install_path)):
    if (install_path == ""):
        install_path = os.getcwd()
        break
    print(color.RED+"Path doesn't exist.")
    print(color.CYAN+"Select install path (enter nothing for "+os.getcwd()+"):"+color.NONE)
    install_path = input()

install_path = install_path.replace("\\", "/")
if (install_path[-1] != '/'):
    install_path += '/'
print(install_path)

PROCESSING_DIR = install_path+PROCESSING_DIR


# 2. Begin Processing download
# Remove any old installations
if (os.path.exists("processing.zip")):
    os.remove("processing.zip")

if (os.path.exists("processing.tgz")):
    os.remove("processing.tgz")

if (os.path.exists(PROCESSING_DIR)):
    print("Deleting old dir...")
    shutil.rmtree(PROCESSING_DIR)

# TODO: Check for newer Timeway version via the github download page.


def download_file(url, destination):
    # Open the URL
    with urllib.request.urlopen(url) as response:
        # Get the total file size
        total_size = int(response.getheader('Content-Length').strip())
        downloaded_size = 0
        
        # Open destination file to write
        with open(destination, 'wb') as out_file:
            while True:
                # Read 8KB chunks
                chunk = response.read(8192)
                if not chunk:
                    break
                out_file.write(chunk)
                
                # Update the downloaded size
                downloaded_size += len(chunk)
                
                # Calculate and print the progress
                progress = (downloaded_size / total_size) * 100
                print(f'Downloading... ({progress:.2f}%)', end='\r')

    print('\nDone.')

def extract_zip(file_path, destination):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Get the total number of files in the zip
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        extracted_files = 0
        
        # Extract files one by one
        for file_name in zip_ref.namelist():
            destination_file = os.path.join(destination, file_name)
            
            # Check if the file already exists
            if not os.path.exists(destination_file):
                zip_ref.extract(file_name, destination)
                extracted_files += 1
            
            # Calculate and display progress
            progress = (extracted_files / total_files) * 100
            print(f'Extracting... ({progress:.2f}%)', end='\r')

    print('\nDone.')

def extract_tgz(file_path, extract_path):
    # Open the .tgz file
    with tarfile.open(file_path, 'r:gz') as tar:
        # Get the total number of files
        total_files = len(tar.getmembers())

        # Extract files one by one
        for index, member in enumerate(tar.getmembers()):
            tar.extract(member, path=extract_path)
            # Calculate completion percentage
            completion_percentage = (index + 1) / total_files * 100
            print(f'Extracting... ({completion_percentage:.2f}%)', end='\r')

    print("Done.")


def is_wsl():
    # Check for the WSL environment
    if platform.system() == 'Linux':
        # Check if the /proc/version file contains 'Microsoft'
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return True
    return False



# Install processing
if (True):
    print(color.CYAN+"Install Processing"+color.NONE)
    try:
        if (os.name == "nt"):
            download_file(PROCESSING_DOWNLOAD_URL_WINDOWS, install_path+'processing.zip')
        elif (os.name == "posix" and is_wsl()):
            download_file(PROCESSING_DOWNLOAD_URL_WINDOWS, install_path+'processing.zip')
        elif (os.name == "posix" and not is_wsl()):
            download_file(PROCESSING_DOWNLOAD_URL_LINUX, install_path+'processing.tgz')
        else:
            error("Unknown operating system (os.name: "+os.name+", is_wsl: "+str(is_wsl())+")")
            exit(1)

    except urllib.error.URLError:
        error("Couldn't download file, connection error.")
        exit(1)
    except:
        error("Unknown download error.")
        exit(1)

    try:
        if (os.name == "nt"):
            extract_zip(install_path+'processing.zip', PROCESSING_DIR)
        elif (os.name == "posix" and is_wsl()):
            extract_zip(install_path+'processing.zip', PROCESSING_DIR)
        elif (os.name == "posix" and not is_wsl()):
            extract_tgz(install_path+'processing.tgz', PROCESSING_DIR)
        else:
            error("Unknown operating system (os.name: "+os.name+", is_wsl: "+str(is_wsl())+")")
            exit(1)

    except:
        error("ZIP extract error, perhaps zip file is corrupted?")
        exit(1)


# Delete zip
if (os.path.exists("processing.zip")):
    os.remove(install_path+"processing.zip")

# Have a peek inside and update PROCESSING_DIR
zip_contents = os.listdir(PROCESSING_DIR)
if (len(zip_contents) == 0):
    error("Empty ZIP file! ZIP file may be corrupted.")
    exit(1)

PROCESSING_DIR += "/"+zip_contents[0]+"/"
print(PROCESSING_DIR)

# Stage 3:
# Replace core with patch
print("Patching core...")
if (os.path.exists(PROCESSING_DIR+"core")):
    shutil.rmtree(PROCESSING_DIR+"core")
else:
    print(color.GOLD+"Warning: original core appears to be missing. This may indicate a corrupted download. This isn't an issue yet but further issues may arise."+color.NONE)

# Copy core patch
shutil.copytree(CORE_DIR, PROCESSING_DIR+"core")

# Stage 4:
# Icons install
def copy_from(src, dst):
    files = os.listdir(src)
    for file in files:
        shutil.copyfile(src+"/"+file, dst+"/"+file)

print("Installing Timeway icons...")
if (os.path.exists(PROCESSING_DIR+"modes/java/application")):
    copy_from(ICONS_DIR, PROCESSING_DIR+"modes/java/application")
else:
    print(color.GOLD+"Warning: "+PROCESSING_DIR+"modes/java/application not found. This may indicate a corrupted install."+color.NONE)


# Stage 5:
# Theme and thumb install
print("Installing theme...")
if (os.path.exists(PROCESSING_DIR+"lib/theme")):
    # Copy theme
    shutil.copyfile(THEME_DIR+"/theme.txt", PROCESSING_DIR+"lib/theme/theme.txt")
    # Copy default theme
    if (os.path.exists(PROCESSING_DIR+"lib/theme/Alloys/imilac.txt")):
        shutil.copyfile(THEME_DIR+"/theme.txt", PROCESSING_DIR+"lib/theme/Alloys/imilac.txt")
    # Eh can't be bothered with warnings for this part.
else:
    print(color.GOLD+"Warning: "+PROCESSING_DIR+"lib/theme not found. This may indicate a corrupted install."+color.NONE)

# TODO: Thumbnail


# Stage 6:
# Install libraries
print("Installing Processing libraries...")


documents_path = os.path.expanduser("~/Documents").replace("\\", "/")
if (documents_path[-1] != '/'):
    documents_path += '/'

if (is_wsl()):
    print(color.GOLD+"WSL detected, accessing your mnt windows drive.")
    users_path = ""
    for x in range(97, 123):
        if (os.path.exists("/mnt/"+chr(x)+"/Users")):
            users_path = "/mnt/"+chr(x)+"/Users/"
            break
        
    if (users_path == ""):
        error("Could not find your Windows documents folder in the WSL environment (no /mnt/[a-z] exists)")
        exit(1)

    found = False
    # Go to C:/Users/ and find which folder we have permission to access
    for folder in os.listdir(users_path):
        if (os.path.isdir(users_path+folder) 
            and folder.lower() != "all users"
            and folder.lower() != "public"
            and folder.lower() != "default"
            and folder.lower() != "default user"
            ):
            try:
                os.listdir(users_path+folder)
                users_path = users_path+folder
                found = True
            except:
                continue

    if (found):
        print(color.GREEN+"Found "+users_path+""+color.NONE)
    else:
        print(color.GOLD+"Couldn't find your user folder!"+color.NONE)
        print(color.GOLD+"Gonna need some user input here."+color.NONE)
        users_path = input(color.GOLD+"Enter path to your user folder: "+color.NONE)
        # Repeat until folder exists
        while (not os.path.isdir(users_path)):
            users_path = input(color.GOLD+"Invalid path, try again: "+color.NONE)
            if (not os.path.isdir(users_path)):
                continue
            if (not os.path.isdir(users_path)):
                print(color.RED+"Video library doesn't exist in this user folder."+color.NONE)

        print(color.GREEN+"OK! "+users_path+color.NONE)
                
    if (users_path[-1] != '/'):
        users_path += '/'
     
    documents_path = users_path+"Documents/"

    # Shouldn't happen on a windows machine
    if (not os.path.exists(documents_path)):
        error("No Documents folder exists in your user directory.")
        exit(1)
    
print(color.CYAN+"Documents path selected: "+documents_path+color.NONE)

library_path = documents_path+"Processing/libraries/"



def copy_library(src, dst): 
    global copyskip
    if (os.path.exists(dst)):
        print(color.GOLD+src+" already exists. Replace? (Y/n)"+color.NONE)
        yn = input()
        if (yn.lower() == 'y'):
            shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(color.GOLD+"Replaced."+color.NONE)
        else:
            print(color.WHITE+"Ignored."+color.NONE)
            copyskip = True
    else:
        shutil.copytree(src, dst)



# Ok, NOW we can go ahead and install the libraries
if (not os.path.exists(library_path)):
    os.makedirs(library_path)
else:
    print(color.RED+color.BOLD+"WARNING  "+color.NONE+"TWEngine-based projects uses patched libraries, and these may replace some of your existing libraries in your Documents/Processing/Libraries folder. Press enter to proceed.")
    input()

copyskip = False
library_files = os.listdir(LIB_DIR)
i = 1
for file in library_files:
    print('Copy library '+str(i)+"/"+str(len(library_files))+"...", end='\r')
    copy_library(LIB_DIR+"/"+file, library_path+file)
    i+=1

if (copyskip):
    print(color.RED+color.BOLD+"WARNING  "+color.NONE+"Some libraries were skipped due to denied file replacement. Your TWEngine-based project may not function properly.")

print(color.GREEN+"TWEngine toolkit successfully installed! Have fun!"+color.NONE)
