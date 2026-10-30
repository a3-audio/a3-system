# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later

find_package(GTest REQUIRED)
include(GoogleTest)

juce_add_console_app(a3-canvas-tests PRODUCT_NAME "a3-canvas-tests")
target_sources(a3-canvas-tests PRIVATE
    TestRunner.cpp
    AppCatalogTests.cpp
    CoreProbeTests.cpp
    PackagesTests.cpp
    StartPlanTests.cpp
    SystemdTests.cpp
    TileStatusTests.cpp
    ${A3CANVAS_LIBRARY_SOURCES})
target_include_directories(a3-canvas-tests PRIVATE "${PROJECT_SOURCE_DIR}/Source" "${CMAKE_CURRENT_SOURCE_DIR}")
target_compile_definitions(a3-canvas-tests PRIVATE ${A3CANVAS_DEFINITIONS}
    A3CANVAS_FIXTURES="${CMAKE_CURRENT_SOURCE_DIR}/fixtures")
target_compile_options(a3-canvas-tests PRIVATE -Werror=switch)
target_link_libraries(a3-canvas-tests
    PRIVATE ${A3CANVAS_JUCE_MODULES} GTest::gtest
    PUBLIC juce::juce_recommended_config_flags juce::juce_recommended_warning_flags)
# PRE_TEST: the list is read when ctest runs, under xvfb-run, not at build time.
gtest_discover_tests(a3-canvas-tests DISCOVERY_MODE PRE_TEST)
