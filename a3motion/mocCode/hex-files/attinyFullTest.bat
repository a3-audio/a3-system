
cd C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\avrdude-ver6.3\
SET hexFile="firstTest.hex"
cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\hex-files\%hexFile% %hexFile%
avrdude.exe -c jtag2updi -P com7 -p t1626 -U flash:w:%hexFile%
rm %hexFile%
pause
