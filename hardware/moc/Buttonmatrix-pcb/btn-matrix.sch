EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 11693 16535 portrait
encoding utf-8
Sheet 1 1
Title "A³Pandemic - A³motion - Buttonmatrix-Modul"
Date "2021-08-04"
Rev "v.0.1"
Comp "A³ Ambisonic Audio Adventures (Haftungsbeschränkt) UG & Co. KG"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S0
U 1 1 6072FECA
P 3750 3700
F 0 "S0" H 4250 3550 50  0000 L CNN
F 1 "228CMVARGBFR" H 4050 3450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 4800 4200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 4800 4100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 4800 4000 50  0001 L CNN "Description"
F 5 "7.3" H 4800 3900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 4800 3800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 4800 3700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 4800 3600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 4800 3500 50  0001 L CNN "Manufacturer_Part_Number"
	1    3750 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 2300 5250 4550
Wire Wire Line
	4250 4550 4250 4400
Wire Wire Line
	5350 2200 5350 4400
Text GLabel 4950 3800 2    50   Output ~ 0
btn00
NoConn ~ 4150 2400
Wire Wire Line
	4950 2300 5250 2300
Wire Wire Line
	4950 2200 5350 2200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U0
U 1 1 6072F106
P 4550 2300
F 0 "U0" H 4550 2781 50  0000 C CNN
F 1 "WS2811" H 4550 2690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 4250 2450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 4350 2550 50  0001 C CNN
	1    4550 2300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0102
U 1 1 6074000E
P 4550 2600
F 0 "#PWR0102" H 4550 2350 50  0001 C CNN
F 1 "GND" V 4555 2472 50  0000 R CNN
F 2 "" H 4550 2600 50  0001 C CNN
F 3 "" H 4550 2600 50  0001 C CNN
	1    4550 2600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0103
U 1 1 60740506
P 4250 3000
F 0 "#PWR0103" H 4250 2850 50  0001 C CNN
F 1 "+5V" H 4265 3173 50  0000 C CNN
F 2 "" H 4250 3000 50  0001 C CNN
F 3 "" H 4250 3000 50  0001 C CNN
	1    4250 3000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C0
U 1 1 60740C37
P 4800 2000
F 0 "C0" V 5052 2000 50  0000 C CNN
F 1 "104" V 4961 2000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4838 1850 50  0001 C CNN
F 3 "" H 4800 2000 50  0001 C CNN
F 4 "https://www.digikey.de/product-detail/de/kemet/C1206Y104K9RAC7800/399-13304-1-ND/5879274" V 4800 2000 50  0001 C CNN "link"
	1    4800 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R0.3
U 1 1 607415CA
P 4300 2000
F 0 "R0.3" V 4200 2000 50  0000 C CNN
F 1 "100" V 4300 2000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 4230 2000 50  0001 C CNN
F 3 "~" H 4300 2000 50  0001 C CNN
	1    4300 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 2000 4650 2000
Wire Wire Line
	4450 2000 4550 2000
Connection ~ 4550 2000
$Comp
L btn-matrix-rescue:GND-power #PWR0104
U 1 1 60741F37
P 4950 2000
F 0 "#PWR0104" H 4950 1750 50  0001 C CNN
F 1 "GND" V 4955 1872 50  0000 R CNN
F 2 "" H 4950 2000 50  0001 C CNN
F 3 "" H 4950 2000 50  0001 C CNN
	1    4950 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0105
U 1 1 60742DD1
P 4150 2000
F 0 "#PWR0105" H 4150 1850 50  0001 C CNN
F 1 "+5V" V 4165 2128 50  0000 L CNN
F 2 "" H 4150 2000 50  0001 C CNN
F 3 "" H 4150 2000 50  0001 C CNN
	1    4150 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R0.1
U 1 1 6074438C
P 4000 2200
F 0 "R0.1" V 3900 2200 50  0000 C CNN
F 1 "33" V 4000 2200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3930 2200 50  0001 C CNN
F 3 "~" H 4000 2200 50  0001 C CNN
	1    4000 2200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R0.2
U 1 1 60746DFB
P 4000 2300
F 0 "R0.2" V 4100 2300 50  0000 C CNN
F 1 "33" V 4000 2300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3930 2300 50  0001 C CNN
F 3 "~" H 4000 2300 50  0001 C CNN
	1    4000 2300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S1
U 1 1 6077C9F5
P 5600 3700
F 0 "S1" H 6100 3550 50  0000 L CNN
F 1 "228CMVARGBFR" H 5900 3450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 6650 4200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 6650 4100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 6650 4000 50  0001 L CNN "Description"
F 5 "7.3" H 6650 3900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 6650 3800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 6650 3700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 6650 3600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 6650 3500 50  0001 L CNN "Manufacturer_Part_Number"
	1    5600 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7050 2300 7050 4550
Wire Wire Line
	7050 4550 6100 4550
Wire Wire Line
	6100 4550 6100 4400
Wire Wire Line
	7150 2200 7150 4400
Wire Wire Line
	6200 4400 7150 4400
Text GLabel 6800 3800 2    50   Output ~ 0
btn01
NoConn ~ 5950 2400
Wire Wire Line
	6750 2300 7050 2300
Wire Wire Line
	6750 2200 7150 2200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U1
U 1 1 6077CA0E
P 6350 2300
F 0 "U1" H 6350 2781 50  0000 C CNN
F 1 "WS2811" H 6350 2690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 6050 2450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 6150 2550 50  0001 C CNN
	1    6350 2300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0107
U 1 1 6077CA14
P 6350 2600
F 0 "#PWR0107" H 6350 2350 50  0001 C CNN
F 1 "GND" V 6355 2472 50  0000 R CNN
F 2 "" H 6350 2600 50  0001 C CNN
F 3 "" H 6350 2600 50  0001 C CNN
	1    6350 2600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0108
U 1 1 6077CA1A
P 6100 3000
F 0 "#PWR0108" H 6100 2850 50  0001 C CNN
F 1 "+5V" H 6115 3173 50  0000 C CNN
F 2 "" H 6100 3000 50  0001 C CNN
F 3 "" H 6100 3000 50  0001 C CNN
	1    6100 3000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C1
U 1 1 6077CA20
P 6600 2000
F 0 "C1" V 6852 2000 50  0000 C CNN
F 1 "104" V 6761 2000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 6638 1850 50  0001 C CNN
F 3 "~" H 6600 2000 50  0001 C CNN
	1    6600 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R1.3
U 1 1 6077CA26
P 6100 2000
F 0 "R1.3" V 6000 2000 50  0000 C CNN
F 1 "100" V 6100 2000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 6030 2000 50  0001 C CNN
F 3 "~" H 6100 2000 50  0001 C CNN
	1    6100 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	6350 2000 6450 2000
Wire Wire Line
	6250 2000 6350 2000
Connection ~ 6350 2000
$Comp
L btn-matrix-rescue:GND-power #PWR0109
U 1 1 6077CA2F
P 6750 2000
F 0 "#PWR0109" H 6750 1750 50  0001 C CNN
F 1 "GND" V 6755 1872 50  0000 R CNN
F 2 "" H 6750 2000 50  0001 C CNN
F 3 "" H 6750 2000 50  0001 C CNN
	1    6750 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0110
U 1 1 6077CA35
P 5950 2000
F 0 "#PWR0110" H 5950 1850 50  0001 C CNN
F 1 "+5V" V 5965 2128 50  0000 L CNN
F 2 "" H 5950 2000 50  0001 C CNN
F 3 "" H 5950 2000 50  0001 C CNN
	1    5950 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R1.1
U 1 1 6077CA3B
P 5800 2200
F 0 "R1.1" V 5700 2200 50  0000 C CNN
F 1 "33" V 5800 2200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5730 2200 50  0001 C CNN
F 3 "~" H 5800 2200 50  0001 C CNN
	1    5800 2200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R1.2
U 1 1 6077CA41
P 5800 2300
F 0 "R1.2" V 5900 2300 50  0000 C CNN
F 1 "33" V 5800 2300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5730 2300 50  0001 C CNN
F 3 "~" H 5800 2300 50  0001 C CNN
	1    5800 2300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S2
U 1 1 60781B69
P 7450 3700
F 0 "S2" H 7950 3550 50  0000 L CNN
F 1 "228CMVARGBFR" H 7750 3450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 8500 4200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 8500 4100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 8500 4000 50  0001 L CNN "Description"
F 5 "7.3" H 8500 3900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 8500 3800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 8500 3700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 8500 3600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 8500 3500 50  0001 L CNN "Manufacturer_Part_Number"
	1    7450 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8600 3000 8050 3000
Wire Wire Line
	8900 2300 8900 4550
Wire Wire Line
	8900 4550 8150 4550
Wire Wire Line
	8150 4550 7950 4400
Wire Wire Line
	9000 2200 9000 4400
Wire Wire Line
	8050 4400 9000 4400
Text GLabel 8650 3800 2    50   Output ~ 0
btn02
NoConn ~ 7800 2400
Wire Wire Line
	8600 2400 8600 3000
Wire Wire Line
	8600 2300 8900 2300
Wire Wire Line
	8600 2200 9000 2200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U2
U 1 1 60781B82
P 8200 2300
F 0 "U2" H 8200 2781 50  0000 C CNN
F 1 "WS2811" H 8200 2690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 7900 2450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 8000 2550 50  0001 C CNN
	1    8200 2300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0112
U 1 1 60781B88
P 8200 2600
F 0 "#PWR0112" H 8200 2350 50  0001 C CNN
F 1 "GND" V 8205 2472 50  0000 R CNN
F 2 "" H 8200 2600 50  0001 C CNN
F 3 "" H 8200 2600 50  0001 C CNN
	1    8200 2600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0113
U 1 1 60781B8E
P 7950 3000
F 0 "#PWR0113" H 7950 2850 50  0001 C CNN
F 1 "+5V" H 7965 3173 50  0000 C CNN
F 2 "" H 7950 3000 50  0001 C CNN
F 3 "" H 7950 3000 50  0001 C CNN
	1    7950 3000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C2
U 1 1 60781B94
P 8450 2000
F 0 "C2" V 8702 2000 50  0000 C CNN
F 1 "104" V 8611 2000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 8488 1850 50  0001 C CNN
F 3 "~" H 8450 2000 50  0001 C CNN
	1    8450 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R2.3
U 1 1 60781B9A
P 7950 2000
F 0 "R2.3" V 7850 2000 50  0000 C CNN
F 1 "100" V 7950 2000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7880 2000 50  0001 C CNN
F 3 "~" H 7950 2000 50  0001 C CNN
	1    7950 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	8200 2000 8300 2000
Wire Wire Line
	8100 2000 8200 2000
Connection ~ 8200 2000
$Comp
L btn-matrix-rescue:GND-power #PWR0114
U 1 1 60781BA3
P 8600 2000
F 0 "#PWR0114" H 8600 1750 50  0001 C CNN
F 1 "GND" V 8605 1872 50  0000 R CNN
F 2 "" H 8600 2000 50  0001 C CNN
F 3 "" H 8600 2000 50  0001 C CNN
	1    8600 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0115
U 1 1 60781BA9
P 7800 2000
F 0 "#PWR0115" H 7800 1850 50  0001 C CNN
F 1 "+5V" V 7815 2128 50  0000 L CNN
F 2 "" H 7800 2000 50  0001 C CNN
F 3 "" H 7800 2000 50  0001 C CNN
	1    7800 2000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R2.1
U 1 1 60781BAF
P 7650 2200
F 0 "R2.1" V 7550 2200 50  0000 C CNN
F 1 "33" V 7650 2200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7580 2200 50  0001 C CNN
F 3 "~" H 7650 2200 50  0001 C CNN
	1    7650 2200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R2.2
U 1 1 60781BB5
P 7650 2300
F 0 "R2.2" V 7750 2300 50  0000 C CNN
F 1 "33" V 7650 2300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7580 2300 50  0001 C CNN
F 3 "~" H 7650 2300 50  0001 C CNN
	1    7650 2300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S3
U 1 1 60786253
P 9300 3750
F 0 "S3" H 9800 3600 50  0000 L CNN
F 1 "228CMVARGBFR" H 9600 3500 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 10350 4250 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 10350 4150 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 10350 4050 50  0001 L CNN "Description"
F 5 "7.3" H 10350 3950 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 10350 3850 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 10350 3750 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 10350 3650 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 10350 3550 50  0001 L CNN "Manufacturer_Part_Number"
	1    9300 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	10500 3050 9900 3050
Wire Wire Line
	10800 2350 10800 4600
Wire Wire Line
	10800 4600 10050 4600
Wire Wire Line
	10050 4600 9800 4450
Wire Wire Line
	10900 2250 10900 4450
Wire Wire Line
	9900 4450 10900 4450
Text GLabel 10500 3850 2    50   Output ~ 0
btn03
NoConn ~ 9700 2450
Wire Wire Line
	10500 2450 10500 3050
Wire Wire Line
	10500 2350 10800 2350
Wire Wire Line
	10500 2250 10900 2250
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U3
U 1 1 6078626C
P 10100 2350
F 0 "U3" H 10100 2831 50  0000 C CNN
F 1 "WS2811" H 10100 2740 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 9800 2500 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 9900 2600 50  0001 C CNN
	1    10100 2350
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0117
U 1 1 60786272
P 10100 2650
F 0 "#PWR0117" H 10100 2400 50  0001 C CNN
F 1 "GND" V 10105 2522 50  0000 R CNN
F 2 "" H 10100 2650 50  0001 C CNN
F 3 "" H 10100 2650 50  0001 C CNN
	1    10100 2650
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0118
U 1 1 60786278
P 9800 3050
F 0 "#PWR0118" H 9800 2900 50  0001 C CNN
F 1 "+5V" H 9815 3223 50  0000 C CNN
F 2 "" H 9800 3050 50  0001 C CNN
F 3 "" H 9800 3050 50  0001 C CNN
	1    9800 3050
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C3
U 1 1 6078627E
P 10350 2050
F 0 "C3" V 10602 2050 50  0000 C CNN
F 1 "104" V 10511 2050 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 10388 1900 50  0001 C CNN
F 3 "~" H 10350 2050 50  0001 C CNN
	1    10350 2050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R3.3
U 1 1 60786284
P 9850 2050
F 0 "R3.3" V 9750 2050 50  0000 C CNN
F 1 "100" V 9850 2050 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9780 2050 50  0001 C CNN
F 3 "~" H 9850 2050 50  0001 C CNN
	1    9850 2050
	0    1    1    0   
$EndComp
Wire Wire Line
	10100 2050 10200 2050
Wire Wire Line
	10000 2050 10100 2050
Connection ~ 10100 2050
$Comp
L btn-matrix-rescue:GND-power #PWR0119
U 1 1 6078628D
P 10500 2050
F 0 "#PWR0119" H 10500 1800 50  0001 C CNN
F 1 "GND" V 10505 1922 50  0000 R CNN
F 2 "" H 10500 2050 50  0001 C CNN
F 3 "" H 10500 2050 50  0001 C CNN
	1    10500 2050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0120
U 1 1 60786293
P 9700 2050
F 0 "#PWR0120" H 9700 1900 50  0001 C CNN
F 1 "+5V" V 9715 2178 50  0000 L CNN
F 2 "" H 9700 2050 50  0001 C CNN
F 3 "" H 9700 2050 50  0001 C CNN
	1    9700 2050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R3.1
U 1 1 60786299
P 9550 2250
F 0 "R3.1" V 9450 2250 50  0000 C CNN
F 1 "33" V 9550 2250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9480 2250 50  0001 C CNN
F 3 "~" H 9550 2250 50  0001 C CNN
	1    9550 2250
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R3.2
U 1 1 6078629F
P 9550 2350
F 0 "R3.2" V 9650 2350 50  0000 C CNN
F 1 "33" V 9550 2350 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9480 2350 50  0001 C CNN
F 3 "~" H 9550 2350 50  0001 C CNN
	1    9550 2350
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S4
U 1 1 607BE839
P 3750 6700
F 0 "S4" H 4250 6550 50  0000 L CNN
F 1 "228CMVARGBFR" H 4050 6450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 4800 7200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 4800 7100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 4800 7000 50  0001 L CNN "Description"
F 5 "7.3" H 4800 6900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 4800 6800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 4800 6700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 4800 6600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 4800 6500 50  0001 L CNN "Manufacturer_Part_Number"
	1    3750 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 6000 4350 6000
Wire Wire Line
	5200 5300 5200 7550
Wire Wire Line
	5200 7550 4450 7550
Wire Wire Line
	4450 7550 4250 7400
Wire Wire Line
	5300 5200 5300 7400
Wire Wire Line
	4350 7400 5300 7400
Text GLabel 4950 6800 2    50   Output ~ 0
btn04
NoConn ~ 4100 5400
Wire Wire Line
	4900 5400 4900 6000
Wire Wire Line
	4900 5300 5200 5300
Wire Wire Line
	4900 5200 5300 5200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U4
U 1 1 607BE852
P 4500 5300
F 0 "U4" H 4500 5781 50  0000 C CNN
F 1 "WS2811" H 4500 5690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 4200 5450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 4300 5550 50  0001 C CNN
	1    4500 5300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0122
U 1 1 607BE858
P 4500 5600
F 0 "#PWR0122" H 4500 5350 50  0001 C CNN
F 1 "GND" V 4505 5472 50  0000 R CNN
F 2 "" H 4500 5600 50  0001 C CNN
F 3 "" H 4500 5600 50  0001 C CNN
	1    4500 5600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0123
U 1 1 607BE85E
P 4250 6000
F 0 "#PWR0123" H 4250 5850 50  0001 C CNN
F 1 "+5V" H 4265 6173 50  0000 C CNN
F 2 "" H 4250 6000 50  0001 C CNN
F 3 "" H 4250 6000 50  0001 C CNN
	1    4250 6000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C4
U 1 1 607BE864
P 4750 5000
F 0 "C4" V 5002 5000 50  0000 C CNN
F 1 "104" V 4911 5000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4788 4850 50  0001 C CNN
F 3 "~" H 4750 5000 50  0001 C CNN
	1    4750 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R4.3
U 1 1 607BE86A
P 4250 5000
F 0 "R4.3" V 4150 5000 50  0000 C CNN
F 1 "100" V 4250 5000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 4180 5000 50  0001 C CNN
F 3 "~" H 4250 5000 50  0001 C CNN
	1    4250 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	4500 5000 4600 5000
Wire Wire Line
	4400 5000 4500 5000
Connection ~ 4500 5000
$Comp
L btn-matrix-rescue:GND-power #PWR0124
U 1 1 607BE873
P 4900 5000
F 0 "#PWR0124" H 4900 4750 50  0001 C CNN
F 1 "GND" V 4905 4872 50  0000 R CNN
F 2 "" H 4900 5000 50  0001 C CNN
F 3 "" H 4900 5000 50  0001 C CNN
	1    4900 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0125
U 1 1 607BE879
P 4100 5000
F 0 "#PWR0125" H 4100 4850 50  0001 C CNN
F 1 "+5V" V 4115 5128 50  0000 L CNN
F 2 "" H 4100 5000 50  0001 C CNN
F 3 "" H 4100 5000 50  0001 C CNN
	1    4100 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R4.1
U 1 1 607BE87F
P 3950 5200
F 0 "R4.1" V 3850 5200 50  0000 C CNN
F 1 "33" V 3950 5200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3880 5200 50  0001 C CNN
F 3 "~" H 3950 5200 50  0001 C CNN
	1    3950 5200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R4.2
U 1 1 607BE885
P 3950 5300
F 0 "R4.2" V 4050 5300 50  0000 C CNN
F 1 "33" V 3950 5300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3880 5300 50  0001 C CNN
F 3 "~" H 3950 5300 50  0001 C CNN
	1    3950 5300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S5
U 1 1 607BE891
P 5550 6700
F 0 "S5" H 6050 6550 50  0000 L CNN
F 1 "228CMVARGBFR" H 5850 6450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 6600 7200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 6600 7100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 6600 7000 50  0001 L CNN "Description"
F 5 "7.3" H 6600 6900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 6600 6800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 6600 6700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 6600 6600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 6600 6500 50  0001 L CNN "Manufacturer_Part_Number"
	1    5550 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6700 6000 6150 6000
Wire Wire Line
	7000 5300 7000 7550
Wire Wire Line
	7000 7550 6250 7550
Wire Wire Line
	6250 7550 6050 7400
Wire Wire Line
	7100 5200 7100 7400
Wire Wire Line
	6150 7400 7100 7400
Text GLabel 6750 6800 2    50   Output ~ 0
btn05
NoConn ~ 5900 5400
Wire Wire Line
	6700 5400 6700 6000
Wire Wire Line
	6700 5300 7000 5300
Wire Wire Line
	6700 5200 7100 5200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U5
U 1 1 607BE8AA
P 6300 5300
F 0 "U5" H 6300 5781 50  0000 C CNN
F 1 "WS2811" H 6300 5690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 6000 5450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 6100 5550 50  0001 C CNN
	1    6300 5300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0127
U 1 1 607BE8B0
P 6300 5600
F 0 "#PWR0127" H 6300 5350 50  0001 C CNN
F 1 "GND" V 6305 5472 50  0000 R CNN
F 2 "" H 6300 5600 50  0001 C CNN
F 3 "" H 6300 5600 50  0001 C CNN
	1    6300 5600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0128
U 1 1 607BE8B6
P 6050 6000
F 0 "#PWR0128" H 6050 5850 50  0001 C CNN
F 1 "+5V" H 6065 6173 50  0000 C CNN
F 2 "" H 6050 6000 50  0001 C CNN
F 3 "" H 6050 6000 50  0001 C CNN
	1    6050 6000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C5
U 1 1 607BE8BC
P 6550 5000
F 0 "C5" V 6802 5000 50  0000 C CNN
F 1 "104" V 6711 5000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 6588 4850 50  0001 C CNN
F 3 "~" H 6550 5000 50  0001 C CNN
	1    6550 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R5.3
U 1 1 607BE8C2
P 6050 5000
F 0 "R5.3" V 5950 5000 50  0000 C CNN
F 1 "100" V 6050 5000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5980 5000 50  0001 C CNN
F 3 "~" H 6050 5000 50  0001 C CNN
	1    6050 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	6300 5000 6400 5000
Wire Wire Line
	6200 5000 6300 5000
Connection ~ 6300 5000
$Comp
L btn-matrix-rescue:GND-power #PWR0129
U 1 1 607BE8CB
P 6700 5000
F 0 "#PWR0129" H 6700 4750 50  0001 C CNN
F 1 "GND" V 6705 4872 50  0000 R CNN
F 2 "" H 6700 5000 50  0001 C CNN
F 3 "" H 6700 5000 50  0001 C CNN
	1    6700 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0130
U 1 1 607BE8D1
P 5900 5000
F 0 "#PWR0130" H 5900 4850 50  0001 C CNN
F 1 "+5V" V 5915 5128 50  0000 L CNN
F 2 "" H 5900 5000 50  0001 C CNN
F 3 "" H 5900 5000 50  0001 C CNN
	1    5900 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R5.1
U 1 1 607BE8D7
P 5750 5200
F 0 "R5.1" V 5650 5200 50  0000 C CNN
F 1 "33" V 5750 5200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5680 5200 50  0001 C CNN
F 3 "~" H 5750 5200 50  0001 C CNN
	1    5750 5200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R5.2
U 1 1 607BE8DD
P 5750 5300
F 0 "R5.2" V 5850 5300 50  0000 C CNN
F 1 "33" V 5750 5300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5680 5300 50  0001 C CNN
F 3 "~" H 5750 5300 50  0001 C CNN
	1    5750 5300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S6
U 1 1 607BE8E9
P 7350 6700
F 0 "S6" H 7850 6550 50  0000 L CNN
F 1 "228CMVARGBFR" H 7650 6450 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 8400 7200 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 8400 7100 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 8400 7000 50  0001 L CNN "Description"
F 5 "7.3" H 8400 6900 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 8400 6800 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 8400 6700 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 8400 6600 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 8400 6500 50  0001 L CNN "Manufacturer_Part_Number"
	1    7350 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8550 6000 7950 6000
Wire Wire Line
	8850 5300 8850 7550
Wire Wire Line
	8850 7550 8100 7550
Wire Wire Line
	8100 7550 7850 7400
Wire Wire Line
	8950 5200 8950 7400
Wire Wire Line
	7950 7400 8950 7400
Text GLabel 8550 6800 2    50   Output ~ 0
btn06
NoConn ~ 7750 5400
Wire Wire Line
	8550 5400 8550 6000
Wire Wire Line
	8550 5300 8850 5300
Wire Wire Line
	8550 5200 8950 5200
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U6
U 1 1 607BE902
P 8150 5300
F 0 "U6" H 8150 5781 50  0000 C CNN
F 1 "WS2811" H 8150 5690 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 7850 5450 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 7950 5550 50  0001 C CNN
	1    8150 5300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0132
U 1 1 607BE908
P 8150 5600
F 0 "#PWR0132" H 8150 5350 50  0001 C CNN
F 1 "GND" V 8155 5472 50  0000 R CNN
F 2 "" H 8150 5600 50  0001 C CNN
F 3 "" H 8150 5600 50  0001 C CNN
	1    8150 5600
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0133
U 1 1 607BE90E
P 7850 6000
F 0 "#PWR0133" H 7850 5850 50  0001 C CNN
F 1 "+5V" H 7865 6173 50  0000 C CNN
F 2 "" H 7850 6000 50  0001 C CNN
F 3 "" H 7850 6000 50  0001 C CNN
	1    7850 6000
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C6
U 1 1 607BE914
P 8400 5000
F 0 "C6" V 8652 5000 50  0000 C CNN
F 1 "104" V 8561 5000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 8438 4850 50  0001 C CNN
F 3 "~" H 8400 5000 50  0001 C CNN
	1    8400 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R6.3
U 1 1 607BE91A
P 7900 5000
F 0 "R6.3" V 7800 5000 50  0000 C CNN
F 1 "100" V 7900 5000 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7830 5000 50  0001 C CNN
F 3 "~" H 7900 5000 50  0001 C CNN
	1    7900 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	8150 5000 8250 5000
Wire Wire Line
	8050 5000 8150 5000
Connection ~ 8150 5000
$Comp
L btn-matrix-rescue:GND-power #PWR0134
U 1 1 607BE923
P 8550 5000
F 0 "#PWR0134" H 8550 4750 50  0001 C CNN
F 1 "GND" V 8555 4872 50  0000 R CNN
F 2 "" H 8550 5000 50  0001 C CNN
F 3 "" H 8550 5000 50  0001 C CNN
	1    8550 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0135
U 1 1 607BE929
P 7750 5000
F 0 "#PWR0135" H 7750 4850 50  0001 C CNN
F 1 "+5V" V 7765 5128 50  0000 L CNN
F 2 "" H 7750 5000 50  0001 C CNN
F 3 "" H 7750 5000 50  0001 C CNN
	1    7750 5000
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R6.1
U 1 1 607BE92F
P 7600 5200
F 0 "R6.1" V 7500 5200 50  0000 C CNN
F 1 "33" V 7600 5200 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7530 5200 50  0001 C CNN
F 3 "~" H 7600 5200 50  0001 C CNN
	1    7600 5200
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R6.2
U 1 1 607BE935
P 7600 5300
F 0 "R6.2" V 7700 5300 50  0000 C CNN
F 1 "33" V 7600 5300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7530 5300 50  0001 C CNN
F 3 "~" H 7600 5300 50  0001 C CNN
	1    7600 5300
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S7
U 1 1 607BE941
P 9250 6750
F 0 "S7" H 9750 6600 50  0000 L CNN
F 1 "228CMVARGBFR" H 9550 6500 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 10300 7250 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 10300 7150 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 10300 7050 50  0001 L CNN "Description"
F 5 "7.3" H 10300 6950 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 10300 6850 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 10300 6750 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 10300 6650 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 10300 6550 50  0001 L CNN "Manufacturer_Part_Number"
	1    9250 6750
	1    0    0    -1  
$EndComp
Wire Wire Line
	10450 6050 9850 6050
Wire Wire Line
	10750 5350 10750 7600
Wire Wire Line
	10750 7600 10000 7600
Wire Wire Line
	10000 7600 9750 7450
Wire Wire Line
	10850 5250 10850 7450
Wire Wire Line
	9850 7450 10850 7450
Text GLabel 10450 6850 2    50   Output ~ 0
btn07
NoConn ~ 9650 5450
Wire Wire Line
	10450 5450 10450 6050
Wire Wire Line
	10450 5350 10750 5350
Wire Wire Line
	10450 5250 10850 5250
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U7
U 1 1 607BE95A
P 10050 5350
F 0 "U7" H 10050 5831 50  0000 C CNN
F 1 "WS2811" H 10050 5740 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 9750 5500 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 9850 5600 50  0001 C CNN
	1    10050 5350
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0137
U 1 1 607BE960
P 10050 5650
F 0 "#PWR0137" H 10050 5400 50  0001 C CNN
F 1 "GND" V 10055 5522 50  0000 R CNN
F 2 "" H 10050 5650 50  0001 C CNN
F 3 "" H 10050 5650 50  0001 C CNN
	1    10050 5650
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0138
U 1 1 607BE966
P 9750 6050
F 0 "#PWR0138" H 9750 5900 50  0001 C CNN
F 1 "+5V" H 9765 6223 50  0000 C CNN
F 2 "" H 9750 6050 50  0001 C CNN
F 3 "" H 9750 6050 50  0001 C CNN
	1    9750 6050
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C7
U 1 1 607BE96C
P 10300 5050
F 0 "C7" V 10552 5050 50  0000 C CNN
F 1 "104" V 10461 5050 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 10338 4900 50  0001 C CNN
F 3 "~" H 10300 5050 50  0001 C CNN
	1    10300 5050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R7.3
U 1 1 607BE972
P 9800 5050
F 0 "R7.3" V 9700 5050 50  0000 C CNN
F 1 "100" V 9800 5050 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9730 5050 50  0001 C CNN
F 3 "~" H 9800 5050 50  0001 C CNN
	1    9800 5050
	0    1    1    0   
$EndComp
Wire Wire Line
	10050 5050 10150 5050
Wire Wire Line
	9950 5050 10050 5050
Connection ~ 10050 5050
$Comp
L btn-matrix-rescue:GND-power #PWR0139
U 1 1 607BE97B
P 10450 5050
F 0 "#PWR0139" H 10450 4800 50  0001 C CNN
F 1 "GND" V 10455 4922 50  0000 R CNN
F 2 "" H 10450 5050 50  0001 C CNN
F 3 "" H 10450 5050 50  0001 C CNN
	1    10450 5050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0140
U 1 1 607BE981
P 9650 5050
F 0 "#PWR0140" H 9650 4900 50  0001 C CNN
F 1 "+5V" V 9665 5178 50  0000 L CNN
F 2 "" H 9650 5050 50  0001 C CNN
F 3 "" H 9650 5050 50  0001 C CNN
	1    9650 5050
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R7.1
U 1 1 607BE987
P 9500 5250
F 0 "R7.1" V 9400 5250 50  0000 C CNN
F 1 "33" V 9500 5250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9430 5250 50  0001 C CNN
F 3 "~" H 9500 5250 50  0001 C CNN
	1    9500 5250
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R7.2
U 1 1 607BE98D
P 9500 5350
F 0 "R7.2" V 9600 5350 50  0000 C CNN
F 1 "33" V 9500 5350 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9430 5350 50  0001 C CNN
F 3 "~" H 9500 5350 50  0001 C CNN
	1    9500 5350
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S8
U 1 1 607D70DD
P 3650 9950
F 0 "S8" H 4150 9800 50  0000 L CNN
F 1 "228CMVARGBFR" H 3950 9700 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 4700 10450 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 4700 10350 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 4700 10250 50  0001 L CNN "Description"
F 5 "7.3" H 4700 10150 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 4700 10050 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 4700 9950 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 4700 9850 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 4700 9750 50  0001 L CNN "Manufacturer_Part_Number"
	1    3650 9950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 9250 4250 9250
Wire Wire Line
	5150 8550 5150 10800
Wire Wire Line
	5150 10800 4400 10800
Wire Wire Line
	4400 10800 4150 10650
Wire Wire Line
	5250 8450 5250 10650
Wire Wire Line
	4250 10650 5250 10650
Text GLabel 4850 10050 2    50   Output ~ 0
btn08
NoConn ~ 4050 8650
Wire Wire Line
	4850 8650 4850 9250
Wire Wire Line
	4850 8550 5150 8550
Wire Wire Line
	4850 8450 5250 8450
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U8
U 1 1 607D70F6
P 4450 8550
F 0 "U8" H 4450 9031 50  0000 C CNN
F 1 "WS2811" H 4450 8940 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 4150 8700 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 4250 8800 50  0001 C CNN
	1    4450 8550
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0142
U 1 1 607D70FC
P 4450 8850
F 0 "#PWR0142" H 4450 8600 50  0001 C CNN
F 1 "GND" V 4455 8722 50  0000 R CNN
F 2 "" H 4450 8850 50  0001 C CNN
F 3 "" H 4450 8850 50  0001 C CNN
	1    4450 8850
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0143
U 1 1 607D7102
P 4150 9250
F 0 "#PWR0143" H 4150 9100 50  0001 C CNN
F 1 "+5V" H 4165 9423 50  0000 C CNN
F 2 "" H 4150 9250 50  0001 C CNN
F 3 "" H 4150 9250 50  0001 C CNN
	1    4150 9250
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C8
U 1 1 607D7108
P 4700 8250
F 0 "C8" V 4952 8250 50  0000 C CNN
F 1 "104" V 4861 8250 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4738 8100 50  0001 C CNN
F 3 "~" H 4700 8250 50  0001 C CNN
	1    4700 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R8.3
U 1 1 607D710E
P 4200 8250
F 0 "R8.3" V 4100 8250 50  0000 C CNN
F 1 "100" V 4200 8250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 4130 8250 50  0001 C CNN
F 3 "~" H 4200 8250 50  0001 C CNN
	1    4200 8250
	0    1    1    0   
$EndComp
Wire Wire Line
	4450 8250 4550 8250
Wire Wire Line
	4350 8250 4450 8250
Connection ~ 4450 8250
$Comp
L btn-matrix-rescue:GND-power #PWR0144
U 1 1 607D7117
P 4850 8250
F 0 "#PWR0144" H 4850 8000 50  0001 C CNN
F 1 "GND" V 4855 8122 50  0000 R CNN
F 2 "" H 4850 8250 50  0001 C CNN
F 3 "" H 4850 8250 50  0001 C CNN
	1    4850 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0145
U 1 1 607D711D
P 4050 8250
F 0 "#PWR0145" H 4050 8100 50  0001 C CNN
F 1 "+5V" V 4065 8378 50  0000 L CNN
F 2 "" H 4050 8250 50  0001 C CNN
F 3 "" H 4050 8250 50  0001 C CNN
	1    4050 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R8.1
U 1 1 607D7123
P 3900 8450
F 0 "R8.1" V 3800 8450 50  0000 C CNN
F 1 "33" V 3900 8450 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3830 8450 50  0001 C CNN
F 3 "~" H 3900 8450 50  0001 C CNN
	1    3900 8450
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R8.2
U 1 1 607D7129
P 3900 8550
F 0 "R8.2" V 4000 8550 50  0000 C CNN
F 1 "33" V 3900 8550 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3830 8550 50  0001 C CNN
F 3 "~" H 3900 8550 50  0001 C CNN
	1    3900 8550
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S9
U 1 1 607D7135
P 5400 9950
F 0 "S9" H 5900 9800 50  0000 L CNN
F 1 "228CMVARGBFR" H 5700 9700 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 6450 10450 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 6450 10350 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 6450 10250 50  0001 L CNN "Description"
F 5 "7.3" H 6450 10150 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 6450 10050 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 6450 9950 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 6450 9850 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 6450 9750 50  0001 L CNN "Manufacturer_Part_Number"
	1    5400 9950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6650 9250 6000 9250
Wire Wire Line
	6950 8550 6950 10800
Wire Wire Line
	6950 10800 6200 10800
Wire Wire Line
	6200 10800 5900 10650
Wire Wire Line
	7050 8450 7050 10650
Wire Wire Line
	6000 10650 7050 10650
Text GLabel 6600 10050 2    50   Output ~ 0
btn09
NoConn ~ 5850 8650
Wire Wire Line
	6650 8650 6650 9250
Wire Wire Line
	6650 8550 6950 8550
Wire Wire Line
	6650 8450 7050 8450
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U9
U 1 1 607D714E
P 6250 8550
F 0 "U9" H 6250 9031 50  0000 C CNN
F 1 "WS2811" H 6250 8940 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 5950 8700 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 6050 8800 50  0001 C CNN
	1    6250 8550
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0147
U 1 1 607D7154
P 6250 8850
F 0 "#PWR0147" H 6250 8600 50  0001 C CNN
F 1 "GND" V 6255 8722 50  0000 R CNN
F 2 "" H 6250 8850 50  0001 C CNN
F 3 "" H 6250 8850 50  0001 C CNN
	1    6250 8850
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0148
U 1 1 607D715A
P 5900 9250
F 0 "#PWR0148" H 5900 9100 50  0001 C CNN
F 1 "+5V" H 5915 9423 50  0000 C CNN
F 2 "" H 5900 9250 50  0001 C CNN
F 3 "" H 5900 9250 50  0001 C CNN
	1    5900 9250
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C9
U 1 1 607D7160
P 6500 8250
F 0 "C9" V 6752 8250 50  0000 C CNN
F 1 "104" V 6661 8250 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 6538 8100 50  0001 C CNN
F 3 "~" H 6500 8250 50  0001 C CNN
	1    6500 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R9.3
U 1 1 607D7166
P 6000 8250
F 0 "R9.3" V 5900 8250 50  0000 C CNN
F 1 "100" V 6000 8250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5930 8250 50  0001 C CNN
F 3 "~" H 6000 8250 50  0001 C CNN
	1    6000 8250
	0    1    1    0   
$EndComp
Wire Wire Line
	6250 8250 6350 8250
Wire Wire Line
	6150 8250 6250 8250
Connection ~ 6250 8250
$Comp
L btn-matrix-rescue:GND-power #PWR0149
U 1 1 607D716F
P 6650 8250
F 0 "#PWR0149" H 6650 8000 50  0001 C CNN
F 1 "GND" V 6655 8122 50  0000 R CNN
F 2 "" H 6650 8250 50  0001 C CNN
F 3 "" H 6650 8250 50  0001 C CNN
	1    6650 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0150
U 1 1 607D7175
P 5850 8250
F 0 "#PWR0150" H 5850 8100 50  0001 C CNN
F 1 "+5V" V 5865 8378 50  0000 L CNN
F 2 "" H 5850 8250 50  0001 C CNN
F 3 "" H 5850 8250 50  0001 C CNN
	1    5850 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R9.1
U 1 1 607D717B
P 5700 8450
F 0 "R9.1" V 5600 8450 50  0000 C CNN
F 1 "33" V 5700 8450 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5630 8450 50  0001 C CNN
F 3 "~" H 5700 8450 50  0001 C CNN
	1    5700 8450
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R9.2
U 1 1 607D7181
P 5700 8550
F 0 "R9.2" V 5800 8550 50  0000 C CNN
F 1 "33" V 5700 8550 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5630 8550 50  0001 C CNN
F 3 "~" H 5700 8550 50  0001 C CNN
	1    5700 8550
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S10
U 1 1 607D718D
P 7200 9950
F 0 "S10" H 7700 9800 50  0000 L CNN
F 1 "228CMVARGBFR" H 7500 9700 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 8250 10450 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 8250 10350 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 8250 10250 50  0001 L CNN "Description"
F 5 "7.3" H 8250 10150 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 8250 10050 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 8250 9950 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 8250 9850 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 8250 9750 50  0001 L CNN "Manufacturer_Part_Number"
	1    7200 9950
	1    0    0    -1  
$EndComp
Wire Wire Line
	8500 9250 7800 9250
Wire Wire Line
	8800 8550 8800 10800
Wire Wire Line
	8800 10800 8050 10800
Wire Wire Line
	8050 10800 7700 10650
Wire Wire Line
	8900 8450 8900 10650
Wire Wire Line
	7800 10650 8900 10650
Text GLabel 8400 10050 2    50   Output ~ 0
btn10
NoConn ~ 7700 8650
Wire Wire Line
	8500 8650 8500 9250
Wire Wire Line
	8500 8550 8800 8550
Wire Wire Line
	8500 8450 8900 8450
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U10
U 1 1 607D71A6
P 8100 8550
F 0 "U10" H 8100 9031 50  0000 C CNN
F 1 "WS2811" H 8100 8940 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 7800 8700 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 7900 8800 50  0001 C CNN
	1    8100 8550
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0152
U 1 1 607D71AC
P 8100 8850
F 0 "#PWR0152" H 8100 8600 50  0001 C CNN
F 1 "GND" V 8105 8722 50  0000 R CNN
F 2 "" H 8100 8850 50  0001 C CNN
F 3 "" H 8100 8850 50  0001 C CNN
	1    8100 8850
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0153
U 1 1 607D71B2
P 7700 9250
F 0 "#PWR0153" H 7700 9100 50  0001 C CNN
F 1 "+5V" H 7715 9423 50  0000 C CNN
F 2 "" H 7700 9250 50  0001 C CNN
F 3 "" H 7700 9250 50  0001 C CNN
	1    7700 9250
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C10
U 1 1 607D71B8
P 8350 8250
F 0 "C10" V 8602 8250 50  0000 C CNN
F 1 "104" V 8511 8250 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 8388 8100 50  0001 C CNN
F 3 "~" H 8350 8250 50  0001 C CNN
	1    8350 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R10.3
U 1 1 607D71BE
P 7850 8250
F 0 "R10.3" V 7750 8250 50  0000 C CNN
F 1 "100" V 7850 8250 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7780 8250 50  0001 C CNN
F 3 "~" H 7850 8250 50  0001 C CNN
	1    7850 8250
	0    1    1    0   
$EndComp
Wire Wire Line
	8100 8250 8200 8250
Wire Wire Line
	8000 8250 8100 8250
Connection ~ 8100 8250
$Comp
L btn-matrix-rescue:GND-power #PWR0154
U 1 1 607D71C7
P 8500 8250
F 0 "#PWR0154" H 8500 8000 50  0001 C CNN
F 1 "GND" V 8505 8122 50  0000 R CNN
F 2 "" H 8500 8250 50  0001 C CNN
F 3 "" H 8500 8250 50  0001 C CNN
	1    8500 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0155
U 1 1 607D71CD
P 7700 8250
F 0 "#PWR0155" H 7700 8100 50  0001 C CNN
F 1 "+5V" V 7715 8378 50  0000 L CNN
F 2 "" H 7700 8250 50  0001 C CNN
F 3 "" H 7700 8250 50  0001 C CNN
	1    7700 8250
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R10.1
U 1 1 607D71D3
P 7550 8450
F 0 "R10.1" V 7450 8450 50  0000 C CNN
F 1 "33" V 7550 8450 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7480 8450 50  0001 C CNN
F 3 "~" H 7550 8450 50  0001 C CNN
	1    7550 8450
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R10.2
U 1 1 607D71D9
P 7550 8550
F 0 "R10.2" V 7650 8550 50  0000 C CNN
F 1 "33" V 7550 8550 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7480 8550 50  0001 C CNN
F 3 "~" H 7550 8550 50  0001 C CNN
	1    7550 8550
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S11
U 1 1 607D71E5
P 9150 10000
F 0 "S11" H 9650 9850 50  0000 L CNN
F 1 "228CMVARGBFR" H 9450 9750 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 10200 10500 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 10200 10400 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 10200 10300 50  0001 L CNN "Description"
F 5 "7.3" H 10200 10200 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 10200 10100 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 10200 10000 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 10200 9900 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 10200 9800 50  0001 L CNN "Manufacturer_Part_Number"
	1    9150 10000
	1    0    0    -1  
$EndComp
Wire Wire Line
	10400 9300 9750 9300
Wire Wire Line
	10700 8600 10700 10850
Wire Wire Line
	10700 10850 9950 10850
Wire Wire Line
	9950 10850 9650 10700
Wire Wire Line
	10800 8500 10800 10700
Wire Wire Line
	9750 10700 10800 10700
Text GLabel 10350 10100 2    50   Output ~ 0
btn11
NoConn ~ 9600 8700
Wire Wire Line
	10400 8700 10400 9300
Wire Wire Line
	10400 8600 10700 8600
Wire Wire Line
	10400 8500 10800 8500
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U11
U 1 1 607D71FE
P 10000 8600
F 0 "U11" H 10000 9081 50  0000 C CNN
F 1 "WS2811" H 10000 8990 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 9700 8750 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 9800 8850 50  0001 C CNN
	1    10000 8600
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0157
U 1 1 607D7204
P 10000 8900
F 0 "#PWR0157" H 10000 8650 50  0001 C CNN
F 1 "GND" V 10005 8772 50  0000 R CNN
F 2 "" H 10000 8900 50  0001 C CNN
F 3 "" H 10000 8900 50  0001 C CNN
	1    10000 8900
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0158
U 1 1 607D720A
P 9650 9300
F 0 "#PWR0158" H 9650 9150 50  0001 C CNN
F 1 "+5V" H 9665 9473 50  0000 C CNN
F 2 "" H 9650 9300 50  0001 C CNN
F 3 "" H 9650 9300 50  0001 C CNN
	1    9650 9300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C11
U 1 1 607D7210
P 10250 8300
F 0 "C11" V 10502 8300 50  0000 C CNN
F 1 "104" V 10411 8300 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 10288 8150 50  0001 C CNN
F 3 "~" H 10250 8300 50  0001 C CNN
	1    10250 8300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R11.3
U 1 1 607D7216
P 9750 8300
F 0 "R11.3" V 9650 8300 50  0000 C CNN
F 1 "100" V 9750 8300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9680 8300 50  0001 C CNN
F 3 "~" H 9750 8300 50  0001 C CNN
	1    9750 8300
	0    1    1    0   
$EndComp
Wire Wire Line
	10000 8300 10100 8300
Wire Wire Line
	9900 8300 10000 8300
Connection ~ 10000 8300
$Comp
L btn-matrix-rescue:GND-power #PWR0159
U 1 1 607D721F
P 10400 8300
F 0 "#PWR0159" H 10400 8050 50  0001 C CNN
F 1 "GND" V 10405 8172 50  0000 R CNN
F 2 "" H 10400 8300 50  0001 C CNN
F 3 "" H 10400 8300 50  0001 C CNN
	1    10400 8300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0160
U 1 1 607D7225
P 9600 8300
F 0 "#PWR0160" H 9600 8150 50  0001 C CNN
F 1 "+5V" V 9615 8428 50  0000 L CNN
F 2 "" H 9600 8300 50  0001 C CNN
F 3 "" H 9600 8300 50  0001 C CNN
	1    9600 8300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R11.1
U 1 1 607D722B
P 9450 8500
F 0 "R11.1" V 9350 8500 50  0000 C CNN
F 1 "33" V 9450 8500 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9380 8500 50  0001 C CNN
F 3 "~" H 9450 8500 50  0001 C CNN
	1    9450 8500
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R11.2
U 1 1 607D7231
P 9450 8600
F 0 "R11.2" V 9550 8600 50  0000 C CNN
F 1 "33" V 9450 8600 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9380 8600 50  0001 C CNN
F 3 "~" H 9450 8600 50  0001 C CNN
	1    9450 8600
	0    1    1    0   
$EndComp
Wire Wire Line
	4800 12300 4150 12300
Wire Wire Line
	5100 11600 5100 13850
Wire Wire Line
	5100 13850 4350 13850
Wire Wire Line
	4350 13850 4050 13700
Wire Wire Line
	5200 11500 5200 13700
Wire Wire Line
	4150 13700 5200 13700
Text GLabel 4750 13100 2    50   Output ~ 0
btn12
NoConn ~ 4000 11700
Wire Wire Line
	4800 11700 4800 12300
Wire Wire Line
	4800 11600 5100 11600
Wire Wire Line
	4800 11500 5200 11500
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U12
U 1 1 607EFF88
P 4400 11600
F 0 "U12" H 4400 12081 50  0000 C CNN
F 1 "WS2811" H 4400 11990 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 4100 11750 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 4200 11850 50  0001 C CNN
	1    4400 11600
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0162
U 1 1 607EFF8E
P 4400 11900
F 0 "#PWR0162" H 4400 11650 50  0001 C CNN
F 1 "GND" V 4405 11772 50  0000 R CNN
F 2 "" H 4400 11900 50  0001 C CNN
F 3 "" H 4400 11900 50  0001 C CNN
	1    4400 11900
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0163
U 1 1 607EFF94
P 4050 12300
F 0 "#PWR0163" H 4050 12150 50  0001 C CNN
F 1 "+5V" H 4065 12473 50  0000 C CNN
F 2 "" H 4050 12300 50  0001 C CNN
F 3 "" H 4050 12300 50  0001 C CNN
	1    4050 12300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C12
U 1 1 607EFF9A
P 4650 11300
F 0 "C12" V 4902 11300 50  0000 C CNN
F 1 "104" V 4811 11300 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4688 11150 50  0001 C CNN
F 3 "~" H 4650 11300 50  0001 C CNN
	1    4650 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R12.3
U 1 1 607EFFA0
P 4150 11300
F 0 "R12.3" V 4050 11300 50  0000 C CNN
F 1 "100" V 4150 11300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 4080 11300 50  0001 C CNN
F 3 "~" H 4150 11300 50  0001 C CNN
	1    4150 11300
	0    1    1    0   
$EndComp
Wire Wire Line
	4400 11300 4500 11300
Wire Wire Line
	4300 11300 4400 11300
Connection ~ 4400 11300
$Comp
L btn-matrix-rescue:GND-power #PWR0164
U 1 1 607EFFA9
P 4800 11300
F 0 "#PWR0164" H 4800 11050 50  0001 C CNN
F 1 "GND" V 4805 11172 50  0000 R CNN
F 2 "" H 4800 11300 50  0001 C CNN
F 3 "" H 4800 11300 50  0001 C CNN
	1    4800 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0165
U 1 1 607EFFAF
P 4000 11300
F 0 "#PWR0165" H 4000 11150 50  0001 C CNN
F 1 "+5V" V 4015 11428 50  0000 L CNN
F 2 "" H 4000 11300 50  0001 C CNN
F 3 "" H 4000 11300 50  0001 C CNN
	1    4000 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R12.1
U 1 1 607EFFB5
P 3850 11500
F 0 "R12.1" V 3750 11500 50  0000 C CNN
F 1 "33" V 3850 11500 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3780 11500 50  0001 C CNN
F 3 "~" H 3850 11500 50  0001 C CNN
	1    3850 11500
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R12.2
U 1 1 607EFFBB
P 3850 11600
F 0 "R12.2" V 3950 11600 50  0000 C CNN
F 1 "33" V 3850 11600 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 3780 11600 50  0001 C CNN
F 3 "~" H 3850 11600 50  0001 C CNN
	1    3850 11600
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S13
U 1 1 607EFFC7
P 5400 13000
F 0 "S13" H 5900 12850 50  0000 L CNN
F 1 "228CMVARGBFR" H 5700 12750 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 6450 13500 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 6450 13400 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 6450 13300 50  0001 L CNN "Description"
F 5 "7.3" H 6450 13200 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 6450 13100 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 6450 13000 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 6450 12900 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 6450 12800 50  0001 L CNN "Manufacturer_Part_Number"
	1    5400 13000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6600 12300 6000 12300
Wire Wire Line
	6900 11600 6900 13850
Wire Wire Line
	6900 13850 6150 13850
Wire Wire Line
	6150 13850 5900 13700
Wire Wire Line
	7000 11500 7000 13700
Wire Wire Line
	6000 13700 7000 13700
Text GLabel 6600 13100 2    50   Output ~ 0
btn13
NoConn ~ 5800 11700
Wire Wire Line
	6600 11700 6600 12300
Wire Wire Line
	6600 11600 6900 11600
Wire Wire Line
	6600 11500 7000 11500
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U13
U 1 1 607EFFE0
P 6200 11600
F 0 "U13" H 6200 12081 50  0000 C CNN
F 1 "WS2811" H 6200 11990 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 5900 11750 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 6000 11850 50  0001 C CNN
	1    6200 11600
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0167
U 1 1 607EFFE6
P 6200 11900
F 0 "#PWR0167" H 6200 11650 50  0001 C CNN
F 1 "GND" V 6205 11772 50  0000 R CNN
F 2 "" H 6200 11900 50  0001 C CNN
F 3 "" H 6200 11900 50  0001 C CNN
	1    6200 11900
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0168
U 1 1 607EFFEC
P 5900 12300
F 0 "#PWR0168" H 5900 12150 50  0001 C CNN
F 1 "+5V" H 5915 12473 50  0000 C CNN
F 2 "" H 5900 12300 50  0001 C CNN
F 3 "" H 5900 12300 50  0001 C CNN
	1    5900 12300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C13
U 1 1 607EFFF2
P 6450 11300
F 0 "C13" V 6702 11300 50  0000 C CNN
F 1 "104" V 6611 11300 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 6488 11150 50  0001 C CNN
F 3 "~" H 6450 11300 50  0001 C CNN
	1    6450 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R13.3
U 1 1 607EFFF8
P 5950 11300
F 0 "R13.3" V 5850 11300 50  0000 C CNN
F 1 "100" V 5950 11300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5880 11300 50  0001 C CNN
F 3 "~" H 5950 11300 50  0001 C CNN
	1    5950 11300
	0    1    1    0   
$EndComp
Wire Wire Line
	6200 11300 6300 11300
Wire Wire Line
	6100 11300 6200 11300
Connection ~ 6200 11300
$Comp
L btn-matrix-rescue:GND-power #PWR0169
U 1 1 607F0001
P 6600 11300
F 0 "#PWR0169" H 6600 11050 50  0001 C CNN
F 1 "GND" V 6605 11172 50  0000 R CNN
F 2 "" H 6600 11300 50  0001 C CNN
F 3 "" H 6600 11300 50  0001 C CNN
	1    6600 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0170
U 1 1 607F0007
P 5800 11300
F 0 "#PWR0170" H 5800 11150 50  0001 C CNN
F 1 "+5V" V 5815 11428 50  0000 L CNN
F 2 "" H 5800 11300 50  0001 C CNN
F 3 "" H 5800 11300 50  0001 C CNN
	1    5800 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R13.1
U 1 1 607F000D
P 5650 11500
F 0 "R13.1" V 5550 11500 50  0000 C CNN
F 1 "33" V 5650 11500 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5580 11500 50  0001 C CNN
F 3 "~" H 5650 11500 50  0001 C CNN
	1    5650 11500
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R13.2
U 1 1 607F0013
P 5650 11600
F 0 "R13.2" V 5750 11600 50  0000 C CNN
F 1 "33" V 5650 11600 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 5580 11600 50  0001 C CNN
F 3 "~" H 5650 11600 50  0001 C CNN
	1    5650 11600
	0    1    1    0   
$EndComp
Wire Wire Line
	8450 12300 7800 12300
Wire Wire Line
	8750 11600 8750 13850
Wire Wire Line
	8750 13850 8000 13850
Wire Wire Line
	8000 13850 7700 13700
Wire Wire Line
	8850 11500 8850 13700
Wire Wire Line
	7800 13700 8850 13700
Text GLabel 8400 13100 2    50   Output ~ 0
btn14
NoConn ~ 7650 11700
Wire Wire Line
	8450 11700 8450 12300
Wire Wire Line
	8450 11600 8750 11600
Wire Wire Line
	8450 11500 8850 11500
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U14
U 1 1 607F0038
P 8050 11600
F 0 "U14" H 8050 12081 50  0000 C CNN
F 1 "WS2811" H 8050 11990 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 7750 11750 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 7850 11850 50  0001 C CNN
	1    8050 11600
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0172
U 1 1 607F003E
P 8050 11900
F 0 "#PWR0172" H 8050 11650 50  0001 C CNN
F 1 "GND" V 8055 11772 50  0000 R CNN
F 2 "" H 8050 11900 50  0001 C CNN
F 3 "" H 8050 11900 50  0001 C CNN
	1    8050 11900
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0173
U 1 1 607F0044
P 7700 12300
F 0 "#PWR0173" H 7700 12150 50  0001 C CNN
F 1 "+5V" H 7715 12473 50  0000 C CNN
F 2 "" H 7700 12300 50  0001 C CNN
F 3 "" H 7700 12300 50  0001 C CNN
	1    7700 12300
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C14
U 1 1 607F004A
P 8300 11300
F 0 "C14" V 8552 11300 50  0000 C CNN
F 1 "104" V 8461 11300 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 8338 11150 50  0001 C CNN
F 3 "~" H 8300 11300 50  0001 C CNN
	1    8300 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R14.3
U 1 1 607F0050
P 7800 11300
F 0 "R14.3" V 7700 11300 50  0000 C CNN
F 1 "100" V 7800 11300 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7730 11300 50  0001 C CNN
F 3 "~" H 7800 11300 50  0001 C CNN
	1    7800 11300
	0    1    1    0   
$EndComp
Wire Wire Line
	8050 11300 8150 11300
Wire Wire Line
	7950 11300 8050 11300
Connection ~ 8050 11300
$Comp
L btn-matrix-rescue:GND-power #PWR0174
U 1 1 607F0059
P 8450 11300
F 0 "#PWR0174" H 8450 11050 50  0001 C CNN
F 1 "GND" V 8455 11172 50  0000 R CNN
F 2 "" H 8450 11300 50  0001 C CNN
F 3 "" H 8450 11300 50  0001 C CNN
	1    8450 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0175
U 1 1 607F005F
P 7650 11300
F 0 "#PWR0175" H 7650 11150 50  0001 C CNN
F 1 "+5V" V 7665 11428 50  0000 L CNN
F 2 "" H 7650 11300 50  0001 C CNN
F 3 "" H 7650 11300 50  0001 C CNN
	1    7650 11300
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R14.1
U 1 1 607F0065
P 7500 11500
F 0 "R14.1" V 7400 11500 50  0000 C CNN
F 1 "33" V 7500 11500 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7430 11500 50  0001 C CNN
F 3 "~" H 7500 11500 50  0001 C CNN
	1    7500 11500
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R14.2
U 1 1 607F006B
P 7500 11600
F 0 "R14.2" V 7600 11600 50  0000 C CNN
F 1 "33" V 7500 11600 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 7430 11600 50  0001 C CNN
F 3 "~" H 7500 11600 50  0001 C CNN
	1    7500 11600
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S15
U 1 1 607F0077
P 9000 13050
F 0 "S15" H 9500 12900 50  0000 L CNN
F 1 "228CMVARGBFR" H 9300 12800 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 10050 13550 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 10050 13450 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 10050 13350 50  0001 L CNN "Description"
F 5 "7.3" H 10050 13250 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 10050 13150 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 10050 13050 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 10050 12950 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 10050 12850 50  0001 L CNN "Manufacturer_Part_Number"
	1    9000 13050
	1    0    0    -1  
$EndComp
Wire Wire Line
	10350 12350 9600 12350
Wire Wire Line
	10650 11650 10650 13900
Wire Wire Line
	10650 13900 9900 13900
Wire Wire Line
	9900 13900 9500 13750
Wire Wire Line
	10750 11550 10750 13750
Wire Wire Line
	9600 13750 10750 13750
Text GLabel 10200 13150 2    50   Output ~ 0
btn15
Wire Wire Line
	10350 11750 10350 12350
Wire Wire Line
	10350 11650 10650 11650
Wire Wire Line
	10350 11550 10750 11550
$Comp
L btn-matrix-rescue:WS2811-Driver_LED U15
U 1 1 607F0090
P 9950 11650
F 0 "U15" H 9950 12131 50  0000 C CNN
F 1 "WS2811" H 9950 12040 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 9650 11800 50  0001 C CNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2811.pdf" H 9750 11900 50  0001 C CNN
	1    9950 11650
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR0177
U 1 1 607F0096
P 9950 11950
F 0 "#PWR0177" H 9950 11700 50  0001 C CNN
F 1 "GND" V 9955 11822 50  0000 R CNN
F 2 "" H 9950 11950 50  0001 C CNN
F 3 "" H 9950 11950 50  0001 C CNN
	1    9950 11950
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0178
U 1 1 607F009C
P 9500 12350
F 0 "#PWR0178" H 9500 12200 50  0001 C CNN
F 1 "+5V" H 9515 12523 50  0000 C CNN
F 2 "" H 9500 12350 50  0001 C CNN
F 3 "" H 9500 12350 50  0001 C CNN
	1    9500 12350
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:C-Device C15
U 1 1 607F00A2
P 10200 11350
F 0 "C15" V 10452 11350 50  0000 C CNN
F 1 "104" V 10361 11350 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 10238 11200 50  0001 C CNN
F 3 "~" H 10200 11350 50  0001 C CNN
	1    10200 11350
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R15.3
U 1 1 607F00A8
P 9700 11350
F 0 "R15.3" V 9600 11350 50  0000 C CNN
F 1 "100" V 9700 11350 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9630 11350 50  0001 C CNN
F 3 "~" H 9700 11350 50  0001 C CNN
	1    9700 11350
	0    1    1    0   
$EndComp
Wire Wire Line
	9950 11350 10050 11350
Wire Wire Line
	9850 11350 9950 11350
Connection ~ 9950 11350
$Comp
L btn-matrix-rescue:GND-power #PWR0179
U 1 1 607F00B1
P 10350 11350
F 0 "#PWR0179" H 10350 11100 50  0001 C CNN
F 1 "GND" V 10355 11222 50  0000 R CNN
F 2 "" H 10350 11350 50  0001 C CNN
F 3 "" H 10350 11350 50  0001 C CNN
	1    10350 11350
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0180
U 1 1 607F00B7
P 9550 11350
F 0 "#PWR0180" H 9550 11200 50  0001 C CNN
F 1 "+5V" V 9565 11478 50  0000 L CNN
F 2 "" H 9550 11350 50  0001 C CNN
F 3 "" H 9550 11350 50  0001 C CNN
	1    9550 11350
	0    -1   -1   0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R15.1
U 1 1 607F00BD
P 9400 11550
F 0 "R15.1" V 9300 11550 50  0000 C CNN
F 1 "33" V 9400 11550 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9330 11550 50  0001 C CNN
F 3 "~" H 9400 11550 50  0001 C CNN
	1    9400 11550
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:R-Device R15.2
U 1 1 607F00C3
P 9400 11650
F 0 "R15.2" V 9500 11650 50  0000 C CNN
F 1 "33" V 9400 11650 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric" V 9330 11650 50  0001 C CNN
F 3 "~" H 9400 11650 50  0001 C CNN
	1    9400 11650
	0    1    1    0   
$EndComp
Wire Wire Line
	3850 2300 3650 2300
Wire Wire Line
	3650 2300 3650 4600
Wire Wire Line
	3650 4600 5450 4600
Wire Wire Line
	5450 4600 5450 2200
Wire Wire Line
	5450 2200 5650 2200
Wire Wire Line
	5650 2300 5500 2300
Wire Wire Line
	5500 2300 5500 4600
Wire Wire Line
	5500 4600 7250 4600
Wire Wire Line
	7250 4600 7250 2200
Wire Wire Line
	7250 2200 7500 2200
Wire Wire Line
	7500 2300 7350 2300
Wire Wire Line
	7350 2300 7350 4600
Wire Wire Line
	7350 4600 9100 4600
Wire Wire Line
	9100 4600 9100 2250
Wire Wire Line
	9100 2250 9400 2250
Wire Wire Line
	9400 2350 9200 2350
Wire Wire Line
	9200 2350 9200 4650
Wire Wire Line
	9200 4650 3650 4650
Wire Wire Line
	3650 4650 3650 5200
Wire Wire Line
	3650 5200 3800 5200
Wire Wire Line
	3800 5300 3650 5300
Wire Wire Line
	3650 5300 3650 7750
Wire Wire Line
	3650 7750 5400 7750
Wire Wire Line
	5400 7750 5400 5200
Wire Wire Line
	5400 5200 5600 5200
Wire Wire Line
	5600 5300 5450 5300
Wire Wire Line
	5450 5300 5450 7750
Wire Wire Line
	5450 7750 7250 7750
Wire Wire Line
	7250 7750 7250 5200
Wire Wire Line
	7250 5200 7450 5200
Wire Wire Line
	7450 5300 7300 5300
Wire Wire Line
	7300 5300 7300 7750
Wire Wire Line
	7300 7750 9100 7750
Wire Wire Line
	9100 7750 9100 5250
Wire Wire Line
	9100 5250 9350 5250
Wire Wire Line
	9350 5350 9200 5350
Wire Wire Line
	9200 5350 9200 7850
Wire Wire Line
	9200 7850 3550 7850
Wire Wire Line
	3550 7850 3550 8450
Wire Wire Line
	3550 8450 3750 8450
Wire Wire Line
	3750 8550 3600 8550
Wire Wire Line
	3600 8550 3600 10850
Wire Wire Line
	3600 10850 5300 10850
Wire Wire Line
	5300 10850 5300 8450
Wire Wire Line
	5300 8450 5550 8450
Wire Wire Line
	5550 8550 5350 8550
Wire Wire Line
	5350 8550 5350 10850
Wire Wire Line
	5350 10850 7100 10850
Wire Wire Line
	7100 10850 7100 8450
Wire Wire Line
	7100 8450 7400 8450
Wire Wire Line
	7400 8550 7150 8550
Wire Wire Line
	7150 8550 7150 10850
Wire Wire Line
	7150 10850 9000 10850
Wire Wire Line
	9000 10850 9000 8500
Wire Wire Line
	9000 8500 9300 8500
Wire Wire Line
	9300 8600 9100 8600
Wire Wire Line
	9100 8600 9100 10950
Wire Wire Line
	9100 10950 3650 10950
Wire Wire Line
	3650 10950 3650 11500
Wire Wire Line
	3650 11500 3700 11500
Wire Wire Line
	3700 11600 3500 11600
Wire Wire Line
	3500 11600 3500 14150
Wire Wire Line
	3500 14150 5250 14150
Wire Wire Line
	5250 14150 5250 11500
Wire Wire Line
	5250 11500 5500 11500
Wire Wire Line
	5500 11600 5500 11650
Wire Wire Line
	5500 11650 5350 11650
Wire Wire Line
	5350 11650 5350 14150
Wire Wire Line
	5350 14150 7050 14150
Wire Wire Line
	7050 14150 7050 11500
Wire Wire Line
	7050 11500 7350 11500
Wire Wire Line
	7350 11600 7150 11600
Wire Wire Line
	7150 11600 7150 14150
Wire Wire Line
	7150 14150 8950 14150
Wire Wire Line
	8950 14150 8950 11550
Wire Wire Line
	8950 11550 9250 11550
Text GLabel 3850 2200 0    50   Input ~ 0
LED_DAT_IN
$Comp
L btn-matrix-rescue:GND-power #PWR0181
U 1 1 60B9BFC6
P 1600 6700
F 0 "#PWR0181" H 1600 6450 50  0001 C CNN
F 1 "GND" V 1605 6572 50  0000 R CNN
F 2 "" H 1600 6700 50  0001 C CNN
F 3 "" H 1600 6700 50  0001 C CNN
	1    1600 6700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+5V-power #PWR0182
U 1 1 60B9CB67
P 2100 6700
F 0 "#PWR0182" H 2100 6550 50  0001 C CNN
F 1 "+5V" V 2115 6828 50  0000 L CNN
F 2 "" H 2100 6700 50  0001 C CNN
F 3 "" H 2100 6700 50  0001 C CNN
	1    2100 6700
	0    1    1    0   
$EndComp
Text GLabel 1600 6900 0    50   Input ~ 0
btn00
Text GLabel 2100 6900 2    50   Input ~ 0
btn01
Text GLabel 1600 7000 0    50   Input ~ 0
btn02
Text GLabel 2100 7000 2    50   Input ~ 0
btn03
Text GLabel 1600 7100 0    50   Input ~ 0
btn04
Text GLabel 2100 7100 2    50   Input ~ 0
btn05
Text GLabel 1600 7200 0    50   Input ~ 0
btn06
Text GLabel 2100 7200 2    50   Input ~ 0
btn07
Text GLabel 1600 7300 0    50   Input ~ 0
btn08
Text GLabel 2100 7300 2    50   Input ~ 0
btn09
Text GLabel 1600 7400 0    50   Input ~ 0
btn10
Text GLabel 2100 7400 2    50   Input ~ 0
btn11
Text GLabel 1600 7500 0    50   Input ~ 0
btn12
Text GLabel 2100 7500 2    50   Input ~ 0
btn13
Text GLabel 1600 7600 0    50   Input ~ 0
btn14
Text GLabel 2100 7600 2    50   Input ~ 0
btn15
Text GLabel 1600 7800 0    50   Output ~ 0
LED_DAT_IN
Text GLabel 9100 11650 3    50   Output ~ 0
LED_DAT_OUT
Wire Wire Line
	9100 11650 9250 11650
Text GLabel 2100 7800 2    50   Input ~ 0
LED_DAT_OUT
$Comp
L btn-matrix-rescue:+5V-power #PWR01
U 1 1 60BF098C
P 4050 800
F 0 "#PWR01" H 4050 650 50  0001 C CNN
F 1 "+5V" H 4065 973 50  0000 C CNN
F 2 "" H 4050 800 50  0001 C CNN
F 3 "" H 4050 800 50  0001 C CNN
	1    4050 800 
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:GND-power #PWR02
U 1 1 60BF11FD
P 4450 800
F 0 "#PWR02" H 4450 550 50  0001 C CNN
F 1 "GND" H 4455 627 50  0000 C CNN
F 2 "" H 4450 800 50  0001 C CNN
F 3 "" H 4450 800 50  0001 C CNN
	1    4450 800 
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:PWR_FLAG-power #FLG02
U 1 1 60BF1DBF
P 4450 800
F 0 "#FLG02" H 4450 875 50  0001 C CNN
F 1 "PWR_FLAG" H 4450 973 50  0000 C CNN
F 2 "" H 4450 800 50  0001 C CNN
F 3 "~" H 4450 800 50  0001 C CNN
	1    4450 800 
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:PWR_FLAG-power #FLG01
U 1 1 60BF26D7
P 4050 800
F 0 "#FLG01" H 4050 875 50  0001 C CNN
F 1 "PWR_FLAG" H 4050 973 50  0000 C CNN
F 2 "" H 4050 800 50  0001 C CNN
F 3 "~" H 4050 800 50  0001 C CNN
	1    4050 800 
	-1   0    0    1   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR03
U 1 1 60787FEC
P 2100 6800
F 0 "#PWR03" H 2100 6650 50  0001 C CNN
F 1 "+3.3V" V 2115 6928 50  0000 L CNN
F 2 "" H 2100 6800 50  0001 C CNN
F 3 "" H 2100 6800 50  0001 C CNN
	1    2100 6800
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR07
U 1 1 60846E2B
P 4950 3700
F 0 "#PWR07" H 4950 3550 50  0001 C CNN
F 1 "+3.3V" V 4965 3828 50  0000 L CNN
F 2 "" H 4950 3700 50  0001 C CNN
F 3 "" H 4950 3700 50  0001 C CNN
	1    4950 3700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR011
U 1 1 6084B009
P 6800 3700
F 0 "#PWR011" H 6800 3550 50  0001 C CNN
F 1 "+3.3V" V 6815 3828 50  0000 L CNN
F 2 "" H 6800 3700 50  0001 C CNN
F 3 "" H 6800 3700 50  0001 C CNN
	1    6800 3700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR015
U 1 1 60875D48
P 8650 3700
F 0 "#PWR015" H 8650 3550 50  0001 C CNN
F 1 "+3.3V" V 8665 3828 50  0000 L CNN
F 2 "" H 8650 3700 50  0001 C CNN
F 3 "" H 8650 3700 50  0001 C CNN
	1    8650 3700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR019
U 1 1 60877331
P 10500 3750
F 0 "#PWR019" H 10500 3600 50  0001 C CNN
F 1 "+3.3V" V 10515 3878 50  0000 L CNN
F 2 "" H 10500 3750 50  0001 C CNN
F 3 "" H 10500 3750 50  0001 C CNN
	1    10500 3750
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR018
U 1 1 60885E0C
P 10450 6750
F 0 "#PWR018" H 10450 6600 50  0001 C CNN
F 1 "+3.3V" V 10465 6878 50  0000 L CNN
F 2 "" H 10450 6750 50  0001 C CNN
F 3 "" H 10450 6750 50  0001 C CNN
	1    10450 6750
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR014
U 1 1 6089CD35
P 8550 6700
F 0 "#PWR014" H 8550 6550 50  0001 C CNN
F 1 "+3.3V" V 8565 6828 50  0000 L CNN
F 2 "" H 8550 6700 50  0001 C CNN
F 3 "" H 8550 6700 50  0001 C CNN
	1    8550 6700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR010
U 1 1 608B0919
P 6750 6700
F 0 "#PWR010" H 6750 6550 50  0001 C CNN
F 1 "+3.3V" V 6765 6828 50  0000 L CNN
F 2 "" H 6750 6700 50  0001 C CNN
F 3 "" H 6750 6700 50  0001 C CNN
	1    6750 6700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR06
U 1 1 608C6AA3
P 4950 6700
F 0 "#PWR06" H 4950 6550 50  0001 C CNN
F 1 "+3.3V" V 4965 6828 50  0000 L CNN
F 2 "" H 4950 6700 50  0001 C CNN
F 3 "" H 4950 6700 50  0001 C CNN
	1    4950 6700
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR05
U 1 1 608E0853
P 4850 9950
F 0 "#PWR05" H 4850 9800 50  0001 C CNN
F 1 "+3.3V" V 4865 10078 50  0000 L CNN
F 2 "" H 4850 9950 50  0001 C CNN
F 3 "" H 4850 9950 50  0001 C CNN
	1    4850 9950
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR09
U 1 1 608F58EF
P 6600 9950
F 0 "#PWR09" H 6600 9800 50  0001 C CNN
F 1 "+3.3V" V 6615 10078 50  0000 L CNN
F 2 "" H 6600 9950 50  0001 C CNN
F 3 "" H 6600 9950 50  0001 C CNN
	1    6600 9950
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR013
U 1 1 60909441
P 8400 9950
F 0 "#PWR013" H 8400 9800 50  0001 C CNN
F 1 "+3.3V" V 8415 10078 50  0000 L CNN
F 2 "" H 8400 9950 50  0001 C CNN
F 3 "" H 8400 9950 50  0001 C CNN
	1    8400 9950
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR017
U 1 1 6091CB9B
P 10350 10000
F 0 "#PWR017" H 10350 9850 50  0001 C CNN
F 1 "+3.3V" V 10365 10128 50  0000 L CNN
F 2 "" H 10350 10000 50  0001 C CNN
F 3 "" H 10350 10000 50  0001 C CNN
	1    10350 10000
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR04
U 1 1 6093269F
P 4750 13000
F 0 "#PWR04" H 4750 12850 50  0001 C CNN
F 1 "+3.3V" V 4765 13128 50  0000 L CNN
F 2 "" H 4750 13000 50  0001 C CNN
F 3 "" H 4750 13000 50  0001 C CNN
	1    4750 13000
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR08
U 1 1 6094647F
P 6600 13000
F 0 "#PWR08" H 6600 12850 50  0001 C CNN
F 1 "+3.3V" V 6615 13128 50  0000 L CNN
F 2 "" H 6600 13000 50  0001 C CNN
F 3 "" H 6600 13000 50  0001 C CNN
	1    6600 13000
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR012
U 1 1 60959C81
P 8400 13000
F 0 "#PWR012" H 8400 12850 50  0001 C CNN
F 1 "+3.3V" V 8415 13128 50  0000 L CNN
F 2 "" H 8400 13000 50  0001 C CNN
F 3 "" H 8400 13000 50  0001 C CNN
	1    8400 13000
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:+3.3V-power #PWR016
U 1 1 6096FC43
P 10200 13050
F 0 "#PWR016" H 10200 12900 50  0001 C CNN
F 1 "+3.3V" V 10215 13178 50  0000 L CNN
F 2 "" H 10200 13050 50  0001 C CNN
F 3 "" H 10200 13050 50  0001 C CNN
	1    10200 13050
	0    1    1    0   
$EndComp
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S12
U 1 1 607EFF6F
P 3550 13000
F 0 "S12" H 4050 12850 50  0000 L CNN
F 1 "228CMVARGBFR" H 3850 12750 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 4600 13500 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 4600 13400 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 4600 13300 50  0001 L CNN "Description"
F 5 "7.3" H 4600 13200 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 4600 13100 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 4600 13000 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 4600 12900 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 4600 12800 50  0001 L CNN "Manufacturer_Part_Number"
	1    3550 13000
	1    0    0    -1  
$EndComp
NoConn ~ 9550 11750
$Comp
L btn-matrix-rescue:+3.3V-power #PWR0101
U 1 1 60C539E5
P 3600 800
F 0 "#PWR0101" H 3600 650 50  0001 C CNN
F 1 "+3.3V" H 3615 973 50  0000 C CNN
F 2 "" H 3600 800 50  0001 C CNN
F 3 "" H 3600 800 50  0001 C CNN
	1    3600 800 
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:PWR_FLAG-power #FLG0101
U 1 1 60C54976
P 3600 800
F 0 "#FLG0101" H 3600 875 50  0001 C CNN
F 1 "PWR_FLAG" H 3600 973 50  0000 C CNN
F 2 "" H 3600 800 50  0001 C CNN
F 3 "~" H 3600 800 50  0001 C CNN
	1    3600 800 
	-1   0    0    1   
$EndComp
$Comp
L btn-matrix-rescue:Conn_02x12_Odd_Even-Connector_Generic J2
U 1 1 60C716FD
P 1800 7200
F 0 "J2" H 1850 7917 50  0000 C CNN
F 1 "Conn_02x12_Odd_Even" H 1850 7826 50  0000 C CNN
F 2 "Connector_IDC:IDC-Header_2x12_P2.54mm_Vertical" H 1800 7200 50  0001 C CNN
F 3 "~" H 1800 7200 50  0001 C CNN
	1    1800 7200
	1    0    0    -1  
$EndComp
NoConn ~ 1600 6800
NoConn ~ 1600 7700
NoConn ~ 2100 7700
Wire Wire Line
	4350 4400 5350 4400
Wire Wire Line
	4250 4550 5250 4550
NoConn ~ 3750 3700
NoConn ~ 3750 3800
Wire Wire Line
	6750 3000 6750 2400
Wire Wire Line
	6200 3000 6750 3000
Wire Wire Line
	4350 3000 4950 3000
Wire Wire Line
	4950 3000 4950 2400
NoConn ~ 5600 3700
NoConn ~ 5600 3800
NoConn ~ 7450 3700
NoConn ~ 7450 3800
NoConn ~ 9300 3750
NoConn ~ 9300 3850
NoConn ~ 3750 6700
NoConn ~ 3750 6800
NoConn ~ 5550 6700
NoConn ~ 5550 6800
NoConn ~ 7350 6700
NoConn ~ 7350 6800
NoConn ~ 9250 6750
NoConn ~ 9250 6850
NoConn ~ 3650 9950
NoConn ~ 3650 10050
NoConn ~ 5400 9950
NoConn ~ 5400 10050
NoConn ~ 7200 9950
NoConn ~ 7200 10050
NoConn ~ 9150 10000
NoConn ~ 9150 10100
NoConn ~ 5400 13000
NoConn ~ 5400 13100
NoConn ~ 3550 13000
NoConn ~ 3550 13100
$Comp
L btn-matrix-rescue:228CMVARGBFR-SamacSys_Parts S14
U 1 1 607F001F
P 7200 13000
F 0 "S14" H 7700 12850 50  0000 L CNN
F 1 "228CMVARGBFR" H 7500 12750 50  0000 L CNN
F 2 "SamacSys_Parts:228CMVARGBFR" H 8250 13500 50  0001 L CNN
F 3 "https://www.mouser.co.za/datasheet/2/96/228C-1371171.pdf" H 8250 13400 50  0001 L CNN
F 4 "Tactile Switches Color Red,Green,Blue SMD Gullwing" H 8250 13300 50  0001 L CNN "Description"
F 5 "7.3" H 8250 13200 50  0001 L CNN "Height"
F 6 "774-228CMVARGBFR" H 8250 13100 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/CTS-Electronic-Components/228CMVARGBFR?qs=gTYE2QTfZfSFpUQ%252Bb6QA4w%3D%3D" H 8250 13000 50  0001 L CNN "Mouser Price/Stock"
F 8 "CTS" H 8250 12900 50  0001 L CNN "Manufacturer_Name"
F 9 "228CMVARGBFR" H 8250 12800 50  0001 L CNN "Manufacturer_Part_Number"
	1    7200 13000
	1    0    0    -1  
$EndComp
NoConn ~ 7200 13000
NoConn ~ 7200 13100
NoConn ~ 9000 13050
NoConn ~ 9000 13150
$Comp
L btn-matrix-rescue:MountingHole_Pad-Mechanical H1
U 1 1 609E24F5
P 1200 1250
F 0 "H1" H 1300 1299 50  0000 L CNN
F 1 "MountingHole_Pad" H 1300 1208 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_Pad_Via" H 1200 1250 50  0001 C CNN
F 3 "~" H 1200 1250 50  0001 C CNN
	1    1200 1250
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:MountingHole_Pad-Mechanical H2
U 1 1 609E3700
P 1200 1550
F 0 "H2" H 1300 1599 50  0000 L CNN
F 1 "MountingHole_Pad" H 1300 1508 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_Pad_Via" H 1200 1550 50  0001 C CNN
F 3 "~" H 1200 1550 50  0001 C CNN
	1    1200 1550
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:MountingHole_Pad-Mechanical H3
U 1 1 609E408C
P 1200 1850
F 0 "H3" H 1300 1899 50  0000 L CNN
F 1 "MountingHole_Pad" H 1300 1808 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_Pad_Via" H 1200 1850 50  0001 C CNN
F 3 "~" H 1200 1850 50  0001 C CNN
	1    1200 1850
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:MountingHole_Pad-Mechanical H4
U 1 1 609E4F0A
P 1200 2150
F 0 "H4" H 1300 2199 50  0000 L CNN
F 1 "MountingHole_Pad" H 1300 2108 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_Pad_Via" H 1200 2150 50  0001 C CNN
F 3 "~" H 1200 2150 50  0001 C CNN
	1    1200 2150
	1    0    0    -1  
$EndComp
$Comp
L btn-matrix-rescue:MountingHole_Pad-Mechanical H5
U 1 1 609E58C9
P 1200 2450
F 0 "H5" H 1300 2499 50  0000 L CNN
F 1 "MountingHole_Pad" H 1300 2408 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.7mm_Pad_Via" H 1200 2450 50  0001 C CNN
F 3 "~" H 1200 2450 50  0001 C CNN
	1    1200 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1200 1350 1050 1350
Wire Wire Line
	1050 1350 1050 1650
Wire Wire Line
	1050 1650 1200 1650
Wire Wire Line
	1050 1650 1050 1950
Wire Wire Line
	1050 1950 1200 1950
Connection ~ 1050 1650
Wire Wire Line
	1050 1950 1050 2250
Wire Wire Line
	1050 2250 1200 2250
Connection ~ 1050 1950
Wire Wire Line
	1050 2250 1050 2550
Wire Wire Line
	1050 2550 1200 2550
Connection ~ 1050 2250
$Comp
L btn-matrix-rescue:GND-power #PWR020
U 1 1 60A35E71
P 1200 2550
F 0 "#PWR020" H 1200 2300 50  0001 C CNN
F 1 "GND" H 1205 2377 50  0000 C CNN
F 2 "" H 1200 2550 50  0001 C CNN
F 3 "" H 1200 2550 50  0001 C CNN
	1    1200 2550
	1    0    0    -1  
$EndComp
Connection ~ 1200 2550
$Bitmap
Pos 7900 15000
Scale 2.000000
Data
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52 00 00 01 0B 00 00 00 32 08 06 00 00 00 4B 57 FE 
83 00 00 00 04 73 42 49 54 08 08 08 08 7C 08 64 88 00 00 00 09 70 48 59 73 00 00 2E 18 00 00 2E 
18 01 2A AA 27 20 00 00 15 D9 49 44 41 54 78 9C ED 9D 79 54 14 57 F6 C7 BF 8D B2 34 08 0A A8 2C 
46 C0 C8 12 22 DA 10 04 5C 30 A0 71 43 C0 28 51 44 51 D9 A2 C6 98 A3 46 93 30 31 63 12 33 32 51 
1C 1D FD 45 A3 22 02 2A 08 46 54 44 14 62 00 A3 63 04 94 65 D0 20 08 CA A2 80 6C 8D 6C 23 B2 34 
FD FB C3 43 87 E2 55 F5 42 37 0A 49 7D CE E9 73 A8 5B 6F B9 D5 54 DD 7A EF BE FB 6E 73 00 94 82 
85 85 85 45 3C 6D 1C 00 C2 D7 AD 05 0B 0B CB 80 A7 4D E9 75 6B C0 C2 C2 32 38 18 DA F3 C0 DF DF 
1F 13 27 4E 7C 5D BA B0 B0 B0 0C 20 72 72 72 70 F2 E4 49 D1 31 C5 58 B8 BB BB 63 D1 A2 45 AF 5C 
29 16 16 96 81 47 4C 4C 0C C5 58 B0 D3 10 16 16 16 A9 18 CA 74 E2 FA 8D EB C8 C9 CD 51 48 27 7C 
3E 1F B7 D3 6F E3 45 DB 0B DA F3 2A 2A 2A B0 B6 B6 86 A5 A5 25 2C 2C 2C A0 AE AE 2E 55 BB 9D 9D 
9D 28 2E 2E C6 83 07 0F 90 93 93 83 FA FA 7A DA 72 43 94 86 80 67 C3 83 B1 B1 71 9F F4 EF EC EC 
44 C5 E3 0A 08 85 AC 2F 98 E5 CF CD 8A 15 2B 60 6F 6F 4F 7B 8E D1 58 94 94 16 E3 0D E3 31 72 77 
7E 25 21 11 27 C3 4E 42 20 10 10 E7 B8 5C 2E D6 AF 5F 8F BF FD ED 6F 18 35 6A 54 9F DA B7 B3 B5 
03 00 74 74 74 20 2C 2C 0C 41 41 41 78 F2 E4 09 51 EE 5A EA 35 CC 9E 37 1B 01 6B FD 31 74 28 E3 
65 33 92 92 92 82 A4 CB 49 7D D2 91 85 65 B0 60 6D 6D CD 68 2C FA 75 1A 12 7F 21 1E E1 C7 C2 69 
0D 85 9F 9F 1F 1E 3D 7A 84 BD 7B F7 F6 D9 50 F4 44 59 59 19 EB D6 AD C3 C3 87 0F 71 E0 C0 01 70 
B9 5C A2 4C F2 CF C9 38 B0 F7 FF FA 34 42 58 E9 E3 0D 03 43 03 B9 F5 64 61 19 AC F4 9B B1 48 FB 
2D 0D 91 27 A2 08 B9 AA AA 2A 42 43 43 11 16 16 06 03 03 C5 3F 7C 2A 2A 2A D8 B8 71 23 D2 D2 D2 
F0 E6 9B 6F 12 E7 D3 6F A5 E3 64 F8 29 99 DB 55 55 55 C5 27 9B 3F 81 92 12 EB E6 61 F9 6B D2 2F 
77 FE 83 82 07 F8 61 FF 41 E2 0D 6E 68 68 88 5F 7F FD 15 01 01 01 FD D1 2D 05 1E 8F 87 CC CC 4C 
2C 58 B0 80 38 97 70 31 01 89 09 89 32 B7 69 6E 61 86 85 8B DD 15 A1 1E 0B CB A0 43 E1 C6 A2 BA 
AA 1A BB 83 82 D1 D1 DE 41 91 1B 18 18 20 2D 2D 0D 53 A6 4C 51 74 97 8C 68 6B 6B E3 D2 A5 4B 58 
B2 64 09 71 2E 3C 34 02 D9 99 D9 32 B7 E9 B1 C4 03 1A C3 34 14 A1 1E 0B CB A0 42 E1 C6 22 2C 24 
0C CD 4D CD 14 99 A6 A6 26 AE 5C B9 02 23 23 23 45 77 27 11 25 25 25 9C 3A 75 0A D3 A6 4D A3 C8 
85 42 21 42 0E 1F 43 7B 7B BB 4C ED 71 D5 B9 70 75 27 47 2B 2C 2C 7F 76 14 6A 2C 72 73 72 91 9D 
45 5D 6E 1D 3A 74 28 62 63 63 61 6D 6D AD C8 AE 64 42 4D 4D 0D F1 F1 F1 30 37 37 A7 C8 F9 75 7C 
C4 5F 88 97 B9 BD 05 EE 0B A4 5E DE 65 61 F9 B3 A0 30 63 D1 D5 D5 85 13 61 27 09 F9 CE 9D 3B 31 
77 EE 5C 45 75 D3 67 74 75 75 71 E6 CC 19 C2 41 19 77 EE 22 EA F9 F4 F1 19 4C 68 68 68 60 81 BB 
8B 22 D5 63 61 19 F0 C8 1E 70 C0 40 F2 D5 14 3C 79 4C 8D 6F 30 33 33 C3 A7 9F 7E AA A8 2E E4 C6 
DA DA 1A 7E 7E 7E 38 7E FC B8 48 D6 D6 D6 86 D3 A7 A2 F1 C9 E6 0D 32 B5 B5 C0 6D 01 CE 9F BD 80 
AE AE 2E 89 65 C5 F9 69 84 42 21 1A 1A 1A 50 57 57 87 67 CF 9E D1 B6 67 6F 6F 4F 18 B9 EA EA 6A 
94 94 94 88 ED D7 C0 C0 80 36 10 2D 37 37 17 AD AD AD 62 EB AA A9 A9 D1 8E 06 EB EA EA F0 F0 E1 
43 A9 EB D4 D7 D7 A3 B0 B0 50 6C 5F DD 0C 19 32 04 26 26 26 30 37 37 87 99 99 19 0C 0C 0C 50 53 
53 83 F2 F2 72 94 96 96 22 2B 2B 4B AA EF 5B 56 CC CC CC 60 69 69 09 23 23 23 8C 19 33 06 6D 6D 
6D E0 F3 F9 E0 F3 F9 28 2D 2D 45 6E 6E 2E FE F7 BF FF C9 D4 A6 89 89 09 F4 F5 F5 09 79 6D 6D 2D 
1E 3D 7A A4 28 D5 5F 29 0A 33 16 3F 5F 21 03 96 FE FD EF 7F 43 45 45 45 51 5D 28 84 9D 3B 77 E2 
CC 99 33 68 69 69 11 C9 6E FD 76 0B 6B 3E FA 10 AA 6A AA 52 B7 A3 A9 A5 09 8B B7 2C 90 7F 3F 5F 
62 D9 B4 B4 34 A9 DA EC EA EA 42 51 51 11 4E 9F 3E 8D 53 A7 4E 89 8C 81 97 97 17 61 74 F9 7C 3E 
AC AC AC 50 55 55 45 DB 96 9A 9A 1A 92 93 93 F1 F6 DB 6F 53 E4 A9 A9 A9 98 3D 7B B6 44 5D 4C 4C 
4C 68 F5 AE AF AF 87 99 99 19 6D B4 2C 5D 9D 8B 17 2F 4A DC 6F 64 64 64 84 DD BB 77 C3 C3 C3 43 
EC FD 52 51 51 81 98 98 18 84 84 84 48 6D 80 C4 61 6F 6F 8F ED DB B7 C3 CD CD 4D 6C B9 EE FF CB 
B1 63 C7 B0 77 EF 5E A9 DA 8E 8B 8B 03 8F C7 23 E4 25 25 25 18 3F 7E FC A0 8C 06 56 C8 34 E4 69 
E5 53 3C 2E A3 8E 2A 66 CF 9E 0D 57 57 57 89 75 85 42 21 8A 8B 8B 11 17 17 87 A8 A8 28 5C BB 76 
0D B5 B5 B5 52 F5 DB D1 D1 81 7B F7 EE 21 3A 3A 1A 67 CF 9E C5 6F BF FD 86 E7 CF 9F 8B AD A3 AF 
AF 8F 4D 9B 36 51 DB 69 EF 40 EE 7F 73 A5 EA B3 27 B6 76 EF C8 5C 47 1C 4A 4A 4A B0 B0 B0 C0 8E 
1D 3B 90 97 97 87 19 33 66 00 00 BE FC F2 4B FC FE FB EF 94 B2 BA BA BA 38 76 EC 18 63 5B 41 41 
41 84 A1 78 F6 EC 19 7C 7C 7C E4 BA 51 75 74 74 F0 F5 D7 5F F7 B9 7E 4F 34 34 34 F0 DD 77 DF A1 
A0 A0 00 5E 5E 5E 12 5F 2C 63 C6 8C C1 D6 AD 5B E1 EF EF 2F 77 DF F3 E6 CD 43 5A 5A 9A 44 43 01 
FC F1 7F B1 B3 B3 93 AA 6D 3B 3B 3B 5A 43 01 00 E3 C6 8D 93 CA 58 0F 44 14 62 2C D2 6F A5 13 32 
5F 5F 5F B1 75 5A 5B 5B B1 6D DB 36 0C 1F 3E 1C E3 C7 8F C7 E2 C5 8B B1 72 E5 4A CC 9A 35 0B 86 
86 86 70 73 73 43 66 66 26 6D DD CA CA 4A 2C 5D BA 14 1A 1A 1A 98 34 69 12 56 AC 58 01 4F 4F 4F 
38 3A 3A 42 4F 4F 0F 7E 7E 7E A8 A8 A8 60 EC DB CB CB 8B 90 DD C9 B8 23 FE 22 69 98 6C 3F 59 E6 
3A D2 C2 E5 72 71 E9 D2 25 8C 1A 35 0A 6D 6D 6D F0 F6 F6 46 5B 5B 1B A5 8C 9B 9B 1B FC FC FC 88 
BA 4E 4E 4E D8 BC 79 33 21 5F BF 7E 3D CA CB CB E5 D6 ED E3 8F 3F 26 9C C5 B2 A2 AC AC 8C 6B D7 
AE 61 FB F6 ED B4 D1 B6 C0 CB 97 41 7F 60 62 62 82 98 98 18 C6 00 BB DE DF B3 AC AC 5D BB 56 AE 
F3 03 15 05 19 8B 0C CA B1 8A 8A 0A DC DD 99 83 97 6E DF BE 0D 2B 2B 2B 7C FF FD F7 68 6E 6E 26 
CE 77 76 76 E2 F2 E5 CB 98 36 6D 1A 8E 1C 39 42 39 17 15 15 05 4B 4B 4B C4 C6 C6 D2 DE 4C 2D 2D 
2D 88 88 88 00 8F C7 43 72 72 32 6D FF 56 56 56 30 35 35 A5 C8 B2 EE 64 CB 3C 1F 1E F3 C6 18 E8 
E9 EB C9 54 A7 1B 1E 8F 07 6D 6D 6D 68 6B 6B C3 CE CE 0E 3B 77 EE 24 CA 0C 1F 3E 5C B4 E4 7B F7 
EE 5D 7C F5 D5 57 44 99 FD FB F7 53 96 A4 35 35 35 11 11 11 41 3C 08 91 91 91 38 73 E6 4C 9F 74 
ED 8D B2 B2 32 FE F5 AF 7F C9 D5 C6 8E 1D 3B 68 DF D4 8F 1E 3D C2 F2 E5 CB 61 61 61 01 2E 97 0B 
0D 0D 0D 4C 9C 38 11 4B 96 2C 41 52 92 62 F6 E6 B8 B9 B9 61 C4 88 11 14 59 6C 6C 2C 5C 5C 5C 30 
76 EC 58 A8 A9 A9 41 4B 4B 0B 56 56 56 58 BC 78 31 C2 C2 C2 C0 E7 F3 A5 6A 7B D8 B0 61 B4 2F A3 
9E BC FF FE FB 18 3D 7A 74 9F F5 7F 5D C8 6D 2C 5A 5A 5A 50 FC A8 98 22 9B 33 67 0E B4 B4 B4 18 
CB 2F 5B B6 0C C5 C5 D4 3A EA EA EA 78 EB AD B7 28 37 79 47 47 07 36 6C D8 80 2B 57 AE 00 00 F2 
F2 F2 E0 EF EF 8F A6 A6 26 4A 5D 1D 1D 1D 8C 1B 37 8E 22 E3 F3 F9 58 B2 64 09 A3 33 69 F1 E2 C5 
94 E3 E6 E6 66 94 3F 91 FD AD 6B 66 6E 26 73 1D 00 68 6A 6A 42 43 43 03 1A 1A 1A 90 99 99 89 ED 
DB B7 E3 F6 ED DB 44 B9 9E 0E C3 7D FB F6 21 35 35 95 72 5E 4B 4B 0B E1 E1 E1 E0 70 38 00 5E FA 
89 4C 4C 4C 28 65 CA CA CA F0 C9 27 9F F4 49 4F 26 DC DD DD F1 DE 7B EF F5 A9 AE B3 B3 33 02 03 
03 09 79 64 64 24 78 3C 1E 62 62 62 50 58 58 08 81 40 80 E7 CF 9F E3 F7 DF 7F C7 B9 73 E7 E0 E2 
E2 02 5B 5B 5B DC BC 79 53 2E DD 6D 6C 6C 28 C7 ED ED ED 58 B5 6A 15 92 92 92 44 23 AF E6 E6 66 
E4 E5 E5 21 2E 2E 0E 01 01 01 D0 D3 D3 C3 B6 6D DB 24 B6 BD 7C F9 72 0C 1B 36 8C 22 4B 49 49 A1 
1C 2B 2B 2B C3 C7 C7 47 AE 6B 78 1D C8 6D 2C E8 96 1D 67 CD 9A C5 58 3E 30 30 10 A5 A5 A5 7F 28 
A0 A4 84 5D BB 76 A1 A9 A9 09 F9 F9 F9 78 FA F4 29 96 2F 5F 2E 3A 3F 73 E6 4C 68 69 69 41 20 10 
C0 CF CF 8F 12 44 35 72 E4 48 24 26 26 82 CF E7 A3 B8 B8 18 F7 EF DF 87 99 D9 CB 87 57 59 59 99 
30 08 3D 99 3E 7D 3A 79 2D F5 CF C4 5E 2B 1D 3A BA 3A 32 D7 61 82 2E 40 2C 2F 2F 4F F4 B7 50 28 
84 8F 8F 0F 1A 1A 1A 28 65 66 CD 9A 85 0D 1B 36 C0 D5 D5 95 08 A5 EF EA EA C2 EA D5 AB D1 D8 D8 
28 B7 7E 2F 5E 50 53 0C EC DB B7 AF 4F 7B 65 BE FD F6 5B A2 5E 69 69 29 D6 AD 5B 27 71 D5 21 3B 
3B 1B 09 09 09 32 F7 D9 93 91 23 47 52 8E BB 53 24 88 43 20 10 10 2F 38 3A D6 AC 59 43 39 EE EC 
EC 84 8F 8F 0F 31 32 F9 F0 C3 0F A5 D4 76 E0 20 B7 B1 78 46 F3 80 19 1A 1A D2 96 6D 6D 6D C5 D1 
A3 47 29 B2 45 8B 16 21 30 30 10 43 86 0C 01 00 8C 1E 3D 1A 61 61 61 D8 B8 71 23 32 32 32 90 9C 
9C 0C 47 47 47 A4 A5 A5 E1 CE 1D AA 5F 21 38 38 18 F3 E7 CF 17 1D 5B 5A 5A E2 E2 C5 8B D8 B2 65 
0B 8A 8B 8B 11 1E 1E 8E F1 E3 C7 D3 EA 42 B7 AC D5 F0 AC 81 A6 A4 78 74 15 60 2C 4C 4D 4D B1 75 
EB 56 38 3A 3A 52 E4 1D 1D 1D B8 7A F5 2A 45 56 5E 5E 8E F5 EB D7 13 6D EC DE BD 9B B2 24 DC CD 
9E 3D 7B 70 E3 C6 0D B9 75 04 80 1B 37 6E 50 FC 48 93 26 4D EA D3 3E 9F 49 93 26 11 B2 AF BE FA 
4A A2 73 5A 51 DC BF 7F 9F 90 5D BE 7C 19 21 21 21 98 37 6F 1E 31 45 91 16 1E 8F 47 4C AD 12 13 
13 45 AB 38 3D 31 37 37 87 93 93 53 9F FA 79 5D C8 6F 2C 68 1E 30 A6 DD A4 79 79 79 C4 76 F5 95 
2B 57 12 E5 D4 D4 D4 70 E0 C0 01 CA BE FA DE AB 01 4A 4A 4A B4 75 2D 2D 2D B1 77 EF 5E BC F1 C6 
1B 62 F5 A6 37 16 AF 6E 64 51 52 52 02 A1 50 08 A1 50 88 A2 A2 22 C2 07 D0 3D 8D EA 3D E5 02 5E 
A6 3B 8B 8A A2 EE E8 55 57 57 87 9E 1E D5 7F 92 93 93 83 ED DB B7 F7 49 3F 3A 84 42 21 B1 84 FB 
8F 7F FC 03 9A 9A 9A 52 B7 31 76 EC 58 68 6B 6B 13 72 BA 29 58 7F 11 17 17 47 F8 A7 74 74 74 B0 
66 CD 1A 24 25 25 E1 D9 B3 67 28 2D 2D C5 89 13 27 E0 ED ED 2D B5 7F 81 CE 71 79 E2 C4 09 00 C0 
A9 53 E4 4E E7 C1 E6 E8 94 DB 58 D0 3D 60 74 0F 22 F0 D2 49 D7 9B DE F3 6B 26 7A 1B 8B D1 A3 47 
43 59 59 59 AA BA 74 D0 E9 48 67 F8 24 A1 A3 A3 B8 69 48 37 42 A1 10 81 81 81 B8 74 E9 12 63 99 
0D 1B 36 E0 F1 E3 C7 8C E7 5B 5B 5B E1 ED ED AD F0 15 85 9B 37 6F 22 36 36 56 74 AC A7 A7 87 2F 
BF FC 52 EA FA 74 A3 8A 8E 8E 0E CA D4 B4 BF C9 C8 C8 90 E8 A0 35 36 36 C6 EA D5 AB 11 19 19 89 
F2 F2 72 EC D9 B3 87 F0 45 F4 84 CB E5 C2 DB DB 9B 22 AB AF AF 17 FD 0F 33 32 32 88 D8 10 0F 0F 
8F 7E B9 7F FA 0B B9 8D 45 67 67 27 21 63 5A 2F EF 19 08 D5 8D B4 0F 7C EF 21 AA 3C 86 02 78 B9 
67 A5 F7 BC 99 EE 5A 24 A1 AC 22 9F 1E 74 70 38 1C 84 86 86 22 35 35 95 F1 AD DD D8 D8 88 D5 AB 
57 33 AE E0 7C F1 C5 17 C8 CF FF 23 60 6C ED DA B5 F8 F5 D7 5F 19 3F 3D 13 B3 4A E2 8B 2F BE A0 
2C 2F 7E FA E9 A7 52 A7 2C D4 D0 20 77 EC 76 74 74 F4 E9 BB EF 66 CB 96 2D 62 AF ED C7 1F 7F 24 
EA 04 06 06 C2 D3 D3 13 95 95 95 12 DB 57 56 56 C6 67 9F 7D 86 9B 37 6F 32 DE DB 9E 9E 9E 18 3E 
7C 38 45 76 E6 CC 19 8A 1F AA F7 77 AC A6 A6 86 55 AB 56 49 73 89 03 02 B9 8D C5 08 9A 21 E5 D3 
A7 4F 69 CB F6 0E 12 02 20 F6 ED 28 AE 6E 55 55 95 5C C1 45 35 35 35 C4 83 D6 FB 9F 2D 0D B2 EE 
2B E9 C6 D7 D7 17 2E 2E 2E 70 71 71 41 40 40 00 4E 9F 3E 4D 38 C1 9C 9D 9D C5 06 5E 5D BF 7E 1D 
21 21 21 84 3C 2D 2D 0D 07 0F 1E A4 C8 DE 7C F3 4D 38 39 39 31 7E 98 52 A9 D1 51 52 52 82 FD FB 
F7 8B 8E D5 D4 D4 B0 7B F7 6E A9 EA D2 8D 2E D5 D5 D5 19 FD 5C D2 D0 3D FF 67 FA BC F3 0E 7D F0 
DC D9 B3 67 61 64 64 84 19 33 66 20 38 38 18 77 EE DC 11 1B 63 C1 E3 F1 18 57 44 7A 3B 36 81 3F 
A6 20 DD 44 46 46 12 F7 2C 5D BD 81 8A DC C6 42 5B 9B 74 06 31 85 20 5B 59 59 11 32 A6 A1 F6 D1 
A3 47 11 1F FF C7 8E D0 DE 75 3B 3A 3A 90 98 48 26 B0 11 08 04 D8 B6 6D 1B ED 4D 29 49 C7 11 23 
64 37 16 74 0E 5E 69 B8 7E FD 3A 92 92 92 90 94 94 84 B0 B0 30 78 7B 7B 63 C5 8A 15 44 39 4F 4F 
4F B1 53 B5 B2 B2 32 42 26 AD 01 96 87 7F FE F3 9F A8 A9 A9 11 1D 2F 5B B6 8C 48 03 40 47 51 51 
11 B1 AA 02 D0 BF 48 5E 05 02 81 00 37 6F DE 44 60 60 20 EC ED ED A1 A9 A9 89 39 73 E6 20 3C 3C 
9C D6 5F 44 17 7D F9 F6 DB 6F 13 AB 6B 2D 2D 2D B0 B1 B1 C1 47 1F 7D 24 FA B8 B8 B8 10 2F D2 09 
13 26 60 EA D4 A9 8A BD A8 7E 42 7E 63 A1 23 FD C8 42 5F 5F 9F 78 83 45 44 44 10 0F FD A5 4B 97 
F0 F1 C7 1F E3 FD F7 DF C7 E4 C9 93 F1 F3 CF 3F 63 CA 94 29 84 A3 69 EB D6 AD 94 38 8A AE AE 2E 
6C DB B6 0D DF 7F FF 3D AC AD AD E1 E1 E1 41 59 7A EC 09 AD B1 A0 31 7C 92 E0 F7 71 64 41 C7 2F 
BF FC 42 CC DD 39 1C 0E 26 4C 98 20 77 DB CD CD CD A8 AE AE 66 FC 48 1B 62 DF 4D 53 53 13 E1 3C 
A5 0B 2C EB 8D 40 20 A0 FD 9F C8 E3 88 6D 6C 6C 14 7B 6D D2 06 54 01 2F 5F 42 C9 C9 C9 F0 F7 F7 
C7 BA 75 EB 88 F3 16 16 16 84 8C 6E 74 30 6C D8 30 1C 3E 7C 98 F8 D0 8D A0 06 8B A3 B3 5F 8C 85 
38 CF 76 58 58 18 65 DE F7 E2 C5 0B B8 BA BA C2 CE CE 0E 1F 7C F0 01 8C 8D 8D B1 70 E1 42 D1 14 
21 2B 2B 0B 7C 3E 1F 23 46 8C 20 86 D6 05 05 05 98 34 69 12 9C 9C 9C E0 EE EE 0E 5D 5D 5D 04 07 
07 03 78 E9 24 4C 4A 4A A2 4D 16 0C 00 F7 EE DD 23 64 C3 FB 30 B2 60 FA F9 81 BE A0 AF AF 8F 31 
63 C8 8C EA 8A D8 69 19 14 14 04 7D 7D 7D C6 4F F7 3E 14 59 38 7E FC 38 65 04 27 6D 4E D5 F0 F0 
70 42 F6 EE BB EF 4A 15 38 C6 E5 72 89 51 48 60 60 A0 D8 6B EB BD 47 69 CE 9C 39 52 FD F2 1E DD 
3D D2 FB 45 A8 AA AA 2A B7 DF C1 D3 D3 93 31 88 71 20 A1 80 69 88 36 46 EB 51 DF F8 F1 F1 F1 8C 
19 A8 26 4C 98 80 E0 E0 60 51 5C 05 F0 F2 C1 CE CC CC C4 F9 F3 E7 89 21 F4 37 DF 7C 23 1A 9E 2F 
5D BA 94 58 D7 7F FE FC 39 6E DC B8 81 84 84 04 4A B0 92 AA AA 2A 22 22 22 68 BD EF C0 CB DD 90 
3D 51 56 56 86 91 B1 EC 99 BC CA 1F 93 3F 3B 20 2B 4A 4A 4A B0 B1 B1 C1 9E 3D 7B 68 1D B7 AF 72 
59 51 16 04 02 01 B6 6C D9 22 73 BD 43 87 0E D1 4E 21 7F F8 E1 07 44 47 47 D3 1A 1D 5D 5D 5D 04 
06 06 A2 A4 A4 04 AB 57 AF EE 93 BE DD B8 BA BA E2 EE DD BB 48 4F 4F 47 40 40 00 0C 0D 0D 45 11 
B0 DD E8 E9 E9 61 DF BE 7D 44 DD DC 5C EA 86 43 0F 0F 0F E8 EA EA CA A5 8F BA BA 3A B1 92 32 10 
51 C8 DE 90 29 D3 1C 28 C7 0D 0D 0D 44 88 6B 4F 36 6D DA 84 8C 8C 0C D8 DA DA 32 96 31 32 32 42 
6C 6C 2C BE FD F6 5B 8A 3C 34 34 14 17 2F 5E C4 D8 B1 63 19 EB DA DA DA E2 D6 AD 5B F0 F4 F4 A4 
3D 5F 53 53 83 F4 74 EA E6 B7 09 13 27 30 6E 68 62 A2 B1 B1 11 45 85 F4 B9 1D 24 91 92 92 82 82 
82 02 14 14 14 A0 AE AE 0E D9 D9 D9 B4 37 CC 7F FE F3 1F 99 86 D1 AF 9A 94 94 14 B1 4B BC 4C F8 
F9 F9 D1 4E 7D BC BC BC 50 59 59 89 CA CA 4A A4 A4 A4 20 23 23 03 75 75 75 A8 AB AB C3 AE 5D BB 
88 58 12 79 70 70 70 40 68 68 28 2A 2A 2A D0 D2 D2 82 7B F7 EE E1 EA D5 AB 78 FC F8 31 AA AA AA 
68 93 36 75 6F 3D E8 86 6E 0A E2 EB EB 0B 2E 97 CB F8 71 71 21 13 27 0D 06 47 A7 42 F2 59 38 4C 
9D 82 F8 0B D4 1B 26 3A 3A 9A F6 4B E9 C6 D6 D6 16 19 19 19 C8 C9 C9 41 7E 7E 3E F2 F3 F3 D1 DC 
DC 0C 23 23 23 BC F3 CE 3B 98 39 73 26 63 28 F1 C2 85 0B 31 67 CE 1C 64 65 65 89 EA 72 38 1C 18 
19 19 C1 D9 D9 99 71 7B 70 37 74 41 39 76 0E D2 6D 3F EE 49 D6 9D EC 3E AF C8 D0 FD 4C 41 6F CA 
CA CA B0 74 E9 D2 3E B5 FF 2A F9 EC B3 CF 30 7F FE 7C 99 96 B3 AB AB AB 31 7F FE 7C 1C 3A 74 88 
36 39 90 81 81 41 BF FC 54 04 13 EA EA EA B0 B2 B2 A2 75 C2 77 73 E2 C4 09 44 47 47 8B 8E 4D 4D 
4D E1 EC EC 4C 29 D3 D2 D2 82 B3 67 CF D2 3A 71 BB B9 7A F5 2A CA CB CB 29 81 83 36 36 36 B0 B5 
B5 45 56 56 56 DF 2F A2 9F 51 88 B1 30 33 37 85 8E AE 0E 65 19 F1 F4 E9 D3 F8 FC F3 CF C5 CE 0D 
87 0C 19 82 C9 93 27 63 F2 64 D9 B7 7A 73 B9 5C 38 3A 3A 12 21 D2 92 68 6B 6B C3 AE 5D BB 28 32 
0E 87 83 C9 76 CC A3 1C 26 32 6F D3 6F A1 97 97 8A 8A 0A 1C 3F 7E 1C 47 8E 1C 41 75 75 75 BF F4 
A1 48 0A 0B 0B F1 E3 8F 3F 12 79 42 24 91 9D 9D 8D A9 53 A7 C2 CB CB 0B BB 76 ED 92 2A 56 23 3D 
3D 9D 71 37 B1 B4 A4 A6 A6 82 C7 E3 61 EA D4 A9 50 55 95 9C F0 A8 B1 B1 11 21 21 21 F8 E6 9B 6F 
28 F2 35 6B D6 10 D3 97 73 E7 CE 49 0C 5B EF EA EA 42 54 54 14 B1 99 6E ED DA B5 B4 4E D5 81 82 
42 8C 05 87 C3 81 F3 2C 27 9C 3F 7B 41 24 13 08 04 D8 BC 79 B3 D8 E9 C8 EB 60 FF FE FD 44 3A 3A 
CB 09 96 32 87 6D B7 B7 B7 E3 EE 7F C5 2F CF 76 23 29 B5 A0 40 20 40 6D 6D AD C8 7B FF E0 C1 03 
46 C7 6C 6F 92 93 93 89 B7 D8 83 07 0F A4 AA 2B 8E EA EA 6A 42 6F 71 51 96 3B 76 EC A0 3D 2F 4D 
0A B9 98 98 18 C4 C5 C5 C1 CE CE 0E E6 E6 E6 8C 69 F5 2E 5C B8 C0 98 D2 4F 16 E2 E3 E3 11 1F 1F 
2F 7A E1 38 38 38 C0 C0 C0 00 7A 7A 7A A2 69 4E 79 79 39 2A 2A 2A 50 54 54 84 E8 E8 68 DA 65 D4 
BB 77 EF 12 DF 91 B4 DB E8 0F 1D 3A 44 AC C8 D1 F5 31 90 E0 00 10 8D A3 2F 5C B8 20 4A 81 16 71 
32 1C C3 46 30 87 B7 F6 A6 B5 B5 15 1B D7 6F 22 36 63 9D 3B 77 0E 1E 1E 1E 8A D1 56 4E AA AB AB 
61 66 66 46 C9 A1 C1 E1 70 10 14 BC 53 E6 AD E6 29 BF A4 E0 C8 C1 A3 92 0B B2 B0 0C 22 C2 C3 C3 
45 89 AB 62 62 62 7A EE 00 6F 53 58 76 6F 2E 97 8B 15 AB 96 13 F2 75 EB D6 A1 A8 A8 48 51 DD F4 
99 F6 F6 76 78 7B 7B 13 C9 76 A6 CF 98 2E B3 A1 10 08 04 38 F7 D3 79 45 AA C7 C2 32 E0 51 E8 EF 
86 38 CF 72 C6 78 53 EA 96 F0 BA BA 3A CC 9F 3F 9F 12 ED F7 AA 11 0A 85 F0 F5 F5 25 A6 44 2A 2A 
2A 58 E9 23 FB 92 D5 B5 E4 6B A8 AD 91 2D 88 89 85 65 B0 A3 50 63 C1 E1 70 B0 66 FD 87 C4 E6 AA 
E2 E2 62 B8 BA BA CA 9C 4E 5D 51 7C FE F9 E7 14 2F 76 37 4B BD 96 40 77 A4 6C 6B E4 9D 9D 9D 38 
77 96 1D 55 B0 FC F5 50 F8 CF 17 8E 37 1D 8F 4D 5B 36 12 5E E2 CC CC 4C CC 9C 39 13 4F 9E C8 1F 
C4 24 2D 2F 5E BC 40 40 40 00 6D FA 76 E7 F7 9C B1 E8 03 F1 29 EA E9 48 FE 39 19 75 B5 75 8A 50 
8F 85 65 50 D1 2F BF A2 EE 30 D5 01 BE 1F FA 12 F2 3B 77 EE C0 D6 D6 96 C8 23 D9 1F 94 95 95 C1 
D1 D1 11 61 61 61 C4 39 9E 0D 0F 1F 6D 90 7D 89 AA BA AA 1A 51 27 4F 2B 42 3D 16 96 41 47 BF 18 
0B 00 58 E0 E6 02 F7 45 64 86 EF DA DA 5A CC 9D 3B 17 41 41 41 62 03 57 FA 8A 50 28 C4 4F 3F FD 
C4 18 E0 62 32 CE 18 5B 03 B7 50 C2 CD A5 6D F7 E0 FE 83 FD A2 33 0B CB 60 A0 DF 8C 05 00 AC F2 
5D 89 C5 4B 16 13 53 12 81 40 80 BF FF FD EF 30 35 35 C5 E1 C3 87 65 FE 25 73 26 12 12 12 60 6B 
6B 8B 65 CB 96 D1 86 48 4F E4 4D C4 D7 DF 7D 2D 73 58 37 00 5C 3C 1F 8F 82 7C F9 E3 17 58 58 06 
2B 8C 41 59 5A 5A C3 51 55 4D 9F 97 42 16 66 CF 9D 0D 63 63 63 24 5E 4E A4 4D 2C 12 BC 27 18 27 
4F 9D C4 A2 45 8B 30 7D FA 74 51 76 6E 69 A9 AA AA C2 AD 5B B7 90 90 90 20 4A C4 6A 32 CE 84 52 
86 C3 E1 C0 61 AA 03 1C DF 75 44 6B EB 0B B4 B6 CA 36 3A 68 69 69 41 C9 C3 12 38 38 38 48 2E CC 
C2 32 88 19 35 6A 14 E3 39 C6 A0 2C 16 16 96 BF 36 FD 16 94 C5 C2 C2 F2 E7 86 32 0D 29 2C 2C 24 
B6 6E B3 B0 B0 FC 35 E9 BD 0F 87 32 0D 61 61 61 61 61 80 9D 86 B0 B0 B0 48 07 6B 2C 58 58 58 A4 
E2 FF 01 E5 95 A4 88 29 16 25 65 00 00 00 00 49 45 4E 44 AE 42 60 82 
EndData
$EndBitmap
$EndSCHEMATC
