cp C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyFullTest\attinyFullTest\attinyFullTest.X\dist\Release\production\attinyFullTest.X.production.hex C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyHelloWorld\avrdude-ver6.3\attinyFullTest.hex

cd C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyHelloWorld\avrdude-ver6.3\

avrdude.exe -c jtag2updi -P com7 -p t1626 -U flash:w:attinyFullTest.hex


