#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-lcc.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum-lcc.png'])
    ]

setup(
    name="Electrum-LCC",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    packages=[
        'electrum_lcc',
        'electrum_lcc_gui',
        'electrum_lcc_gui.qt',
        'electrum_lcc_plugins',
        'electrum_lcc_plugins.audio_modem',
        'electrum_lcc_plugins.cosigner_pool',
        'electrum_lcc_plugins.email_requests',
        'electrum_lcc_plugins.hw_wallet',
        'electrum_lcc_plugins.keepkey',
        'electrum_lcc_plugins.labels',
        'electrum_lcc_plugins.ledger',
        'electrum_lcc_plugins.trezor',
        'electrum_lcc_plugins.digitalbitbox',
        'electrum_lcc_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_lcc': 'lib',
        'electrum_lcc_gui': 'gui',
        'electrum_lcc_plugins': 'plugins',
    },
    package_data={
        'electrum_lcc': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-lcc'],
    data_files=data_files,
    description="Lightweight Litecoin Cash Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://github.com/litecoincash-project/electrum-lcc",
    long_description="""Lightweight Litecoin Cash Wallet"""
)

# Optional modules (not required to run Electrum)
import pip
opt_modules = requirements_hw + ['pycryptodomex']
[ pip.main(['install', m]) for m in opt_modules ]
