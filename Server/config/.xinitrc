# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps
if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi
if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi
if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi
if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

# Edit line to fit your audio-hardware. Find out with:
# cat /proc/asound/cards

exec /usr/bin/jackd -R -a a -dalsa -dhw:USBStreamer -r48000 -p64 -n2 -P -i8 -o8 -na3jack &

# No autoconnect(-a): On
# Driver(-d): alsa
# Samplerate(-r): 44100
# Periods(-p): 64
# Realtime-Mode(-P): On
# Inputs(-i): 8
# Outputs(-o): 8
# Jack-Servername(-n): a3jack

sleep 3
exec i3
