from visual_behavior.visualization.extended_trials import daily

def plot_session_summary(dataset):

    mouse_id = "M{}".format(dataset.metadata['donor_id'].values[0])

    fig = daily.make_daily_figure(
        dataset.all_trials,
        mouse_id=mouse_id,
        reward_window=[0.15, 0.75],
        sliding_window=100,
    )

    return fig
