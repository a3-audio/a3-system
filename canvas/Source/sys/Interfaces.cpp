// SPDX-FileCopyrightText: 2026 Raphael Eismann
// SPDX-License-Identifier: GPL-3.0-or-later
#include "Interfaces.h"

#include <arpa/inet.h>
#include <ifaddrs.h>
#include <netinet/in.h>

namespace canvas
{
// getifaddrs, not juce::IPAddress::getAllAddresses: only it names the interface, which is how a
// container bridge is told from the A³ network.
std::vector<InterfaceAddress> listInterfaces()
{
    std::vector<InterfaceAddress> found;
    ifaddrs* list = nullptr;
    if (getifaddrs (&list) != 0)
        return found;
    for (auto* entry = list; entry != nullptr; entry = entry->ifa_next)
    {
        if (entry->ifa_addr == nullptr || entry->ifa_addr->sa_family != AF_INET)
            continue;
        char text[INET_ADDRSTRLEN] = {};
        const auto* address = reinterpret_cast<const sockaddr_in*> (entry->ifa_addr);
        if (inet_ntop (AF_INET, &address->sin_addr, text, sizeof (text)) != nullptr)
            found.push_back ({ entry->ifa_name, text });
    }
    freeifaddrs (list);
    return found;
}
}
