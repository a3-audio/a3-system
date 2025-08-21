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
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/default/6d4764e0de55452e74bf51553ae4ef8c48bf628f .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o  -o ${OBJECTDIR}/src/adc.o src/adc.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/default/cd9ff20ad6183cafdee5331ac21b68263fcec40a .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o  -o ${OBJECTDIR}/src/button.o src/button.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/eep.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  .generated_files/flags/default/5affee72f536c811f1c3391f581de481a35e7d97 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT ${OBJECTDIR}/_ext/797462307/eep.o  -o ${OBJECTDIR}/_ext/797462307/eep.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/default/a47a7bc73133e60b7fab904de747467f76a720ec .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o  -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/default/1d29c0ce9021ac8c7f12e22efbf397b1bf43dbd8 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o  -o ${OBJECTDIR}/src/timer.o src/timer.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/main.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  .generated_files/flags/default/1ac657833b702817424570ba269eb7f390fe2682 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/main.o.d" -MT "${OBJECTDIR}/_ext/797462307/main.o.d" -MT ${OBJECTDIR}/_ext/797462307/main.o  -o ${OBJECTDIR}/_ext/797462307/main.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  .generated_files/flags/default/791c6ffc83c81caa12b8e511d1a33dc1aad8c4 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/encoderAlternative.o  -o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  .generated_files/flags/default/6e942e0883777c87c0232545fe01b897fc3682f7 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS} -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/i2cAlternative.o  -o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
else
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/default/bc13acfdada78d62ed3d1e121cdf9c1153674530 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o  -o ${OBJECTDIR}/src/adc.o src/adc.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/default/8a1c9a96bbeb7aecf1eee2233fb08280dbede688 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o  -o ${OBJECTDIR}/src/button.o src/button.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/eep.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  .generated_files/flags/default/88b54982d1f78dabe0ea6abbe16344008d0e4c0c .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/eep.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT "${OBJECTDIR}/_ext/797462307/eep.o.d" -MT ${OBJECTDIR}/_ext/797462307/eep.o  -o ${OBJECTDIR}/_ext/797462307/eep.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/eep.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/default/83e48a0e7031745ccf585f09c8e24b9a80ea49ca .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o  -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/default/d9d7179b052b1c4ef5241ff3c8039a04d85d586d .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o  -o ${OBJECTDIR}/src/timer.o src/timer.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/main.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  .generated_files/flags/default/27ca0f0a5312eba4c07493cb9834b60f917a442b .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/main.o.d" -MT "${OBJECTDIR}/_ext/797462307/main.o.d" -MT ${OBJECTDIR}/_ext/797462307/main.o  -o ${OBJECTDIR}/_ext/797462307/main.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/main.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  .generated_files/flags/default/409e3ecd99496fe5715e67f7b17ab8dd4e1bc563 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/encoderAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/encoderAlternative.o  -o ${OBJECTDIR}/_ext/797462307/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/encoderAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/797462307/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  .generated_files/flags/default/e5cc2920bab22a4760975261a6e5a20cc2e0d84c .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/797462307" 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/797462307/i2cAlternative.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626 ${PACK_COMPILER_OPTIONS} ${PACK_COMMON_OPTIONS}  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -Wall -MD -MP -MF "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/797462307/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/797462307/i2cAlternative.o  -o ${OBJECTDIR}/_ext/797462307/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/src/i2cAlternative.c  -DXPRJ_default=$(CND_CONF)  $(COMPARISON_BUILD) 
	
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

DEPFILES=$(wildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
