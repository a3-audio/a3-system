EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text GLabel 10650 7150 0    50   Input ~ 0
mux_selBtn_fx
Wire Wire Line
	10650 6550 10650 6250
Text GLabel 10650 6750 0    50   Input ~ 0
s2
Text GLabel 10650 6850 0    50   Input ~ 0
s1
Text GLabel 10650 6950 0    50   Input ~ 0
s0
NoConn ~ 14450 6500
NoConn ~ 14450 6600
Text GLabel 9000 5900 0    50   Input ~ 0
display_scl2
Text GLabel 9000 5800 0    50   Input ~ 0
display_sda2
$Comp
L mixer.pcb-rescue:GND-power #PWR0237
U 1 1 6112A339
P 9000 5700
F 0 "#PWR0237" H 9000 5450 50  0001 C CNN
F 1 "GND" V 9005 5572 50  0000 R CNN
F 2 "" H 9000 5700 50  0001 C CNN
F 3 "" H 9000 5700 50  0001 C CNN
	1    9000 5700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0236
U 1 1 6112A333
P 9000 5600
F 0 "#PWR0236" H 9000 5450 50  0001 C CNN
F 1 "+3.3V" V 9015 5728 50  0000 L CNN
F 2 "" H 9000 5600 50  0001 C CNN
F 3 "" H 9000 5600 50  0001 C CNN
	1    9000 5600
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x04-Connector_Generic display_2
U 1 1 6112A32D
P 9200 5700
F 0 "display_2" H 9118 5275 50  0001 C CNN
F 1 "Conn_01x04" H 9118 5366 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" H 9200 5700 50  0001 C CNN
F 3 "~" H 9200 5700 50  0001 C CNN
F 4 "display_2  " H 9200 5700 50  0000 L CNN "Field4"
	1    9200 5700
	1    0    0    -1  
$EndComp
Text GLabel 9000 6600 0    50   Input ~ 0
display_scl1
Text GLabel 9000 6500 0    50   Input ~ 0
display_sda1
$Comp
L mixer.pcb-rescue:GND-power #PWR0235
U 1 1 6112697F
P 9000 6400
F 0 "#PWR0235" H 9000 6150 50  0001 C CNN
F 1 "GND" V 9005 6272 50  0000 R CNN
F 2 "" H 9000 6400 50  0001 C CNN
F 3 "" H 9000 6400 50  0001 C CNN
	1    9000 6400
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0234
U 1 1 611261BB
P 9000 6300
F 0 "#PWR0234" H 9000 6150 50  0001 C CNN
F 1 "+3.3V" V 9015 6428 50  0000 L CNN
F 2 "" H 9000 6300 50  0001 C CNN
F 3 "" H 9000 6300 50  0001 C CNN
	1    9000 6300
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x04-Connector_Generic display_1
U 1 1 6112534C
P 9200 6400
F 0 "display_1" H 9118 5975 50  0001 C CNN
F 1 "Conn_01x04" H 9118 6066 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" H 9200 6400 50  0001 C CNN
F 3 "~" H 9200 6400 50  0001 C CNN
F 4 "display_1  " H 9200 6400 50  0000 L CNN "Field4"
	1    9200 6400
	1    0    0    -1  
$EndComp
Wire Wire Line
	14700 5300 15250 5300
Wire Wire Line
	14700 6700 14700 5300
Wire Wire Line
	14450 6700 14700 6700
Wire Wire Line
	14750 5950 15250 5950
Wire Wire Line
	14750 6800 14750 5950
Wire Wire Line
	14450 6800 14750 6800
Wire Wire Line
	14800 6900 14450 6900
Wire Wire Line
	14800 6600 14800 6900
Wire Wire Line
	15250 6600 14800 6600
Wire Wire Line
	14550 7250 15250 7250
Wire Wire Line
	14550 7000 14550 7250
Wire Wire Line
	14450 7000 14550 7000
Wire Wire Line
	14500 7100 14450 7100
Wire Wire Line
	14500 7900 14500 7100
Wire Wire Line
	15250 7900 14500 7900
Wire Wire Line
	14450 8550 15250 8550
Wire Wire Line
	14450 7200 14450 8550
$Comp
L mixer.pcb-rescue:GND-power #PWR0223
U 1 1 60909E72
P 15250 5200
F 0 "#PWR0223" H 15250 4950 50  0001 C CNN
F 1 "GND" V 15255 5072 50  0000 R CNN
F 2 "" H 15250 5200 50  0001 C CNN
F 3 "" H 15250 5200 50  0001 C CNN
	1    15250 5200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0222
U 1 1 60909E6C
P 15250 5100
F 0 "#PWR0222" H 15250 4950 50  0001 C CNN
F 1 "+3.3V" V 15265 5228 50  0000 L CNN
F 2 "" H 15250 5100 50  0001 C CNN
F 3 "" H 15250 5100 50  0001 C CNN
	1    15250 5100
	0    -1   -1   0   
$EndComp
Text GLabel 15250 5400 0    50   Input ~ 0
rEnc5_DT
Text GLabel 15250 5500 0    50   Input ~ 0
rEnc5_clk
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx2_enc3
U 1 1 60909E64
P 15450 5300
F 0 "fx2_enc3" H 15368 4875 50  0001 C CNN
F 1 "Conn_01x05" H 15368 4966 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 5300 50  0001 C CNN
F 3 "~" H 15450 5300 50  0001 C CNN
F 4 "fx2_enc3  " H 15450 5300 50  0000 L CNN "Field4"
	1    15450 5300
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0221
U 1 1 60909E5E
P 15250 5850
F 0 "#PWR0221" H 15250 5600 50  0001 C CNN
F 1 "GND" V 15255 5722 50  0000 R CNN
F 2 "" H 15250 5850 50  0001 C CNN
F 3 "" H 15250 5850 50  0001 C CNN
	1    15250 5850
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0220
U 1 1 60909E58
P 15250 5750
F 0 "#PWR0220" H 15250 5600 50  0001 C CNN
F 1 "+3.3V" V 15265 5878 50  0000 L CNN
F 2 "" H 15250 5750 50  0001 C CNN
F 3 "" H 15250 5750 50  0001 C CNN
	1    15250 5750
	0    -1   -1   0   
$EndComp
Text GLabel 15250 6050 0    50   Input ~ 0
rEnc4_DT
Text GLabel 15250 6150 0    50   Input ~ 0
rEnc4_clk
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx2_enc2
U 1 1 60909E50
P 15450 5950
F 0 "fx2_enc2" H 15368 5525 50  0001 C CNN
F 1 "Conn_01x05" H 15368 5616 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 5950 50  0001 C CNN
F 3 "~" H 15450 5950 50  0001 C CNN
F 4 "fx2_enc2  " H 15450 5950 50  0000 L CNN "Field4"
	1    15450 5950
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0219
U 1 1 60902119
P 15250 6500
F 0 "#PWR0219" H 15250 6250 50  0001 C CNN
F 1 "GND" V 15255 6372 50  0000 R CNN
F 2 "" H 15250 6500 50  0001 C CNN
F 3 "" H 15250 6500 50  0001 C CNN
	1    15250 6500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0218
U 1 1 60902113
P 15250 6400
F 0 "#PWR0218" H 15250 6250 50  0001 C CNN
F 1 "+3.3V" V 15265 6528 50  0000 L CNN
F 2 "" H 15250 6400 50  0001 C CNN
F 3 "" H 15250 6400 50  0001 C CNN
	1    15250 6400
	0    -1   -1   0   
$EndComp
Text GLabel 15250 6700 0    50   Input ~ 0
rEnc3_DT
Text GLabel 15250 6800 0    50   Input ~ 0
rEnc3_clk
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx2_enc1
U 1 1 6090210B
P 15450 6600
F 0 "fx2_enc1" H 15368 6175 50  0001 C CNN
F 1 "Conn_01x05" H 15368 6266 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 6600 50  0001 C CNN
F 3 "~" H 15450 6600 50  0001 C CNN
F 4 "fx2_enc1  " H 15450 6600 50  0000 L CNN "Field4"
	1    15450 6600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0217
U 1 1 60902105
P 15250 7150
F 0 "#PWR0217" H 15250 6900 50  0001 C CNN
F 1 "GND" V 15255 7022 50  0000 R CNN
F 2 "" H 15250 7150 50  0001 C CNN
F 3 "" H 15250 7150 50  0001 C CNN
	1    15250 7150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0216
U 1 1 609020FF
P 15250 7050
F 0 "#PWR0216" H 15250 6900 50  0001 C CNN
F 1 "+3.3V" V 15265 7178 50  0000 L CNN
F 2 "" H 15250 7050 50  0001 C CNN
F 3 "" H 15250 7050 50  0001 C CNN
	1    15250 7050
	0    -1   -1   0   
$EndComp
Text GLabel 15250 7350 0    50   Input ~ 0
rEnc2_DT
Text GLabel 15250 7450 0    50   Input ~ 0
rEnc2_clk
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx1_enc3
U 1 1 609020F7
P 15450 7250
F 0 "fx1_enc3" H 15368 6825 50  0001 C CNN
F 1 "Conn_01x05" H 15368 6916 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 7250 50  0001 C CNN
F 3 "~" H 15450 7250 50  0001 C CNN
F 4 "fx1_enc3  " H 15450 7250 50  0000 L CNN "Field4"
	1    15450 7250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0215
U 1 1 608F6C96
P 15250 7800
F 0 "#PWR0215" H 15250 7550 50  0001 C CNN
F 1 "GND" V 15255 7672 50  0000 R CNN
F 2 "" H 15250 7800 50  0001 C CNN
F 3 "" H 15250 7800 50  0001 C CNN
	1    15250 7800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0214
U 1 1 608F6C90
P 15250 7700
F 0 "#PWR0214" H 15250 7550 50  0001 C CNN
F 1 "+3.3V" V 15265 7828 50  0000 L CNN
F 2 "" H 15250 7700 50  0001 C CNN
F 3 "" H 15250 7700 50  0001 C CNN
	1    15250 7700
	0    -1   -1   0   
$EndComp
Text GLabel 15250 8000 0    50   Input ~ 0
rEnc1_DT
Text GLabel 15250 8100 0    50   Input ~ 0
rEnc1_clk
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx1_enc2
U 1 1 608F6C88
P 15450 7900
F 0 "fx1_enc2" H 15368 7475 50  0001 C CNN
F 1 "Conn_01x05" H 15368 7566 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 7900 50  0001 C CNN
F 3 "~" H 15450 7900 50  0001 C CNN
F 4 "fx1_enc2  " H 15450 7900 50  0000 L CNN "Field4"
	1    15450 7900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0213
U 1 1 608D2671
P 15250 8450
F 0 "#PWR0213" H 15250 8200 50  0001 C CNN
F 1 "GND" V 15255 8322 50  0000 R CNN
F 2 "" H 15250 8450 50  0001 C CNN
F 3 "" H 15250 8450 50  0001 C CNN
	1    15250 8450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0212
U 1 1 608D1C65
P 15250 8350
F 0 "#PWR0212" H 15250 8200 50  0001 C CNN
F 1 "+3.3V" V 15265 8478 50  0000 L CNN
F 2 "" H 15250 8350 50  0001 C CNN
F 3 "" H 15250 8350 50  0001 C CNN
	1    15250 8350
	0    -1   -1   0   
$EndComp
Text GLabel 15250 8650 0    50   Input ~ 0
rEnc0_DT
Text GLabel 15250 8750 0    50   Input ~ 0
rEnc0_clk
Text GLabel 13750 7200 0    50   Input ~ 0
mux_encBtn_fx
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0211
U 1 1 608BBCC9
P 14050 7400
F 0 "#PWR0211" H 14050 7250 50  0001 C CNN
F 1 "+3.3V" V 14065 7528 50  0000 L CNN
F 2 "" H 14050 7400 50  0001 C CNN
F 3 "" H 14050 7400 50  0001 C CNN
	1    14050 7400
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0210
U 1 1 608BB298
P 14050 6300
F 0 "#PWR0210" H 14050 6050 50  0001 C CNN
F 1 "GND" H 14055 6127 50  0000 C CNN
F 2 "" H 14050 6300 50  0001 C CNN
F 3 "" H 14050 6300 50  0001 C CNN
	1    14050 6300
	-1   0    0    1   
$EndComp
Connection ~ 14050 6300
Wire Wire Line
	14050 6300 14150 6300
Wire Wire Line
	13750 6300 14050 6300
Wire Wire Line
	13750 6600 13750 6300
Text GLabel 13750 6800 0    50   Input ~ 0
s2
Text GLabel 13750 6900 0    50   Input ~ 0
s1
Text GLabel 13750 7000 0    50   Input ~ 0
s0
$Comp
L mixer.pcb-rescue:74HC4051-74xx fxEncBtns1
U 1 1 60872CBE
P 14050 6900
F 0 "fxEncBtns1" H 14100 7581 50  0000 C CNN
F 1 "74HC4051" H 14100 7490 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 14050 6500 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 14050 6500 50  0001 C CNN
	1    14050 6900
	1    0    0    1   
$EndComp
Text GLabel 7500 5700 0    50   Input ~ 0
neopixel
$Comp
L mixer.pcb-rescue:GND-power #PWR0207
U 1 1 607656B6
P 7500 5800
F 0 "#PWR0207" H 7500 5550 50  0001 C CNN
F 1 "GND" V 7505 5672 50  0000 R CNN
F 2 "" H 7500 5800 50  0001 C CNN
F 3 "" H 7500 5800 50  0001 C CNN
	1    7500 5800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0196
U 1 1 6025BCEA
P 9000 7650
F 0 "#PWR0196" H 9000 7500 50  0001 C CNN
F 1 "+3.3V" V 9015 7778 50  0000 L CNN
F 2 "" H 9000 7650 50  0001 C CNN
F 3 "" H 9000 7650 50  0001 C CNN
	1    9000 7650
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_btn_1
U 1 1 6037D85D
P 9200 7650
F 0 "pfl_btn_1" H 9280 7642 50  0001 L CNN
F 1 "Conn_01x02" H 9280 7551 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 9200 7650 50  0001 C CNN
F 3 "~" H 9200 7650 50  0001 C CNN
F 4 "pfl_btn_1  " H 9200 7650 50  0000 L CNN "Field4"
	1    9200 7650
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0197
U 1 1 6048B6AA
P 9000 7900
F 0 "#PWR0197" H 9000 7750 50  0001 C CNN
F 1 "+3.3V" V 9015 8028 50  0000 L CNN
F 2 "" H 9000 7900 50  0001 C CNN
F 3 "" H 9000 7900 50  0001 C CNN
	1    9000 7900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_btn_2
U 1 1 6048B6B0
P 9200 7900
F 0 "pfl_btn_2" H 9280 7892 50  0001 L CNN
F 1 "Conn_01x02" H 9280 7801 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 9200 7900 50  0001 C CNN
F 3 "~" H 9200 7900 50  0001 C CNN
F 4 "pfl_btn_2  " H 9200 7900 50  0000 L CNN "Field4"
	1    9200 7900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0198
U 1 1 60492E77
P 9000 8150
F 0 "#PWR0198" H 9000 8000 50  0001 C CNN
F 1 "+3.3V" V 9015 8278 50  0000 L CNN
F 2 "" H 9000 8150 50  0001 C CNN
F 3 "" H 9000 8150 50  0001 C CNN
	1    9000 8150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_btn_3
U 1 1 60492E7D
P 9200 8150
F 0 "pfl_btn_3" H 9280 8142 50  0001 L CNN
F 1 "Conn_01x02" H 9280 8051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 9200 8150 50  0001 C CNN
F 3 "~" H 9200 8150 50  0001 C CNN
F 4 "pfl_btn_3  " H 9200 8150 50  0000 L CNN "Field4"
	1    9200 8150
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0199
U 1 1 6049A132
P 9000 8400
F 0 "#PWR0199" H 9000 8250 50  0001 C CNN
F 1 "+3.3V" V 9015 8528 50  0000 L CNN
F 2 "" H 9000 8400 50  0001 C CNN
F 3 "" H 9000 8400 50  0001 C CNN
	1    9000 8400
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_btn_4
U 1 1 6049A138
P 9200 8400
F 0 "pfl_btn_4" H 9280 8392 50  0001 L CNN
F 1 "Conn_01x02" H 9280 8301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 9200 8400 50  0001 C CNN
F 3 "~" H 9200 8400 50  0001 C CNN
F 4 "pfl_btn_4  " H 9200 8400 50  0000 L CNN "Field4"
	1    9200 8400
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0200
U 1 1 604A19B3
P 9000 8650
F 0 "#PWR0200" H 9000 8500 50  0001 C CNN
F 1 "+3.3V" V 9015 8778 50  0000 L CNN
F 2 "" H 9000 8650 50  0001 C CNN
F 3 "" H 9000 8650 50  0001 C CNN
	1    9000 8650
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_btn_master1
U 1 1 604A19B9
P 9200 8650
F 0 "pfl_btn_master1" H 9280 8642 50  0001 L CNN
F 1 "Conn_01x02" H 9280 8551 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 9200 8650 50  0001 C CNN
F 3 "~" H 9200 8650 50  0001 C CNN
F 4 "pfl_btn_master  " H 9200 8650 50  0000 L CNN "Field4"
	1    9200 8650
	1    0    0    -1  
$EndComp
Text GLabel 9000 7750 0    50   Input ~ 0
pfl_btn_ch1
Text GLabel 9000 8000 0    50   Input ~ 0
pfl_btn_ch2
Text GLabel 9000 8250 0    50   Input ~ 0
pfl_btn_ch3
Text GLabel 9000 8500 0    50   Input ~ 0
pfl_btn_ch4
Text GLabel 9000 8750 0    50   Input ~ 0
pfl_btn_master
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_led_1
U 1 1 6068794A
P 7700 7650
F 0 "pfl_led_1" H 7780 7642 50  0001 L CNN
F 1 "Conn_01x02" H 7780 7551 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7700 7650 50  0001 C CNN
F 3 "~" H 7700 7650 50  0001 C CNN
F 4 "pfl_led_1  " H 7700 7650 50  0000 L CNN "Field4"
	1    7700 7650
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_led_2
U 1 1 60687956
P 7700 7900
F 0 "pfl_led_2" H 7780 7892 50  0001 L CNN
F 1 "Conn_01x02" H 7780 7801 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7700 7900 50  0001 C CNN
F 3 "~" H 7700 7900 50  0001 C CNN
F 4 "pfl_led_2  " H 7700 7900 50  0000 L CNN "Field4"
	1    7700 7900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_led_3
U 1 1 60687962
P 7700 8150
F 0 "pfl_led_3" H 7780 8142 50  0001 L CNN
F 1 "Conn_01x02" H 7780 8051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7700 8150 50  0001 C CNN
F 3 "~" H 7700 8150 50  0001 C CNN
F 4 "pfl_led_3  " H 7700 8150 50  0000 L CNN "Field4"
	1    7700 8150
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_led_4
U 1 1 6068796E
P 7700 8400
F 0 "pfl_led_4" H 7780 8392 50  0001 L CNN
F 1 "Conn_01x02" H 7780 8301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7700 8400 50  0001 C CNN
F 3 "~" H 7700 8400 50  0001 C CNN
F 4 "pfl_led_4  " H 7700 8400 50  0000 L CNN "Field4"
	1    7700 8400
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic pfl_led_master1
U 1 1 6068797A
P 7700 8650
F 0 "pfl_led_master1" H 7780 8642 50  0001 L CNN
F 1 "Conn_01x02" H 7780 8551 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7700 8650 50  0001 C CNN
F 3 "~" H 7700 8650 50  0001 C CNN
F 4 "pfl_led_master  " H 7700 8650 50  0000 L CNN "Field4"
	1    7700 8650
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0247
U 1 1 6087B9AE
P 7500 7150
F 0 "#PWR0247" H 7500 7000 50  0001 C CNN
F 1 "+3.3V" V 7515 7278 50  0000 L CNN
F 2 "" H 7500 7150 50  0001 C CNN
F 3 "" H 7500 7150 50  0001 C CNN
	1    7500 7150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0246
U 1 1 6087B9A8
P 7500 7350
F 0 "#PWR0246" H 7500 7100 50  0001 C CNN
F 1 "GND" V 7505 7222 50  0000 R CNN
F 2 "" H 7500 7350 50  0001 C CNN
F 3 "" H 7500 7350 50  0001 C CNN
	1    7500 7350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0245
U 1 1 6086F86A
P 7500 6800
F 0 "#PWR0245" H 7500 6650 50  0001 C CNN
F 1 "+3.3V" V 7515 6928 50  0000 L CNN
F 2 "" H 7500 6800 50  0001 C CNN
F 3 "" H 7500 6800 50  0001 C CNN
	1    7500 6800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0244
U 1 1 6086F864
P 7500 7000
F 0 "#PWR0244" H 7500 6750 50  0001 C CNN
F 1 "GND" V 7505 6872 50  0000 R CNN
F 2 "" H 7500 7000 50  0001 C CNN
F 3 "" H 7500 7000 50  0001 C CNN
	1    7500 7000
	0    1    1    0   
$EndComp
Text GLabel 7500 7250 0    50   Input ~ 0
pin29
Text GLabel 7500 6900 0    50   Input ~ 0
pin28
Text GLabel 7500 6500 0    50   Input ~ 0
vu_clk
Text GLabel 7500 6400 0    50   Input ~ 0
vu_cs
Text GLabel 7500 6300 0    50   Input ~ 0
vu_din
Text GLabel 2100 7600 0    50   Input ~ 0
s0
Text GLabel 2100 7700 0    50   Input ~ 0
s1
Text GLabel 2100 7800 0    50   Input ~ 0
s2
Text GLabel 5150 6550 2    50   Input ~ 0
mux_ch1
$Comp
L mixer.pcb-rescue:GND-power #PWR0107
U 1 1 5FFE5E36
P 2100 5500
F 0 "#PWR0107" H 2100 5250 50  0001 C CNN
F 1 "GND" V 2105 5372 50  0000 R CNN
F 2 "" H 2100 5500 50  0001 C CNN
F 3 "" H 2100 5500 50  0001 C CNN
	1    2100 5500
	0    1    1    0   
$EndComp
NoConn ~ 4300 5350
NoConn ~ 4300 5500
NoConn ~ 4300 8050
NoConn ~ 4300 8150
NoConn ~ 4300 8250
NoConn ~ 4300 8350
NoConn ~ 4300 8450
NoConn ~ 4300 8550
NoConn ~ 2100 8650
NoConn ~ 2100 8550
NoConn ~ 2100 8450
NoConn ~ 2100 8350
NoConn ~ 2100 8250
NoConn ~ 2100 8100
NoConn ~ 2100 8000
NoConn ~ 2900 8950
NoConn ~ 3050 8950
NoConn ~ 3200 8950
NoConn ~ 3350 8950
NoConn ~ 3500 8950
Text GLabel 5150 6250 2    50   Input ~ 0
mux_ch2
Text GLabel 5150 8650 2    50   Input ~ 0
pfl_btn_ch1
Text GLabel 5150 8350 2    50   Input ~ 0
pfl_btn_ch2
Text GLabel 5150 8050 2    50   Input ~ 0
pfl_btn_ch3
Text GLabel 5150 7750 2    50   Input ~ 0
pfl_btn_ch4
Text GLabel 5150 7450 2    50   Input ~ 0
pfl_btn_master
Text GLabel 1200 7100 0    50   Input ~ 0
pfl_led_ch1
Text GLabel 4850 7300 2    50   Input ~ 0
pfl_led_ch2
Text GLabel 4850 7200 2    50   Input ~ 0
pfl_led_ch3
Text GLabel 4850 7100 2    50   Input ~ 0
pfl_led_ch4
Text GLabel 4850 7000 2    50   Input ~ 0
pfl_led_master
$Comp
L mixer.pcb-rescue:GND-power #PWR0208
U 1 1 6076C36F
P 4300 6900
F 0 "#PWR0208" H 4300 6650 50  0001 C CNN
F 1 "GND" V 4305 6772 50  0000 R CNN
F 2 "" H 4300 6900 50  0001 C CNN
F 3 "" H 4300 6900 50  0001 C CNN
	1    4300 6900
	0    -1   -1   0   
$EndComp
Text GLabel 2100 6700 0    50   Input ~ 0
rEnc5_clk
Text GLabel 2100 6600 0    50   Input ~ 0
rEnc5_DT
Text GLabel 2100 6500 0    50   Input ~ 0
rEnc4_clk
Text GLabel 2100 6400 0    50   Input ~ 0
rEnc4_DT
Text GLabel 2100 6300 0    50   Input ~ 0
rEnc3_clk
Text GLabel 2100 6200 0    50   Input ~ 0
rEnc3_DT
Text GLabel 2100 6100 0    50   Input ~ 0
rEnc2_clk
Text GLabel 2100 6000 0    50   Input ~ 0
rEnc2_DT
Text GLabel 2100 5900 0    50   Input ~ 0
rEnc1_clk
Text GLabel 2100 5800 0    50   Input ~ 0
rEnc1_DT
Text GLabel 2100 5700 0    50   Input ~ 0
rEnc0_clk
Text GLabel 2100 5600 0    50   Input ~ 0
rEnc0_DT
Text GLabel 1500 6800 0    50   Input ~ 0
mux_encBtn_fx
Text GLabel 1500 7400 0    50   Input ~ 0
mux_selBtn_fx
Text GLabel 5150 5350 2    50   Input ~ 0
mux_master
Text GLabel 5150 5650 2    50   Input ~ 0
mux_ch4
Text GLabel 5150 5950 2    50   Input ~ 0
mux_ch3
Text GLabel 4300 6400 2    50   Input ~ 0
display_sda1
Text GLabel 4300 6500 2    50   Input ~ 0
display_scl1
Text GLabel 2100 7100 0    50   Input ~ 0
display_sda2
Text GLabel 2100 7000 0    50   Input ~ 0
display_scl2
Text GLabel 4300 6300 2    50   Input ~ 0
vu_din
Text GLabel 4300 6600 2    50   Input ~ 0
vu_cs
Text GLabel 4300 6700 2    50   Input ~ 0
vu_clk
Text GLabel 1500 7700 0    50   Input ~ 0
pin28
Text GLabel 1500 8000 0    50   Input ~ 0
pin29
$Comp
L mixer.pcb-rescue:Teensy4.1-teensy U5
U 1 1 5FF8B2D7
P 3200 7650
F 0 "U5" H 3200 10215 50  0001 C CNN
F 1 "Teensy4.1" H 3200 10124 50  0000 C CNN
F 2 "teensy:Teensy41" H 2800 8050 50  0001 C CNN
F 3 "" H 2800 8050 50  0001 C CNN
	1    3200 7650
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0209
U 1 1 6076DEA4
P 950 6050
F 0 "#PWR0209" H 950 5900 50  0001 C CNN
F 1 "+3.3V" V 965 6178 50  0000 L CNN
F 2 "" H 950 6050 50  0001 C CNN
F 3 "" H 950 6050 50  0001 C CNN
	1    950  6050
	1    0    0    -1  
$EndComp
Text GLabel 4300 6800 2    50   Input ~ 0
neopixel
$Comp
L mixer.pcb-rescue:GND-power #PWR0105
U 1 1 607676BE
P 4300 5600
F 0 "#PWR0105" H 4300 5350 50  0001 C CNN
F 1 "GND" H 4305 5427 50  0000 C CNN
F 2 "" H 4300 5600 50  0001 C CNN
F 3 "" H 4300 5600 50  0001 C CNN
	1    4300 5600
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Connector_Generic_Conn_01x05-mixer.pcb VU_Matrix1
U 1 1 5FFCCC67
P 7700 6300
F 0 "VU_Matrix1" H 7618 5875 50  0001 C CNN
F 1 "MAX7219 led matrix vu" H 7618 5966 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 7700 6300 50  0001 C CNN
F 3 "" H 7700 6300 50  0001 C CNN
F 4 "VU_Matrix  " H 7700 6300 50  0000 L CNN "Field4"
	1    7700 6300
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0101
U 1 1 5FFD1DCA
P 7500 6200
F 0 "#PWR0101" H 7500 5950 50  0001 C CNN
F 1 "GND" V 7505 6072 50  0000 R CNN
F 2 "" H 7500 6200 50  0001 C CNN
F 3 "" H 7500 6200 50  0001 C CNN
	1    7500 6200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic spare(29)1
U 1 1 6087B9A2
P 7700 7250
F 0 "spare(29)1" H 7780 7292 50  0001 L CNN
F 1 "Conn_01x03" H 7780 7201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 7700 7250 50  0001 C CNN
F 3 "~" H 7700 7250 50  0001 C CNN
F 4 "  spare(29)" H 7700 7250 50  0000 L CNN "Field4"
	1    7700 7250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic spare(28)1
U 1 1 6086F85E
P 7700 6900
F 0 "spare(28)1" H 7780 6942 50  0001 L CNN
F 1 "Conn_01x03" H 7780 6851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 7700 6900 50  0001 C CNN
F 3 "~" H 7700 6900 50  0001 C CNN
F 4 "  spare(28)" H 7700 6900 50  0000 L CNN "Field4"
	1    7700 6900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x05-Connector_Generic fx1_enc1
U 1 1 608C8283
P 15450 8550
F 0 "fx1_enc1" H 15368 8125 50  0001 C CNN
F 1 "Conn_01x05" H 15368 8216 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical" H 15450 8550 50  0001 C CNN
F 3 "~" H 15450 8550 50  0001 C CNN
F 4 "fx1_enc1  " H 15450 8550 50  0000 L CNN "Field4"
	1    15450 8550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_5
U 1 1 600CE365
P 3200 2900
F 0 "MuxCh1_5" H 3280 2942 50  0000 L CNN
F 1 "Conn_01x03" H 3280 2851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 2900 50  0001 C CNN
F 3 "~" H 3200 2900 50  0001 C CNN
F 4 "  MuxCh1_5" H 3200 2900 50  0001 L CNN "Field4"
	1    3200 2900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_6
U 1 1 600CE35F
P 3200 3350
F 0 "MuxCh1_6" H 3280 3392 50  0000 L CNN
F 1 "Conn_01x03" H 3280 3301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 3350 50  0001 C CNN
F 3 "~" H 3200 3350 50  0001 C CNN
F 4 "  MuxCh1_6" H 3200 3350 50  0001 L CNN "Field4"
	1    3200 3350
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_8
U 1 1 600CE359
P 3200 4250
F 0 "MuxCh1_8" H 3280 4292 50  0000 L CNN
F 1 "Conn_01x03" H 3280 4201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 4250 50  0001 C CNN
F 3 "~" H 3200 4250 50  0001 C CNN
F 4 "  MuxCh1_8" H 3200 4250 50  0001 L CNN "Field4"
	1    3200 4250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_4
U 1 1 600CE33B
P 3200 2450
F 0 "MuxCh1_4" H 3280 2492 50  0000 L CNN
F 1 "Conn_01x03" H 3280 2401 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 2450 50  0001 C CNN
F 3 "~" H 3200 2450 50  0001 C CNN
F 4 "  MuxCh1_4" H 3200 2450 50  0001 L CNN "Field4"
	1    3200 2450
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_7
U 1 1 600CE335
P 3200 3800
F 0 "MuxCh1_7" H 3280 3842 50  0000 L CNN
F 1 "Conn_01x03" H 3280 3751 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 3800 50  0001 C CNN
F 3 "~" H 3200 3800 50  0001 C CNN
F 4 "  MuxCh1_7" H 3200 3800 50  0001 L CNN "Field4"
	1    3200 3800
	1    0    0    -1  
$EndComp
Text GLabel 1300 2500 0    50   Input ~ 0
s0
Text GLabel 1300 2600 0    50   Input ~ 0
s1
Text GLabel 1300 2300 0    50   Input ~ 0
mux_ch1
Text GLabel 1300 2700 0    50   Input ~ 0
s2
Wire Wire Line
	1700 3200 1600 3200
Wire Wire Line
	1600 3200 1300 3200
Wire Wire Line
	1300 3200 1300 2900
Connection ~ 1600 3200
$Comp
L mixer.pcb-rescue:GND-power #PWR0158
U 1 1 600CE2E7
P 1600 3200
F 0 "#PWR0158" H 1600 2950 50  0001 C CNN
F 1 "GND" H 1605 3027 50  0000 C CNN
F 2 "" H 1600 3200 50  0001 C CNN
F 3 "" H 1600 3200 50  0001 C CNN
	1    1600 3200
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0154
U 1 1 600CE2FF
P 3000 2350
F 0 "#PWR0154" H 3000 2200 50  0001 C CNN
F 1 "+3.3V" V 3015 2478 50  0000 L CNN
F 2 "" H 3000 2350 50  0001 C CNN
F 3 "" H 3000 2350 50  0001 C CNN
	1    3000 2350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0153
U 1 1 600CE305
P 3000 2550
F 0 "#PWR0153" H 3000 2300 50  0001 C CNN
F 1 "GND" V 3005 2422 50  0000 R CNN
F 2 "" H 3000 2550 50  0001 C CNN
F 3 "" H 3000 2550 50  0001 C CNN
	1    3000 2550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0152
U 1 1 600CE30B
P 3000 2800
F 0 "#PWR0152" H 3000 2650 50  0001 C CNN
F 1 "+3.3V" V 3015 2928 50  0000 L CNN
F 2 "" H 3000 2800 50  0001 C CNN
F 3 "" H 3000 2800 50  0001 C CNN
	1    3000 2800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0151
U 1 1 600CE311
P 3000 3000
F 0 "#PWR0151" H 3000 2750 50  0001 C CNN
F 1 "GND" V 3005 2872 50  0000 R CNN
F 2 "" H 3000 3000 50  0001 C CNN
F 3 "" H 3000 3000 50  0001 C CNN
	1    3000 3000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0150
U 1 1 600CE317
P 3000 3250
F 0 "#PWR0150" H 3000 3100 50  0001 C CNN
F 1 "+3.3V" V 3015 3378 50  0000 L CNN
F 2 "" H 3000 3250 50  0001 C CNN
F 3 "" H 3000 3250 50  0001 C CNN
	1    3000 3250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0149
U 1 1 600CE31D
P 3000 3450
F 0 "#PWR0149" H 3000 3200 50  0001 C CNN
F 1 "GND" V 3005 3322 50  0000 R CNN
F 2 "" H 3000 3450 50  0001 C CNN
F 3 "" H 3000 3450 50  0001 C CNN
	1    3000 3450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0148
U 1 1 600CE323
P 3000 3700
F 0 "#PWR0148" H 3000 3550 50  0001 C CNN
F 1 "+3.3V" V 3015 3828 50  0000 L CNN
F 2 "" H 3000 3700 50  0001 C CNN
F 3 "" H 3000 3700 50  0001 C CNN
	1    3000 3700
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0147
U 1 1 600CE329
P 3000 3900
F 0 "#PWR0147" H 3000 3650 50  0001 C CNN
F 1 "GND" V 3005 3772 50  0000 R CNN
F 2 "" H 3000 3900 50  0001 C CNN
F 3 "" H 3000 3900 50  0001 C CNN
	1    3000 3900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0146
U 1 1 600CE32F
P 3000 4150
F 0 "#PWR0146" H 3000 4000 50  0001 C CNN
F 1 "+3.3V" V 3015 4278 50  0000 L CNN
F 2 "" H 3000 4150 50  0001 C CNN
F 3 "" H 3000 4150 50  0001 C CNN
	1    3000 4150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx MuxCh1
U 1 1 600CE36B
P 1600 2600
F 0 "MuxCh1" H 1650 3281 50  0000 C CNN
F 1 "74HC4051" H 1650 3190 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 1600 2200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 1600 2200 50  0001 C CNN
	1    1600 2600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0142
U 1 1 600CE395
P 3000 4350
F 0 "#PWR0142" H 3000 4100 50  0001 C CNN
F 1 "GND" V 3005 4222 50  0000 R CNN
F 2 "" H 3000 4350 50  0001 C CNN
F 3 "" H 3000 4350 50  0001 C CNN
	1    3000 4350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0144
U 1 1 600CE347
P 3000 1200
F 0 "#PWR0144" H 3000 950 50  0001 C CNN
F 1 "GND" V 3005 1072 50  0000 R CNN
F 2 "" H 3000 1200 50  0001 C CNN
F 3 "" H 3000 1200 50  0001 C CNN
	1    3000 1200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0145
U 1 1 600CE341
P 3000 1000
F 0 "#PWR0145" H 3000 850 50  0001 C CNN
F 1 "+3.3V" V 3015 1128 50  0000 L CNN
F 2 "" H 3000 1000 50  0001 C CNN
F 3 "" H 3000 1000 50  0001 C CNN
	1    3000 1000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R9
U 1 1 60232D50
P 2550 950
F 0 "R9" H 2480 904 50  0001 C CNN
F 1 "100k   " H 2480 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 950 50  0001 C CNN
F 3 "~" H 2550 950 50  0001 C CNN
	1    2550 950 
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_1
U 1 1 600CE371
P 3200 1100
F 0 "MuxCh1_1" H 3280 1142 50  0000 L CNN
F 1 "Conn_01x03" H 3280 1051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 1100 50  0001 C CNN
F 3 "~" H 3200 1100 50  0001 C CNN
F 4 "  MuxCh1_1" H 3200 1100 50  0001 L CNN "Field4"
	1    3200 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 1100 3000 1100
$Comp
L mixer.pcb-rescue:GND-power #PWR0103
U 1 1 603CAD81
P 2550 800
F 0 "#PWR0103" H 2550 550 50  0001 C CNN
F 1 "GND" V 2555 672 50  0000 R CNN
F 2 "" H 2550 800 50  0001 C CNN
F 3 "" H 2550 800 50  0001 C CNN
	1    2550 800 
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0155
U 1 1 600CE2F9
P 3000 2100
F 0 "#PWR0155" H 3000 1850 50  0001 C CNN
F 1 "GND" V 3005 1972 50  0000 R CNN
F 2 "" H 3000 2100 50  0001 C CNN
F 3 "" H 3000 2100 50  0001 C CNN
	1    3000 2100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0143
U 1 1 600CE38F
P 3000 1650
F 0 "#PWR0143" H 3000 1400 50  0001 C CNN
F 1 "GND" V 3005 1522 50  0000 R CNN
F 2 "" H 3000 1650 50  0001 C CNN
F 3 "" H 3000 1650 50  0001 C CNN
	1    3000 1650
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0156
U 1 1 600CE2F3
P 3000 1900
F 0 "#PWR0156" H 3000 1750 50  0001 C CNN
F 1 "+3.3V" V 3015 2028 50  0000 L CNN
F 2 "" H 3000 1900 50  0001 C CNN
F 3 "" H 3000 1900 50  0001 C CNN
	1    3000 1900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0157
U 1 1 600CE2ED
P 3000 1450
F 0 "#PWR0157" H 3000 1300 50  0001 C CNN
F 1 "+3.3V" V 3015 1578 50  0000 L CNN
F 2 "" H 3000 1450 50  0001 C CNN
F 3 "" H 3000 1450 50  0001 C CNN
	1    3000 1450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_2
U 1 1 600CE353
P 3200 1550
F 0 "MuxCh1_2" H 3280 1592 50  0000 L CNN
F 1 "Conn_01x03" H 3280 1501 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 1550 50  0001 C CNN
F 3 "~" H 3200 1550 50  0001 C CNN
F 4 "  MuxCh1_2" H 3200 1550 50  0001 L CNN "Field4"
	1    3200 1550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0104
U 1 1 603E87C9
P 2550 1250
F 0 "#PWR0104" H 2550 1000 50  0001 C CNN
F 1 "GND" V 2555 1122 50  0000 R CNN
F 2 "" H 2550 1250 50  0001 C CNN
F 3 "" H 2550 1250 50  0001 C CNN
	1    2550 1250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R10
U 1 1 6087B97C
P 2550 1400
F 0 "R10" H 2480 1354 50  0001 C CNN
F 1 "100k   " H 2480 1400 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 1400 50  0001 C CNN
F 3 "~" H 2550 1400 50  0001 C CNN
	1    2550 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 1550 3000 1550
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_3
U 1 1 600CE34D
P 3200 2000
F 0 "MuxCh1_3" H 3280 2042 50  0000 L CNN
F 1 "Conn_01x03" H 3280 1951 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 3200 2000 50  0001 C CNN
F 3 "~" H 3200 2000 50  0001 C CNN
F 4 "  MuxCh1_3" H 3200 2000 50  0001 L CNN "Field4"
	1    3200 2000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R11
U 1 1 6090D08D
P 2550 1850
F 0 "R11" H 2480 1804 50  0001 C CNN
F 1 "100k   " H 2480 1850 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 1850 50  0001 C CNN
F 3 "~" H 2550 1850 50  0001 C CNN
	1    2550 1850
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 2000 3000 2000
$Comp
L mixer.pcb-rescue:GND-power #PWR0108
U 1 1 6090D094
P 2550 1700
F 0 "#PWR0108" H 2550 1450 50  0001 C CNN
F 1 "GND" V 2555 1572 50  0000 R CNN
F 2 "" H 2550 1700 50  0001 C CNN
F 3 "" H 2550 1700 50  0001 C CNN
	1    2550 1700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0109
U 1 1 6090D09A
P 2550 2150
F 0 "#PWR0109" H 2550 1900 50  0001 C CNN
F 1 "GND" V 2555 2022 50  0000 R CNN
F 2 "" H 2550 2150 50  0001 C CNN
F 3 "" H 2550 2150 50  0001 C CNN
	1    2550 2150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R12
U 1 1 6090D0A0
P 2550 2300
F 0 "R12" H 2480 2254 50  0001 C CNN
F 1 "100k   " H 2480 2300 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 2300 50  0001 C CNN
F 3 "~" H 2550 2300 50  0001 C CNN
	1    2550 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 2450 3000 2450
$Comp
L mixer.pcb-rescue:R-Device R13
U 1 1 6091657E
P 2550 2750
F 0 "R13" H 2480 2704 50  0001 C CNN
F 1 "100k   " H 2480 2750 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 2750 50  0001 C CNN
F 3 "~" H 2550 2750 50  0001 C CNN
	1    2550 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 2900 3000 2900
$Comp
L mixer.pcb-rescue:GND-power #PWR0110
U 1 1 60916585
P 2550 2600
F 0 "#PWR0110" H 2550 2350 50  0001 C CNN
F 1 "GND" V 2555 2472 50  0000 R CNN
F 2 "" H 2550 2600 50  0001 C CNN
F 3 "" H 2550 2600 50  0001 C CNN
	1    2550 2600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0111
U 1 1 6091658B
P 2550 3050
F 0 "#PWR0111" H 2550 2800 50  0001 C CNN
F 1 "GND" V 2555 2922 50  0000 R CNN
F 2 "" H 2550 3050 50  0001 C CNN
F 3 "" H 2550 3050 50  0001 C CNN
	1    2550 3050
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R14
U 1 1 60916591
P 2550 3200
F 0 "R14" H 2480 3154 50  0001 C CNN
F 1 "100k   " H 2480 3200 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 3200 50  0001 C CNN
F 3 "~" H 2550 3200 50  0001 C CNN
	1    2550 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 3350 3000 3350
$Comp
L mixer.pcb-rescue:R-Device R15
U 1 1 60920904
P 2550 3650
F 0 "R15" H 2480 3604 50  0001 C CNN
F 1 "100k   " H 2480 3650 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 3650 50  0001 C CNN
F 3 "~" H 2550 3650 50  0001 C CNN
	1    2550 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 3800 3000 3800
$Comp
L mixer.pcb-rescue:GND-power #PWR0112
U 1 1 6092090B
P 2550 3500
F 0 "#PWR0112" H 2550 3250 50  0001 C CNN
F 1 "GND" V 2555 3372 50  0000 R CNN
F 2 "" H 2550 3500 50  0001 C CNN
F 3 "" H 2550 3500 50  0001 C CNN
	1    2550 3500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0113
U 1 1 60920911
P 2550 3950
F 0 "#PWR0113" H 2550 3700 50  0001 C CNN
F 1 "GND" V 2555 3822 50  0000 R CNN
F 2 "" H 2550 3950 50  0001 C CNN
F 3 "" H 2550 3950 50  0001 C CNN
	1    2550 3950
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R16
U 1 1 60920917
P 2550 4100
F 0 "R16" H 2480 4054 50  0001 C CNN
F 1 "100k   " H 2480 4100 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2480 4100 50  0001 C CNN
F 3 "~" H 2550 4100 50  0001 C CNN
	1    2550 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	2550 4250 3000 4250
Wire Wire Line
	2000 4250 2000 3000
Wire Wire Line
	2050 3800 2050 2900
Wire Wire Line
	2050 2900 2000 2900
Wire Wire Line
	2100 3350 2100 2800
Wire Wire Line
	2100 2800 2000 2800
Wire Wire Line
	2150 2900 2150 2700
Wire Wire Line
	2150 2700 2000 2700
Wire Wire Line
	2000 1100 2000 2300
Wire Wire Line
	2050 1550 2050 2400
Wire Wire Line
	2050 2400 2000 2400
Wire Wire Line
	2000 2500 2100 2500
Wire Wire Line
	2150 2450 2150 2600
Wire Wire Line
	2150 2600 2000 2600
Wire Wire Line
	2550 1100 2000 1100
Connection ~ 2550 1100
Wire Wire Line
	2050 1550 2550 1550
Connection ~ 2550 1550
Wire Wire Line
	2100 2500 2100 2000
Wire Wire Line
	2550 2000 2100 2000
Connection ~ 2550 2000
Wire Wire Line
	2150 2450 2550 2450
Connection ~ 2550 2450
Wire Wire Line
	2550 2900 2150 2900
Connection ~ 2550 2900
Wire Wire Line
	2100 3350 2550 3350
Connection ~ 2550 3350
Wire Wire Line
	2550 3800 2050 3800
Connection ~ 2550 3800
Wire Wire Line
	2000 4250 2550 4250
Connection ~ 2550 4250
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_13
U 1 1 60B90E21
P 6250 2900
F 0 "MuxCh1_13" H 6330 2942 50  0000 L CNN
F 1 "Conn_01x03" H 6330 2851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 2900 50  0001 C CNN
F 3 "~" H 6250 2900 50  0001 C CNN
F 4 "  MuxCh1_5" H 6250 2900 50  0001 L CNN "Field4"
	1    6250 2900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_14
U 1 1 60B90E28
P 6250 3350
F 0 "MuxCh1_14" H 6330 3392 50  0000 L CNN
F 1 "Conn_01x03" H 6330 3301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 3350 50  0001 C CNN
F 3 "~" H 6250 3350 50  0001 C CNN
F 4 "  MuxCh1_6" H 6250 3350 50  0001 L CNN "Field4"
	1    6250 3350
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_16
U 1 1 60B90E2F
P 6250 4250
F 0 "MuxCh1_16" H 6330 4292 50  0000 L CNN
F 1 "Conn_01x03" H 6330 4201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 4250 50  0001 C CNN
F 3 "~" H 6250 4250 50  0001 C CNN
F 4 "  MuxCh1_8" H 6250 4250 50  0001 L CNN "Field4"
	1    6250 4250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_12
U 1 1 60B90E36
P 6250 2450
F 0 "MuxCh1_12" H 6330 2492 50  0000 L CNN
F 1 "Conn_01x03" H 6330 2401 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 2450 50  0001 C CNN
F 3 "~" H 6250 2450 50  0001 C CNN
F 4 "  MuxCh1_4" H 6250 2450 50  0001 L CNN "Field4"
	1    6250 2450
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_15
U 1 1 60B90E3D
P 6250 3800
F 0 "MuxCh1_15" H 6330 3842 50  0000 L CNN
F 1 "Conn_01x03" H 6330 3751 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 3800 50  0001 C CNN
F 3 "~" H 6250 3800 50  0001 C CNN
F 4 "  MuxCh1_7" H 6250 3800 50  0001 L CNN "Field4"
	1    6250 3800
	1    0    0    -1  
$EndComp
Text GLabel 4350 2500 0    50   Input ~ 0
s0
Text GLabel 4350 2600 0    50   Input ~ 0
s1
Text GLabel 4350 2300 0    50   Input ~ 0
mux_ch2
Text GLabel 4350 2700 0    50   Input ~ 0
s2
Wire Wire Line
	4750 3200 4650 3200
Wire Wire Line
	4650 3200 4350 3200
Wire Wire Line
	4350 3200 4350 2900
Connection ~ 4650 3200
$Comp
L mixer.pcb-rescue:GND-power #PWR0115
U 1 1 60B90E51
P 4650 3200
F 0 "#PWR0115" H 4650 2950 50  0001 C CNN
F 1 "GND" H 4655 3027 50  0000 C CNN
F 2 "" H 4650 3200 50  0001 C CNN
F 3 "" H 4650 3200 50  0001 C CNN
	1    4650 3200
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0116
U 1 1 60B90E57
P 6050 2350
F 0 "#PWR0116" H 6050 2200 50  0001 C CNN
F 1 "+3.3V" V 6065 2478 50  0000 L CNN
F 2 "" H 6050 2350 50  0001 C CNN
F 3 "" H 6050 2350 50  0001 C CNN
	1    6050 2350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0117
U 1 1 60B90E5D
P 6050 2550
F 0 "#PWR0117" H 6050 2300 50  0001 C CNN
F 1 "GND" V 6055 2422 50  0000 R CNN
F 2 "" H 6050 2550 50  0001 C CNN
F 3 "" H 6050 2550 50  0001 C CNN
	1    6050 2550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0118
U 1 1 60B90E63
P 6050 2800
F 0 "#PWR0118" H 6050 2650 50  0001 C CNN
F 1 "+3.3V" V 6065 2928 50  0000 L CNN
F 2 "" H 6050 2800 50  0001 C CNN
F 3 "" H 6050 2800 50  0001 C CNN
	1    6050 2800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0119
U 1 1 60B90E69
P 6050 3000
F 0 "#PWR0119" H 6050 2750 50  0001 C CNN
F 1 "GND" V 6055 2872 50  0000 R CNN
F 2 "" H 6050 3000 50  0001 C CNN
F 3 "" H 6050 3000 50  0001 C CNN
	1    6050 3000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0120
U 1 1 60B90E6F
P 6050 3250
F 0 "#PWR0120" H 6050 3100 50  0001 C CNN
F 1 "+3.3V" V 6065 3378 50  0000 L CNN
F 2 "" H 6050 3250 50  0001 C CNN
F 3 "" H 6050 3250 50  0001 C CNN
	1    6050 3250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0121
U 1 1 60B90E75
P 6050 3450
F 0 "#PWR0121" H 6050 3200 50  0001 C CNN
F 1 "GND" V 6055 3322 50  0000 R CNN
F 2 "" H 6050 3450 50  0001 C CNN
F 3 "" H 6050 3450 50  0001 C CNN
	1    6050 3450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0122
U 1 1 60B90E7B
P 6050 3700
F 0 "#PWR0122" H 6050 3550 50  0001 C CNN
F 1 "+3.3V" V 6065 3828 50  0000 L CNN
F 2 "" H 6050 3700 50  0001 C CNN
F 3 "" H 6050 3700 50  0001 C CNN
	1    6050 3700
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0123
U 1 1 60B90E81
P 6050 3900
F 0 "#PWR0123" H 6050 3650 50  0001 C CNN
F 1 "GND" V 6055 3772 50  0000 R CNN
F 2 "" H 6050 3900 50  0001 C CNN
F 3 "" H 6050 3900 50  0001 C CNN
	1    6050 3900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0124
U 1 1 60B90E87
P 6050 4150
F 0 "#PWR0124" H 6050 4000 50  0001 C CNN
F 1 "+3.3V" V 6065 4278 50  0000 L CNN
F 2 "" H 6050 4150 50  0001 C CNN
F 3 "" H 6050 4150 50  0001 C CNN
	1    6050 4150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx MuxCh2
U 1 1 60B90E8D
P 4650 2600
F 0 "MuxCh2" H 4700 3281 50  0000 C CNN
F 1 "74HC4051" H 4700 3190 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 4650 2200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 4650 2200 50  0001 C CNN
	1    4650 2600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0125
U 1 1 60B90E93
P 6050 4350
F 0 "#PWR0125" H 6050 4100 50  0001 C CNN
F 1 "GND" V 6055 4222 50  0000 R CNN
F 2 "" H 6050 4350 50  0001 C CNN
F 3 "" H 6050 4350 50  0001 C CNN
	1    6050 4350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0126
U 1 1 60B90E99
P 6050 1200
F 0 "#PWR0126" H 6050 950 50  0001 C CNN
F 1 "GND" V 6055 1072 50  0000 R CNN
F 2 "" H 6050 1200 50  0001 C CNN
F 3 "" H 6050 1200 50  0001 C CNN
	1    6050 1200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0127
U 1 1 60B90E9F
P 6050 1000
F 0 "#PWR0127" H 6050 850 50  0001 C CNN
F 1 "+3.3V" V 6065 1128 50  0000 L CNN
F 2 "" H 6050 1000 50  0001 C CNN
F 3 "" H 6050 1000 50  0001 C CNN
	1    6050 1000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R22
U 1 1 60B90EA5
P 5600 950
F 0 "R22" H 5530 904 50  0001 C CNN
F 1 "100k   " H 5530 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 950 50  0001 C CNN
F 3 "~" H 5600 950 50  0001 C CNN
	1    5600 950 
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_9
U 1 1 60B90EAC
P 6250 1100
F 0 "MuxCh1_9" H 6330 1142 50  0000 L CNN
F 1 "Conn_01x03" H 6330 1051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 1100 50  0001 C CNN
F 3 "~" H 6250 1100 50  0001 C CNN
F 4 "  MuxCh1_1" H 6250 1100 50  0001 L CNN "Field4"
	1    6250 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 1100 6050 1100
$Comp
L mixer.pcb-rescue:GND-power #PWR0128
U 1 1 60B90EB3
P 5600 800
F 0 "#PWR0128" H 5600 550 50  0001 C CNN
F 1 "GND" V 5605 672 50  0000 R CNN
F 2 "" H 5600 800 50  0001 C CNN
F 3 "" H 5600 800 50  0001 C CNN
	1    5600 800 
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0129
U 1 1 60B90EB9
P 6050 2100
F 0 "#PWR0129" H 6050 1850 50  0001 C CNN
F 1 "GND" V 6055 1972 50  0000 R CNN
F 2 "" H 6050 2100 50  0001 C CNN
F 3 "" H 6050 2100 50  0001 C CNN
	1    6050 2100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0130
U 1 1 60B90EBF
P 6050 1650
F 0 "#PWR0130" H 6050 1400 50  0001 C CNN
F 1 "GND" V 6055 1522 50  0000 R CNN
F 2 "" H 6050 1650 50  0001 C CNN
F 3 "" H 6050 1650 50  0001 C CNN
	1    6050 1650
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0131
U 1 1 60B90EC5
P 6050 1900
F 0 "#PWR0131" H 6050 1750 50  0001 C CNN
F 1 "+3.3V" V 6065 2028 50  0000 L CNN
F 2 "" H 6050 1900 50  0001 C CNN
F 3 "" H 6050 1900 50  0001 C CNN
	1    6050 1900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0132
U 1 1 60B90ECB
P 6050 1450
F 0 "#PWR0132" H 6050 1300 50  0001 C CNN
F 1 "+3.3V" V 6065 1578 50  0000 L CNN
F 2 "" H 6050 1450 50  0001 C CNN
F 3 "" H 6050 1450 50  0001 C CNN
	1    6050 1450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_10
U 1 1 60B90ED2
P 6250 1550
F 0 "MuxCh1_10" H 6330 1592 50  0000 L CNN
F 1 "Conn_01x03" H 6330 1501 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 1550 50  0001 C CNN
F 3 "~" H 6250 1550 50  0001 C CNN
F 4 "  MuxCh1_2" H 6250 1550 50  0001 L CNN "Field4"
	1    6250 1550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0133
U 1 1 60B90ED8
P 5600 1250
F 0 "#PWR0133" H 5600 1000 50  0001 C CNN
F 1 "GND" V 5605 1122 50  0000 R CNN
F 2 "" H 5600 1250 50  0001 C CNN
F 3 "" H 5600 1250 50  0001 C CNN
	1    5600 1250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R23
U 1 1 60B90EDE
P 5600 1400
F 0 "R23" H 5530 1354 50  0001 C CNN
F 1 "100k   " H 5530 1400 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 1400 50  0001 C CNN
F 3 "~" H 5600 1400 50  0001 C CNN
	1    5600 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 1550 6050 1550
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_11
U 1 1 60B90EE6
P 6250 2000
F 0 "MuxCh1_11" H 6330 2042 50  0000 L CNN
F 1 "Conn_01x03" H 6330 1951 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 6250 2000 50  0001 C CNN
F 3 "~" H 6250 2000 50  0001 C CNN
F 4 "  MuxCh1_3" H 6250 2000 50  0001 L CNN "Field4"
	1    6250 2000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R24
U 1 1 60B90EEC
P 5600 1850
F 0 "R24" H 5530 1804 50  0001 C CNN
F 1 "100k   " H 5530 1850 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 1850 50  0001 C CNN
F 3 "~" H 5600 1850 50  0001 C CNN
	1    5600 1850
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 2000 6050 2000
$Comp
L mixer.pcb-rescue:GND-power #PWR0134
U 1 1 60B90EF3
P 5600 1700
F 0 "#PWR0134" H 5600 1450 50  0001 C CNN
F 1 "GND" V 5605 1572 50  0000 R CNN
F 2 "" H 5600 1700 50  0001 C CNN
F 3 "" H 5600 1700 50  0001 C CNN
	1    5600 1700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0135
U 1 1 60B90EF9
P 5600 2150
F 0 "#PWR0135" H 5600 1900 50  0001 C CNN
F 1 "GND" V 5605 2022 50  0000 R CNN
F 2 "" H 5600 2150 50  0001 C CNN
F 3 "" H 5600 2150 50  0001 C CNN
	1    5600 2150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R25
U 1 1 60B90EFF
P 5600 2300
F 0 "R25" H 5530 2254 50  0001 C CNN
F 1 "100k   " H 5530 2300 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 2300 50  0001 C CNN
F 3 "~" H 5600 2300 50  0001 C CNN
	1    5600 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 2450 6050 2450
$Comp
L mixer.pcb-rescue:R-Device R26
U 1 1 60B90F06
P 5600 2750
F 0 "R26" H 5530 2704 50  0001 C CNN
F 1 "100k   " H 5530 2750 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 2750 50  0001 C CNN
F 3 "~" H 5600 2750 50  0001 C CNN
	1    5600 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 2900 6050 2900
$Comp
L mixer.pcb-rescue:GND-power #PWR0136
U 1 1 60B90F0D
P 5600 2600
F 0 "#PWR0136" H 5600 2350 50  0001 C CNN
F 1 "GND" V 5605 2472 50  0000 R CNN
F 2 "" H 5600 2600 50  0001 C CNN
F 3 "" H 5600 2600 50  0001 C CNN
	1    5600 2600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0137
U 1 1 60B90F13
P 5600 3050
F 0 "#PWR0137" H 5600 2800 50  0001 C CNN
F 1 "GND" V 5605 2922 50  0000 R CNN
F 2 "" H 5600 3050 50  0001 C CNN
F 3 "" H 5600 3050 50  0001 C CNN
	1    5600 3050
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R27
U 1 1 60B90F19
P 5600 3200
F 0 "R27" H 5530 3154 50  0001 C CNN
F 1 "100k   " H 5530 3200 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 3200 50  0001 C CNN
F 3 "~" H 5600 3200 50  0001 C CNN
	1    5600 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 3350 6050 3350
$Comp
L mixer.pcb-rescue:R-Device R28
U 1 1 60B90F20
P 5600 3650
F 0 "R28" H 5530 3604 50  0001 C CNN
F 1 "100k   " H 5530 3650 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 3650 50  0001 C CNN
F 3 "~" H 5600 3650 50  0001 C CNN
	1    5600 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 3800 6050 3800
$Comp
L mixer.pcb-rescue:GND-power #PWR0138
U 1 1 60B90F27
P 5600 3500
F 0 "#PWR0138" H 5600 3250 50  0001 C CNN
F 1 "GND" V 5605 3372 50  0000 R CNN
F 2 "" H 5600 3500 50  0001 C CNN
F 3 "" H 5600 3500 50  0001 C CNN
	1    5600 3500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0139
U 1 1 60B90F2D
P 5600 3950
F 0 "#PWR0139" H 5600 3700 50  0001 C CNN
F 1 "GND" V 5605 3822 50  0000 R CNN
F 2 "" H 5600 3950 50  0001 C CNN
F 3 "" H 5600 3950 50  0001 C CNN
	1    5600 3950
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R29
U 1 1 60B90F33
P 5600 4100
F 0 "R29" H 5530 4054 50  0001 C CNN
F 1 "100k   " H 5530 4100 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5530 4100 50  0001 C CNN
F 3 "~" H 5600 4100 50  0001 C CNN
	1    5600 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	5600 4250 6050 4250
Wire Wire Line
	5050 4250 5050 3000
Wire Wire Line
	5100 3800 5100 2900
Wire Wire Line
	5100 2900 5050 2900
Wire Wire Line
	5150 3350 5150 2800
Wire Wire Line
	5150 2800 5050 2800
Wire Wire Line
	5200 2900 5200 2700
Wire Wire Line
	5200 2700 5050 2700
Wire Wire Line
	5050 1100 5050 2300
Wire Wire Line
	5100 1550 5100 2400
Wire Wire Line
	5100 2400 5050 2400
Wire Wire Line
	5050 2500 5150 2500
Wire Wire Line
	5200 2450 5200 2600
Wire Wire Line
	5200 2600 5050 2600
Wire Wire Line
	5600 1100 5050 1100
Connection ~ 5600 1100
Wire Wire Line
	5100 1550 5600 1550
Connection ~ 5600 1550
Wire Wire Line
	5150 2500 5150 2000
Wire Wire Line
	5600 2000 5150 2000
Connection ~ 5600 2000
Wire Wire Line
	5200 2450 5600 2450
Connection ~ 5600 2450
Wire Wire Line
	5600 2900 5200 2900
Connection ~ 5600 2900
Wire Wire Line
	5150 3350 5600 3350
Connection ~ 5600 3350
Wire Wire Line
	5600 3800 5100 3800
Connection ~ 5600 3800
Wire Wire Line
	5050 4250 5600 4250
Connection ~ 5600 4250
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_21
U 1 1 60BA96A5
P 9350 2900
F 0 "MuxCh1_21" H 9430 2942 50  0000 L CNN
F 1 "Conn_01x03" H 9430 2851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 2900 50  0001 C CNN
F 3 "~" H 9350 2900 50  0001 C CNN
F 4 "  MuxCh1_5" H 9350 2900 50  0001 L CNN "Field4"
	1    9350 2900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_22
U 1 1 60BA96AC
P 9350 3350
F 0 "MuxCh1_22" H 9430 3392 50  0000 L CNN
F 1 "Conn_01x03" H 9430 3301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 3350 50  0001 C CNN
F 3 "~" H 9350 3350 50  0001 C CNN
F 4 "  MuxCh1_6" H 9350 3350 50  0001 L CNN "Field4"
	1    9350 3350
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_24
U 1 1 60BA96B3
P 9350 4250
F 0 "MuxCh1_24" H 9430 4292 50  0000 L CNN
F 1 "Conn_01x03" H 9430 4201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 4250 50  0001 C CNN
F 3 "~" H 9350 4250 50  0001 C CNN
F 4 "  MuxCh1_8" H 9350 4250 50  0001 L CNN "Field4"
	1    9350 4250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_20
U 1 1 60BA96BA
P 9350 2450
F 0 "MuxCh1_20" H 9430 2492 50  0000 L CNN
F 1 "Conn_01x03" H 9430 2401 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 2450 50  0001 C CNN
F 3 "~" H 9350 2450 50  0001 C CNN
F 4 "  MuxCh1_4" H 9350 2450 50  0001 L CNN "Field4"
	1    9350 2450
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_23
U 1 1 60BA96C1
P 9350 3800
F 0 "MuxCh1_23" H 9430 3842 50  0000 L CNN
F 1 "Conn_01x03" H 9430 3751 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 3800 50  0001 C CNN
F 3 "~" H 9350 3800 50  0001 C CNN
F 4 "  MuxCh1_7" H 9350 3800 50  0001 L CNN "Field4"
	1    9350 3800
	1    0    0    -1  
$EndComp
Text GLabel 7450 2500 0    50   Input ~ 0
s0
Text GLabel 7450 2600 0    50   Input ~ 0
s1
Text GLabel 7450 2300 0    50   Input ~ 0
mux_ch3
Text GLabel 7450 2700 0    50   Input ~ 0
s2
Wire Wire Line
	7850 3200 7750 3200
Wire Wire Line
	7750 3200 7450 3200
Wire Wire Line
	7450 3200 7450 2900
Connection ~ 7750 3200
$Comp
L mixer.pcb-rescue:GND-power #PWR0141
U 1 1 60BA96D5
P 7750 3200
F 0 "#PWR0141" H 7750 2950 50  0001 C CNN
F 1 "GND" H 7755 3027 50  0000 C CNN
F 2 "" H 7750 3200 50  0001 C CNN
F 3 "" H 7750 3200 50  0001 C CNN
	1    7750 3200
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0160
U 1 1 60BA96DB
P 9150 2350
F 0 "#PWR0160" H 9150 2200 50  0001 C CNN
F 1 "+3.3V" V 9165 2478 50  0000 L CNN
F 2 "" H 9150 2350 50  0001 C CNN
F 3 "" H 9150 2350 50  0001 C CNN
	1    9150 2350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0161
U 1 1 60BA96E1
P 9150 2550
F 0 "#PWR0161" H 9150 2300 50  0001 C CNN
F 1 "GND" V 9155 2422 50  0000 R CNN
F 2 "" H 9150 2550 50  0001 C CNN
F 3 "" H 9150 2550 50  0001 C CNN
	1    9150 2550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0162
U 1 1 60BA96E7
P 9150 2800
F 0 "#PWR0162" H 9150 2650 50  0001 C CNN
F 1 "+3.3V" V 9165 2928 50  0000 L CNN
F 2 "" H 9150 2800 50  0001 C CNN
F 3 "" H 9150 2800 50  0001 C CNN
	1    9150 2800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0163
U 1 1 60BA96ED
P 9150 3000
F 0 "#PWR0163" H 9150 2750 50  0001 C CNN
F 1 "GND" V 9155 2872 50  0000 R CNN
F 2 "" H 9150 3000 50  0001 C CNN
F 3 "" H 9150 3000 50  0001 C CNN
	1    9150 3000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0164
U 1 1 60BA96F3
P 9150 3250
F 0 "#PWR0164" H 9150 3100 50  0001 C CNN
F 1 "+3.3V" V 9165 3378 50  0000 L CNN
F 2 "" H 9150 3250 50  0001 C CNN
F 3 "" H 9150 3250 50  0001 C CNN
	1    9150 3250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0165
U 1 1 60BA96F9
P 9150 3450
F 0 "#PWR0165" H 9150 3200 50  0001 C CNN
F 1 "GND" V 9155 3322 50  0000 R CNN
F 2 "" H 9150 3450 50  0001 C CNN
F 3 "" H 9150 3450 50  0001 C CNN
	1    9150 3450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0166
U 1 1 60BA96FF
P 9150 3700
F 0 "#PWR0166" H 9150 3550 50  0001 C CNN
F 1 "+3.3V" V 9165 3828 50  0000 L CNN
F 2 "" H 9150 3700 50  0001 C CNN
F 3 "" H 9150 3700 50  0001 C CNN
	1    9150 3700
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0167
U 1 1 60BA9705
P 9150 3900
F 0 "#PWR0167" H 9150 3650 50  0001 C CNN
F 1 "GND" V 9155 3772 50  0000 R CNN
F 2 "" H 9150 3900 50  0001 C CNN
F 3 "" H 9150 3900 50  0001 C CNN
	1    9150 3900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0168
U 1 1 60BA970B
P 9150 4150
F 0 "#PWR0168" H 9150 4000 50  0001 C CNN
F 1 "+3.3V" V 9165 4278 50  0000 L CNN
F 2 "" H 9150 4150 50  0001 C CNN
F 3 "" H 9150 4150 50  0001 C CNN
	1    9150 4150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx MuxCh3
U 1 1 60BA9711
P 7750 2600
F 0 "MuxCh3" H 7800 3281 50  0000 C CNN
F 1 "74HC4051" H 7800 3190 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 7750 2200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 7750 2200 50  0001 C CNN
	1    7750 2600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0169
U 1 1 60BA9717
P 9150 4350
F 0 "#PWR0169" H 9150 4100 50  0001 C CNN
F 1 "GND" V 9155 4222 50  0000 R CNN
F 2 "" H 9150 4350 50  0001 C CNN
F 3 "" H 9150 4350 50  0001 C CNN
	1    9150 4350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0170
U 1 1 60BA971D
P 9150 1200
F 0 "#PWR0170" H 9150 950 50  0001 C CNN
F 1 "GND" V 9155 1072 50  0000 R CNN
F 2 "" H 9150 1200 50  0001 C CNN
F 3 "" H 9150 1200 50  0001 C CNN
	1    9150 1200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0171
U 1 1 60BA9723
P 9150 1000
F 0 "#PWR0171" H 9150 850 50  0001 C CNN
F 1 "+3.3V" V 9165 1128 50  0000 L CNN
F 2 "" H 9150 1000 50  0001 C CNN
F 3 "" H 9150 1000 50  0001 C CNN
	1    9150 1000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R44
U 1 1 60BA9729
P 8700 950
F 0 "R44" H 8630 904 50  0001 C CNN
F 1 "100k   " H 8630 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 950 50  0001 C CNN
F 3 "~" H 8700 950 50  0001 C CNN
	1    8700 950 
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_17
U 1 1 60BA9730
P 9350 1100
F 0 "MuxCh1_17" H 9430 1142 50  0000 L CNN
F 1 "Conn_01x03" H 9430 1051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 1100 50  0001 C CNN
F 3 "~" H 9350 1100 50  0001 C CNN
F 4 "  MuxCh1_1" H 9350 1100 50  0001 L CNN "Field4"
	1    9350 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	8700 1100 9150 1100
$Comp
L mixer.pcb-rescue:GND-power #PWR0172
U 1 1 60BA9737
P 8700 800
F 0 "#PWR0172" H 8700 550 50  0001 C CNN
F 1 "GND" V 8705 672 50  0000 R CNN
F 2 "" H 8700 800 50  0001 C CNN
F 3 "" H 8700 800 50  0001 C CNN
	1    8700 800 
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0173
U 1 1 60BA973D
P 9150 2100
F 0 "#PWR0173" H 9150 1850 50  0001 C CNN
F 1 "GND" V 9155 1972 50  0000 R CNN
F 2 "" H 9150 2100 50  0001 C CNN
F 3 "" H 9150 2100 50  0001 C CNN
	1    9150 2100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0174
U 1 1 60BA9743
P 9150 1650
F 0 "#PWR0174" H 9150 1400 50  0001 C CNN
F 1 "GND" V 9155 1522 50  0000 R CNN
F 2 "" H 9150 1650 50  0001 C CNN
F 3 "" H 9150 1650 50  0001 C CNN
	1    9150 1650
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0175
U 1 1 60BA9749
P 9150 1900
F 0 "#PWR0175" H 9150 1750 50  0001 C CNN
F 1 "+3.3V" V 9165 2028 50  0000 L CNN
F 2 "" H 9150 1900 50  0001 C CNN
F 3 "" H 9150 1900 50  0001 C CNN
	1    9150 1900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0176
U 1 1 60BA974F
P 9150 1450
F 0 "#PWR0176" H 9150 1300 50  0001 C CNN
F 1 "+3.3V" V 9165 1578 50  0000 L CNN
F 2 "" H 9150 1450 50  0001 C CNN
F 3 "" H 9150 1450 50  0001 C CNN
	1    9150 1450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_18
U 1 1 60BA9756
P 9350 1550
F 0 "MuxCh1_18" H 9430 1592 50  0000 L CNN
F 1 "Conn_01x03" H 9430 1501 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 1550 50  0001 C CNN
F 3 "~" H 9350 1550 50  0001 C CNN
F 4 "  MuxCh1_2" H 9350 1550 50  0001 L CNN "Field4"
	1    9350 1550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0177
U 1 1 60BA975C
P 8700 1250
F 0 "#PWR0177" H 8700 1000 50  0001 C CNN
F 1 "GND" V 8705 1122 50  0000 R CNN
F 2 "" H 8700 1250 50  0001 C CNN
F 3 "" H 8700 1250 50  0001 C CNN
	1    8700 1250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R45
U 1 1 60BA9762
P 8700 1400
F 0 "R45" H 8630 1354 50  0001 C CNN
F 1 "100k   " H 8630 1400 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 1400 50  0001 C CNN
F 3 "~" H 8700 1400 50  0001 C CNN
	1    8700 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 1550 9150 1550
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_19
U 1 1 60BA976A
P 9350 2000
F 0 "MuxCh1_19" H 9430 2042 50  0000 L CNN
F 1 "Conn_01x03" H 9430 1951 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 9350 2000 50  0001 C CNN
F 3 "~" H 9350 2000 50  0001 C CNN
F 4 "  MuxCh1_3" H 9350 2000 50  0001 L CNN "Field4"
	1    9350 2000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R46
U 1 1 60BA9770
P 8700 1850
F 0 "R46" H 8630 1804 50  0001 C CNN
F 1 "100k   " H 8630 1850 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 1850 50  0001 C CNN
F 3 "~" H 8700 1850 50  0001 C CNN
	1    8700 1850
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 2000 9150 2000
$Comp
L mixer.pcb-rescue:GND-power #PWR0178
U 1 1 60BA9777
P 8700 1700
F 0 "#PWR0178" H 8700 1450 50  0001 C CNN
F 1 "GND" V 8705 1572 50  0000 R CNN
F 2 "" H 8700 1700 50  0001 C CNN
F 3 "" H 8700 1700 50  0001 C CNN
	1    8700 1700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0179
U 1 1 60BA977D
P 8700 2150
F 0 "#PWR0179" H 8700 1900 50  0001 C CNN
F 1 "GND" V 8705 2022 50  0000 R CNN
F 2 "" H 8700 2150 50  0001 C CNN
F 3 "" H 8700 2150 50  0001 C CNN
	1    8700 2150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R47
U 1 1 60BA9783
P 8700 2300
F 0 "R47" H 8630 2254 50  0001 C CNN
F 1 "100k   " H 8630 2300 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 2300 50  0001 C CNN
F 3 "~" H 8700 2300 50  0001 C CNN
	1    8700 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 2450 9150 2450
$Comp
L mixer.pcb-rescue:R-Device R48
U 1 1 60BA978A
P 8700 2750
F 0 "R48" H 8630 2704 50  0001 C CNN
F 1 "100k   " H 8630 2750 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 2750 50  0001 C CNN
F 3 "~" H 8700 2750 50  0001 C CNN
	1    8700 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 2900 9150 2900
$Comp
L mixer.pcb-rescue:GND-power #PWR0180
U 1 1 60BA9791
P 8700 2600
F 0 "#PWR0180" H 8700 2350 50  0001 C CNN
F 1 "GND" V 8705 2472 50  0000 R CNN
F 2 "" H 8700 2600 50  0001 C CNN
F 3 "" H 8700 2600 50  0001 C CNN
	1    8700 2600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0181
U 1 1 60BA9797
P 8700 3050
F 0 "#PWR0181" H 8700 2800 50  0001 C CNN
F 1 "GND" V 8705 2922 50  0000 R CNN
F 2 "" H 8700 3050 50  0001 C CNN
F 3 "" H 8700 3050 50  0001 C CNN
	1    8700 3050
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R49
U 1 1 60BA979D
P 8700 3200
F 0 "R49" H 8630 3154 50  0001 C CNN
F 1 "100k   " H 8630 3200 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 3200 50  0001 C CNN
F 3 "~" H 8700 3200 50  0001 C CNN
	1    8700 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 3350 9150 3350
$Comp
L mixer.pcb-rescue:R-Device R50
U 1 1 60BA97A4
P 8700 3650
F 0 "R50" H 8630 3604 50  0001 C CNN
F 1 "100k   " H 8630 3650 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 3650 50  0001 C CNN
F 3 "~" H 8700 3650 50  0001 C CNN
	1    8700 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 3800 9150 3800
$Comp
L mixer.pcb-rescue:GND-power #PWR0182
U 1 1 60BA97AB
P 8700 3500
F 0 "#PWR0182" H 8700 3250 50  0001 C CNN
F 1 "GND" V 8705 3372 50  0000 R CNN
F 2 "" H 8700 3500 50  0001 C CNN
F 3 "" H 8700 3500 50  0001 C CNN
	1    8700 3500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0183
U 1 1 60BA97B1
P 8700 3950
F 0 "#PWR0183" H 8700 3700 50  0001 C CNN
F 1 "GND" V 8705 3822 50  0000 R CNN
F 2 "" H 8700 3950 50  0001 C CNN
F 3 "" H 8700 3950 50  0001 C CNN
	1    8700 3950
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R51
U 1 1 60BA97B7
P 8700 4100
F 0 "R51" H 8630 4054 50  0001 C CNN
F 1 "100k   " H 8630 4100 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 4100 50  0001 C CNN
F 3 "~" H 8700 4100 50  0001 C CNN
	1    8700 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 4250 9150 4250
Wire Wire Line
	8150 4250 8150 3000
Wire Wire Line
	8200 3800 8200 2900
Wire Wire Line
	8200 2900 8150 2900
Wire Wire Line
	8250 3350 8250 2800
Wire Wire Line
	8250 2800 8150 2800
Wire Wire Line
	8300 2900 8300 2700
Wire Wire Line
	8300 2700 8150 2700
Wire Wire Line
	8150 1100 8150 2300
Wire Wire Line
	8200 1550 8200 2400
Wire Wire Line
	8200 2400 8150 2400
Wire Wire Line
	8150 2500 8250 2500
Wire Wire Line
	8300 2450 8300 2600
Wire Wire Line
	8300 2600 8150 2600
Wire Wire Line
	8700 1100 8150 1100
Connection ~ 8700 1100
Wire Wire Line
	8200 1550 8700 1550
Connection ~ 8700 1550
Wire Wire Line
	8250 2500 8250 2000
Wire Wire Line
	8700 2000 8250 2000
Connection ~ 8700 2000
Wire Wire Line
	8300 2450 8700 2450
Connection ~ 8700 2450
Wire Wire Line
	8700 2900 8300 2900
Connection ~ 8700 2900
Wire Wire Line
	8250 3350 8700 3350
Connection ~ 8700 3350
Wire Wire Line
	8700 3800 8200 3800
Connection ~ 8700 3800
Wire Wire Line
	8150 4250 8700 4250
Connection ~ 8700 4250
$Comp
L mixer.pcb-rescue:R-Device R38
U 1 1 60BA97DC
P 5250 6650
F 0 "R38" H 5180 6604 50  0001 C CNN
F 1 "100k" V 5180 6650 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5180 6650 50  0001 C CNN
F 3 "~" H 5250 6650 50  0001 C CNN
	1    5250 6650
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0184
U 1 1 60BA97E2
P 5400 6650
F 0 "#PWR0184" H 5400 6400 50  0001 C CNN
F 1 "GND" V 5405 6522 50  0000 R CNN
F 2 "" H 5400 6650 50  0001 C CNN
F 3 "" H 5400 6650 50  0001 C CNN
	1    5400 6650
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_29
U 1 1 60BC2863
P 12500 2900
F 0 "MuxCh1_29" H 12580 2942 50  0000 L CNN
F 1 "Conn_01x03" H 12580 2851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 2900 50  0001 C CNN
F 3 "~" H 12500 2900 50  0001 C CNN
F 4 "  MuxCh1_5" H 12500 2900 50  0001 L CNN "Field4"
	1    12500 2900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_30
U 1 1 60BC286A
P 12500 3350
F 0 "MuxCh1_30" H 12580 3392 50  0000 L CNN
F 1 "Conn_01x03" H 12580 3301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 3350 50  0001 C CNN
F 3 "~" H 12500 3350 50  0001 C CNN
F 4 "  MuxCh1_6" H 12500 3350 50  0001 L CNN "Field4"
	1    12500 3350
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_32
U 1 1 60BC2871
P 12500 4250
F 0 "MuxCh1_32" H 12580 4292 50  0000 L CNN
F 1 "Conn_01x03" H 12580 4201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 4250 50  0001 C CNN
F 3 "~" H 12500 4250 50  0001 C CNN
F 4 "  MuxCh1_8" H 12500 4250 50  0001 L CNN "Field4"
	1    12500 4250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_28
U 1 1 60BC2878
P 12500 2450
F 0 "MuxCh1_28" H 12580 2492 50  0000 L CNN
F 1 "Conn_01x03" H 12580 2401 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 2450 50  0001 C CNN
F 3 "~" H 12500 2450 50  0001 C CNN
F 4 "  MuxCh1_4" H 12500 2450 50  0001 L CNN "Field4"
	1    12500 2450
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_31
U 1 1 60BC287F
P 12500 3800
F 0 "MuxCh1_31" H 12580 3842 50  0000 L CNN
F 1 "Conn_01x03" H 12580 3751 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 3800 50  0001 C CNN
F 3 "~" H 12500 3800 50  0001 C CNN
F 4 "  MuxCh1_7" H 12500 3800 50  0001 L CNN "Field4"
	1    12500 3800
	1    0    0    -1  
$EndComp
Text GLabel 10600 2500 0    50   Input ~ 0
s0
Text GLabel 10600 2600 0    50   Input ~ 0
s1
Text GLabel 10600 2300 0    50   Input ~ 0
mux_ch4
Text GLabel 10600 2700 0    50   Input ~ 0
s2
Wire Wire Line
	11000 3200 10900 3200
Wire Wire Line
	10900 3200 10600 3200
Wire Wire Line
	10600 3200 10600 2900
Connection ~ 10900 3200
$Comp
L mixer.pcb-rescue:GND-power #PWR0186
U 1 1 60BC2893
P 10900 3200
F 0 "#PWR0186" H 10900 2950 50  0001 C CNN
F 1 "GND" H 10905 3027 50  0000 C CNN
F 2 "" H 10900 3200 50  0001 C CNN
F 3 "" H 10900 3200 50  0001 C CNN
	1    10900 3200
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0187
U 1 1 60BC2899
P 12300 2350
F 0 "#PWR0187" H 12300 2200 50  0001 C CNN
F 1 "+3.3V" V 12315 2478 50  0000 L CNN
F 2 "" H 12300 2350 50  0001 C CNN
F 3 "" H 12300 2350 50  0001 C CNN
	1    12300 2350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0188
U 1 1 60BC289F
P 12300 2550
F 0 "#PWR0188" H 12300 2300 50  0001 C CNN
F 1 "GND" V 12305 2422 50  0000 R CNN
F 2 "" H 12300 2550 50  0001 C CNN
F 3 "" H 12300 2550 50  0001 C CNN
	1    12300 2550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0189
U 1 1 60BC28A5
P 12300 2800
F 0 "#PWR0189" H 12300 2650 50  0001 C CNN
F 1 "+3.3V" V 12315 2928 50  0000 L CNN
F 2 "" H 12300 2800 50  0001 C CNN
F 3 "" H 12300 2800 50  0001 C CNN
	1    12300 2800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0190
U 1 1 60BC28AB
P 12300 3000
F 0 "#PWR0190" H 12300 2750 50  0001 C CNN
F 1 "GND" V 12305 2872 50  0000 R CNN
F 2 "" H 12300 3000 50  0001 C CNN
F 3 "" H 12300 3000 50  0001 C CNN
	1    12300 3000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0191
U 1 1 60BC28B1
P 12300 3250
F 0 "#PWR0191" H 12300 3100 50  0001 C CNN
F 1 "+3.3V" V 12315 3378 50  0000 L CNN
F 2 "" H 12300 3250 50  0001 C CNN
F 3 "" H 12300 3250 50  0001 C CNN
	1    12300 3250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0192
U 1 1 60BC28B7
P 12300 3450
F 0 "#PWR0192" H 12300 3200 50  0001 C CNN
F 1 "GND" V 12305 3322 50  0000 R CNN
F 2 "" H 12300 3450 50  0001 C CNN
F 3 "" H 12300 3450 50  0001 C CNN
	1    12300 3450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0193
U 1 1 60BC28BD
P 12300 3700
F 0 "#PWR0193" H 12300 3550 50  0001 C CNN
F 1 "+3.3V" V 12315 3828 50  0000 L CNN
F 2 "" H 12300 3700 50  0001 C CNN
F 3 "" H 12300 3700 50  0001 C CNN
	1    12300 3700
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0194
U 1 1 60BC28C3
P 12300 3900
F 0 "#PWR0194" H 12300 3650 50  0001 C CNN
F 1 "GND" V 12305 3772 50  0000 R CNN
F 2 "" H 12300 3900 50  0001 C CNN
F 3 "" H 12300 3900 50  0001 C CNN
	1    12300 3900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0195
U 1 1 60BC28C9
P 12300 4150
F 0 "#PWR0195" H 12300 4000 50  0001 C CNN
F 1 "+3.3V" V 12315 4278 50  0000 L CNN
F 2 "" H 12300 4150 50  0001 C CNN
F 3 "" H 12300 4150 50  0001 C CNN
	1    12300 4150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx MuxCh4
U 1 1 60BC28CF
P 10900 2600
F 0 "MuxCh4" H 10950 3281 50  0000 C CNN
F 1 "74HC4051" H 10950 3190 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 10900 2200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 10900 2200 50  0001 C CNN
	1    10900 2600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0238
U 1 1 60BC28D5
P 12300 4350
F 0 "#PWR0238" H 12300 4100 50  0001 C CNN
F 1 "GND" V 12305 4222 50  0000 R CNN
F 2 "" H 12300 4350 50  0001 C CNN
F 3 "" H 12300 4350 50  0001 C CNN
	1    12300 4350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0239
U 1 1 60BC28DB
P 12300 1200
F 0 "#PWR0239" H 12300 950 50  0001 C CNN
F 1 "GND" V 12305 1072 50  0000 R CNN
F 2 "" H 12300 1200 50  0001 C CNN
F 3 "" H 12300 1200 50  0001 C CNN
	1    12300 1200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0240
U 1 1 60BC28E1
P 12300 1000
F 0 "#PWR0240" H 12300 850 50  0001 C CNN
F 1 "+3.3V" V 12315 1128 50  0000 L CNN
F 2 "" H 12300 1000 50  0001 C CNN
F 3 "" H 12300 1000 50  0001 C CNN
	1    12300 1000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R52
U 1 1 60BC28E7
P 11850 950
F 0 "R52" H 11780 904 50  0001 C CNN
F 1 "100k   " H 11780 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 950 50  0001 C CNN
F 3 "~" H 11850 950 50  0001 C CNN
	1    11850 950 
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_25
U 1 1 60BC28EE
P 12500 1100
F 0 "MuxCh1_25" H 12580 1142 50  0000 L CNN
F 1 "Conn_01x03" H 12580 1051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 1100 50  0001 C CNN
F 3 "~" H 12500 1100 50  0001 C CNN
F 4 "  MuxCh1_1" H 12500 1100 50  0001 L CNN "Field4"
	1    12500 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	11850 1100 12300 1100
$Comp
L mixer.pcb-rescue:GND-power #PWR0241
U 1 1 60BC28F5
P 11850 800
F 0 "#PWR0241" H 11850 550 50  0001 C CNN
F 1 "GND" V 11855 672 50  0000 R CNN
F 2 "" H 11850 800 50  0001 C CNN
F 3 "" H 11850 800 50  0001 C CNN
	1    11850 800 
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0242
U 1 1 60BC28FB
P 12300 2100
F 0 "#PWR0242" H 12300 1850 50  0001 C CNN
F 1 "GND" V 12305 1972 50  0000 R CNN
F 2 "" H 12300 2100 50  0001 C CNN
F 3 "" H 12300 2100 50  0001 C CNN
	1    12300 2100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0243
U 1 1 60BC2901
P 12300 1650
F 0 "#PWR0243" H 12300 1400 50  0001 C CNN
F 1 "GND" V 12305 1522 50  0000 R CNN
F 2 "" H 12300 1650 50  0001 C CNN
F 3 "" H 12300 1650 50  0001 C CNN
	1    12300 1650
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0248
U 1 1 60BC2907
P 12300 1900
F 0 "#PWR0248" H 12300 1750 50  0001 C CNN
F 1 "+3.3V" V 12315 2028 50  0000 L CNN
F 2 "" H 12300 1900 50  0001 C CNN
F 3 "" H 12300 1900 50  0001 C CNN
	1    12300 1900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0249
U 1 1 60BC290D
P 12300 1450
F 0 "#PWR0249" H 12300 1300 50  0001 C CNN
F 1 "+3.3V" V 12315 1578 50  0000 L CNN
F 2 "" H 12300 1450 50  0001 C CNN
F 3 "" H 12300 1450 50  0001 C CNN
	1    12300 1450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_26
U 1 1 60BC2914
P 12500 1550
F 0 "MuxCh1_26" H 12580 1592 50  0000 L CNN
F 1 "Conn_01x03" H 12580 1501 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 1550 50  0001 C CNN
F 3 "~" H 12500 1550 50  0001 C CNN
F 4 "  MuxCh1_2" H 12500 1550 50  0001 L CNN "Field4"
	1    12500 1550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0250
U 1 1 60BC291A
P 11850 1250
F 0 "#PWR0250" H 11850 1000 50  0001 C CNN
F 1 "GND" V 11855 1122 50  0000 R CNN
F 2 "" H 11850 1250 50  0001 C CNN
F 3 "" H 11850 1250 50  0001 C CNN
	1    11850 1250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R53
U 1 1 60BC2920
P 11850 1400
F 0 "R53" H 11780 1354 50  0001 C CNN
F 1 "100k   " H 11780 1400 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 1400 50  0001 C CNN
F 3 "~" H 11850 1400 50  0001 C CNN
	1    11850 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 1550 12300 1550
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_27
U 1 1 60BC2928
P 12500 2000
F 0 "MuxCh1_27" H 12580 2042 50  0000 L CNN
F 1 "Conn_01x03" H 12580 1951 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 12500 2000 50  0001 C CNN
F 3 "~" H 12500 2000 50  0001 C CNN
F 4 "  MuxCh1_3" H 12500 2000 50  0001 L CNN "Field4"
	1    12500 2000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R54
U 1 1 60BC292E
P 11850 1850
F 0 "R54" H 11780 1804 50  0001 C CNN
F 1 "100k   " H 11780 1850 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 1850 50  0001 C CNN
F 3 "~" H 11850 1850 50  0001 C CNN
	1    11850 1850
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 2000 12300 2000
$Comp
L mixer.pcb-rescue:GND-power #PWR0251
U 1 1 60BC2935
P 11850 1700
F 0 "#PWR0251" H 11850 1450 50  0001 C CNN
F 1 "GND" V 11855 1572 50  0000 R CNN
F 2 "" H 11850 1700 50  0001 C CNN
F 3 "" H 11850 1700 50  0001 C CNN
	1    11850 1700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0252
U 1 1 60BC293B
P 11850 2150
F 0 "#PWR0252" H 11850 1900 50  0001 C CNN
F 1 "GND" V 11855 2022 50  0000 R CNN
F 2 "" H 11850 2150 50  0001 C CNN
F 3 "" H 11850 2150 50  0001 C CNN
	1    11850 2150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R55
U 1 1 60BC2941
P 11850 2300
F 0 "R55" H 11780 2254 50  0001 C CNN
F 1 "100k   " H 11780 2300 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 2300 50  0001 C CNN
F 3 "~" H 11850 2300 50  0001 C CNN
	1    11850 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 2450 12300 2450
$Comp
L mixer.pcb-rescue:R-Device R56
U 1 1 60BC2948
P 11850 2750
F 0 "R56" H 11780 2704 50  0001 C CNN
F 1 "100k   " H 11780 2750 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 2750 50  0001 C CNN
F 3 "~" H 11850 2750 50  0001 C CNN
	1    11850 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 2900 12300 2900
$Comp
L mixer.pcb-rescue:GND-power #PWR0253
U 1 1 60BC294F
P 11850 2600
F 0 "#PWR0253" H 11850 2350 50  0001 C CNN
F 1 "GND" V 11855 2472 50  0000 R CNN
F 2 "" H 11850 2600 50  0001 C CNN
F 3 "" H 11850 2600 50  0001 C CNN
	1    11850 2600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0254
U 1 1 60BC2955
P 11850 3050
F 0 "#PWR0254" H 11850 2800 50  0001 C CNN
F 1 "GND" V 11855 2922 50  0000 R CNN
F 2 "" H 11850 3050 50  0001 C CNN
F 3 "" H 11850 3050 50  0001 C CNN
	1    11850 3050
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R57
U 1 1 60BC295B
P 11850 3200
F 0 "R57" H 11780 3154 50  0001 C CNN
F 1 "100k   " H 11780 3200 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 3200 50  0001 C CNN
F 3 "~" H 11850 3200 50  0001 C CNN
	1    11850 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 3350 12300 3350
$Comp
L mixer.pcb-rescue:R-Device R58
U 1 1 60BC2962
P 11850 3650
F 0 "R58" H 11780 3604 50  0001 C CNN
F 1 "100k   " H 11780 3650 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 3650 50  0001 C CNN
F 3 "~" H 11850 3650 50  0001 C CNN
	1    11850 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 3800 12300 3800
$Comp
L mixer.pcb-rescue:GND-power #PWR0255
U 1 1 60BC2969
P 11850 3500
F 0 "#PWR0255" H 11850 3250 50  0001 C CNN
F 1 "GND" V 11855 3372 50  0000 R CNN
F 2 "" H 11850 3500 50  0001 C CNN
F 3 "" H 11850 3500 50  0001 C CNN
	1    11850 3500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0256
U 1 1 60BC296F
P 11850 3950
F 0 "#PWR0256" H 11850 3700 50  0001 C CNN
F 1 "GND" V 11855 3822 50  0000 R CNN
F 2 "" H 11850 3950 50  0001 C CNN
F 3 "" H 11850 3950 50  0001 C CNN
	1    11850 3950
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R59
U 1 1 60BC2975
P 11850 4100
F 0 "R59" H 11780 4054 50  0001 C CNN
F 1 "100k   " H 11780 4100 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11780 4100 50  0001 C CNN
F 3 "~" H 11850 4100 50  0001 C CNN
	1    11850 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	11850 4250 12300 4250
Wire Wire Line
	11300 4250 11300 3000
Wire Wire Line
	11350 3800 11350 2900
Wire Wire Line
	11350 2900 11300 2900
Wire Wire Line
	11400 3350 11400 2800
Wire Wire Line
	11400 2800 11300 2800
Wire Wire Line
	11450 2900 11450 2700
Wire Wire Line
	11450 2700 11300 2700
Wire Wire Line
	11300 1100 11300 2300
Wire Wire Line
	11350 1550 11350 2400
Wire Wire Line
	11350 2400 11300 2400
Wire Wire Line
	11300 2500 11400 2500
Wire Wire Line
	11450 2450 11450 2600
Wire Wire Line
	11450 2600 11300 2600
Wire Wire Line
	11850 1100 11300 1100
Connection ~ 11850 1100
Wire Wire Line
	11350 1550 11850 1550
Connection ~ 11850 1550
Wire Wire Line
	11400 2500 11400 2000
Wire Wire Line
	11850 2000 11400 2000
Connection ~ 11850 2000
Wire Wire Line
	11450 2450 11850 2450
Connection ~ 11850 2450
Wire Wire Line
	11850 2900 11450 2900
Connection ~ 11850 2900
Wire Wire Line
	11400 3350 11850 3350
Connection ~ 11850 3350
Wire Wire Line
	11850 3800 11350 3800
Connection ~ 11850 3800
Wire Wire Line
	11300 4250 11850 4250
Connection ~ 11850 4250
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_37
U 1 1 60BD8FBA
P 15450 2900
F 0 "MuxCh1_37" H 15530 2942 50  0000 L CNN
F 1 "Conn_01x03" H 15530 2851 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 2900 50  0001 C CNN
F 3 "~" H 15450 2900 50  0001 C CNN
F 4 "  MuxCh1_5" H 15450 2900 50  0001 L CNN "Field4"
	1    15450 2900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_38
U 1 1 60BD8FC1
P 15450 3350
F 0 "MuxCh1_38" H 15530 3392 50  0000 L CNN
F 1 "Conn_01x03" H 15530 3301 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 3350 50  0001 C CNN
F 3 "~" H 15450 3350 50  0001 C CNN
F 4 "  MuxCh1_6" H 15450 3350 50  0001 L CNN "Field4"
	1    15450 3350
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_40
U 1 1 60BD8FC8
P 15450 4250
F 0 "MuxCh1_40" H 15530 4292 50  0000 L CNN
F 1 "Conn_01x03" H 15530 4201 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 4250 50  0001 C CNN
F 3 "~" H 15450 4250 50  0001 C CNN
F 4 "  MuxCh1_8" H 15450 4250 50  0001 L CNN "Field4"
	1    15450 4250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_36
U 1 1 60BD8FCF
P 15450 2450
F 0 "MuxCh1_36" H 15530 2492 50  0000 L CNN
F 1 "Conn_01x03" H 15530 2401 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 2450 50  0001 C CNN
F 3 "~" H 15450 2450 50  0001 C CNN
F 4 "  MuxCh1_4" H 15450 2450 50  0001 L CNN "Field4"
	1    15450 2450
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_39
U 1 1 60BD8FD6
P 15450 3800
F 0 "MuxCh1_39" H 15530 3842 50  0000 L CNN
F 1 "Conn_01x03" H 15530 3751 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 3800 50  0001 C CNN
F 3 "~" H 15450 3800 50  0001 C CNN
F 4 "  MuxCh1_7" H 15450 3800 50  0001 L CNN "Field4"
	1    15450 3800
	1    0    0    -1  
$EndComp
Text GLabel 13550 2500 0    50   Input ~ 0
s0
Text GLabel 13550 2600 0    50   Input ~ 0
s1
Text GLabel 13550 2300 0    50   Input ~ 0
mux_master
Text GLabel 13550 2700 0    50   Input ~ 0
s2
Wire Wire Line
	13950 3200 13850 3200
Wire Wire Line
	13850 3200 13550 3200
Wire Wire Line
	13550 3200 13550 2900
Connection ~ 13850 3200
$Comp
L mixer.pcb-rescue:GND-power #PWR0258
U 1 1 60BD8FEA
P 13850 3200
F 0 "#PWR0258" H 13850 2950 50  0001 C CNN
F 1 "GND" H 13855 3027 50  0000 C CNN
F 2 "" H 13850 3200 50  0001 C CNN
F 3 "" H 13850 3200 50  0001 C CNN
	1    13850 3200
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0259
U 1 1 60BD8FF0
P 15250 2350
F 0 "#PWR0259" H 15250 2200 50  0001 C CNN
F 1 "+3.3V" V 15265 2478 50  0000 L CNN
F 2 "" H 15250 2350 50  0001 C CNN
F 3 "" H 15250 2350 50  0001 C CNN
	1    15250 2350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0260
U 1 1 60BD8FF6
P 15250 2550
F 0 "#PWR0260" H 15250 2300 50  0001 C CNN
F 1 "GND" V 15255 2422 50  0000 R CNN
F 2 "" H 15250 2550 50  0001 C CNN
F 3 "" H 15250 2550 50  0001 C CNN
	1    15250 2550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0261
U 1 1 60BD8FFC
P 15250 2800
F 0 "#PWR0261" H 15250 2650 50  0001 C CNN
F 1 "+3.3V" V 15265 2928 50  0000 L CNN
F 2 "" H 15250 2800 50  0001 C CNN
F 3 "" H 15250 2800 50  0001 C CNN
	1    15250 2800
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0262
U 1 1 60BD9002
P 15250 3000
F 0 "#PWR0262" H 15250 2750 50  0001 C CNN
F 1 "GND" V 15255 2872 50  0000 R CNN
F 2 "" H 15250 3000 50  0001 C CNN
F 3 "" H 15250 3000 50  0001 C CNN
	1    15250 3000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0263
U 1 1 60BD9008
P 15250 3250
F 0 "#PWR0263" H 15250 3100 50  0001 C CNN
F 1 "+3.3V" V 15265 3378 50  0000 L CNN
F 2 "" H 15250 3250 50  0001 C CNN
F 3 "" H 15250 3250 50  0001 C CNN
	1    15250 3250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0264
U 1 1 60BD900E
P 15250 3450
F 0 "#PWR0264" H 15250 3200 50  0001 C CNN
F 1 "GND" V 15255 3322 50  0000 R CNN
F 2 "" H 15250 3450 50  0001 C CNN
F 3 "" H 15250 3450 50  0001 C CNN
	1    15250 3450
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0265
U 1 1 60BD9014
P 15250 3700
F 0 "#PWR0265" H 15250 3550 50  0001 C CNN
F 1 "+3.3V" V 15265 3828 50  0000 L CNN
F 2 "" H 15250 3700 50  0001 C CNN
F 3 "" H 15250 3700 50  0001 C CNN
	1    15250 3700
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0266
U 1 1 60BD901A
P 15250 3900
F 0 "#PWR0266" H 15250 3650 50  0001 C CNN
F 1 "GND" V 15255 3772 50  0000 R CNN
F 2 "" H 15250 3900 50  0001 C CNN
F 3 "" H 15250 3900 50  0001 C CNN
	1    15250 3900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0267
U 1 1 60BD9020
P 15250 4150
F 0 "#PWR0267" H 15250 4000 50  0001 C CNN
F 1 "+3.3V" V 15265 4278 50  0000 L CNN
F 2 "" H 15250 4150 50  0001 C CNN
F 3 "" H 15250 4150 50  0001 C CNN
	1    15250 4150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx MuxCh5
U 1 1 60BD9026
P 13850 2600
F 0 "MuxCh5" H 13900 3281 50  0000 C CNN
F 1 "74HC4051" H 13900 3190 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 13850 2200 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 13850 2200 50  0001 C CNN
	1    13850 2600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0268
U 1 1 60BD902C
P 15250 4350
F 0 "#PWR0268" H 15250 4100 50  0001 C CNN
F 1 "GND" V 15255 4222 50  0000 R CNN
F 2 "" H 15250 4350 50  0001 C CNN
F 3 "" H 15250 4350 50  0001 C CNN
	1    15250 4350
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0269
U 1 1 60BD9032
P 15250 1200
F 0 "#PWR0269" H 15250 950 50  0001 C CNN
F 1 "GND" V 15255 1072 50  0000 R CNN
F 2 "" H 15250 1200 50  0001 C CNN
F 3 "" H 15250 1200 50  0001 C CNN
	1    15250 1200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0270
U 1 1 60BD9038
P 15250 1000
F 0 "#PWR0270" H 15250 850 50  0001 C CNN
F 1 "+3.3V" V 15265 1128 50  0000 L CNN
F 2 "" H 15250 1000 50  0001 C CNN
F 3 "" H 15250 1000 50  0001 C CNN
	1    15250 1000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R60
U 1 1 60BD903E
P 14800 950
F 0 "R60" H 14730 904 50  0001 C CNN
F 1 "100k   " H 14730 950 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 950 50  0001 C CNN
F 3 "~" H 14800 950 50  0001 C CNN
	1    14800 950 
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_33
U 1 1 60BD9045
P 15450 1100
F 0 "MuxCh1_33" H 15530 1142 50  0000 L CNN
F 1 "Conn_01x03" H 15530 1051 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 1100 50  0001 C CNN
F 3 "~" H 15450 1100 50  0001 C CNN
F 4 "  MuxCh1_1" H 15450 1100 50  0001 L CNN "Field4"
	1    15450 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	14800 1100 15250 1100
$Comp
L mixer.pcb-rescue:GND-power #PWR0271
U 1 1 60BD904C
P 14800 800
F 0 "#PWR0271" H 14800 550 50  0001 C CNN
F 1 "GND" V 14805 672 50  0000 R CNN
F 2 "" H 14800 800 50  0001 C CNN
F 3 "" H 14800 800 50  0001 C CNN
	1    14800 800 
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0272
U 1 1 60BD9052
P 15250 2100
F 0 "#PWR0272" H 15250 1850 50  0001 C CNN
F 1 "GND" V 15255 1972 50  0000 R CNN
F 2 "" H 15250 2100 50  0001 C CNN
F 3 "" H 15250 2100 50  0001 C CNN
	1    15250 2100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0273
U 1 1 60BD9058
P 15250 1650
F 0 "#PWR0273" H 15250 1400 50  0001 C CNN
F 1 "GND" V 15255 1522 50  0000 R CNN
F 2 "" H 15250 1650 50  0001 C CNN
F 3 "" H 15250 1650 50  0001 C CNN
	1    15250 1650
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0274
U 1 1 60BD905E
P 15250 1900
F 0 "#PWR0274" H 15250 1750 50  0001 C CNN
F 1 "+3.3V" V 15265 2028 50  0000 L CNN
F 2 "" H 15250 1900 50  0001 C CNN
F 3 "" H 15250 1900 50  0001 C CNN
	1    15250 1900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0275
U 1 1 60BD9064
P 15250 1450
F 0 "#PWR0275" H 15250 1300 50  0001 C CNN
F 1 "+3.3V" V 15265 1578 50  0000 L CNN
F 2 "" H 15250 1450 50  0001 C CNN
F 3 "" H 15250 1450 50  0001 C CNN
	1    15250 1450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_34
U 1 1 60BD906B
P 15450 1550
F 0 "MuxCh1_34" H 15530 1592 50  0000 L CNN
F 1 "Conn_01x03" H 15530 1501 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 1550 50  0001 C CNN
F 3 "~" H 15450 1550 50  0001 C CNN
F 4 "  MuxCh1_2" H 15450 1550 50  0001 L CNN "Field4"
	1    15450 1550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0276
U 1 1 60BD9071
P 14800 1250
F 0 "#PWR0276" H 14800 1000 50  0001 C CNN
F 1 "GND" V 14805 1122 50  0000 R CNN
F 2 "" H 14800 1250 50  0001 C CNN
F 3 "" H 14800 1250 50  0001 C CNN
	1    14800 1250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R61
U 1 1 60BD9077
P 14800 1400
F 0 "R61" H 14730 1354 50  0001 C CNN
F 1 "100k   " H 14730 1400 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 1400 50  0001 C CNN
F 3 "~" H 14800 1400 50  0001 C CNN
	1    14800 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 1550 15250 1550
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic MuxCh1_35
U 1 1 60BD907F
P 15450 2000
F 0 "MuxCh1_35" H 15530 2042 50  0000 L CNN
F 1 "Conn_01x03" H 15530 1951 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 15450 2000 50  0001 C CNN
F 3 "~" H 15450 2000 50  0001 C CNN
F 4 "  MuxCh1_3" H 15450 2000 50  0001 L CNN "Field4"
	1    15450 2000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R62
U 1 1 60BD9085
P 14800 1850
F 0 "R62" H 14730 1804 50  0001 C CNN
F 1 "100k   " H 14730 1850 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 1850 50  0001 C CNN
F 3 "~" H 14800 1850 50  0001 C CNN
	1    14800 1850
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 2000 15250 2000
$Comp
L mixer.pcb-rescue:GND-power #PWR0277
U 1 1 60BD908C
P 14800 1700
F 0 "#PWR0277" H 14800 1450 50  0001 C CNN
F 1 "GND" V 14805 1572 50  0000 R CNN
F 2 "" H 14800 1700 50  0001 C CNN
F 3 "" H 14800 1700 50  0001 C CNN
	1    14800 1700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0278
U 1 1 60BD9092
P 14800 2150
F 0 "#PWR0278" H 14800 1900 50  0001 C CNN
F 1 "GND" V 14805 2022 50  0000 R CNN
F 2 "" H 14800 2150 50  0001 C CNN
F 3 "" H 14800 2150 50  0001 C CNN
	1    14800 2150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R63
U 1 1 60BD9098
P 14800 2300
F 0 "R63" H 14730 2254 50  0001 C CNN
F 1 "100k   " H 14730 2300 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 2300 50  0001 C CNN
F 3 "~" H 14800 2300 50  0001 C CNN
	1    14800 2300
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 2450 15250 2450
$Comp
L mixer.pcb-rescue:R-Device R64
U 1 1 60BD909F
P 14800 2750
F 0 "R64" H 14730 2704 50  0001 C CNN
F 1 "100k   " H 14730 2750 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 2750 50  0001 C CNN
F 3 "~" H 14800 2750 50  0001 C CNN
	1    14800 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 2900 15250 2900
$Comp
L mixer.pcb-rescue:GND-power #PWR0279
U 1 1 60BD90A6
P 14800 2600
F 0 "#PWR0279" H 14800 2350 50  0001 C CNN
F 1 "GND" V 14805 2472 50  0000 R CNN
F 2 "" H 14800 2600 50  0001 C CNN
F 3 "" H 14800 2600 50  0001 C CNN
	1    14800 2600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0280
U 1 1 60BD90AC
P 14800 3050
F 0 "#PWR0280" H 14800 2800 50  0001 C CNN
F 1 "GND" V 14805 2922 50  0000 R CNN
F 2 "" H 14800 3050 50  0001 C CNN
F 3 "" H 14800 3050 50  0001 C CNN
	1    14800 3050
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R65
U 1 1 60BD90B2
P 14800 3200
F 0 "R65" H 14730 3154 50  0001 C CNN
F 1 "100k   " H 14730 3200 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 3200 50  0001 C CNN
F 3 "~" H 14800 3200 50  0001 C CNN
	1    14800 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 3350 15250 3350
$Comp
L mixer.pcb-rescue:R-Device R66
U 1 1 60BD90B9
P 14800 3650
F 0 "R66" H 14730 3604 50  0001 C CNN
F 1 "100k   " H 14730 3650 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 3650 50  0001 C CNN
F 3 "~" H 14800 3650 50  0001 C CNN
	1    14800 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 3800 15250 3800
$Comp
L mixer.pcb-rescue:GND-power #PWR0281
U 1 1 60BD90C0
P 14800 3500
F 0 "#PWR0281" H 14800 3250 50  0001 C CNN
F 1 "GND" V 14805 3372 50  0000 R CNN
F 2 "" H 14800 3500 50  0001 C CNN
F 3 "" H 14800 3500 50  0001 C CNN
	1    14800 3500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0282
U 1 1 60BD90C6
P 14800 3950
F 0 "#PWR0282" H 14800 3700 50  0001 C CNN
F 1 "GND" V 14805 3822 50  0000 R CNN
F 2 "" H 14800 3950 50  0001 C CNN
F 3 "" H 14800 3950 50  0001 C CNN
	1    14800 3950
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R67
U 1 1 60BD90CC
P 14800 4100
F 0 "R67" H 14730 4054 50  0001 C CNN
F 1 "100k   " H 14730 4100 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 14730 4100 50  0001 C CNN
F 3 "~" H 14800 4100 50  0001 C CNN
	1    14800 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	14800 4250 15250 4250
Wire Wire Line
	14250 4250 14250 3000
Wire Wire Line
	14300 3800 14300 2900
Wire Wire Line
	14300 2900 14250 2900
Wire Wire Line
	14350 3350 14350 2800
Wire Wire Line
	14350 2800 14250 2800
Wire Wire Line
	14400 2900 14400 2700
Wire Wire Line
	14400 2700 14250 2700
Wire Wire Line
	14250 1100 14250 2300
Wire Wire Line
	14300 1550 14300 2400
Wire Wire Line
	14300 2400 14250 2400
Wire Wire Line
	14250 2500 14350 2500
Wire Wire Line
	14400 2450 14400 2600
Wire Wire Line
	14400 2600 14250 2600
Wire Wire Line
	14800 1100 14250 1100
Connection ~ 14800 1100
Wire Wire Line
	14300 1550 14800 1550
Connection ~ 14800 1550
Wire Wire Line
	14350 2500 14350 2000
Wire Wire Line
	14800 2000 14350 2000
Connection ~ 14800 2000
Wire Wire Line
	14400 2450 14800 2450
Connection ~ 14800 2450
Wire Wire Line
	14800 2900 14400 2900
Connection ~ 14800 2900
Wire Wire Line
	14350 3350 14800 3350
Connection ~ 14800 3350
Wire Wire Line
	14800 3800 14300 3800
Connection ~ 14800 3800
Wire Wire Line
	14250 4250 14800 4250
Connection ~ 14800 4250
Wire Wire Line
	5100 6650 5100 6550
Wire Wire Line
	5100 6550 5150 6550
$Comp
L mixer.pcb-rescue:R-Device R37
U 1 1 60F4E7F0
P 5250 6350
F 0 "R37" H 5180 6304 50  0001 C CNN
F 1 "100k" V 5180 6350 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5180 6350 50  0001 C CNN
F 3 "~" H 5250 6350 50  0001 C CNN
	1    5250 6350
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5100 6350 5100 6250
$Comp
L mixer.pcb-rescue:R-Device R36
U 1 1 60F5C1C8
P 5250 6050
F 0 "R36" H 5180 6004 50  0001 C CNN
F 1 "100k" V 5180 6050 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5180 6050 50  0001 C CNN
F 3 "~" H 5250 6050 50  0001 C CNN
	1    5250 6050
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5100 6050 5100 5950
$Comp
L mixer.pcb-rescue:R-Device R34
U 1 1 60F69A22
P 5250 5450
F 0 "R34" H 5180 5404 50  0001 C CNN
F 1 "100k" V 5180 5450 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5180 5450 50  0001 C CNN
F 3 "~" H 5250 5450 50  0001 C CNN
	1    5250 5450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5100 5450 5100 5350
$Comp
L mixer.pcb-rescue:R-Device R35
U 1 1 60F772A8
P 5250 5750
F 0 "R35" H 5180 5704 50  0001 C CNN
F 1 "100k" V 5180 5750 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5180 5750 50  0001 C CNN
F 3 "~" H 5250 5750 50  0001 C CNN
	1    5250 5750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5100 5750 5100 5650
$Comp
L mixer.pcb-rescue:GND-power #PWR0283
U 1 1 60FED591
P 5400 6350
F 0 "#PWR0283" H 5400 6100 50  0001 C CNN
F 1 "GND" V 5405 6222 50  0000 R CNN
F 2 "" H 5400 6350 50  0001 C CNN
F 3 "" H 5400 6350 50  0001 C CNN
	1    5400 6350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0284
U 1 1 60FFAEDB
P 5400 6050
F 0 "#PWR0284" H 5400 5800 50  0001 C CNN
F 1 "GND" V 5405 5922 50  0000 R CNN
F 2 "" H 5400 6050 50  0001 C CNN
F 3 "" H 5400 6050 50  0001 C CNN
	1    5400 6050
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0285
U 1 1 61008938
P 5400 5750
F 0 "#PWR0285" H 5400 5500 50  0001 C CNN
F 1 "GND" V 5405 5622 50  0000 R CNN
F 2 "" H 5400 5750 50  0001 C CNN
F 3 "" H 5400 5750 50  0001 C CNN
	1    5400 5750
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0286
U 1 1 610162DF
P 5400 5450
F 0 "#PWR0286" H 5400 5200 50  0001 C CNN
F 1 "GND" V 5405 5322 50  0000 R CNN
F 2 "" H 5400 5450 50  0001 C CNN
F 3 "" H 5400 5450 50  0001 C CNN
	1    5400 5450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5100 6550 4900 6550
Wire Wire Line
	4900 6550 4900 6200
Wire Wire Line
	4900 6200 4300 6200
Connection ~ 5100 6550
Wire Wire Line
	4300 6100 4950 6100
Wire Wire Line
	4950 6100 4950 6250
Wire Wire Line
	4950 6250 5100 6250
Connection ~ 5100 6250
Wire Wire Line
	5100 6250 5150 6250
Wire Wire Line
	5150 5950 5100 5950
Wire Wire Line
	4950 5950 4950 6000
Wire Wire Line
	4950 6000 4300 6000
Connection ~ 5100 5950
Wire Wire Line
	5100 5950 4950 5950
Wire Wire Line
	4300 5900 4900 5900
Wire Wire Line
	4900 5900 4900 5650
Wire Wire Line
	4900 5650 5100 5650
Connection ~ 5100 5650
Wire Wire Line
	5100 5650 5150 5650
Wire Wire Line
	5150 5350 5100 5350
Wire Wire Line
	4850 5350 4850 5800
Wire Wire Line
	4850 5800 4300 5800
Connection ~ 5100 5350
Wire Wire Line
	5100 5350 4850 5350
$Comp
L mixer.pcb-rescue:R-Device R19
U 1 1 61241B90
P 1350 7300
F 0 "R19" H 1280 7254 50  0001 C CNN
F 1 "100k" V 1280 7300 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 1280 7300 50  0001 C CNN
F 3 "~" H 1350 7300 50  0001 C CNN
	1    1350 7300
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0295
U 1 1 61241B96
P 1200 7300
F 0 "#PWR0295" H 1200 7050 50  0001 C CNN
F 1 "GND" V 1205 7172 50  0000 R CNN
F 2 "" H 1200 7300 50  0001 C CNN
F 3 "" H 1200 7300 50  0001 C CNN
	1    1200 7300
	0    1    1    0   
$EndComp
Wire Wire Line
	2100 7300 1500 7300
Wire Wire Line
	1500 7400 1500 7300
Connection ~ 1500 7300
$Comp
L mixer.pcb-rescue:R-Device R18
U 1 1 60220BEC
P 1350 7100
F 0 "R18" H 1280 7054 50  0001 C CNN
F 1 "500" V 1280 7100 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 1280 7100 50  0001 C CNN
F 3 "~" H 1350 7100 50  0001 C CNN
	1    1350 7100
	0    1    1    0   
$EndComp
Wire Wire Line
	2100 7200 1500 7200
Wire Wire Line
	1500 7200 1500 7100
Wire Wire Line
	2100 7400 1650 7400
Wire Wire Line
	1650 7400 1650 7600
Wire Wire Line
	1650 7600 1500 7600
Wire Wire Line
	1500 7800 1700 7800
Wire Wire Line
	1700 7500 2100 7500
Wire Wire Line
	1700 7500 1700 7800
$Comp
L mixer.pcb-rescue:R-Device R30
U 1 1 60348613
P 4700 7000
F 0 "R30" H 4630 6954 50  0001 C CNN
F 1 "500" V 4630 7000 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 7000 50  0001 C CNN
F 3 "~" H 4700 7000 50  0001 C CNN
	1    4700 7000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R31
U 1 1 6035EF22
P 4700 7100
F 0 "R31" H 4630 7054 50  0001 C CNN
F 1 "500" V 4630 7100 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 7100 50  0001 C CNN
F 3 "~" H 4700 7100 50  0001 C CNN
	1    4700 7100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R32
U 1 1 6037379A
P 4700 7200
F 0 "R32" H 4630 7154 50  0001 C CNN
F 1 "500" V 4630 7200 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 7200 50  0001 C CNN
F 3 "~" H 4700 7200 50  0001 C CNN
	1    4700 7200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R33
U 1 1 60388323
P 4700 7300
F 0 "R33" H 4630 7254 50  0001 C CNN
F 1 "500" V 4630 7300 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4630 7300 50  0001 C CNN
F 3 "~" H 4700 7300 50  0001 C CNN
	1    4700 7300
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 7000 4300 7000
Wire Wire Line
	4300 7100 4550 7100
Wire Wire Line
	4550 7200 4300 7200
Wire Wire Line
	4300 7300 4550 7300
$Comp
L mixer.pcb-rescue:R-Device R43
U 1 1 604E9EA6
P 5300 8750
F 0 "R43" H 5230 8704 50  0001 C CNN
F 1 "100k" V 5230 8750 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 8750 50  0001 C CNN
F 3 "~" H 5300 8750 50  0001 C CNN
	1    5300 8750
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0296
U 1 1 604E9EAC
P 5450 8750
F 0 "#PWR0296" H 5450 8500 50  0001 C CNN
F 1 "GND" V 5455 8622 50  0000 R CNN
F 2 "" H 5450 8750 50  0001 C CNN
F 3 "" H 5450 8750 50  0001 C CNN
	1    5450 8750
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R42
U 1 1 6051B24B
P 5300 8450
F 0 "R42" H 5230 8404 50  0001 C CNN
F 1 "100k" V 5230 8450 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 8450 50  0001 C CNN
F 3 "~" H 5300 8450 50  0001 C CNN
	1    5300 8450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0297
U 1 1 6051B251
P 5450 8450
F 0 "#PWR0297" H 5450 8200 50  0001 C CNN
F 1 "GND" V 5455 8322 50  0000 R CNN
F 2 "" H 5450 8450 50  0001 C CNN
F 3 "" H 5450 8450 50  0001 C CNN
	1    5450 8450
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R41
U 1 1 605504C3
P 5300 8150
F 0 "R41" H 5230 8104 50  0001 C CNN
F 1 "100k" V 5230 8150 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 8150 50  0001 C CNN
F 3 "~" H 5300 8150 50  0001 C CNN
	1    5300 8150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0298
U 1 1 605504C9
P 5450 8150
F 0 "#PWR0298" H 5450 7900 50  0001 C CNN
F 1 "GND" V 5455 8022 50  0000 R CNN
F 2 "" H 5450 8150 50  0001 C CNN
F 3 "" H 5450 8150 50  0001 C CNN
	1    5450 8150
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R40
U 1 1 6057E057
P 5300 7850
F 0 "R40" H 5230 7804 50  0001 C CNN
F 1 "100k" V 5230 7850 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 7850 50  0001 C CNN
F 3 "~" H 5300 7850 50  0001 C CNN
	1    5300 7850
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0299
U 1 1 6057E05D
P 5450 7850
F 0 "#PWR0299" H 5450 7600 50  0001 C CNN
F 1 "GND" V 5455 7722 50  0000 R CNN
F 2 "" H 5450 7850 50  0001 C CNN
F 3 "" H 5450 7850 50  0001 C CNN
	1    5450 7850
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R39
U 1 1 605AE1F6
P 5300 7550
F 0 "R39" H 5230 7504 50  0001 C CNN
F 1 "100k" V 5230 7550 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 7550 50  0001 C CNN
F 3 "~" H 5300 7550 50  0001 C CNN
	1    5300 7550
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0300
U 1 1 605AE1FC
P 5450 7550
F 0 "#PWR0300" H 5450 7300 50  0001 C CNN
F 1 "GND" V 5455 7422 50  0000 R CNN
F 2 "" H 5450 7550 50  0001 C CNN
F 3 "" H 5450 7550 50  0001 C CNN
	1    5450 7550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5150 7400 4300 7400
Wire Wire Line
	5150 7400 5150 7550
Wire Wire Line
	4300 7500 5100 7500
Wire Wire Line
	5100 7500 5100 7750
Wire Wire Line
	5100 7750 5150 7750
Wire Wire Line
	5150 7750 5150 7850
Wire Wire Line
	5150 8050 5050 8050
Wire Wire Line
	5050 8050 5050 7600
Wire Wire Line
	5050 7600 4300 7600
Wire Wire Line
	4300 7700 5000 7700
Wire Wire Line
	5000 7700 5000 8350
Wire Wire Line
	5000 8350 5150 8350
Wire Wire Line
	5150 8150 5150 8050
Wire Wire Line
	5150 8350 5150 8450
Wire Wire Line
	5150 8750 5150 8650
Wire Wire Line
	5150 8650 4950 8650
Wire Wire Line
	4950 8650 4950 7800
Wire Wire Line
	4950 7800 4300 7800
$Comp
L mixer.pcb-rescue:R-Device R17
U 1 1 60700002
P 1350 6700
F 0 "R17" H 1280 6654 50  0001 C CNN
F 1 "100k" V 1280 6700 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 1280 6700 50  0001 C CNN
F 3 "~" H 1350 6700 50  0001 C CNN
	1    1350 6700
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0301
U 1 1 60700008
P 1200 6700
F 0 "#PWR0301" H 1200 6450 50  0001 C CNN
F 1 "GND" V 1205 6572 50  0000 R CNN
F 2 "" H 1200 6700 50  0001 C CNN
F 3 "" H 1200 6700 50  0001 C CNN
	1    1200 6700
	0    1    1    0   
$EndComp
Wire Wire Line
	2100 6800 1500 6800
Wire Wire Line
	1500 6800 1500 6700
$Comp
L mixer.pcb-rescue:R-Device R21
U 1 1 6078D3A0
P 1350 7900
F 0 "R21" H 1280 7854 50  0001 C CNN
F 1 "100k" V 1280 7900 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 1280 7900 50  0001 C CNN
F 3 "~" H 1350 7900 50  0001 C CNN
	1    1350 7900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0302
U 1 1 6078D3A6
P 1200 7900
F 0 "#PWR0302" H 1200 7650 50  0001 C CNN
F 1 "GND" V 1205 7772 50  0000 R CNN
F 2 "" H 1200 7900 50  0001 C CNN
F 3 "" H 1200 7900 50  0001 C CNN
	1    1200 7900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R20
U 1 1 607FBE7F
P 1350 7600
F 0 "R20" H 1280 7554 50  0001 C CNN
F 1 "100k" V 1280 7600 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 1280 7600 50  0001 C CNN
F 3 "~" H 1350 7600 50  0001 C CNN
	1    1350 7600
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0303
U 1 1 607FBE85
P 1200 7600
F 0 "#PWR0303" H 1200 7350 50  0001 C CNN
F 1 "GND" V 1205 7472 50  0000 R CNN
F 2 "" H 1200 7600 50  0001 C CNN
F 3 "" H 1200 7600 50  0001 C CNN
	1    1200 7600
	0    1    1    0   
$EndComp
Wire Wire Line
	1500 7700 1500 7600
Connection ~ 1500 7600
Wire Wire Line
	1500 7800 1500 7900
Wire Wire Line
	1500 7900 1500 8000
Connection ~ 1500 7900
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0102
U 1 1 602D13B2
P 6950 6400
F 0 "#PWR0102" H 6950 6250 50  0001 C CNN
F 1 "+3.3V" V 6965 6528 50  0000 L CNN
F 2 "" H 6950 6400 50  0001 C CNN
F 3 "" H 6950 6400 50  0001 C CNN
	1    6950 6400
	0    -1   1    0   
$EndComp
$Comp
L mixer.pcb-rescue:CP-Device C2
U 1 1 602D13B8
P 6950 6250
F 0 "C2" H 6832 6204 50  0001 R CNN
F 1 "100 uF" H 6832 6295 50  0000 R CNN
F 2 "Capacitor_THT:CP_Radial_D10.0mm_P2.50mm" H 6988 6100 50  0001 C CNN
F 3 "~" H 6950 6250 50  0001 C CNN
	1    6950 6250
	1    0    0    1   
$EndComp
Wire Wire Line
	7500 6100 7100 6100
Wire Wire Line
	6950 6400 7100 6400
Wire Wire Line
	7100 6400 7100 6100
Connection ~ 6950 6400
Wire Wire Line
	12250 5650 11350 5650
Connection ~ 12250 5650
Wire Wire Line
	12250 5800 12250 5650
Wire Wire Line
	12250 6000 11400 6000
Connection ~ 12250 6000
Wire Wire Line
	12350 6000 12250 6000
Wire Wire Line
	12250 6150 12250 6000
Wire Wire Line
	12250 6350 12350 6350
Connection ~ 12250 6350
Wire Wire Line
	12250 6500 12250 6350
Wire Wire Line
	12250 6700 11500 6700
Connection ~ 12250 6700
Wire Wire Line
	12250 6850 12250 6700
Wire Wire Line
	12250 7050 12350 7050
Connection ~ 12250 7050
Wire Wire Line
	12250 7200 12250 7050
Wire Wire Line
	12250 7400 11450 7400
Connection ~ 12250 7400
Wire Wire Line
	12250 7550 12250 7400
Wire Wire Line
	12250 7750 12350 7750
Connection ~ 12250 7750
Wire Wire Line
	12250 7900 12250 7750
Wire Wire Line
	12250 8100 11350 8100
Connection ~ 12250 8100
Wire Wire Line
	12250 8250 12250 8100
$Comp
L mixer.pcb-rescue:GND-power #PWR0294
U 1 1 611A12EB
P 11950 5800
F 0 "#PWR0294" H 11950 5550 50  0001 C CNN
F 1 "GND" V 11955 5672 50  0000 R CNN
F 2 "" H 11950 5800 50  0001 C CNN
F 3 "" H 11950 5800 50  0001 C CNN
	1    11950 5800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R8
U 1 1 611A12E5
P 12100 5800
F 0 "R8" H 12030 5754 50  0001 C CNN
F 1 "100k" V 12030 5800 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 5800 50  0001 C CNN
F 3 "~" H 12100 5800 50  0001 C CNN
	1    12100 5800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0293
U 1 1 61190C33
P 11950 6150
F 0 "#PWR0293" H 11950 5900 50  0001 C CNN
F 1 "GND" V 11955 6022 50  0000 R CNN
F 2 "" H 11950 6150 50  0001 C CNN
F 3 "" H 11950 6150 50  0001 C CNN
	1    11950 6150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R7
U 1 1 61190C2D
P 12100 6150
F 0 "R7" H 12030 6104 50  0001 C CNN
F 1 "100k" V 12030 6150 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 6150 50  0001 C CNN
F 3 "~" H 12100 6150 50  0001 C CNN
	1    12100 6150
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0292
U 1 1 611805C3
P 11950 6500
F 0 "#PWR0292" H 11950 6250 50  0001 C CNN
F 1 "GND" V 11955 6372 50  0000 R CNN
F 2 "" H 11950 6500 50  0001 C CNN
F 3 "" H 11950 6500 50  0001 C CNN
	1    11950 6500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R6
U 1 1 611805BD
P 12100 6500
F 0 "R6" H 12030 6454 50  0001 C CNN
F 1 "100k" V 12030 6500 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 6500 50  0001 C CNN
F 3 "~" H 12100 6500 50  0001 C CNN
	1    12100 6500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0291
U 1 1 6117007D
P 11950 6850
F 0 "#PWR0291" H 11950 6600 50  0001 C CNN
F 1 "GND" V 11955 6722 50  0000 R CNN
F 2 "" H 11950 6850 50  0001 C CNN
F 3 "" H 11950 6850 50  0001 C CNN
	1    11950 6850
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R5
U 1 1 61170077
P 12100 6850
F 0 "R5" H 12030 6804 50  0001 C CNN
F 1 "100k" V 12030 6850 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 6850 50  0001 C CNN
F 3 "~" H 12100 6850 50  0001 C CNN
	1    12100 6850
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0290
U 1 1 6115F491
P 11950 7200
F 0 "#PWR0290" H 11950 6950 50  0001 C CNN
F 1 "GND" V 11955 7072 50  0000 R CNN
F 2 "" H 11950 7200 50  0001 C CNN
F 3 "" H 11950 7200 50  0001 C CNN
	1    11950 7200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R4
U 1 1 6115F48B
P 12100 7200
F 0 "R4" H 12030 7154 50  0001 C CNN
F 1 "100k" V 12030 7200 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 7200 50  0001 C CNN
F 3 "~" H 12100 7200 50  0001 C CNN
	1    12100 7200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0289
U 1 1 6114F0D1
P 11950 7550
F 0 "#PWR0289" H 11950 7300 50  0001 C CNN
F 1 "GND" V 11955 7422 50  0000 R CNN
F 2 "" H 11950 7550 50  0001 C CNN
F 3 "" H 11950 7550 50  0001 C CNN
	1    11950 7550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R3
U 1 1 6114F0CB
P 12100 7550
F 0 "R3" H 12030 7504 50  0001 C CNN
F 1 "100k" V 12030 7550 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 7550 50  0001 C CNN
F 3 "~" H 12100 7550 50  0001 C CNN
	1    12100 7550
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0288
U 1 1 6113EBBD
P 11950 7900
F 0 "#PWR0288" H 11950 7650 50  0001 C CNN
F 1 "GND" V 11955 7772 50  0000 R CNN
F 2 "" H 11950 7900 50  0001 C CNN
F 3 "" H 11950 7900 50  0001 C CNN
	1    11950 7900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R2
U 1 1 6113EBB7
P 12100 7900
F 0 "R2" H 12030 7854 50  0001 C CNN
F 1 "100k" V 12030 7900 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 7900 50  0001 C CNN
F 3 "~" H 12100 7900 50  0001 C CNN
	1    12100 7900
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0287
U 1 1 61105EB7
P 11950 8250
F 0 "#PWR0287" H 11950 8000 50  0001 C CNN
F 1 "GND" V 11955 8122 50  0000 R CNN
F 2 "" H 11950 8250 50  0001 C CNN
F 3 "" H 11950 8250 50  0001 C CNN
	1    11950 8250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:R-Device R1
U 1 1 61105EB1
P 12100 8250
F 0 "R1" H 12030 8204 50  0001 C CNN
F 1 "100k" V 12030 8250 50  0000 C BNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12030 8250 50  0001 C CNN
F 3 "~" H 12100 8250 50  0001 C CNN
	1    12100 8250
	0    1    1    0   
$EndComp
Wire Wire Line
	12350 8100 12250 8100
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0226
U 1 1 6102C236
P 12350 8000
F 0 "#PWR0226" H 12350 7850 50  0001 C CNN
F 1 "+3.3V" V 12365 8128 50  0000 L CNN
F 2 "" H 12350 8000 50  0001 C CNN
F 3 "" H 12350 8000 50  0001 C CNN
	1    12350 8000
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx1_btn1
U 1 1 60FE8961
P 12550 8000
F 0 "fx1_btn1" H 12468 7675 50  0001 C CNN
F 1 "Conn_01x02" H 12468 7766 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 8000 50  0001 C CNN
F 3 "~" H 12550 8000 50  0001 C CNN
F 4 "fx1_btn1  " H 12550 8000 50  0000 L CNN "Field4"
	1    12550 8000
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:74HC4051-74xx FX-BTNs1
U 1 1 60FAE06B
P 10950 6850
F 0 "FX-BTNs1" H 11000 7531 50  0000 C CNN
F 1 "74HC4051" H 11000 7440 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 10950 6450 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc4051.pdf" H 10950 6450 50  0001 C CNN
	1    10950 6850
	1    0    0    1   
$EndComp
Wire Wire Line
	10650 6250 10950 6250
Wire Wire Line
	10950 6250 11050 6250
Connection ~ 10950 6250
$Comp
L mixer.pcb-rescue:GND-power #PWR0224
U 1 1 60FAE078
P 10950 6250
F 0 "#PWR0224" H 10950 6000 50  0001 C CNN
F 1 "GND" H 10955 6077 50  0000 C CNN
F 2 "" H 10950 6250 50  0001 C CNN
F 3 "" H 10950 6250 50  0001 C CNN
	1    10950 6250
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0225
U 1 1 60FAE07E
P 10950 7350
F 0 "#PWR0225" H 10950 7200 50  0001 C CNN
F 1 "+3.3V" V 10965 7478 50  0000 L CNN
F 2 "" H 10950 7350 50  0001 C CNN
F 3 "" H 10950 7350 50  0001 C CNN
	1    10950 7350
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx1_btn2
U 1 1 60FEA01E
P 12550 7650
F 0 "fx1_btn2" H 12468 7325 50  0001 C CNN
F 1 "Conn_01x02" H 12468 7416 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 7650 50  0001 C CNN
F 3 "~" H 12550 7650 50  0001 C CNN
F 4 "fx1_btn2  " H 12550 7650 50  0000 L CNN "Field4"
	1    12550 7650
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx1_btn3
U 1 1 60FFC332
P 12550 7300
F 0 "fx1_btn3" H 12468 6975 50  0001 C CNN
F 1 "Conn_01x02" H 12468 7066 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 7300 50  0001 C CNN
F 3 "~" H 12550 7300 50  0001 C CNN
F 4 "fx1_btn3  " H 12550 7300 50  0000 L CNN "Field4"
	1    12550 7300
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx1_btn4
U 1 1 60FFC338
P 12550 6950
F 0 "fx1_btn4" H 12468 6625 50  0001 C CNN
F 1 "Conn_01x02" H 12468 6716 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 6950 50  0001 C CNN
F 3 "~" H 12550 6950 50  0001 C CNN
F 4 "fx1_btn4  " H 12550 6950 50  0000 L CNN "Field4"
	1    12550 6950
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx2_btn1
U 1 1 61006035
P 12550 6600
F 0 "fx2_btn1" H 12468 6275 50  0001 C CNN
F 1 "Conn_01x02" H 12468 6366 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 6600 50  0001 C CNN
F 3 "~" H 12550 6600 50  0001 C CNN
F 4 "fx2_btn1  " H 12550 6600 50  0000 L CNN "Field4"
	1    12550 6600
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx2_btn2
U 1 1 6100603B
P 12550 6250
F 0 "fx2_btn2" H 12468 5925 50  0001 C CNN
F 1 "Conn_01x02" H 12468 6016 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 6250 50  0001 C CNN
F 3 "~" H 12550 6250 50  0001 C CNN
F 4 "fx2_btn2  " H 12550 6250 50  0000 L CNN "Field4"
	1    12550 6250
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx2_btn3
U 1 1 61006041
P 12550 5900
F 0 "fx2_btn3" H 12468 5575 50  0001 C CNN
F 1 "Conn_01x02" H 12468 5666 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 5900 50  0001 C CNN
F 3 "~" H 12550 5900 50  0001 C CNN
F 4 "fx2_btn3  " H 12550 5900 50  0000 L CNN "Field4"
	1    12550 5900
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic fx2_btn4
U 1 1 61006047
P 12550 5550
F 0 "fx2_btn4" H 12468 5225 50  0001 C CNN
F 1 "Conn_01x02" H 12468 5316 50  0001 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 12550 5550 50  0001 C CNN
F 3 "~" H 12550 5550 50  0001 C CNN
F 4 "fx2_btn4  " H 12550 5550 50  0000 L CNN "Field4"
	1    12550 5550
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0227
U 1 1 6102D7B5
P 12350 7650
F 0 "#PWR0227" H 12350 7500 50  0001 C CNN
F 1 "+3.3V" V 12365 7778 50  0000 L CNN
F 2 "" H 12350 7650 50  0001 C CNN
F 3 "" H 12350 7650 50  0001 C CNN
	1    12350 7650
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0228
U 1 1 6103529A
P 12350 7300
F 0 "#PWR0228" H 12350 7150 50  0001 C CNN
F 1 "+3.3V" V 12365 7428 50  0000 L CNN
F 2 "" H 12350 7300 50  0001 C CNN
F 3 "" H 12350 7300 50  0001 C CNN
	1    12350 7300
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0229
U 1 1 6103CDC9
P 12350 6950
F 0 "#PWR0229" H 12350 6800 50  0001 C CNN
F 1 "+3.3V" V 12365 7078 50  0000 L CNN
F 2 "" H 12350 6950 50  0001 C CNN
F 3 "" H 12350 6950 50  0001 C CNN
	1    12350 6950
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0230
U 1 1 610448DC
P 12350 6600
F 0 "#PWR0230" H 12350 6450 50  0001 C CNN
F 1 "+3.3V" V 12365 6728 50  0000 L CNN
F 2 "" H 12350 6600 50  0001 C CNN
F 3 "" H 12350 6600 50  0001 C CNN
	1    12350 6600
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0231
U 1 1 6104C462
P 12350 6250
F 0 "#PWR0231" H 12350 6100 50  0001 C CNN
F 1 "+3.3V" V 12365 6378 50  0000 L CNN
F 2 "" H 12350 6250 50  0001 C CNN
F 3 "" H 12350 6250 50  0001 C CNN
	1    12350 6250
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0232
U 1 1 61053FBA
P 12350 5900
F 0 "#PWR0232" H 12350 5750 50  0001 C CNN
F 1 "+3.3V" V 12365 6028 50  0000 L CNN
F 2 "" H 12350 5900 50  0001 C CNN
F 3 "" H 12350 5900 50  0001 C CNN
	1    12350 5900
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0233
U 1 1 6105BB87
P 12350 5550
F 0 "#PWR0233" H 12350 5400 50  0001 C CNN
F 1 "+3.3V" V 12365 5678 50  0000 L CNN
F 2 "" H 12350 5550 50  0001 C CNN
F 3 "" H 12350 5550 50  0001 C CNN
	1    12350 5550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	11350 8100 11350 7150
Wire Wire Line
	11350 7050 11400 7050
Wire Wire Line
	11400 7050 11400 7750
Wire Wire Line
	11400 7750 12250 7750
Wire Wire Line
	12350 7400 12250 7400
Wire Wire Line
	11450 7400 11450 6950
Wire Wire Line
	11450 6950 11350 6950
Wire Wire Line
	11350 6850 11500 6850
Wire Wire Line
	11500 6850 11500 7050
Wire Wire Line
	11500 7050 12250 7050
Wire Wire Line
	12350 6700 12250 6700
Wire Wire Line
	11500 6700 11500 6750
Wire Wire Line
	11500 6750 11350 6750
Wire Wire Line
	11350 6650 11450 6650
Wire Wire Line
	11450 6650 11450 6350
Wire Wire Line
	11450 6350 12250 6350
Wire Wire Line
	11350 6550 11400 6550
Wire Wire Line
	11400 6550 11400 6000
Wire Wire Line
	12350 5650 12250 5650
Wire Wire Line
	11350 5650 11350 6450
$Comp
L mixer.pcb-rescue:GND-power #PWR0114
U 1 1 60372733
P 6950 5300
F 0 "#PWR0114" H 6950 5050 50  0001 C CNN
F 1 "GND" V 6955 5172 50  0000 R CNN
F 2 "" H 6950 5300 50  0001 C CNN
F 3 "" H 6950 5300 50  0001 C CNN
	1    6950 5300
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0140
U 1 1 6038B798
P 6950 6100
F 0 "#PWR0140" H 6950 5850 50  0001 C CNN
F 1 "GND" V 6955 5972 50  0000 R CNN
F 2 "" H 6950 6100 50  0001 C CNN
F 3 "" H 6950 6100 50  0001 C CNN
	1    6950 6100
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0106
U 1 1 5FFE3AE3
P 4600 5250
F 0 "#PWR0106" H 4600 5100 50  0001 C CNN
F 1 "+3.3V" V 4615 5378 50  0000 L CNN
F 2 "" H 4600 5250 50  0001 C CNN
F 3 "" H 4600 5250 50  0001 C CNN
	1    4600 5250
	0    1    1    0   
$EndComp
Wire Wire Line
	4600 5700 4300 5700
Connection ~ 4600 5250
Wire Wire Line
	4250 5250 4600 5250
$Comp
L mixer.pcb-rescue:CP-Device C7
U 1 1 604A0324
P 4600 5100
F 0 "C7" H 4482 5054 50  0001 R CNN
F 1 "100 uF" H 4482 5145 50  0000 R CNN
F 2 "Capacitor_THT:CP_Radial_D10.0mm_P2.50mm" H 4638 4950 50  0001 C CNN
F 3 "~" H 4600 5100 50  0001 C CNN
	1    4600 5100
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic 3.3V_In1
U 1 1 6058C73A
P 9200 7100
F 0 "3.3V_In1" H 9280 7092 50  0000 L CNN
F 1 "Conn_01x02" H 9280 7001 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-AM_1x02_P2.50mm_Vertical" H 9200 7100 50  0001 C CNN
F 3 "~" H 9200 7100 50  0001 C CNN
	1    9200 7100
	1    0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0185
U 1 1 605B3432
P 9000 7200
F 0 "#PWR0185" H 9000 6950 50  0001 C CNN
F 1 "GND" V 9005 7072 50  0000 R CNN
F 2 "" H 9000 7200 50  0001 C CNN
F 3 "" H 9000 7200 50  0001 C CNN
	1    9000 7200
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0257
U 1 1 605B3438
P 9000 7100
F 0 "#PWR0257" H 9000 6950 50  0001 C CNN
F 1 "+3.3V" V 9015 7228 50  0000 L CNN
F 2 "" H 9000 7100 50  0001 C CNN
F 3 "" H 9000 7100 50  0001 C CNN
	1    9000 7100
	0    -1   -1   0   
$EndComp
Text Notes 8950 7000 0    50   ~ 0
Zuleitung
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic 3.3V_Test1
U 1 1 6061354A
P 750 6150
F 0 "3.3V_Test1" V 622 6230 50  0001 L CNN
F 1 "Conn_01x02" V 713 6230 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-AM_1x02_P2.50mm_Vertical" H 750 6150 50  0001 C CNN
F 3 "~" H 750 6150 50  0001 C CNN
	1    750  6150
	-1   0    0    1   
$EndComp
Wire Wire Line
	2100 6900 800  6900
Wire Wire Line
	950  6150 950  6350
Wire Wire Line
	950  6350 800  6350
Wire Wire Line
	800  6350 800  6900
$Comp
L mixer.pcb-rescue:Conn_01x02-Connector_Generic 3.3V_Test2
U 1 1 60744D9F
P 4400 5450
F 0 "3.3V_Test2" H 4318 5125 50  0000 C CNN
F 1 "Conn_01x02" H 4318 5216 50  0000 C CNN
F 2 "Connector_JST:JST_XH_B2B-XH-AM_1x02_P2.50mm_Vertical" H 4400 5450 50  0001 C CNN
F 3 "~" H 4400 5450 50  0001 C CNN
	1    4400 5450
	-1   0    0    1   
$EndComp
Wire Wire Line
	4600 5250 4600 5350
Wire Wire Line
	4600 5450 4600 5700
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0159
U 1 1 600CE2E1
P 1250 2100
F 0 "#PWR0159" H 1250 1950 50  0001 C CNN
F 1 "+3.3V" V 1265 2228 50  0000 L CNN
F 2 "" H 1250 2100 50  0001 C CNN
F 3 "" H 1250 2100 50  0001 C CNN
	1    1250 2100
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:C-Device C4
U 1 1 602DF39F
P 1250 1950
F 0 "C4" H 1365 1996 50  0001 L CNN
F 1 "100 nF" H 1365 1905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 1288 1800 50  0001 C CNN
F 3 "~" H 1250 1950 50  0001 C CNN
	1    1250 1950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1600 2100 1250 2100
Connection ~ 1250 2100
$Comp
L mixer.pcb-rescue:GND-power #PWR0304
U 1 1 60448F72
P 1250 1800
F 0 "#PWR0304" H 1250 1550 50  0001 C CNN
F 1 "GND" V 1255 1672 50  0000 R CNN
F 2 "" H 1250 1800 50  0001 C CNN
F 3 "" H 1250 1800 50  0001 C CNN
	1    1250 1800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0305
U 1 1 604937A2
P 4350 2100
F 0 "#PWR0305" H 4350 1950 50  0001 C CNN
F 1 "+3.3V" V 4365 2228 50  0000 L CNN
F 2 "" H 4350 2100 50  0001 C CNN
F 3 "" H 4350 2100 50  0001 C CNN
	1    4350 2100
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:C-Device C6
U 1 1 604937A8
P 4350 1950
F 0 "C6" H 4465 1996 50  0001 L CNN
F 1 "100 nF" H 4465 1905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 4388 1800 50  0001 C CNN
F 3 "~" H 4350 1950 50  0001 C CNN
	1    4350 1950
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0306
U 1 1 604937AE
P 4350 1800
F 0 "#PWR0306" H 4350 1550 50  0001 C CNN
F 1 "GND" V 4355 1672 50  0000 R CNN
F 2 "" H 4350 1800 50  0001 C CNN
F 3 "" H 4350 1800 50  0001 C CNN
	1    4350 1800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0307
U 1 1 604B0B6E
P 7400 2100
F 0 "#PWR0307" H 7400 1950 50  0001 C CNN
F 1 "+3.3V" V 7415 2228 50  0000 L CNN
F 2 "" H 7400 2100 50  0001 C CNN
F 3 "" H 7400 2100 50  0001 C CNN
	1    7400 2100
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:C-Device C8
U 1 1 604B0B74
P 7400 1950
F 0 "C8" H 7515 1996 50  0001 L CNN
F 1 "100 nF" H 7515 1905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 7438 1800 50  0001 C CNN
F 3 "~" H 7400 1950 50  0001 C CNN
	1    7400 1950
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0308
U 1 1 604B0B7A
P 7400 1800
F 0 "#PWR0308" H 7400 1550 50  0001 C CNN
F 1 "GND" V 7405 1672 50  0000 R CNN
F 2 "" H 7400 1800 50  0001 C CNN
F 3 "" H 7400 1800 50  0001 C CNN
	1    7400 1800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0309
U 1 1 604CD853
P 10600 2100
F 0 "#PWR0309" H 10600 1950 50  0001 C CNN
F 1 "+3.3V" V 10615 2228 50  0000 L CNN
F 2 "" H 10600 2100 50  0001 C CNN
F 3 "" H 10600 2100 50  0001 C CNN
	1    10600 2100
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:C-Device C9
U 1 1 604CD859
P 10600 1950
F 0 "C9" H 10715 1996 50  0001 L CNN
F 1 "100 nF" H 10715 1905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 10638 1800 50  0001 C CNN
F 3 "~" H 10600 1950 50  0001 C CNN
	1    10600 1950
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0310
U 1 1 604CD85F
P 10600 1800
F 0 "#PWR0310" H 10600 1550 50  0001 C CNN
F 1 "GND" V 10605 1672 50  0000 R CNN
F 2 "" H 10600 1800 50  0001 C CNN
F 3 "" H 10600 1800 50  0001 C CNN
	1    10600 1800
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0311
U 1 1 604EA920
P 13550 2100
F 0 "#PWR0311" H 13550 1950 50  0001 C CNN
F 1 "+3.3V" V 13565 2228 50  0000 L CNN
F 2 "" H 13550 2100 50  0001 C CNN
F 3 "" H 13550 2100 50  0001 C CNN
	1    13550 2100
	0    -1   -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:C-Device C10
U 1 1 604EA926
P 13550 1950
F 0 "C10" H 13665 1996 50  0001 L CNN
F 1 "100 nF" H 13665 1905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 13588 1800 50  0001 C CNN
F 3 "~" H 13550 1950 50  0001 C CNN
	1    13550 1950
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0312
U 1 1 604EA92C
P 13550 1800
F 0 "#PWR0312" H 13550 1550 50  0001 C CNN
F 1 "GND" V 13555 1672 50  0000 R CNN
F 2 "" H 13550 1800 50  0001 C CNN
F 3 "" H 13550 1800 50  0001 C CNN
	1    13550 1800
	0    1    1    0   
$EndComp
Wire Wire Line
	4650 2100 4350 2100
Connection ~ 4350 2100
Wire Wire Line
	7750 2100 7400 2100
Connection ~ 7400 2100
Wire Wire Line
	10600 2100 10900 2100
Connection ~ 10600 2100
Wire Wire Line
	13550 2100 13850 2100
Connection ~ 13550 2100
$Comp
L mixer.pcb-rescue:C-Device C5
U 1 1 6062CC8D
P 4250 5100
F 0 "C5" H 4365 5146 50  0001 L CNN
F 1 "100 nF" H 4365 5055 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 4288 4950 50  0001 C CNN
F 3 "~" H 4250 5100 50  0001 C CNN
	1    4250 5100
	-1   0    0    -1  
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0313
U 1 1 6062CC93
P 4250 4950
F 0 "#PWR0313" H 4250 4700 50  0001 C CNN
F 1 "GND" V 4255 4822 50  0000 R CNN
F 2 "" H 4250 4950 50  0001 C CNN
F 3 "" H 4250 4950 50  0001 C CNN
	1    4250 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	4600 4950 4250 4950
Connection ~ 4250 4950
$Comp
L mixer.pcb-rescue:C-Device C3
U 1 1 606E23B3
P 1100 6150
F 0 "C3" H 1215 6196 50  0001 L CNN
F 1 "100 nF" H 1215 6105 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 1138 6000 50  0001 C CNN
F 3 "~" H 1100 6150 50  0001 C CNN
	1    1100 6150
	0    1    -1   0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0314
U 1 1 606E23B9
P 1250 6150
F 0 "#PWR0314" H 1250 5900 50  0001 C CNN
F 1 "GND" V 1255 6022 50  0000 R CNN
F 2 "" H 1250 6150 50  0001 C CNN
F 3 "" H 1250 6150 50  0001 C CNN
	1    1250 6150
	-1   0    0    1   
$EndComp
Connection ~ 950  6150
$Comp
L mixer.pcb-rescue:C-Device C11
U 1 1 6040F556
P 10950 7500
F 0 "C11" H 11065 7546 50  0001 L CNN
F 1 "100 nF" H 11065 7455 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 10988 7350 50  0001 C CNN
F 3 "~" H 10950 7500 50  0001 C CNN
	1    10950 7500
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0315
U 1 1 6040F55C
P 10950 7650
F 0 "#PWR0315" H 10950 7400 50  0001 C CNN
F 1 "GND" V 10955 7522 50  0000 R CNN
F 2 "" H 10950 7650 50  0001 C CNN
F 3 "" H 10950 7650 50  0001 C CNN
	1    10950 7650
	0    1    -1   0   
$EndComp
Connection ~ 10950 7350
$Comp
L mixer.pcb-rescue:C-Device C12
U 1 1 60489670
P 14050 7550
F 0 "C12" H 14165 7596 50  0001 L CNN
F 1 "100 nF" H 14165 7505 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 14088 7400 50  0001 C CNN
F 3 "~" H 14050 7550 50  0001 C CNN
	1    14050 7550
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR0316
U 1 1 60489676
P 14050 7700
F 0 "#PWR0316" H 14050 7450 50  0001 C CNN
F 1 "GND" V 14055 7572 50  0000 R CNN
F 2 "" H 14050 7700 50  0001 C CNN
F 3 "" H 14050 7700 50  0001 C CNN
	1    14050 7700
	0    1    -1   0   
$EndComp
Connection ~ 14050 7400
Text GLabel 7500 8650 0    50   Input ~ 0
pfl_led_master
Text GLabel 7500 8400 0    50   Input ~ 0
pfl_led_ch4
Text GLabel 7500 8150 0    50   Input ~ 0
pfl_led_ch3
Text GLabel 7500 7900 0    50   Input ~ 0
pfl_led_ch2
Text GLabel 7500 7650 0    50   Input ~ 0
pfl_led_ch1
$Comp
L mixer.pcb-rescue:GND-power #PWR?
U 1 1 607B78AC
P 7500 7750
F 0 "#PWR?" H 7500 7500 50  0001 C CNN
F 1 "GND" V 7505 7622 50  0000 R CNN
F 2 "" H 7500 7750 50  0001 C CNN
F 3 "" H 7500 7750 50  0001 C CNN
	1    7500 7750
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR?
U 1 1 607D3D52
P 7500 8000
F 0 "#PWR?" H 7500 7750 50  0001 C CNN
F 1 "GND" V 7505 7872 50  0000 R CNN
F 2 "" H 7500 8000 50  0001 C CNN
F 3 "" H 7500 8000 50  0001 C CNN
	1    7500 8000
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR?
U 1 1 607EFF6E
P 7500 8250
F 0 "#PWR?" H 7500 8000 50  0001 C CNN
F 1 "GND" V 7505 8122 50  0000 R CNN
F 2 "" H 7500 8250 50  0001 C CNN
F 3 "" H 7500 8250 50  0001 C CNN
	1    7500 8250
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR?
U 1 1 6080C500
P 7500 8500
F 0 "#PWR?" H 7500 8250 50  0001 C CNN
F 1 "GND" V 7505 8372 50  0000 R CNN
F 2 "" H 7500 8500 50  0001 C CNN
F 3 "" H 7500 8500 50  0001 C CNN
	1    7500 8500
	0    1    1    0   
$EndComp
$Comp
L mixer.pcb-rescue:GND-power #PWR?
U 1 1 60828DA3
P 7500 8750
F 0 "#PWR?" H 7500 8500 50  0001 C CNN
F 1 "GND" V 7505 8622 50  0000 R CNN
F 2 "" H 7500 8750 50  0001 C CNN
F 3 "" H 7500 8750 50  0001 C CNN
	1    7500 8750
	0    1    1    0   
$EndComp
Connection ~ 6950 5600
$Comp
L mixer.pcb-rescue:CP-Device C1
U 1 1 606F6BA4
P 6950 5450
F 0 "C1" H 6832 5404 50  0001 R CNN
F 1 "100 uF        " H 6832 5495 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D10.0mm_P2.50mm" H 6988 5300 50  0001 C CNN
F 3 "~" H 6950 5450 50  0001 C CNN
	1    6950 5450
	-1   0    0    1   
$EndComp
$Comp
L mixer.pcb-rescue:+3.3V-power #PWR0206
U 1 1 60764E8F
P 6950 5600
F 0 "#PWR0206" H 6950 5450 50  0001 C CNN
F 1 "+3.3V" V 6965 5728 50  0000 L CNN
F 2 "" H 6950 5600 50  0001 C CNN
F 3 "" H 6950 5600 50  0001 C CNN
	1    6950 5600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6950 5600 7500 5600
$Comp
L mixer.pcb-rescue:Conn_01x03-Connector_Generic NeoPixel1
U 1 1 607646F2
P 7700 5700
F 0 "NeoPixel1" H 7780 5742 50  0001 L CNN
F 1 "Conn_01x03" H 7780 5651 50  0001 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 7700 5700 50  0001 C CNN
F 3 "~" H 7700 5700 50  0001 C CNN
F 4 "NeoPixel  " H 7700 5700 50  0000 L CNN "Field4"
	1    7700 5700
	1    0    0    -1  
$EndComp
$EndSCHEMATC
