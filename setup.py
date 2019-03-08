# ---------------------------License Notice------------------------------------------
# Copyright (C) 2019 Enrico Ghidoni (enrico.ghidoni2@studio.unibo.it)
# Copyright (C) 2019 Luca Ottavio Serafini (lucaottavio.serafini@studio.unibo.it)
#
# This file is part of arduino-lidar.
#
# arduino-lidar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# arduino-lidar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with arduino-lidar.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------License Notice------------------------------------------


import setuptools

setuptools.setup(
    name = 'arduino-lidar',
    description = 'Gather LIDAR data from an Arduino board and draw it in realtime using Open3d',
    version = '0.1.0',
    author = 'Enrico Ghidoni, Luca Serafini',
    author_email = 'enrico.ghidoni2@studio.unibo.it, lucaottavio.serafini@studio.unibo.it',
    url = 'https://github.com/enricoghdn/arduino-lidar',
    packages = setuptools.find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Handhelds/PDA\'s',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development',
    ],
    license = 'GNU General Public License Version 3',
    python_requires = '>=3.6,<4',
    install_require = [
        'open3d-python>=0.5.0,<1',
        'numpy>=1.16.2,<2',
        'pyserial>=3.4,<4',
    ],
)