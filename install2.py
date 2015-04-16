##################################################
#                                                #
#            BSPWM Installation Script           #
#                                                #
#               Chris Wilson - 2015              #
#                                                #
##################################################

import os
#import shutil
import sys
import platform

#Source URLs
bspwm_git_dir = "https://github.com/baskerville/bspwm"
sxhkd_git_dir = "https://github.com/baskerville/sxhkd"
xtitle_git_dir = "https://github.com/baskerville/xtitle"
sutils_git_dir = "https://github.com/baskerville/sutils"
lemonbar_git_dir = "https://github.com/LemonBoy/bar"

#Directories
installer_dir = sys.path[0]

from os.path import expanduser
home = expanduser("~")

tmp_dir = "/tmp/bspwm_installer/"

config_dir = "%s/.config" %home
panel_scripts_dir = "%s/.config/panel/" %home
bspwm_scripts_dir = "%s/.config/bspwm/" %home
sxhkd_scripts_dir = "%s/.config/sxhkd/" %home
wallpapers_dir = "%s/wallpapers" %config_dir
bspwmrc_dir = "bspwm/examples/bspwmrc"
sxhkdrc_dir = "bspwm/examples/sxhkdrc"
panel_config_dir = "bspwm/examples/panel/"
panel_fifo = "/tmp/panel-fifo/"

#Package Managers
arch_pm = "pacman -S"
debian_pm = "apt-get install"

#Makes directory (d) if it does not exist
def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def end_install():
    print "Installation Complete."
    cleanup()
    print "Exiting..."
    sys.exit()

def cleanup():
    #Cleanup Files
    print "Cleaning Up..."  
    os.system("rm -rf %s" %tmp_dir)
    print "Cleanup Complete.\n"

print ("\nBSPWM Installer v0.1 \n"
       "Chris Wilson - 2015  \n")

#Attempt to detect distro
distro = platform.dist()
#distro = platform.linux_distribution()
#distro = os.system("uname -v")

if distro == ("Debian", "*", "*"):
    distro = "debian"
elif distro == ("Arch", "*", "*"):
    distro = "arch"
elif distro == ("Ubuntu", "*", "*"):
    distro = "ubuntu"
else:
    print "OS Autodetect Failed!"
    pick_distro = input("Please Select Distribution\n"
                        "1.) Debian\n"
                        "2.) Arch\n"
            	 	    "3.) Ubuntu\n"
            		    "4.) Other\n"
            		    "> ")
    if pick_distro == 1:
        distro = "debian"
    elif pick_distro == 2:
        distro = "arch"
    elif pick_distro == 3:
        distro = "ubuntu"
    else:
        distro = "unknown"

#Download dependencies
print "Downloading Dependencies..."
if pick_distro == 1: #'-qq' quiet
    os.system("sudo %s gcc git make libasound2 xcb libxcb-util0-dev "
         	  "libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev "
	          "libxcb-keysyms1-dev libxcb-xinerama0-dev xorg "
		      "suckless-tools rxvt-unicode feh" %debian_pm)
elif pick_distro == 2:
    os.system("sudo %s libxcb xcb-util xcb-util-keysyms "
              "xcb-util-wm" %arch_pm)
print "Download Complete!\n"

        
#Make dir for temp files
print "Initializing Temporary Directory..."
mkdir(tmp_dir)
os.chdir(tmp_dir)

#Get source files via git
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);

# There is a bug with the current bspwm build that throws
# an Xserver connection error on some distros when using 
# Make. This workaround checks out an older version.
os.system("cd bspwm && git checkout b0e8dd3 && cd ..")

os.system("git clone %s" %sxhkd_git_dir);
print "Download Complete!\n"

#Build Source
print "Building Source..."
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C sxhkd/ && sudo make -C sxhkd/ install")
print "Build Complete!\n"

#Deploy Files to System
print "Deploying System..."

#make dirs for config files
mkdir(config_dir)
mkdir(bspwm_scripts_dir)
mkdir(sxhkd_scripts_dir)

#copy in bspwm configs
#shutil.copy(bspwmrc_dir, bspwm_scripts_dir)
os.system("cp %s %s" %(bspwmrc_dir, bspwm_scripts_dir))
os.system("cp %s %s" %(sxhkdrc_dir, sxhkd_scripts_dir))

#make bspwmrc executable
os.system("chmod +x %s" %bspwmrc_dir)


#make/update file .xinitrc
with open("%s/.xinitrc" %home, "a") as init_file:
    init_file.write("sxhkd &\n exec bspwm")
print "System Deployment Complete!\n"

#Set Background
print "Setting Background"
mkdir("%s/wallpapers" %config_dir)
os.system("cp %s/wallpapers/* %s" %(installer_dir, wallpapers_dir))

if distro == "debian":
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("feh --bg-fill %s/wallpapers/debian.jpg &" %config_dir)
elif distro == "arch":
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc.write("feh --bg-fill %s/wallpapers/arch.jpg &" %confif_dir)
elif distro == "ubuntu":
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("feh --bg-fill %s/wallpapers/ubuntu.jpg &" %config_dir)
else:
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("feh --bg-fill %s/wallpapers/linux.jpg &" %config_dir)
print "Background Set!\n"

print "BSPWM Installed Successfully!\n"

install_panel = input("Would you like to install a panel? (y/n) ")
if install_panel != 'y'
    end_install()  
    
pick_panel = input("Select panel:\n"
                   "1.) None\n"
                   "2.) LemonBar\n"
                   "> ")

#Download dependencies
print "Downloading Source..."
os.system("git clone %s" %xtitle_git_dir);
os.system("git clone %s" %sutils_git_dir);
os.system("git clone %s" %lemonbar_git_dir);
print "Download Complete!\n"

print "Building Source..."
os.system("make -C sutils/ && sudo make -C sutils/ install")
os.system("make -C xtitle/ && sudo make -C xtitle/ install")
os.system("make -C bar/ && sudo make -C bar/ install")
print "Build Complete!"

print "Deploying System..."
mkdir(panel_scripts_dir)
mkdir(panel_fifo_dir)

os.system("cp %s/panel %s/panel" %(panel_config_dir, panel_scripts_dir))
os.system("cp %s/panel_bar %s/panel_bar" %(panel_config_dir, panel_scripts_dir))
os.system("cp %s/panel_color %s/panel_color" %(panel_config_dir, panel_scripts_dir))  

#make panel & panel_bar execuatable
os.system("chmod +x %s/panel %s/panel_bar" 
        %(panel_scripts_dir, panel_scripts_dir))

# LemonBoy's bar changed its name to lemonbar. This does not yet show 
# in the default panel config and needs to be changed

#Start panel with bspwm
open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("panel &" %config_dir)

#Set Environment Variables
os.eviron["PATH"] += os.pathsep + panel_scripts_dir
os.eviron["PANEL_FIFO"] = panel_fifo_path
print "System Deployment Complete!"

print "Panel Sucessfully Installed!"

#TODO - get current term from sxhkdrc
print "The current default terminal is urxvt."
install_panel = input("Would you like to install a different terminal? (y/n) ")
if install_panel != 'y'
    end_install()  

pick_term = input("Select Terminal for Installation:\n"
                        "1.) xterm\n"
                        "2.) zsh\n"
                        "3.) xfce\n"
                        "4.) rxvt\n"
                        "> ")
#TODO - make this work for other distros
if pick_term == 1:
    os.system("sudo %s xterm" %debian_pm)
elif pick_term ==2:
    os.system("sudo %s zsh" %debian_pm)
elif pick_term == 3:
    os.system("sudo %s xfce" %debian_pm)
elif pick_term == 4:
    os.system("sudo %s rxvt" %debian_pm)
else    
    end_install()

end_install()





















































