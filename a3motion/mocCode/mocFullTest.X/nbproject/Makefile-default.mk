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
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
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
SOURCEFILES_QUOTED_IF_SPACED=src/adc.c src/button.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c src/ledandcolor.c src/timer.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/src/adc.o ${OBJECTDIR}/src/button.o ${OBJECTDIR}/_ext/797462307/eep.o ${OBJECTDIR}/src/ledandcolor.o ${OBJECTDIR}/src/timer.o ${OBJECTDIR}/_ext/797462307/main.o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o
POSSIBLE_DEPFILES=${OBJECTDIR}/src/adc.o.d ${OBJECTDIR}/src/button.o.d ${OBJECTDIR}/_ext/797462307/eep.o.d ${OBJECTDIR}/src/ledandcolor.o.d ${OBJECTDIR}/src/timer.o.d ${OBJECTDIR}/_ext/797462307/main.o.d ${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d ${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/src/adc.o ${OBJECTDIR}/src/button.o ${OBJECTDIR}/_ext/797462307/eep.o ${OBJECTDIR}/src/ledandcolor.o ${OBJECTDIR}/src/timer.o ${OBJECTDIR}/_ext/797462307/main.o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o

# Source Files
SOURCEFILES=src/adc.c src/button.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c src/ledandcolor.c src/timer.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c

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
	${MAKE}  -f nbproject/Makefile-default.mk ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

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
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/default/f34390adf49b16833461fdc55ed40a6da3c99364 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o  -o ${OBJECTDIR}/src/adc.o src/adc.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/default/7cb036a34ec58be68e64b1f1715ae57afad55e .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o  -o ${OBJECTDIR}/src/button.o src/button.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/eep.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  .generated_files/flags/default/f8e06a5bd338db5caee73429998379eacc230759 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT ${OBJECTDIR}/_ext/797462307/eep.o  -o ${OBJECTDIR}/_ext/797462307/eep.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/default/2fca07e273fe8ca942b29d1c40773e7af0a29709 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o  -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/default/354074cfb978866ef9780fca2b7bb5136f00132b .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o  -o ${OBJECTDIR}/src/timer.o src/timer.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/main.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  .generated_files/flags/default/438e37545f680a30c6f03bdd47015261fe4fbb19 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/main.o.d" -MT "${OBJECTDIR}/_ext/797462307/main.o.d" -MT ${OBJECTDIR}/_ext/797462307/main.o  -o ${OBJECTDIR}/_ext/797462307/main.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  .generated_files/flags/default/2ae20e1b49e28a547f7ea13690661fac0b54a4e8 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/encoderAlternative.o  -o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  .generated_files/flags/default/e52c988f60755348d177aeb336abfe6f807a94e3 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/i2cAlternative.o  -o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
else
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/default/bac84056225fc7da0a37ecaccfbd8a2b2d6b45a0 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o  -o ${OBJECTDIR}/src/adc.o src/adc.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/default/f2c87bf7b5108608fa7f39a80160717ec9cbc068 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o  -o ${OBJECTDIR}/src/button.o src/button.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/eep.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  .generated_files/flags/default/8c53227167ee8e281bb4e60dd2616dfa8f2d34b9 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT ${OBJECTDIR}/_ext/797462307/eep.o  -o ${OBJECTDIR}/_ext/797462307/eep.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/default/cfbfbf10f66db139b34d8cb0e1317a807c422cc9 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o  -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/default/e405d4a42776863690fe7eda3de8a46afb8cb992 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o  -o ${OBJECTDIR}/src/timer.o src/timer.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/main.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  .generated_files/flags/default/dfcca367d359d4f5417ac9fca99003dfc2f47b00 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/main.o.d" -MT "${OBJECTDIR}/_ext/797462307/main.o.d" -MT ${OBJECTDIR}/_ext/797462307/main.o  -o ${OBJECTDIR}/_ext/797462307/main.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  .generated_files/flags/default/304f187f368c5fe657c3b35a88c4b26e1a3d33ac .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/encoderAlternative.o  -o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  .generated_files/flags/default/bfa22ed5511bd5442b2aef30fd267827bb049a25 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O3 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -Wextra -Wundef -MD -MP -MF "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/i2cAlternative.o  -o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 ${PACK_COMMON_OPTIONS}   -gdwarf-2 -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\mocFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__ICD2RAM=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1 -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,--end-group 
	
	
	
	
	
	
else
${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 ${PACK_COMMON_OPTIONS}  -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\mocFullTest.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION) -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,--end-group 
	${MP_CC_DIR}\\avr-objcopy -O ihex "${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.hex"
	
	
	
	
	
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
