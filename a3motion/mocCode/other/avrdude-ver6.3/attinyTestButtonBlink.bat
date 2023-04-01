cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyTestButtonBlink.X\dist\Release\production\attinyTestButtonBlink.X.production.hex C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\hex-files\attinyTestButtonBlink.hex

cd C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\avrdude-ver6.3\
cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\hex-files\attinyTestButtonBlink.hex attinyTestButtonBlink.hex
avrdude.exe -c jtag2updi -P com7 -p t1626 -U flash:w:attinyTestButtonBlink.hex
rm attinyTestButtonBlink.hex

