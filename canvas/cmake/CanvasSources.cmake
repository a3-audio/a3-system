# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later

# The Canvas's code as one source list, compiled by the app and by the tests
# (one list, so a file cannot be in one and missing from the other).
get_filename_component(A3CANVAS_DIR "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)
set(A3CANVAS_INCLUDE_DIR "${A3CANVAS_DIR}/Source")

# Everything but Main.cpp.
set(_a3canvas_sources
    model/AppCatalog.cpp
    model/Demo.cpp
    model/Greeter.cpp
    model/StartPlan.cpp
    model/TileStatus.cpp
    sys/CoreProbe.cpp
    sys/Packages.cpp
    sys/StatusPoller.cpp
    sys/ProcessRunner.cpp
    sys/Systemd.cpp
    ui/CanvasView.cpp
    ui/CanvasWindow.cpp
    ui/GreeterComponent.cpp
    ui/LookAndFeel_Canvas.cpp
    ui/TileComponent.cpp)
list(TRANSFORM _a3canvas_sources PREPEND "${A3CANVAS_INCLUDE_DIR}/" OUTPUT_VARIABLE A3CANVAS_LIBRARY_SOURCES)

# The website's logo, compiled in (CanvasAssets::a3logo_svg), drawn as a juce::Drawable.
if(NOT TARGET A3CanvasAssets)
    juce_add_binary_data(A3CanvasAssets NAMESPACE CanvasAssets HEADER_NAME CanvasAssets.h
        SOURCES "${A3CANVAS_DIR}/assets/a3-logo.svg")
endif()

set(A3CANVAS_JUCE_MODULES juce::juce_gui_basics A3CanvasAssets)

# No curl: Core and the engine answer plain http on 127.0.0.1, which JUCE's own
# socket client speaks. A3CANVAS_VERSION is what the greeter shows as the Canvas's own.
set(A3CANVAS_DEFINITIONS JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0 JUCE_DISPLAY_SPLASH_SCREEN=0
    A3CANVAS_VERSION="${PROJECT_VERSION}")
