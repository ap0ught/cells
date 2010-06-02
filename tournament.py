#!/usr/bin/env python

import sys
import ConfigParser
from cells import Game

config = ConfigParser.RawConfigParser()

def get_mind(name):
    full_name = 'minds.' + name
    __import__(full_name)
    return sys.modules[full_name]

bounds = None  # HACK
symmetric = None
mind_list = None

def main():
    global bounds,symmetric, mind_list
    try:
        config.read('tournament.cfg')
        bounds = config.getint('terrain', 'bounds')
        symmetric = config.getboolean('terrain', 'symmetric')
        minds_str = str(config.get('minds', 'minds'))
        mind_list = [get_mind(n) for n in minds_str.split(',')]

    except Exception as e:
        print 'Got error: %s' % e
        config.add_section('minds')
        config.set('minds', 'minds', 'mind1,mind2')
        config.add_section('terrain')
        config.set('terrain', 'bounds', '300')
        config.set('terrain', 'symmetric', 'true')

        with open('tournament.cfg', 'wb') as configfile:
            config.write(configfile)

        config.read('tournament.cfg')
        bounds = config.getint('terrain', 'bounds')
        symmetric = config.getboolean('terrain', 'symmetric')

    # accept command line arguments for the minds over those in the config
    try:
        if len(sys.argv)>2:
            mind_list = [get_mind(n) for n in sys.argv[1:] ]
    except (ImportError,IndexError):
        pass


if __name__ == "__main__":
  main()
  while 1:
    game = Game()
    while not game.winner:
        game.tick()
