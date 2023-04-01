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
ifeq "$(wildcard nbproject/Makefile-local-xc8.mk)" "nbproject/Makefile-local-xc8.mk"
include nbproject/Makefile-local-xc8.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=xc8
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
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=src/adc.c src/button.c src/encoder.c src/i2c.c src/init.c src/ledandcolor.c src/timer.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c main.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/src/adc.o ${OBJECTDIR}/src/button.o ${OBJECTDIR}/src/encoder.o ${OBJECTDIR}/src/i2c.o ${OBJECTDIR}/src/init.o ${OBJECTDIR}/src/ledandcolor.o ${OBJECTDIR}/src/timer.o ${OBJECTDIR}/_ext/282020558/i2cAlternative.o ${OBJECTDIR}/main.o ${OBJECTDIR}/_ext/282020558/debug.o ${OBJECTDIR}/_ext/282020558/encoderAlternative.o
POSSIBLE_DEPFILES=${OBJECTDIR}/src/adc.o.d ${OBJECTDIR}/src/button.o.d ${OBJECTDIR}/src/encoder.o.d ${OBJECTDIR}/src/i2c.o.d ${OBJECTDIR}/src/init.o.d ${OBJECTDIR}/src/ledandcolor.o.d ${OBJECTDIR}/src/timer.o.d ${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d ${OBJECTDIR}/main.o.d ${OBJECTDIR}/_ext/282020558/debug.o.d ${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/src/adc.o ${OBJECTDIR}/src/button.o ${OBJECTDIR}/src/encoder.o ${OBJECTDIR}/src/i2c.o ${OBJECTDIR}/src/init.o ${OBJECTDIR}/src/ledandcolor.o ${OBJECTDIR}/src/timer.o ${OBJECTDIR}/_ext/282020558/i2cAlternative.o ${OBJECTDIR}/main.o ${OBJECTDIR}/_ext/282020558/debug.o ${OBJECTDIR}/_ext/282020558/encoderAlternative.o

# Source Files
SOURCEFILES=src/adc.c src/button.c src/encoder.c src/i2c.c src/init.c src/ledandcolor.c src/timer.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c main.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c



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
	${MAKE}  -f nbproject/Makefile-xc8.mk ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=ATtiny1626
# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/xc8/a060c0b30922209a660fb9d6906277690cbf11e4 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o -o ${OBJECTDIR}/src/adc.o src/adc.c 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/xc8/20d355fe055b014cce6532cdb7143f37cf14517c .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o -o ${OBJECTDIR}/src/button.o src/button.c 
	
${OBJECTDIR}/src/encoder.o: src/encoder.c  .generated_files/flags/xc8/6da7c0c57ecd660872b51366c7c6b2faf527de27 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/encoder.o.d 
	@${RM} ${OBJECTDIR}/src/encoder.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/encoder.o.d" -MT "${OBJECTDIR}/src/encoder.o.d" -MT ${OBJECTDIR}/src/encoder.o -o ${OBJECTDIR}/src/encoder.o src/encoder.c 
	
${OBJECTDIR}/src/i2c.o: src/i2c.c  .generated_files/flags/xc8/d6285443b54899bb9c6a1527eb0ee0b8127141fe .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/i2c.o.d 
	@${RM} ${OBJECTDIR}/src/i2c.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/i2c.o.d" -MT "${OBJECTDIR}/src/i2c.o.d" -MT ${OBJECTDIR}/src/i2c.o -o ${OBJECTDIR}/src/i2c.o src/i2c.c 
	
${OBJECTDIR}/src/init.o: src/init.c  .generated_files/flags/xc8/9dd1121cb365d46d43f8d51c47b2120b8f6e2275 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/init.o.d 
	@${RM} ${OBJECTDIR}/src/init.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/init.o.d" -MT "${OBJECTDIR}/src/init.o.d" -MT ${OBJECTDIR}/src/init.o -o ${OBJECTDIR}/src/init.o src/init.c 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/xc8/5ab5a628e6c40adc300b880d8020d96055759e7a .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/xc8/8212996c74c56aa7def288d646d9896abe02519c .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o -o ${OBJECTDIR}/src/timer.o src/timer.c 
	
${OBJECTDIR}/_ext/282020558/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c  .generated_files/flags/xc8/937518a0cc74ab48dfad3db0cb9ca81e4da202c6 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/i2cAlternative.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/282020558/i2cAlternative.o -o ${OBJECTDIR}/_ext/282020558/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c 
	
${OBJECTDIR}/main.o: main.c  .generated_files/flags/xc8/29ab12e56967acb2ddaccb951d14362c11e0f841 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/main.o.d 
	@${RM} ${OBJECTDIR}/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/main.o.d" -MT "${OBJECTDIR}/main.o.d" -MT ${OBJECTDIR}/main.o -o ${OBJECTDIR}/main.o main.c 
	
${OBJECTDIR}/_ext/282020558/debug.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c  .generated_files/flags/xc8/b333e723243ec9f3b72f296aa0bd73ae647ffc80 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/debug.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/debug.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/debug.o.d" -MT "${OBJECTDIR}/_ext/282020558/debug.o.d" -MT ${OBJECTDIR}/_ext/282020558/debug.o -o ${OBJECTDIR}/_ext/282020558/debug.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c 
	
${OBJECTDIR}/_ext/282020558/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c  .generated_files/flags/xc8/91f92f02d3b3e2465cad93d629f19ec5d196c34a .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/encoderAlternative.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -D__DEBUG=1 -g -DDEBUG  -gdwarf-2  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/282020558/encoderAlternative.o -o ${OBJECTDIR}/_ext/282020558/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c 
	
else
${OBJECTDIR}/src/adc.o: src/adc.c  .generated_files/flags/xc8/814b4473de84bfd1b738b4403cdd7b362a4bae83 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/adc.o.d 
	@${RM} ${OBJECTDIR}/src/adc.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/adc.o.d" -MT "${OBJECTDIR}/src/adc.o.d" -MT ${OBJECTDIR}/src/adc.o -o ${OBJECTDIR}/src/adc.o src/adc.c 
	
${OBJECTDIR}/src/button.o: src/button.c  .generated_files/flags/xc8/bd58fcae68d3e463d8386bda1dbc0f370d2c8ce9 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/button.o.d 
	@${RM} ${OBJECTDIR}/src/button.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/button.o.d" -MT "${OBJECTDIR}/src/button.o.d" -MT ${OBJECTDIR}/src/button.o -o ${OBJECTDIR}/src/button.o src/button.c 
	
${OBJECTDIR}/src/encoder.o: src/encoder.c  .generated_files/flags/xc8/3949f404964efcab5e6b3e02795e4d3026dc16ad .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/encoder.o.d 
	@${RM} ${OBJECTDIR}/src/encoder.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/encoder.o.d" -MT "${OBJECTDIR}/src/encoder.o.d" -MT ${OBJECTDIR}/src/encoder.o -o ${OBJECTDIR}/src/encoder.o src/encoder.c 
	
${OBJECTDIR}/src/i2c.o: src/i2c.c  .generated_files/flags/xc8/47a3aac005ca26edeba628b83c9c84121404f032 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/i2c.o.d 
	@${RM} ${OBJECTDIR}/src/i2c.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/i2c.o.d" -MT "${OBJECTDIR}/src/i2c.o.d" -MT ${OBJECTDIR}/src/i2c.o -o ${OBJECTDIR}/src/i2c.o src/i2c.c 
	
${OBJECTDIR}/src/init.o: src/init.c  .generated_files/flags/xc8/77e82d4e8993a07ebb6b7aebe2aad0f63fedb496 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/init.o.d 
	@${RM} ${OBJECTDIR}/src/init.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/init.o.d" -MT "${OBJECTDIR}/src/init.o.d" -MT ${OBJECTDIR}/src/init.o -o ${OBJECTDIR}/src/init.o src/init.c 
	
${OBJECTDIR}/src/ledandcolor.o: src/ledandcolor.c  .generated_files/flags/xc8/4d4a16d29af39d83b25385d245fec6bf7e227ad .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/src/ledandcolor.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/ledandcolor.o.d" -MT "${OBJECTDIR}/src/ledandcolor.o.d" -MT ${OBJECTDIR}/src/ledandcolor.o -o ${OBJECTDIR}/src/ledandcolor.o src/ledandcolor.c 
	
${OBJECTDIR}/src/timer.o: src/timer.c  .generated_files/flags/xc8/f5454758d310a2e3e32b52ee4698062ad519b158 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/timer.o.d 
	@${RM} ${OBJECTDIR}/src/timer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/src/timer.o.d" -MT "${OBJECTDIR}/src/timer.o.d" -MT ${OBJECTDIR}/src/timer.o -o ${OBJECTDIR}/src/timer.o src/timer.c 
	
${OBJECTDIR}/_ext/282020558/i2cAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c  .generated_files/flags/xc8/aefdec20aff7384692c2394d6c0646996ce49f09 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/i2cAlternative.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d" -MT "${OBJECTDIR}/_ext/282020558/i2cAlternative.o.d" -MT ${OBJECTDIR}/_ext/282020558/i2cAlternative.o -o ${OBJECTDIR}/_ext/282020558/i2cAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/i2cAlternative.c 
	
${OBJECTDIR}/main.o: main.c  .generated_files/flags/xc8/393735a4100feefa5d3acbe86aa473f5c3ce3859 .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/main.o.d 
	@${RM} ${OBJECTDIR}/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/main.o.d" -MT "${OBJECTDIR}/main.o.d" -MT ${OBJECTDIR}/main.o -o ${OBJECTDIR}/main.o main.c 
	
${OBJECTDIR}/_ext/282020558/debug.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c  .generated_files/flags/xc8/bb80419c412096f2cfc4d01f84d824e86924e09b .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/debug.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/debug.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/debug.o.d" -MT "${OBJECTDIR}/_ext/282020558/debug.o.d" -MT ${OBJECTDIR}/_ext/282020558/debug.o -o ${OBJECTDIR}/_ext/282020558/debug.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/debug.c 
	
${OBJECTDIR}/_ext/282020558/encoderAlternative.o: C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c  .generated_files/flags/xc8/8744492d0856a52163eceac49f46d597853d861f .generated_files/flags/xc8/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/282020558" 
	@${RM} ${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d 
	@${RM} ${OBJECTDIR}/_ext/282020558/encoderAlternative.o 
	${MP_CC} $(MP_EXTRA_CC_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -c  -x c -D__$(MP_PROCESSOR_OPTION)__   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -DXPRJ_xc8=$(CND_CONF)  $(COMPARISON_BUILD)  -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     -MD -MP -MF "${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d" -MT "${OBJECTDIR}/_ext/282020558/encoderAlternative.o.d" -MT ${OBJECTDIR}/_ext/282020558/encoderAlternative.o -o ${OBJECTDIR}/_ext/282020558/encoderAlternative.o C:/Users/tiri/Documents/GitHub/a3-system/a3motion/mocCode/mocFullTest.X/encoderAlternative.c 
	
endif

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
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -Wl,-Map=${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.map  -D__DEBUG=1  -DXPRJ_xc8=$(CND_CONF)  -Wl,--defsym=__MPLAB_BUILD=1   -mdfp="${DFP_DIR}/xc8"   -gdwarf-2 -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     $(COMPARISON_BUILD) -Wl,--memorysummary,${DISTDIR}/memoryfile.xml -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}      -Wl,--start-group  -Wl,-lm -Wl,--end-group  -Wl,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1
	@${RM} ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.hex 
	
else
${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mcpu=$(MP_PROCESSOR_OPTION) -Wl,-Map=${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.map  -DXPRJ_xc8=$(CND_CONF)  -Wl,--defsym=__MPLAB_BUILD=1   -mdfp="${DFP_DIR}/xc8"  -Wl,--gc-sections -O1 -ffunction-sections -fdata-sections -fshort-enums -fno-common -funsigned-char -funsigned-bitfields -Wall -gdwarf-3 -mconst-data-in-progmem -mno-const-data-in-config-mapped-progmem     $(COMPARISON_BUILD) -Wl,--memorysummary,${DISTDIR}/memoryfile.xml -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  -o ${DISTDIR}/mocFullTest.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}      -Wl,--start-group  -Wl,-lm -Wl,--end-group 
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
