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
#export PATH="/home/aaa/Ambijockey/Server/config/autostart:$PATH"
#export QT_QPA_PLATFORM=offscreen
#exec /usr/bin/jackd -R -dalsa -dhw:USBStreamer -r48000 -p128 -n2 &
#exec /usr/bin/jackd -R -P70 -aa -dalsa -dhw:USBStreamer -r44100 -p64 -i8 -o8 -n2 &
#exec /usr/bin/jackd -aa -dalsa -dhw:USBStreamer -r44100 -p64 -i8 -o8 -n2 -R &
#eval $(ssh-agent -s)

# old exec /usr/bin/jackd -R -aa -dalsa -dhw:USBStreamer -r48000 -p64 -n2 -P -i8 -o8 -na3jack &
# exec /usr/bin/jackd -R -aa -dalsa -dhw:USBStreamer -r44100 -p64 -n2 -i8 -o8 -na3jack &

# No autoconnect(-a): On
# Driver(-d): alsa
# Samplerate(-r): 44100
# Periods(-p): 64
# Realtime-Mode(-P): On
# Inputs(-i): 8
# Outputs(-o): 8
# Jack-Servername(-n): a3jack


#sleep 3
#exec x11vnc &
#sleep 3
exec i3
