import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from math import pi, cos
from src.Other import Colours as CP
from src.Setups.TSP.TSP_Inputs.Optimums import get_best_path


class GraphingHelper:
    def __init__(self, fnum):
        graph_style = 5
        plt.style.use(plt.style.available[graph_style])  # 5, 14, 22
        plt.figure(figsize=(30, 15))
        sns.set_context("paper")

        self.long_names = ['Longitude (Range shifted)', 'Latitude (Range shifted)']
        self.short_names = ['Lat', 'Lon']
        self.cities = self.read_tsp_file(fnum)
        self.opt, _, _ = get_best_path(fnum)
        self.palette = [CP.SPIRIT_0, CP.SPIRIT_1, CP.SPIRIT_2, CP.SPIRIT_9, CP.SPIRIT_7, CP.SPIRIT_6]
        plt.style.use(plt.style.available[13])  ##4, 13, 21
        self.screen_width = 12
        self.single_plot_size = (self.screen_width, 6)
        self.double_plot_size = (self.screen_width, 8)
        self.quad_plot_size = (self.screen_width, 12)

    # region Display Methods
    def start_up_display(self):
        self.cities.plot.scatter(x=self.long_names[1], y=self.long_names[0], c=self.cities.index.get_values(), colormap='winter')
        plt.gcf().set_size_inches(self.single_plot_size)
        plt.title('City Locations (Normalized to origin of 0)')

    def plot_run(self, run_history, hax=None):
        run_history.columns = ['Fitness', 'Route']
        run_history['Fitness'].plot(color=CP.SPIRIT_0)
        plt.axhline(y=self.opt, color=CP.SPIRIT_5, label='Optimum')
        if hax:
            plt.axhline(y=hax, color=CP.SPIRIT_5, label='Optimum')
        plt.gcf().set_size_inches(self.single_plot_size)

    def generation_display(self, generation, fitness, individual, alt_tile=False):
        title = 'Path at Generation {: <5}:   {:4.2f}'
        if alt_tile: title = 'Using {} Method:   {:4.2f}'
        x = self.cities[self.long_names[1]]
        y = self.cities[self.long_names[0]]
        self.cities.plot.scatter(x=self.long_names[1], y=self.long_names[0],  c=self.cities.index.get_values(), colormap='winter')

        tour_len = len(self.cities)
        for i in range(tour_len):
            c1 = individual[i - 1]
            c2 = individual[i]
            per = 2 * pi * i / tour_len
            red_mod = max(cos(per), 0) * 0.4
            bright_mod = -min(cos(per), 0) * 0.4
            plt.plot([x[c1], x[c2]], [y[c1], y[c2]], color=[1 - red_mod, bright_mod, bright_mod])
        plt.title(title.format(generation, fitness))
        plt.gcf().set_size_inches(self.single_plot_size)
        plt.show()

    def alt_generation_display(self, generation, fitness, individual, alt_tile=False):
        title = 'Path at Generation {: <5}:   {:4.2f}'
        if alt_tile: title = 'Using {} Method:   {:4.2f}'
        x = self.cities[self.long_names[1]]
        y = self.cities[self.long_names[0]]

        tour_len = len(self.cities)
        for i in range(tour_len):
            c1 = individual[i - 1]
            c2 = individual[i]
            hue = (0.8 * i / tour_len) + 0.1
            plt.plot([x[c1], x[c2]], [y[c1], y[c2]], color=[1, hue, 0], marker='o')
        plt.title(title.format(generation, fitness))
        plt.gcf().set_size_inches(self.single_plot_size)
        plt.show()

    def quad_plot(self, avgs, opts):
        fig, axes = plt.subplots(ncols=2, nrows=2, figsize=self.quad_plot_size)
        plt.subplots_adjust(wspace=0.2, hspace=0.2)

        val_y_lim = max(avgs.iloc[len(avgs) - 1]) * 1.05
        per_y_lim = max(((avgs.iloc[len(avgs) - 1] / self.opt) - 1) * 100) * 1.25

        def plot_df(df, ax1, ax2, per):
            num = 0
            columns = [column for column in df]
            if ax2 == 0: axes[ax1, ax2].set_title('Averaged')
            if ax2 == 1: axes[ax1, ax2].set_title('Best')
            for column in columns:
                if per:
                    per_col = (((df[column] / self.opt) - 1) * 100)
                    per_col.plot(ax=axes[ax1, ax2], color=self.palette[num], alpha=0.66, legend=True)
                    axes[ax1, ax2].set_ylim([-0.1, per_y_lim])
                else:
                    df[column].plot(ax=axes[ax1, ax2], color=self.palette[num], legend=True)
                    axes[ax1, ax2].set_ylim([self.opt * 0.999, val_y_lim])
                num += 1
            if per:
                axes[ax1, ax2].set_ylabel('Percent Larger')
                axes[ax1, ax2].axhline(y=0, color=CP.SPIRIT_5, label='Optimum')
            else:
                axes[ax1, ax2].set_ylabel('Fitness')
                axes[ax1, ax2].axhline(y=self.opt, color=CP.SPIRIT_5, label='Optimum')

        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(avgs, 0, 0, False)
        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(opts, 0, 1, False)
        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(avgs, 1, 0, True)
        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(opts, 1, 1, True)

    def modular_dual_plot(self, avgs, opts, percent_plot):
        fig, axes = plt.subplots(ncols=2, nrows=1, figsize=self.single_plot_size)
        plt.subplots_adjust(wspace=0.2, hspace=0.2)
        axes[0].set_title('Averaged')
        axes[1].set_title('Best')

        def plot_pers(df, ax1):
            num = 0
            columns = [column for column in df]
            per_y_lim = max(((avgs.iloc[len(avgs) - 1] / self.opt) - 1) * 100) * 1.25
            axes[ax1].set_ylim([-0.1, per_y_lim])
            for column in columns:
                per_col = (((df[column] / self.opt) - 1) * 100)
                per_col.plot(ax=axes[ax1], color=self.palette[num], alpha=0.66, legend=True)
                num += 1
            axes[ax1].set_ylabel('Percent Larger')
            axes[ax1].axhline(y=0, color=CP.SPIRIT_5, label='Optimum')

        def plot_vals(df, ax1):
            num = 0
            columns = [column for column in df]
            val_y_lim = max(avgs.iloc[len(avgs) - 1]) * 1.05
            axes[ax1].set_ylim([self.opt * 0.999, val_y_lim])
            for column in columns:
                df[column].plot(ax=axes[ax1], color=self.palette[num], legend=True)
                num += 1
            axes[ax1].set_ylabel('Fitness')
            axes[ax1].axhline(y=self.opt, color=CP.SPIRIT_5, label='Optimum')

        plot_df = plot_pers if percent_plot else plot_vals

        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(avgs, 0)
        with pd.plotting.plot_params.use('x_compat', True):
            plot_df(opts, 1)

    def indiv_dual_plot(self, indiv_1, indiv_2):
        fig, axes = plt.subplots(ncols=2, nrows=1, figsize=self.single_plot_size)
        plt.subplots_adjust(wspace=0.2, hspace=0.2)

        def alt_generation_display(init_tuple, ax):
            init_method, individual = init_tuple
            title = 'Using {} Method'
            x = self.cities[self.long_names[1]]
            y = self.cities[self.long_names[0]]

            tour_len = len(self.cities)
            for i in range(tour_len):
                c1 = individual[i - 1]
                c2 = individual[i]
                hue = (0.8 * i / tour_len) + 0.1
                plt.plot([x[c1], x[c2]], [y[c1], y[c2]], ax=axes[ax, 0], color=[1, hue, 0], marker='o')
            plt.title(title.format(init_method))

        with pd.plotting.plot_params.use('x_compat', True):
            alt_generation_display(indiv_1, 0)
        with pd.plotting.plot_params.use('x_compat', True):
            alt_generation_display(indiv_2, 1)
    # endregion


    '''
    def long_plot(avgs, opts):
    colours = [CP.SPIRIT_0, CP.SPIRIT_1, CP.SPIRIT_2, CP.SPIRIT_9, CP.SPIRIT_7, CP.SPIRIT_6]
    fig, axes = plt.subplots(nrows=2, figsize=(12, 24))
    plt.subplots_adjust(wspace=0.25, hspace=0.4)
    def plot_df(df, axis):
        num = 0
        for column in df.drop('x', axis=1):
            num += 1
            # plt.plot(df['x'], df[column], ax=axes[axis], marker='', color=colours[num], linewidth=1, alpha=0.9, label=column)
            df[column].plot(ax=axes[axis], color=colours[num], legend=True)
            #((df[column] / opt_dist) - 1).plot(ax=axes[axis], color=colours[num], alpha=0.0, secondary_y=True, legend=False)
            #df.plot(ax=axes[axis], color=CP.KIKI_6, legend=True)
            #df.plot(ax=axes[axis], color=CP.KIKI_7, alpha=0.33, secondary_y=True, legend=True)
            #df.plot(ax=axes[axis], color=CP.KIKI_6, alpha=0.33, secondary_y=True, legend=True)

    plot_df(avgs, 0)
    axes[0].axhline(y=self.opt, color=CP.SPIRIT_5, label='Optimum')
    axes[0].set_title("Average fitnesses over multiple runs", fontsize=12, fontweight=0, color=CP.SPIRIT_3)
    axes[0].set_xlabel("Generations")
    axes[0].set_ylabel("Fitness")
    axes[0].right_ax.set_ylabel('Relative Fitness')

    plot_df(opts, 1)
    axes[1].axhline(y=self.opt, color=CP.SPIRIT_5, label='Optimum')
    axes[1].set_title("Best fitnesses over multiple runs", fontsize=12, fontweight=0, color=CP.SPIRIT_3)
    axes[1].set_xlabel("Generations")
    axes[1].set_ylabel("Fitness")
    axes[1].right_ax.set_ylabel('Relative Fitness')
    '''

    # region Initialization
    def read_tsp_file(self, fnum):
        if fnum == 1:
            fname = "TSP_WesternSahara_29.txt"
        elif fnum == 2:
            print('Warning! Takes approximately 1.5 seconds per decade')
            fname = "TSP_Uruguay_734.txt"
        elif fnum == 3:
            print('Warning! Takes approximately 45 seconds per decade')
            fname = "TSP_Canada_4663.txt"
        else:
            print('Warning! Invalid seletion. Defaulting to test')
            fname = "TSP_Testbed_10.txt"

        script_dir = os.path.dirname(__file__)  # absolute path for directory/folder this script is in
        abs_file_path = os.path.join(script_dir, 'TSP_Inputs', fname)

        # Uses indexing from 0, rather than 1, by skipping the first column in the data.
        cities = pd.read_csv(abs_file_path, usecols=[1, 2], header=None, delimiter=' ')
        cities.columns = self.short_names
        cities.index.names = ['City']
        # Translate and invert the x values, and translate the y values
        cities['Lat'] = cities['Lat'] - (cities['Lat'].min() + (cities['Lat'].max() - cities['Lat'].min()) / 2)
        cities['Lon'] = (cities['Lon'].min() + (cities['Lon'].max() - cities['Lon'].min()) / 2) - cities['Lon']
        cities.columns = self.long_names

        return cities
# endregion