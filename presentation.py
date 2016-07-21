"""

    This module contains almost everything the presentation needs and thus makes the presentation notebook
    itself a little cleaner.
    
"""

import pandas as pd
import numpy as np
import pysiology

import datetime
from pysiology import pyeeg
from pysiology.notebook import Analysis, Experiment, Muse, Mindwave


from notebook.services.config import ConfigManager
from IPython.paths import locate_profile
from IPython import display, get_ipython
from IPython.core.magic import register_cell_magic

import matplotlib.pyplot as plt
import seaborn
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook
from ipywidgets import HTML


# I don't like transitions, they make me feel uneasy
cm = ConfigManager(profile_dir=locate_profile(get_ipython().profile))
cm.update('livereveal', {
              'theme': 'serif',
              'transition': 'none',
              'start_slideshow_at': 'selected',
});



def ep2016_barria_2_style():
    """ These are some adjustments to the style of the presentation.
        particularly important are the width of .container.slides and the font size of the .rise-enabled .text_cell
        """
    style = """
    <style>
    #exit_b, #help_b {
        display: None ! important;
    }

    .container.slides {
        width:1100px ! important;
    }
    .rise-enabled .controls {
        display: None ! important;
    }
    .rise-enabled .text_cell {
        font-size: 130%;
    }
    section#slide-0-0 {
    }
    </style>
    """
    display.display_html(style, raw=True)
    
    
    
@register_cell_magic
def html_nocode(line, cell):
    hide_code_in_slideshow()
    display.display_html(cell, raw=True)
    
def hide_code_in_slideshow():    
    import binascii
    import os
    uid = binascii.hexlify(os.urandom(8)).decode()    
    html = """<div id="%s"></div>
    <script type="text/javascript">
        $(function(){
            var p = $("#%s");
            if (p.length==0) return;
            while (!p.hasClass("cell")) {
                p=p.parent();
                if (p.prop("tagName") =="body") return;
            }
            var cell = p;
            cell.find(".input").addClass("hide-in-slideshow")
        });
    </script>""" % (uid, uid)
    display.display_html(html, raw=True)
    
    
def figure_realtime_1():        
    def handler(experiment, msg):
        if not hasattr(exp.muse, "AF7"):
            return
        if msg.get("mtp")=="muse_stream":
            ts = exp.muse.AF7
            if len(ts)<200:
                return
            values = ts[-1000:].resample("7L").mean().values
            values -= values.mean() -3000
            line1.data_source.data['x'] = np.arange(len(values))
            line1.data_source.data['y'] = values
            ts = exp.muse.AF8
            values = ts[-1000:].resample("7L").mean().values
            values -= values.mean() + 3000
            line2.data_source.data['x'] = np.arange(len(values))
            line2.data_source.data['y'] = values
            push_notebook(handle=handle)

    p = figure(width=800, height=400, y_range=(-5000,5000))
    line1 = p.line(x=[0], y=[0])
    line2 = p.line(x=[0], y=[0], color="red")
    handle = show(p)
    exp = MyExperiment("baseline_1.hdf5")
    exp(handler)


def figure_correlation_1(df):
    f,axes = plt.subplots(1,2, sharex=True, sharey=True)
    f.set_figwidth(12)
    f.set_figheight(6)
    ax = axes[0]
    ax.set_xlim(0,0.012)
    ax.set_ylim(0,0.012)
    ax.set_title("Frontal Electrodes Alpha strength")
    ax.xaxis.set_ticklabels("")
    ax.yaxis.set_ticklabels("")
    ax.xaxis.set_label_text("AF7")
    ax.yaxis.set_label_text("AF8")
    ax.scatter(df.AF7_alpha, df.AF8_alpha, s=2);

    ax = axes[1]
    
    ax.set_xlim(0,0.012)
    ax.set_ylim(0,0.012)
    ax.set_title("Frontal Electrodes Beta 1 strength")

    ax.xaxis.set_label_text("AF7")
    ax.yaxis.set_label_text("AF8")

    ax.scatter(df.AF7_beta_1, df.AF8_beta_1, s=2);


class MyExperiment(Experiment):
    muse = Muse("00:06:66:6F:F0:97", interval=0.25)
    