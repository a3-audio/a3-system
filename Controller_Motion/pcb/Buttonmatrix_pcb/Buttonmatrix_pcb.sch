EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
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
$Comp
L 4xxx:4051 U1
U 1 1 5F9B3CE8
P 3250 2750
F 0 "U1" H 3794 2796 50  0000 L CNN
F 1 "4051" H 3794 2705 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 3250 2750 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4051bms-52bms-53bms.pdf" H 3250 2750 50  0001 C CNN
	1    3250 2750
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW1
U 1 1 5F9B48FC
P 1300 1100
F 0 "SW1" H 1300 1385 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 1294 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 1300 50  0001 C CNN
F 3 "~" H 1300 1300 50  0001 C CNN
	1    1300 1100
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW2
U 1 1 5F9B6E51
P 1300 1550
F 0 "SW2" H 1300 1835 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 1744 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 1750 50  0001 C CNN
F 3 "~" H 1300 1750 50  0001 C CNN
	1    1300 1550
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW3
U 1 1 5F9B9023
P 1300 2000
F 0 "SW3" H 1300 2285 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 2194 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 2200 50  0001 C CNN
F 3 "~" H 1300 2200 50  0001 C CNN
	1    1300 2000
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW4
U 1 1 5F9B9029
P 1300 2450
F 0 "SW4" H 1300 2735 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 2644 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 2650 50  0001 C CNN
F 3 "~" H 1300 2650 50  0001 C CNN
	1    1300 2450
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW5
U 1 1 5F9BFB09
P 1300 2900
F 0 "SW5" H 1300 3185 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 3094 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 3100 50  0001 C CNN
F 3 "~" H 1300 3100 50  0001 C CNN
	1    1300 2900
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW6
U 1 1 5F9BFB0F
P 1300 3350
F 0 "SW6" H 1300 3635 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 3544 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 3550 50  0001 C CNN
F 3 "~" H 1300 3550 50  0001 C CNN
	1    1300 3350
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW7
U 1 1 5F9BFB15
P 1300 3800
F 0 "SW7" H 1300 4085 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 3994 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 4000 50  0001 C CNN
F 3 "~" H 1300 4000 50  0001 C CNN
	1    1300 3800
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_Dual SW8
U 1 1 5F9BFB1B
P 1300 4250
F 0 "SW8" H 1300 4535 50  0000 C CNN
F 1 "SW_Push_Dual" H 1300 4444 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 1300 4450 50  0001 C CNN
F 3 "~" H 1300 4450 50  0001 C CNN
	1    1300 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	1100 1100 1500 1100
Wire Wire Line
	2750 1100 2750 2150
Connection ~ 1500 1100
Wire Wire Line
	1500 1100 2750 1100
Wire Wire Line
	2750 2250 2700 2250
Wire Wire Line
	2700 2250 2700 1550
Wire Wire Line
	2700 1550 1500 1550
Connection ~ 1500 1550
Wire Wire Line
	1500 1550 1100 1550
Wire Wire Line
	1100 2000 1500 2000
Wire Wire Line
	2650 2000 2650 2350
Wire Wire Line
	2650 2350 2750 2350
Connection ~ 1500 2000
Wire Wire Line
	1500 2000 2650 2000
Wire Wire Line
	2750 2450 1500 2450
Connection ~ 1500 2450
Wire Wire Line
	1500 2450 1100 2450
Wire Wire Line
	1100 2900 1500 2900
Wire Wire Line
	1600 2900 1600 2550
Wire Wire Line
	1600 2550 2750 2550
Connection ~ 1500 2900
Wire Wire Line
	1500 2900 1600 2900
Wire Wire Line
	1100 3350 1500 3350
Wire Wire Line
	1650 3350 1650 2650
Wire Wire Line
	1650 2650 2750 2650
Connection ~ 1500 3350
Wire Wire Line
	1500 3350 1650 3350
Wire Wire Line
	1100 3800 1500 3800
Wire Wire Line
	1700 3800 1700 2750
Wire Wire Line
	1700 2750 2750 2750
Connection ~ 1500 3800
Wire Wire Line
	1500 3800 1700 3800
Wire Wire Line
	1100 4250 1500 4250
Wire Wire Line
	1750 4250 1750 2850
Wire Wire Line
	1750 2850 2750 2850
Connection ~ 1500 4250
Wire Wire Line
	1500 4250 1750 4250
Wire Wire Line
	3350 3650 3250 3650
Wire Wire Line
	3250 3650 3250 4550
Wire Wire Line
	3250 4550 1050 4550
Wire Wire Line
	1050 1300 1100 1300
Connection ~ 3250 3650
Connection ~ 1100 1300
Wire Wire Line
	1100 1300 1500 1300
Wire Wire Line
	1500 1750 1100 1750
Connection ~ 1050 1750
Wire Wire Line
	1050 1750 1050 1300
Connection ~ 1100 1750
Wire Wire Line
	1100 1750 1050 1750
Wire Wire Line
	1050 2200 1100 2200
Connection ~ 1050 2200
Wire Wire Line
	1050 2200 1050 1750
Connection ~ 1100 2200
Wire Wire Line
	1100 2200 1500 2200
Wire Wire Line
	1500 2650 1100 2650
Wire Wire Line
	1050 2200 1050 2650
Connection ~ 1050 2650
Wire Wire Line
	1050 2650 1050 3100
Connection ~ 1100 2650
Wire Wire Line
	1100 2650 1050 2650
Wire Wire Line
	1500 3100 1100 3100
Connection ~ 1050 3100
Wire Wire Line
	1050 3100 1050 3550
Connection ~ 1100 3100
Wire Wire Line
	1100 3100 1050 3100
Wire Wire Line
	1500 3550 1100 3550
Connection ~ 1050 3550
Wire Wire Line
	1050 3550 1050 4000
Connection ~ 1100 3550
Wire Wire Line
	1100 3550 1050 3550
Wire Wire Line
	1500 4000 1100 4000
Connection ~ 1050 4000
Wire Wire Line
	1050 4000 1050 4450
Connection ~ 1100 4000
Wire Wire Line
	1100 4000 1050 4000
Wire Wire Line
	1050 4450 1100 4450
Connection ~ 1050 4450
Wire Wire Line
	1050 4450 1050 4550
Connection ~ 1100 4450
Wire Wire Line
	1100 4450 1500 4450
$Comp
L Connector:Conn_01x08_Male J1
U 1 1 5F9F4AF4
P 4600 1400
F 0 "J1" V 4435 1328 50  0000 C CNN
F 1 "Conn_01x08_Male" V 4526 1328 50  0000 C CNN
F 2 "Connector_IDC:IDC-Header_2x04_P2.54mm_Vertical" H 4600 1400 50  0001 C CNN
F 3 "~" H 4600 1400 50  0001 C CNN
	1    4600 1400
	0    1    1    0   
$EndComp
Wire Wire Line
	3250 1850 4200 1850
Wire Wire Line
	4200 1850 4200 1600
Wire Wire Line
	3350 3650 4300 3650
Connection ~ 3350 3650
Wire Wire Line
	3750 2150 4400 2150
Wire Wire Line
	4400 2150 4400 1600
Wire Wire Line
	2750 3350 2750 3700
Wire Wire Line
	2750 3700 4700 3700
Wire Wire Line
	4700 3700 4700 2000
Wire Wire Line
	2750 3250 2700 3250
Wire Wire Line
	2700 3250 2700 3750
Wire Wire Line
	2700 3750 4800 3750
Wire Wire Line
	4800 3750 4800 1950
Wire Wire Line
	2750 3150 2650 3150
Wire Wire Line
	2650 3150 2650 3800
Wire Wire Line
	2650 3800 4900 3800
Wire Wire Line
	4900 3800 4900 1900
$Comp
L 4xxx:4051 U2
U 1 1 5FA1C7AE
P 6800 2950
F 0 "U2" H 7344 2996 50  0000 L CNN
F 1 "4051" H 7344 2905 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 6800 2950 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4051bms-52bms-53bms.pdf" H 6800 2950 50  0001 C CNN
	1    6800 2950
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW16
U 1 1 5FA1C7B4
P 8750 4600
F 0 "SW16" H 8750 4885 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 4794 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 4800 50  0001 C CNN
F 3 "~" H 8750 4800 50  0001 C CNN
	1    8750 4600
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW15
U 1 1 5FA1C7BA
P 8750 4150
F 0 "SW15" H 8750 4435 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 4344 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 4350 50  0001 C CNN
F 3 "~" H 8750 4350 50  0001 C CNN
	1    8750 4150
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW14
U 1 1 5FA1C7C0
P 8750 3700
F 0 "SW14" H 8750 3985 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 3894 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 3900 50  0001 C CNN
F 3 "~" H 8750 3900 50  0001 C CNN
	1    8750 3700
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW13
U 1 1 5FA1C7C6
P 8750 3250
F 0 "SW13" H 8750 3535 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 3444 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 3450 50  0001 C CNN
F 3 "~" H 8750 3450 50  0001 C CNN
	1    8750 3250
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW12
U 1 1 5FA1C7CC
P 8750 2800
F 0 "SW12" H 8750 3085 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 2994 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 3000 50  0001 C CNN
F 3 "~" H 8750 3000 50  0001 C CNN
	1    8750 2800
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW11
U 1 1 5FA1C7D2
P 8750 2350
F 0 "SW11" H 8750 2635 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 2544 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 2550 50  0001 C CNN
F 3 "~" H 8750 2550 50  0001 C CNN
	1    8750 2350
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW10
U 1 1 5FA1C7D8
P 8750 1900
F 0 "SW10" H 8750 2185 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 2094 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 2100 50  0001 C CNN
F 3 "~" H 8750 2100 50  0001 C CNN
	1    8750 1900
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push_Dual SW9
U 1 1 5FA1C7DE
P 8750 1450
F 0 "SW9" H 8750 1735 50  0000 C CNN
F 1 "SW_Push_Dual" H 8750 1644 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH-12mm" H 8750 1650 50  0001 C CNN
F 3 "~" H 8750 1650 50  0001 C CNN
	1    8750 1450
	-1   0    0    1   
$EndComp
Wire Wire Line
	8950 4600 8550 4600
Wire Wire Line
	7300 4600 7300 3550
Connection ~ 8550 4600
Wire Wire Line
	8550 4600 7300 4600
Wire Wire Line
	7300 3450 7350 3450
Wire Wire Line
	7350 3450 7350 4150
Wire Wire Line
	7350 4150 8550 4150
Connection ~ 8550 4150
Wire Wire Line
	8550 4150 8950 4150
Wire Wire Line
	8950 3700 8550 3700
Wire Wire Line
	7400 3700 7400 3350
Wire Wire Line
	7400 3350 7300 3350
Connection ~ 8550 3700
Wire Wire Line
	8550 3700 7400 3700
Wire Wire Line
	7300 3250 8550 3250
Connection ~ 8550 3250
Wire Wire Line
	8550 3250 8950 3250
Wire Wire Line
	8950 2800 8550 2800
Wire Wire Line
	8450 2800 8450 3150
Wire Wire Line
	8450 3150 7300 3150
Connection ~ 8550 2800
Wire Wire Line
	8550 2800 8450 2800
Wire Wire Line
	8950 2350 8550 2350
Wire Wire Line
	8400 2350 8400 3050
Wire Wire Line
	8400 3050 7300 3050
Connection ~ 8550 2350
Wire Wire Line
	8550 2350 8400 2350
Wire Wire Line
	8950 1900 8550 1900
Wire Wire Line
	8350 1900 8350 2950
Wire Wire Line
	8350 2950 7300 2950
Connection ~ 8550 1900
Wire Wire Line
	8550 1900 8350 1900
Wire Wire Line
	8950 1450 8550 1450
Wire Wire Line
	8300 1450 8300 2850
Wire Wire Line
	8300 2850 7300 2850
Connection ~ 8550 1450
Wire Wire Line
	8550 1450 8300 1450
Wire Wire Line
	6700 2050 6800 2050
Wire Wire Line
	6800 2050 6800 1150
Wire Wire Line
	6800 1150 9000 1150
Wire Wire Line
	9000 4400 8950 4400
Connection ~ 6800 2050
Connection ~ 8950 4400
Wire Wire Line
	8950 4400 8550 4400
Wire Wire Line
	8550 3950 8950 3950
Connection ~ 9000 3950
Wire Wire Line
	9000 3950 9000 4400
Connection ~ 8950 3950
Wire Wire Line
	8950 3950 9000 3950
Wire Wire Line
	9000 3500 8950 3500
Connection ~ 9000 3500
Wire Wire Line
	9000 3500 9000 3950
Connection ~ 8950 3500
Wire Wire Line
	8950 3500 8550 3500
Wire Wire Line
	8550 3050 8950 3050
Wire Wire Line
	9000 3500 9000 3050
Connection ~ 9000 3050
Wire Wire Line
	9000 3050 9000 2600
Connection ~ 8950 3050
Wire Wire Line
	8950 3050 9000 3050
Wire Wire Line
	8550 2600 8950 2600
Connection ~ 9000 2600
Wire Wire Line
	9000 2600 9000 2150
Connection ~ 8950 2600
Wire Wire Line
	8950 2600 9000 2600
Wire Wire Line
	8550 2150 8950 2150
Connection ~ 9000 2150
Wire Wire Line
	9000 2150 9000 1700
Connection ~ 8950 2150
Wire Wire Line
	8950 2150 9000 2150
Wire Wire Line
	8550 1700 8950 1700
Connection ~ 9000 1700
Wire Wire Line
	9000 1700 9000 1250
Connection ~ 8950 1700
Wire Wire Line
	8950 1700 9000 1700
Wire Wire Line
	9000 1250 8950 1250
Connection ~ 9000 1250
Wire Wire Line
	9000 1250 9000 1150
Connection ~ 8950 1250
Wire Wire Line
	8950 1250 8550 1250
Connection ~ 6700 2050
Wire Wire Line
	7300 2350 7300 2000
Wire Wire Line
	7300 2450 7350 2450
Wire Wire Line
	7350 2450 7350 1950
Wire Wire Line
	7300 2550 7400 2550
Wire Wire Line
	7400 2550 7400 1900
Wire Wire Line
	4200 3850 4200 1850
Wire Wire Line
	4200 3850 6800 3850
Connection ~ 4200 1850
Wire Wire Line
	4700 2000 7300 2000
Connection ~ 4700 2000
Wire Wire Line
	4700 2000 4700 1600
Wire Wire Line
	4800 1950 7350 1950
Connection ~ 4800 1950
Wire Wire Line
	4800 1950 4800 1600
Wire Wire Line
	4900 1900 7400 1900
Connection ~ 4900 1900
Wire Wire Line
	4900 1900 4900 1600
Wire Wire Line
	4300 1600 4300 2050
Wire Wire Line
	4300 2050 6700 2050
Connection ~ 4300 2050
Wire Wire Line
	4300 2050 4300 3650
Wire Wire Line
	4500 3550 4500 1600
Wire Wire Line
	4500 3550 6300 3550
$EndSCHEMATC
