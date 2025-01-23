import mujoco
import os
# Other imports and helper functions
import time
import itertools
import numpy as np
from typing import Callable, NamedTuple, Optional, Union, List

# Graphics and plotting.
import mediapy as media
import matplotlib.pyplot as plt

# More legible printing from numpy.
np.set_printoptions(precision=21, suppress=True, linewidth=100)

from IPython.display import clear_output
# clear_output()


def massOf(model,geoName):
    return model.body_mass[model.geom_bodyid[model.geom(geoName).id]]

def renderImage(model,data,renderer,joint:bool,trans:bool):
    scene_option = mujoco.MjvOption()
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = joint
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = trans
    mujoco.mj_resetData(model, data)
    mujoco.mj_forward(model, data)
    renderer.update_scene(data,scene_option=scene_option)
    media.show_image(renderer.render())

def renderVideoOpt(model,joint:bool,trans:bool):
    # Visualization option:
    scene_option = mujoco.MjvOption()
    mujoco.mjv_defaultOption(scene_option)
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = True
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = True
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = joint
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = trans
    
    model.vis.scale.contactwidth = 0.05
    model.vis.scale.contactheight = 0.01
    model.vis.scale.forcewidth = 0.02
    model.vis.map.force = 0.01

    return scene_option

def saveVideo(name,height,width,frames,framerate,show:bool):
    current_dir = os.getcwd()
    print(current_dir)
    filename_out = current_dir+'/'+name
    with media.VideoWriter(filename_out, shape=(height, width),fps=framerate, bps=10_000_000) as w:
        for frame in frames:
            w.add_image(frame)
    if(show):
        media.show_video(media.read_video(filename_out), fps=framerate)

def plotter(times,data,legend):
    # Plotting sensors
    num = len(data.items())
    fig,axs = plt.subplots(1,num,figsize=(3*num,4))
    axs = axs.flatten()
    times = np.asarray(times)

    for i,(key, values) in enumerate(data.items()):
        ax = axs[i]
        values = np.asarray(values)
        ax.plot(times,values)
        ax.set_title(key)
        ax.set_ylabel('unit')
    
    for i,(key, values) in enumerate(data.items()):
        print(key)
        print("start is:",values[0])
        print("end is:",values[-1],"\n")
    
    
    ax.legend(legend, frameon=True, loc='lower right');
    plt.tight_layout()