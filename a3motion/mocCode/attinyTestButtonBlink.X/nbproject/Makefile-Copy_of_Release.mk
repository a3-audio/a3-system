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
ifeq "$(wildcard nbproject/Makefile-local-Copy_of_Release.mk)" "nbproject/Makefile-local-Copy_of_Release.mk"
include nbproject/Makefile-local-Copy_of_Release.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=Copy_of_Release
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
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
SOURCEFILES_QUOTED_IF_SPACED=../attinyFullTest/attinyFullTest/src/adc.c ../attinyFullTest/attinyFullTest/src/button.c ../attinyFullTest/attinyFullTest/src/encoder.c ../attinyFullTest/attinyFullTest/src/i2c.c ../attinyFullTest/attinyFullTest/src/init.c ../attinyFullTest/attinyFullTest/src/ledandcolor.c ../attinyFullTest/attinyFullTest/src/timer.c ../attinyFullTest/attinyFullTest/main.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/419621557/adc.o ${OBJECTDIR}/_ext/419621557/button.o ${OBJECTDIR}/_ext/419621557/encoder.o ${OBJECTDIR}/_ext/419621557/i2c.o ${OBJECTDIR}/_ext/419621557/init.o ${OBJECTDIR}/_ext/419621557/ledandcolor.o ${OBJECTDIR}/_ext/419621557/timer.o ${OBJECTDIR}/_ext/586841952/main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/419621557/adc.o.d ${OBJECTDIR}/_ext/419621557/button.o.d ${OBJECTDIR}/_ext/419621557/encoder.o.d ${OBJECTDIR}/_ext/419621557/i2c.o.d ${OBJECTDIR}/_ext/419621557/init.o.d ${OBJECTDIR}/_ext/419621557/ledandcolor.o.d ${OBJECTDIR}/_ext/419621557/timer.o.d ${OBJECTDIR}/_ext/586841952/main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/419621557/adc.o ${OBJECTDIR}/_ext/419621557/button.o ${OBJECTDIR}/_ext/419621557/encoder.o ${OBJECTDIR}/_ext/419621557/i2c.o ${OBJECTDIR}/_ext/419621557/init.o ${OBJECTDIR}/_ext/419621557/ledandcolor.o ${OBJECTDIR}/_ext/419621557/timer.o ${OBJECTDIR}/_ext/586841952/main.o

# Source Files
SOURCEFILES=../attinyFullTest/attinyFullTest/src/adc.c ../attinyFullTest/attinyFullTest/src/button.c ../attinyFullTest/attinyFullTest/src/encoder.c ../attinyFullTest/attinyFullTest/src/i2c.c ../attinyFullTest/attinyFullTest/src/init.c ../attinyFullTest/attinyFullTest/src/ledandcolor.c ../attinyFullTest/attinyFullTest/src/timer.c ../attinyFullTest/attinyFullTest/main.c

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
	${MAKE}  -f nbproject/Makefile-Copy_of_Release.mk ${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

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
${OBJECTDIR}/_ext/419621557/adc.o: ../attinyFullTest/attinyFullTest/src/adc.c  .generated_files/flags/Copy_of_Release/750bdd7661843aff50c49aace3d39710bba9f58b .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/adc.o.d" -MT "${OBJECTDIR}/_ext/419621557/adc.o.d" -MT ${OBJECTDIR}/_ext/419621557/adc.o  -o ${OBJECTDIR}/_ext/419621557/adc.o ../attinyFullTest/attinyFullTest/src/adc.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/button.o: ../attinyFullTest/attinyFullTest/src/button.c  .generated_files/flags/Copy_of_Release/ecdbde38690880ccc96089511e98fec9c1e3d4b6 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/button.o.d" -MT "${OBJECTDIR}/_ext/419621557/button.o.d" -MT ${OBJECTDIR}/_ext/419621557/button.o  -o ${OBJECTDIR}/_ext/419621557/button.o ../attinyFullTest/attinyFullTest/src/button.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/encoder.o: ../attinyFullTest/attinyFullTest/src/encoder.c  .generated_files/flags/Copy_of_Release/257c04f04ddd04ab29a245a1b79b04d1b5de98fb .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/encoder.o.d" -MT "${OBJECTDIR}/_ext/419621557/encoder.o.d" -MT ${OBJECTDIR}/_ext/419621557/encoder.o  -o ${OBJECTDIR}/_ext/419621557/encoder.o ../attinyFullTest/attinyFullTest/src/encoder.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/i2c.o: ../attinyFullTest/attinyFullTest/src/i2c.c  .generated_files/flags/Copy_of_Release/ed74a1ea6adf07689a656c5bd653a842ad3377fe .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/i2c.o.d" -MT "${OBJECTDIR}/_ext/419621557/i2c.o.d" -MT ${OBJECTDIR}/_ext/419621557/i2c.o  -o ${OBJECTDIR}/_ext/419621557/i2c.o ../attinyFullTest/attinyFullTest/src/i2c.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/init.o: ../attinyFullTest/attinyFullTest/src/init.c  .generated_files/flags/Copy_of_Release/dd087298a86ab1acdbb398876483441e42bd184c .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/init.o.d" -MT "${OBJECTDIR}/_ext/419621557/init.o.d" -MT ${OBJECTDIR}/_ext/419621557/init.o  -o ${OBJECTDIR}/_ext/419621557/init.o ../attinyFullTest/attinyFullTest/src/init.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/ledandcolor.o: ../attinyFullTest/attinyFullTest/src/ledandcolor.c  .generated_files/flags/Copy_of_Release/2177c690694952761d5c3efaa760c4179d7b641c .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/419621557/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/419621557/ledandcolor.o  -o ${OBJECTDIR}/_ext/419621557/ledandcolor.o ../attinyFullTest/attinyFullTest/src/ledandcolor.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/timer.o: ../attinyFullTest/attinyFullTest/src/timer.c  .generated_files/flags/Copy_of_Release/9a822f272cb24c63e7ab37b7e31cd0bbbf860c08 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/timer.o.d" -MT "${OBJECTDIR}/_ext/419621557/timer.o.d" -MT ${OBJECTDIR}/_ext/419621557/timer.o  -o ${OBJECTDIR}/_ext/419621557/timer.o ../attinyFullTest/attinyFullTest/src/timer.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/586841952/main.o: ../attinyFullTest/attinyFullTest/main.c  .generated_files/flags/Copy_of_Release/c0c59e25bf80f7f1c6fbc6187c2846bec8fcb40d .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/586841952" 
	@${RM} ${OBJECTDIR}/_ext/586841952/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/586841952/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626" -g -DDEBUG  -gdwarf-2  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/586841952/main.o.d" -MT "${OBJECTDIR}/_ext/586841952/main.o.d" -MT ${OBJECTDIR}/_ext/586841952/main.o  -o ${OBJECTDIR}/_ext/586841952/main.o ../attinyFullTest/attinyFullTest/main.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
else
${OBJECTDIR}/_ext/419621557/adc.o: ../attinyFullTest/attinyFullTest/src/adc.c  .generated_files/flags/Copy_of_Release/3fcac90b8b41c8e9b0c6c1e04318087ebdb79004 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/adc.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/adc.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/adc.o.d" -MT "${OBJECTDIR}/_ext/419621557/adc.o.d" -MT ${OBJECTDIR}/_ext/419621557/adc.o  -o ${OBJECTDIR}/_ext/419621557/adc.o ../attinyFullTest/attinyFullTest/src/adc.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/button.o: ../attinyFullTest/attinyFullTest/src/button.c  .generated_files/flags/Copy_of_Release/8430be6a4f88916096c1b3efa6925ff46b400ffe .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/button.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/button.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/button.o.d" -MT "${OBJECTDIR}/_ext/419621557/button.o.d" -MT ${OBJECTDIR}/_ext/419621557/button.o  -o ${OBJECTDIR}/_ext/419621557/button.o ../attinyFullTest/attinyFullTest/src/button.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/encoder.o: ../attinyFullTest/attinyFullTest/src/encoder.c  .generated_files/flags/Copy_of_Release/a03f20e3a6a54d06577c303d5176182fbaa1baf9 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/encoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/encoder.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/encoder.o.d" -MT "${OBJECTDIR}/_ext/419621557/encoder.o.d" -MT ${OBJECTDIR}/_ext/419621557/encoder.o  -o ${OBJECTDIR}/_ext/419621557/encoder.o ../attinyFullTest/attinyFullTest/src/encoder.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/i2c.o: ../attinyFullTest/attinyFullTest/src/i2c.c  .generated_files/flags/Copy_of_Release/ee74218a98c479ac6f0bd2b1a48ff3d1d44c876b .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/i2c.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/i2c.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/i2c.o.d" -MT "${OBJECTDIR}/_ext/419621557/i2c.o.d" -MT ${OBJECTDIR}/_ext/419621557/i2c.o  -o ${OBJECTDIR}/_ext/419621557/i2c.o ../attinyFullTest/attinyFullTest/src/i2c.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/init.o: ../attinyFullTest/attinyFullTest/src/init.c  .generated_files/flags/Copy_of_Release/1da793c17585ede936273841d890fd6a8f0f8920 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/init.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/init.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/init.o.d" -MT "${OBJECTDIR}/_ext/419621557/init.o.d" -MT ${OBJECTDIR}/_ext/419621557/init.o  -o ${OBJECTDIR}/_ext/419621557/init.o ../attinyFullTest/attinyFullTest/src/init.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/ledandcolor.o: ../attinyFullTest/attinyFullTest/src/ledandcolor.c  .generated_files/flags/Copy_of_Release/f849c4e2cd50adeb338edf36d02f2a8a99a81e43 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/ledandcolor.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/ledandcolor.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/ledandcolor.o.d" -MT "${OBJECTDIR}/_ext/419621557/ledandcolor.o.d" -MT ${OBJECTDIR}/_ext/419621557/ledandcolor.o  -o ${OBJECTDIR}/_ext/419621557/ledandcolor.o ../attinyFullTest/attinyFullTest/src/ledandcolor.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/419621557/timer.o: ../attinyFullTest/attinyFullTest/src/timer.c  .generated_files/flags/Copy_of_Release/7a1d5c823ac603dc2697213bde784980270f6d97 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/419621557" 
	@${RM} ${OBJECTDIR}/_ext/419621557/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/419621557/timer.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/419621557/timer.o.d" -MT "${OBJECTDIR}/_ext/419621557/timer.o.d" -MT ${OBJECTDIR}/_ext/419621557/timer.o  -o ${OBJECTDIR}/_ext/419621557/timer.o ../attinyFullTest/attinyFullTest/src/timer.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
${OBJECTDIR}/_ext/586841952/main.o: ../attinyFullTest/attinyFullTest/main.c  .generated_files/flags/Copy_of_Release/83d13d25dad531bbb217ad3068f0bd40e74972f8 .generated_files/flags/Copy_of_Release/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}/_ext/586841952" 
	@${RM} ${OBJECTDIR}/_ext/586841952/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/586841952/main.o 
	 ${MP_CC}  $(MP_EXTRA_CC_PRE) -mmcu=attiny1626  -I "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/include" -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -x c -c -D__$(MP_PROCESSOR_OPTION)__  -funsigned-char -funsigned-bitfields -Os -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -DNDEBUG -Wall -MD -MP -MF "${OBJECTDIR}/_ext/586841952/main.o.d" -MT "${OBJECTDIR}/_ext/586841952/main.o.d" -MT ${OBJECTDIR}/_ext/586841952/main.o  -o ${OBJECTDIR}/_ext/586841952/main.o ../attinyFullTest/attinyFullTest/main.c  -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD) 
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"   -gdwarf-2 -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyTestButtonBlink.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__ICD2RAM=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1 -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
	
	${MP_CC_DIR}\\avr-objcopy -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.eep" || exit 0
	${MP_CC_DIR}\\avr-objdump -h -S "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" > "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.lss"
	${MP_CC_DIR}\\avr-objcopy -O srec -R .eeprom -R .fuse -R .lock -R .signature "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.srec"
	
	
else
${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -mmcu=attiny1626 -B "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/ATtiny_DFP/1.10.348/gcc/dev/attiny1626"  -D__$(MP_PROCESSOR_OPTION)__  -Wl,-Map="${DISTDIR}\attinyTestButtonBlink.X.${IMAGE_TYPE}.map"    -o ${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}      -DXPRJ_Copy_of_Release=$(CND_CONF)  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION) -Wl,--gc-sections -Wl,--start-group  -Wl,-lm -Wl,-lm -Wl,--end-group 
	${MP_CC_DIR}\\avr-objcopy -O ihex "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.hex"
	${MP_CC_DIR}\\avr-objcopy -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.eep" || exit 0
	${MP_CC_DIR}\\avr-objdump -h -S "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" > "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.lss"
	${MP_CC_DIR}\\avr-objcopy -O srec -R .eeprom -R .fuse -R .lock -R .signature "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}" "${DISTDIR}/attinyTestButtonBlink.X.${IMAGE_TYPE}.srec"
	
	
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
