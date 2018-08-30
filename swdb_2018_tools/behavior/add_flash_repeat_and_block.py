



def add_repeat_to_stimulus_table(stimulus_table):
    repeat = []
    n = 0
    for i, image in enumerate(stimulus_table.image_name.values):
        if image != stimulus_table.image_name.values[i - 1]:
            n = 1
            repeat.append(n)
        else:
            n += 1
            repeat.append(n)
    stimulus_table['repeat'] = repeat
    return stimulus_table


def add_repeat_number_to_flash_response_df(flash_response_df, stimulus_table):
    stimulus_table = add_repeat_to_stimulus_table(stimulus_table)
    flash_response_df = analysis.flash_response_df.copy()
    flash_response_df = flash_response_df.merge(stimulus_table[['flash_number','repeat']],on='flash_number')
    return flash_response_df


def add_image_block_to_stimulus_table(stimulus_table):
    stimulus_table['image_block'] = np.nan
    for image_name in stimulus_table.image_name.unique():
        block = 0
        for index in stimulus_table[stimulus_table.image_name==image_name].index.values:
            if stimulus_table.iloc[index]['repeat'] == 1:
                block +=1
            stimulus_table.loc[index,'image_block'] = int(block)
    return stimulus_table


def add_image_block_to_flash_response_df(flash_response_df, stimulus_table):
    stimulus_table = add_image_block_to_stimulus_table(stimulus_table)
    flash_response_df = flash_response_df.merge(stimulus_table[['flash_number','image_block']],on='flash_number')
    return flash_response_df



if __name__ == '__main__':
    from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset import VisualBehaviorOphysDataset
    from visual_behavior.ophys.response_analysis.response_analysis import ResponseAnalysis

    #change this for AWS or hard drive
    cache_dir = r'\\allen\programs\braintv\workgroups\nc-ophys\visual_behavior\visual_behavior_pilot_analysis'
    experiment_id = 672185644
    dataset = VisualBehaviorOphysDataset(experiment_id, cache_dir=cache_dir)
    analysis = ResponseAnalysis(dataset)

    stimulus_table = analysis.dataset.stimulus_table.copy()
    flash_response_df = analysis.flash_response_df.copy()
    flash_response_df = add_repeat_number_to_flash_response_df(flash_response_df, stimulus_table)
    flash_response_df = add_image_block_to_flash_response_df(flash_response_df, stimulus_table)








