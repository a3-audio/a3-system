cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyFullTest\attinyFullTest\attinyFullTest.X\dist\Release\production\attinyFullTest.X.production.hex C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\hex-files\attinyFullTest.hex

cd C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\avrdude-ver6.3\
cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\hex-files\attinyFullTest.hex attinyFullTest.hex
avrdude.exe -c jtag2updi -P com7 -p t1626 -U flash:w:attinyFullTest.hex
rm attinyFullTest.hex
pause
