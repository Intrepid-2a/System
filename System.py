import numpy as np

from psychopy import core, visual, event, gui, monitors

from psychopy.hardware import keyboard
from pyglet.window import key

import sys, os
sys.path.append(os.path.join('..', 'EyeTracking'))
from EyeTracking import EyeTracker


def localizeSetup(location=None, glasses='RG', trackEyes, filefolder):

    # sanity check on location argument
    if location == None:
        raise Warning("set location to a string: Glasgow or Toronto")
    if isinstance(location, str):
        if location in ['Toronto', 'toronto', 'tor', 'TOR', 't', 'T', 'YYZ']:
            location = 'toronto'
        if location in ['Glasgow', 'glasgow', 'gla', 'GLA', 'g', 'G', 'EGPF']:
            location = 'glasgow'
    else:
        raise Warning("set location to a string: Glasgow or Toronto")


if glasses == 'RG':
    back_col   = [ 0.5, 0.5,  -1.0]
    red_col    = [0.5, -1.0,  -1.0]
    blue_col   = [ -1.0, 0.5, -1.0]
elif glasses == 'RB':
    back_col   = [ 0.5, -1.0,  0.5]
    red_col    = [ 0.5, -1.0, -1.0] #Flipped back 
    blue_col   = [-1.0, -1.0,  0.5] 


    # sanity check on glasses argument, and picking back-ground color
    if isinstance(glasses, str):
        if glasses in ['RG', 'RB']:
            if glasses == 'RG':
                back_col   = [ 0.5,  0.5, -1.0]
                red_col    = [ 0.5, -1.0, -1.0]
                blue_col   = [-1.0,  0.5, -1.0]
            if glasses == 'RB':
                back_col   = [ 0.5, -1.0,  0.5]
                red_col    = [ 0.5, -1.0, -1.0]
                blue_col   = [-1.0, -1.0,  0.5] 
        else:
            raise Warning('glasses should be RG (default) or RB')
    else:
        raise Warning('glasses should be a string')


    if location == 'glasgow':
        # not a calibrated monitor?
        gammaGrid = np.array([  [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                                [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                                [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                                [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ]], dtype=float)

        resolution = [1500, 800] # in pixels
        size       = [None, None] # in cm
        distance   = None # in cm
        screen     = None # index on the system: 0 = first monitor, 1 = second monitor, and so on

        tracker = 'eyelink'


    if location == 'toronto':
        # color calibrated monitor:
        gammaGrid = np.array([  [  0., 135.44739,  2.4203537, np.nan, np.nan, np.nan  ],
                                [  0.,  27.722954, 2.4203537, np.nan, np.nan, np.nan  ],
                                [  0.,  97.999275, 2.4203537, np.nan, np.nan, np.nan  ],
                                [  0.,   9.235623, 2.4203537, np.nan, np.nan, np.nan  ]], dtype=float)

        resolution = [1920, 1080] # in pixels
        size       = [59.8, 33.6] # in cm
        distance   = 50 # in cm
        screen     = 1  # index on the system: 0 = first monitor, 1 = second monitor, and so on

        tracker = 'livetrack'

    mymonitor = monitors.Monitor(name='temp',
                                 distance=distance,
                                 width=size[0])
    mymonitor.setGammaGrid(gammaGrid)
    mymonitor.setSizePix(resolution)

    #win = visual.Window([1000, 500], allowGUI=True, monitor='ccni', units='deg', fullscr=True, color = back_col, colorSpace = 'rgb')
    win = visual.Window(resolution, monitor=mymonitor, allowGUI=True, units='deg', fullscr=True, color=back_col, colorSpace = 'rgb', screen=screen)
            # size = [34.5, 19.5]
            # distance = 40
    win.mouseVisible = False


    tracker=None, 
                 trackEyes=[False, False], 
                 fixationWindow=None,
                 minFixDur=None,
                 fixTimeout=None,
                 psychopyWindow=None, 
                 filefolder=None, 
                 samplemode=None,
                 calibrationpoints=9

    if not any(trackEyes):
        tracker = 'mouse'


    ET = EyeTracker(tracker           = tracker,
                    fixationWindow    = 2.0,
                    minFixDur         = 0.2,
                    fixTimeout        = 3.0,
                    psychopyWindow    = win,
                    filefolder        = filefolder,
                    samplemode        = 'average',
                    calibrationpoints = 5 )

    colors = {'back_col' : back_col,
              'red_col'  : red_col,
              'blue_col' : blue_col }

    return({'win'     : win,
            'tracker' : ET,
            'colors'  : colors})
