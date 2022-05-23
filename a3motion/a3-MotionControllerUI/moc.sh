#!/bin/bash

# A³ Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³ Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³ Core.  If not, see <https://www.gnu.org/licenses/>.

# © Copyright 2021 Patric Schmitz

cd $(dirname $(readlink -f "$0"))
/usr/bin/python3 moc_ui.py --serial_device /dev/ttyACM0 --server_ip "192.168.43.50" --server_port 9000 --encoder_base_port 1337
