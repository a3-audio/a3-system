#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-Debug.mk)" "nbproject/Makefile-local-Debug.mk"
include nbproject/Makefile-local-Debug.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=Debug
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=
else
COMPARISON_BUILD=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=../src/adc.c ../src/button.c ../src/encoder.c ../src/i2c.c ../src/init.c ../src/ledandcolor.c ../src/timer.c ../main.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/1360937237/adc.o ${OBJECTDIR}/_ext/1360937237/button.o ${OBJECTDIR}/_ext/1360937237/encoder.o ${OBJECTDIR}/_ext/1360937237/i2c.o ${OBJECTDIR}/_ext/1360937237/init.o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ${OBJECTDIR}/_ext/1360937237/timer.o ${OBJECTDIR}/_ext/1472/main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/1360937237/adc.o.d ${OBJECTDIR}/_ext/1360937237/button.o.d ${OBJECTDIR}/_ext/1360937237/encoder.o.d ${OBJECTDIR}/_ext/1360937237/i2c.o.d ${OBJECTDIR}/_ext/1360937237/init.o.d ${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d ${OBJECTDIR}/_ext/1360937237/timer.o.d ${OBJECTDIR}/_ext/1472/main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/1360937237/adc.o ${OBJECTDIR}/_ext/1360937237/button.o ${OBJECTDIR}/_ext/1360937237/encoder.o ${OBJECTDIR}/_ext/1360937237/i2c.o ${OBJECTDIR}/_ext/1360937237/init.o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ${OBJECTDIR}/_ext/1360937237/timer.o ${OBJECTDIR}/_ext/1472/main.o

# Source Files
SOURCEFILES=../src/adc.c ../src/button.c ../src/encoder.c ../src/i2c.c ../src/init.c ../src/ledandcolor.c ../src/timer.c ../main.c

# Pack Options 
PACK_COMPILER_OPTIONS=-I "${DFP_DIR}/include"
PACK_COMMON_OPTIONS=-B "${DFP_DIR}/gcc/dev/attiny1626"



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-Debug.mk ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=ATtiny1626
# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assembleWithPreprocess
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/Debug/a9ef7e39972c660500ddbd2ca7cf98f440f52f78 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT ${OBJECTDIR}/_ext/1360937237/adc.o  -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/button.o: ../src/button.c  .generated_files/flags/Debug/384a7b8934d58b284bc3ca949ce1637ba6cf751 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT ${OBJECTDIR}/_ext/1360937237/button.o  -o ${OBJECTDIR}/_ext/1360937237/button.o ../src/button.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/encoder.o: ../src/encoder.c  .generated_files/flags/Debug/b425003f72d5ca83ed1968b951669c37acec5dc0 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT ${OBJECTDIR}/_ext/1360937237/encoder.o  -o ${OBJECTDIR}/_ext/1360937237/encoder.o ../src/encoder.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/i2c.o: ../src/i2c.c  .generated_files/flags/Debug/70a003fff4e545435ea9ad847c49060bf4a0423a .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT ${OBJECTDIR}/_ext/1360937237/i2c.o  -o ${OBJECTDIR}/_ext/1360937237/i2c.o ../src/i2c.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/Debug/71ae8f8c632662a4003ac5bd5b2cd171a52a7f5f .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT ${OBJECTDIR}/_ext/1360937237/init.o  -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/ledandcolor.o: ../src/ledandcolor.c  .generated_files/flags/Debug/6e2a5365af15a04d4b9336d76007366b213efb31 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/1360937237/ledandcolor.o  -o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ../src/ledandcolor.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/timer.o: ../src/timer.c  .generated_files/flags/Debug/2fc4671646a61f3c3d9f82c6a93cbc93a257d918 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT ${OBJECTDIR}/_ext/1360937237/timer.o  -o ${OBJECTDIR}/_ext/1360937237/timer.o ../src/timer.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  .generated_files/flags/Debug/c1ed01658bccc99613e11b1075b8d21bd0656a40 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1472" 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1472/main.o.d" -MT "${OBJECTDIR}/_ext/1472/main.o.d" -MT ${OBJECTDIR}/_ext/1472/main.o  -o ${OBJECTDIR}/_ext/1472/main.o ../main.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
else
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/Debug/b445f1f9ddba1870aef253f27ad95638d89a9397 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT ${OBJECTDIR}/_ext/1360937237/adc.o  -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/button.o: ../src/button.c  .generated_files/flags/Debug/57a81cf653d2475200bfdca2ef68b81a7c2a5576 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT ${OBJECTDIR}/_ext/1360937237/button.o  -o ${OBJECTDIR}/_ext/1360937237/button.o ../src/button.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/encoder.o: ../src/encoder.c  .generated_files/flags/Debug/91e6a3698fb27989bf81f1ecb570a0e94f93c7da .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT ${OBJECTDIR}/_ext/1360937237/encoder.o  -o ${OBJECTDIR}/_ext/1360937237/encoder.o ../src/encoder.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/i2c.o: ../src/i2c.c  .generated_files/flags/Debug/e517f8d553caaf1346c23300df26e17f2de12bd1 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT ${OBJECTDIR}/_ext/1360937237/i2c.o  -o ${OBJECTDIR}/_ext/1360937237/i2c.o ../src/i2c.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/Debug/cd23629d97ffd8773a85beab92f5cbb8e9ad63d5 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT ${OBJECTDIR}/_ext/1360937237/init.o  -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/ledandcolor.o: ../src/ledandcolor.c  .generated_files/flags/Debug/64d9adb50e12ca9636d2f76837cea47342edc14 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/1360937237/ledandcolor.o  -o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ../src/ledandcolor.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1360937237/timer.o: ../src/timer.c  .generated_files/flags/Debug/533a3b566bbd1f4d3ccfd2b8d6c9b9291b42e6ec .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT ${OBJECTDIR}/_ext/1360937237/timer.o  -o ${OBJECTDIR}/_ext/1360937237/timer.o ../src/timer.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  .generated_files/flags/Debug/ff5d1a7f5ac5457ce7b20d0f2423781b4d0a946 .generated_files/flags/Debug/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1472" 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O0 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1472/main.o.d" -MT "${OBJECTDIR}/_ext/1472/main.o.d" -MT ${OBJECTDIR}/_ext/1472/main.o  -o ${OBJECTDIR}/_ext/1472/main.o ../main.c  -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -g2
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"   -gdwarf-2 -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__ICD2RAM=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1 -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
	
	${MP_CC_DIR}\\avr-objcopy -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.eep" || exit 0
	${MP_CC_DIR}\\avr-objdump -h -S "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" > "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.lss"
	${MP_CC_DIR}\\avr-objcopy -O srec -R .eeprom -R .fuse -R .lock -R .signature "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.srec"
	
	
else
${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Debug=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION) -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
	${MP_CC_DIR}\\avr-objcopy -O ihex "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.hex"
	${MP_CC_DIR}\\avr-objcopy -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.eep" || exit 0
	${MP_CC_DIR}\\avr-objdump -h -S "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" > "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.lss"
	${MP_CC_DIR}\\avr-objcopy -O srec -R .eeprom -R .fuse -R .lock -R .signature "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.srec"
	
	
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${OBJECTDIR}
	${RM} -r ${DISTDIR}

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
