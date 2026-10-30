// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include "model/Network.h"

namespace canvas
{
// This machine's IPv4 addresses with their interfaces' names (getifaddrs).
std::vector<InterfaceAddress> listInterfaces();
}
