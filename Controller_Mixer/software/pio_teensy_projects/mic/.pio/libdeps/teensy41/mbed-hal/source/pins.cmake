set(pinScript  "${CMAKE_CURRENT_LIST_DIR}/pins.py")
set(genIncRoot "${CMAKE_BINARY_DIR}/generated/include")
set(pinFileDir "${genIncRoot}/${PROJECT_NAME}")
set(pinFile    "${pinFileDir}/pins.array")

file(MAKE_DIRECTORY "${pinFileDir}")

set_source_files_properties("${pinFile}" PROPERTIES HEADER_FILE_ONLY TRUE
                            OBJECT_DEPENDS "${YOTTA_CONFIG_MERGED_JSON_FILE}")
set_source_files_properties("../mbed-hal/PinNames.h" PROPERTIES HEADER_FILE_ONLY TRUE
                            OBJECT_DEPENDS "${pinFile}")
set_source_files_properties("pins.c" PROPERTIES
                            OBJECT_DEPENDS "${pinFile}")

add_custom_target(mbed-hal_pinnames ALL DEPENDS "${pinFile}" "${YOTTA_CONFIG_MERGED_JSON_FILE}")

# make sure mbed-hal depends on the dummy pinNames target, so that even if
# "ALL" isn't being built, the pins file still gets generated
add_dependencies(mbed-hal mbed-hal_pinnames)

add_custom_command(OUTPUT "${pinFile}"
                  MAIN_DEPENDENCY "${YOTTA_CONFIG_MERGED_JSON_FILE}"
                  DEPENDS "${YOTTA_CONFIG_MERGED_JSON_FILE}"
                  COMMAND python "${pinScript}" "${YOTTA_CONFIG_MERGED_JSON_FILE}" "${pinFile}"
                  COMMENT "Generating ${pinFile}")
