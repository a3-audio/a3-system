# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later

# A³ Canvas: one window with a tile per A³ program, its state, and start/stop.
# JUCE 9.0.3 from ~/local/juce, as A3 Desk, StemDeck and Motion UI build it.
cmake_minimum_required(VERSION 3.22)
project(A3Canvas VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ccache when installed, as StemDeck has it (2026-10-03).
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
    set(CCACHE_LAUNCHER "${CMAKE_COMMAND}" -E env "CCACHE_BASEDIR=${CMAKE_SOURCE_DIR}"
        "CCACHE_NOHASHDIR=true" "${CCACHE_PROGRAM}")
    set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_LAUNCHER})
    set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_LAUNCHER})
endif()

find_package(JUCE 9.0.3 CONFIG REQUIRED)

# Everything but Main.cpp: the app and the tests compile the same list.
include(cmake/CanvasSources.cmake)

juce_add_gui_app(A3Canvas PRODUCT_NAME "a3-canvas")
target_sources(A3Canvas PRIVATE Source/Main.cpp ${A3CANVAS_LIBRARY_SOURCES})
target_include_directories(A3Canvas PRIVATE ${A3CANVAS_INCLUDE_DIRS})
target_compile_definitions(A3Canvas PRIVATE ${A3CANVAS_DEFINITIONS}
    JUCE_APPLICATION_NAME_STRING="$<TARGET_PROPERTY:A3Canvas,JUCE_PRODUCT_NAME>"
    JUCE_APPLICATION_VERSION_STRING="$<TARGET_PROPERTY:A3Canvas,JUCE_VERSION>")
# A rewrite that drops a case must not compile (memory feedback_a-rewrite-drops-a-case).
target_compile_options(A3Canvas PRIVATE -Werror=switch)
target_link_libraries(A3Canvas
    PRIVATE ${A3CANVAS_JUCE_MODULES}
    PUBLIC juce::juce_recommended_config_flags juce::juce_recommended_lto_flags
           juce::juce_recommended_warning_flags)

option(A3CANVAS_TESTS "Build the unit tests" OFF)
if(A3CANVAS_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
