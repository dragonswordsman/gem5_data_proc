#!/usr/bin/env python3

import os.path as osp
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns

import sys
sys.path.append('..')

import common as c
import target_stats as t

stat_dir = osp.expanduser('~/gem5-results-2017/xbar-rand-hint')

benchmarks = [*c.get_spec2017_int(), *c.get_spec2017_fp()]
points = []
for b in benchmarks:
    for i in range(0, 3):
        points.append(f'{b}_{i}')
stat_files = [osp.join(stat_dir, point, 'stats.txt') for point in points]

matrix = {}
for point, stat_file in zip(points, stat_files):
    d = c.get_stats(stat_file, t.packet_targets, re_targets=True)
    matrix[point] = d
df = pd.DataFrame.from_dict(matrix, orient='index')

fig, ax = plt.subplots()
# ax.set_ylim((0, 1.1))
width = 0.85

colors = ['#7d5c80', '#016201', '#fefe01', 'orange', '#cccccc', '#820000']
cumulative = np.array([0.0] * len(df))
rects = []
names = ['TotalP', 'KeySrcP']

rect = plt.bar(df.index, df['TotalP'].values, bottom=cumulative,
        edgecolor='grey', color='white', width=width)
rects.append(rect)

rect = plt.bar(df.index, df['KeySrcP'].values, bottom=cumulative,
        edgecolor='black', color=colors[0], width=width)
rects.append(rect)

benchmarks_ordered = []
for point in df.index:
    if point.endswith('_0'):
        benchmarks_ordered.append(point.split('_')[0])

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(np.arange(-0.5, 20 * 3 + 1, 3)))
ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(np.arange(1, 20 * 3 + 1, 3)))

ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
# ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

for tick in ax.xaxis.get_major_ticks():
    # tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)

for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    # tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')

ax.set_xticklabels(benchmarks_ordered, minor=True, rotation=90)

ax.set_ylabel('Number of pointers')
ax.set_xlabel('Simulation points from SPEC 2017')
ax.legend(rects, names, fontsize='small', ncol=6)

plt.tight_layout()
for f in ['eps', 'png']:
    plt.savefig(f'./{f}/crit_pointers.{f}', format=f'{f}')

plt.show()

