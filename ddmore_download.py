# SPDX-FileCopyrightText: 2020-2026 Rikard Nordgren and Stella Belin
#
# SPDX-License-Identifier: BSD-3-Clause

import os

for i in range(1, 324):
    os.system(f'wget http://repository.ddmore.eu/model/download/DDMODEL00000{str(i).zfill(3)}' + ' -P ddmore')
