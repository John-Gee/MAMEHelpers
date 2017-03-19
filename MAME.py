import mameparser
import sethandling
import transmission


if __name__ == "__main__":
    blacklist = ('mach3', 'cobra', 'usvsthem', 'firefox', 'cubeqst', 'gtfore05', 'bmfinal', 'gtfore04', 'vaportrx', 'gtfore03', 'turrett', 'calspeed', 'dstage', 'ddr2m', 'gtfore06', 'bm', 'ddr3mk', 'dsf', 'gtf', 'popn')
    romset = mameparser.get_romset('mame-183.xml', blacklist)
    parents = tuple(romset.keys())
    print(len(parents))
    #transmission.set_them_folders('6', parents)
    #parents = tuple(map(lambda x: x + ".zip", romset.keys()))
    #transmission.set_them_files('5', parents)
    #sethandling.keep_only_set(parents, "MAME/")
