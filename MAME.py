#!/usr/bin/python


import argparse
import sys


import mameparser
import sethandling
import transmission


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mame script')
    parser.add_argument('liste', metavar='list',
                    help='The Mame list generated with -listxml')
    parser.add_argument('folder', metavar='folder',
                    help='The Mame ROMs folder on disk')
    parser.add_argument('RID', metavar='RID',
                    help='The ROMs Torrent ID in transmission (starts at 1)')
    parser.add_argument('CID', metavar='CID',
                    help='The CHDs Torrent ID in transmission (starts at 1)')
    args  = parser.parse_args()
    liste  = args.liste
    folder = args.folder
    RID    = args.RID
    CID    = args.CID

    blacklist = ('mach3', 'cobra', 'usvsthem', 'firefox', 'cubeqst', 'gtfore05', 'bmfinal', 'gtfore04', 'vaportrx', 'gtfore03', 'turrett', 'calspeed', 'dstage', 'ddr2m', 'gtfore06', 'bm', 'ddr3mk', 'dsf', 'gtf', 'popn')
    romset = mameparser.get_romset(liste, blacklist)
    parents = tuple(sorted(romset.keys()))
    print('Number of parents to get: {0}'.format(len(parents)))
    sethandling.keep_only_set(parents, folder, False)
    print('Set Handling done')
    transmission.set_them_folders(CID, parents)
    print('set them folders done')
    parents = tuple(map(lambda x: x + '.zip', sorted(romset.keys())))
    transmission.set_them_files(RID, parents)
    print('set them files done')
