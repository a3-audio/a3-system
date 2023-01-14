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
ifeq "$(wildcard nbproject/Makefile-local-Release.mk)" "nbproject/Makefile-local-Release.mk"
include nbproject/Makefile-local-Release.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=Release
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

# The following macros may be used in the pre and post step lines
_/_=\\
ShExtension=.bat
Device=ATtiny1626
ProjectDir="C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyFullTest\attinyFullTest\attinyFullTest.X"
ProjectName=attinyFullTest
ConfName=Release
ImagePath="dist\Release\${IMAGE_TYPE}\attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}"
ImageDir="dist\Release\${IMAGE_TYPE}"
ImageName="attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}"
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IsDebug="true"
else
IsDebug="false"
endif

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-Release.mk ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
	@echo "--------------------------------------"
	@echo "User defined post-build step: [C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyHelloWorld\avrdude-ver6.3\attinyFullTest.bat]"
	@C:\Users\tiri\Documents\GitHub\a3-system\a3motion\mocCode\attinyHelloWorld\avrdude-ver6.3\attinyFullTest.bat
	@echo "--------------------------------------"

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
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/Release/52cdf52be7fc8e7774f424e2fac849fcf4cee91d .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT ${OBJECTDIR}/_ext/1360937237/adc.o  -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/button.o: ../src/button.c  .generated_files/flags/Release/733d003aeed8ed16c4649a5dce5b7619090cd616 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT ${OBJECTDIR}/_ext/1360937237/button.o  -o ${OBJECTDIR}/_ext/1360937237/button.o ../src/button.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/encoder.o: ../src/encoder.c  .generated_files/flags/Release/8e142ee539f7b98c80d7c09cc5bf67461ccf5db4 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT ${OBJECTDIR}/_ext/1360937237/encoder.o  -o ${OBJECTDIR}/_ext/1360937237/encoder.o ../src/encoder.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/i2c.o: ../src/i2c.c  .generated_files/flags/Release/1c170c3ad75cba4c306597de82c7996078939e96 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT ${OBJECTDIR}/_ext/1360937237/i2c.o  -o ${OBJECTDIR}/_ext/1360937237/i2c.o ../src/i2c.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/Release/76017ce241e4ef57ad791c82b6fb122b2d7c19b1 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT ${OBJECTDIR}/_ext/1360937237/init.o  -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/ledandcolor.o: ../src/ledandcolor.c  .generated_files/flags/Release/9a21463f73d42dbe988eeb22c3edb3daf9b002c6 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/1360937237/ledandcolor.o  -o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ../src/ledandcolor.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/timer.o: ../src/timer.c  .generated_files/flags/Release/16578e8e9b089a70c7c0e0f9db8e260f9867a7eb .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT ${OBJECTDIR}/_ext/1360937237/timer.o  -o ${OBJECTDIR}/_ext/1360937237/timer.o ../src/timer.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  .generated_files/flags/Release/bc700697c4baad4003b2aabfc8af20e355907920 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1472" 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1472/main.o.d" -MT "${OBJECTDIR}/_ext/1472/main.o.d" -MT ${OBJECTDIR}/_ext/1472/main.o  -o ${OBJECTDIR}/_ext/1472/main.o ../main.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
else
${OBJECTDIR}/_ext/1360937237/adc.o: ../src/adc.c  .generated_files/flags/Release/51df5072977878e31cf8af64af31dc8850d37d82 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT "${OBJECTDIR}/_ext/1360937237/adc.o.d" -MT ${OBJECTDIR}/_ext/1360937237/adc.o  -o ${OBJECTDIR}/_ext/1360937237/adc.o ../src/adc.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/button.o: ../src/button.c  .generated_files/flags/Release/b024f7b9bf48de0bb6fea1b4a1a4874b83b16a30 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT "${OBJECTDIR}/_ext/1360937237/button.o.d" -MT ${OBJECTDIR}/_ext/1360937237/button.o  -o ${OBJECTDIR}/_ext/1360937237/button.o ../src/button.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/encoder.o: ../src/encoder.c  .generated_files/flags/Release/53cf4986ad158d4aba51af1a2b08fb4ccf9f28a .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT "${OBJECTDIR}/_ext/1360937237/encoder.o.d" -MT ${OBJECTDIR}/_ext/1360937237/encoder.o  -o ${OBJECTDIR}/_ext/1360937237/encoder.o ../src/encoder.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/i2c.o: ../src/i2c.c  .generated_files/flags/Release/f2ca531fd893c4b56a3f9a2a88a9c85f047aacb6 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT "${OBJECTDIR}/_ext/1360937237/i2c.o.d" -MT ${OBJECTDIR}/_ext/1360937237/i2c.o  -o ${OBJECTDIR}/_ext/1360937237/i2c.o ../src/i2c.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/init.o: ../src/init.c  .generated_files/flags/Release/8667f60b5511e93e60474956358930063b110813 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT "${OBJECTDIR}/_ext/1360937237/init.o.d" -MT ${OBJECTDIR}/_ext/1360937237/init.o  -o ${OBJECTDIR}/_ext/1360937237/init.o ../src/init.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/ledandcolor.o: ../src/ledandcolor.c  .generated_files/flags/Release/81a1ec43bd9272bf0fdb764f4734d880c95f807d .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/1360937237/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/1360937237/ledandcolor.o  -o ${OBJECTDIR}/_ext/1360937237/ledandcolor.o ../src/ledandcolor.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1360937237/timer.o: ../src/timer.c  .generated_files/flags/Release/46e61e07bed0ce7a92b2eb8e93b511c5d2ef0462 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1360937237" 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1360937237/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT "${OBJECTDIR}/_ext/1360937237/timer.o.d" -MT ${OBJECTDIR}/_ext/1360937237/timer.o  -o ${OBJECTDIR}/_ext/1360937237/timer.o ../src/timer.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  .generated_files/flags/Release/8392a6a1658172b8841e5a695321c692cd2aa866 .generated_files/flags/Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/1472" 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/1472/main.o.d" -MT "${OBJECTDIR}/_ext/1472/main.o.d" -MT ${OBJECTDIR}/_ext/1472/main.o  -o ${OBJECTDIR}/_ext/1472/main.o ../main.c  -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
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
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"   -gdwarf-2 -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__ICD2RAM=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1 -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
	
	${MP_CC_DIR}\\avr-objcopy -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.eep" || exit 0
	${MP_CC_DIR}\\avr-objdump -h -S "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" > "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.lss"
	${MP_CC_DIR}\\avr-objcopy -O srec -R .eeprom -R .fuse -R .lock -R .signature "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.srec"
	
	
else
${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Release=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION) -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
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
