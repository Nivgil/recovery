import os
import json
import pickle
from bokeh.plotting import figure
from bokeh.palettes import Category10 as palette
from bokeh.models import NumeralTickFormatter
import argparse


def create_graphs(sim_num=None, variable=None, resolution='epoch'):
    CONFIGURATIONS_DIR = os.path.join(os.path.dirname(__file__))
    if sim_num is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--sim_num', action='store')
        parser.add_argument('--resolution', action='store', default='iteration')
        args = vars(parser.parse_args())
        sim_num = args['sim_num']
        resolution = args['resolution']
    folder_name = 'simulation_{}'.format(sim_num)
    colors = palette[10]

    if resolution == 'epoch':
        x_axis_label = 't [Epochs]'
    else:
        x_axis_label = 'Iterations'

    p_loss = figure(plot_width=600, plot_height=600, min_border=10, min_border_left=50,
                    x_axis_label=x_axis_label, y_axis_label='L(w(t))',
                    title="Training & Test Loss", y_axis_type='log', x_axis_type='log')
    p_loss.background_fill_color = "#fafafa"

    p_weight_norm = figure(plot_width=600, plot_height=600, min_border=10, min_border_left=50,
                           x_axis_label=x_axis_label, y_axis_label='||w(t)||',
                           title="The Norm of w(t)", x_axis_type='log', y_axis_type='log')
    p_weight_norm.background_fill_color = "#fafafa"

    p_gradient_norm = figure(plot_width=600, plot_height=600, min_border=10, min_border_left=50,
                             x_axis_label=x_axis_label, y_axis_label='||g||',
                             title="The Norm of Gradients", x_axis_type='log', y_axis_type='log')
    p_gradient_norm.background_fill_color = "#fafafa"

    p_error = figure(plot_width=600, plot_height=600, min_border=10, min_border_left=50,
                     x_axis_label=x_axis_label, y_axis_label='Error Rate',
                     title="Training & Test Error", x_axis_type='log')
    p_error.background_fill_color = "#fafafa"
    p_error.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

    idx = -1
    for file in os.listdir(os.path.join(CONFIGURATIONS_DIR, folder_name)):
        if file.endswith('.log'):
            continue
        with open(os.path.join(CONFIGURATIONS_DIR, folder_name, file), 'rb') as pickle_in:
            stats_test, stats_train = pickle.load(pickle_in)
        with open(os.path.join(CONFIGURATIONS_DIR, folder_name, file + '.log'), 'rb') as log_file:
            params_dict = json.load(log_file)
        idx += 1
        legend = params_dict['optimizer'] + '_' + str(params_dict['batch_size']) + '_' + str(params_dict['workers_num'])
        stats_train.export_data(handle_loss=p_loss,
                                handle_error=p_error,
                                handle_weight_norm=p_weight_norm,
                                handle_gradient_norm=p_gradient_norm,
                                legend=legend,
                                color=colors[idx % 10],
                                line_dash='solid',
                                resolution=resolution)
        min_score_test, mean_score_test = stats_test.export_data(handle_loss=p_loss,
                               handle_error=p_error,
                               legend=legend,
                               color=colors[idx % 10],
                               line_dash='dashed',
                               resolution=resolution)
    p_loss.legend.click_policy = "hide"
    p_loss.legend.location = 'bottom_left'
    p_error.legend.click_policy = "hide"
    p_weight_norm.legend.click_policy = "hide"
    p_weight_norm.legend.location = "top_left"
    p_gradient_norm.legend.click_policy = "hide"
    p_gradient_norm.legend.location = "bottom_left"

    return [p_loss, p_error, p_weight_norm, p_gradient_norm, min_score_test, mean_score_test]


if __name__ == '__main__':
    create_graphs()
