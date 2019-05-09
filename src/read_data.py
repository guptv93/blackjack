import pandas as pd

def get_human_results():
    human_data = pd.read_csv("data.csv")

    group_count = human_data.groupby(['PlayerSum', 'DealerCard', 'HasAce']).size().reset_index().rename(columns={0: 'Count'})
    # print(group_count)

    hit_count = human_data.groupby(['PlayerSum', 'DealerCard', 'HasAce']).Action.value_counts().unstack(fill_value=0).loc[:,'HIT']
    # print(hit_count)

    state_hit_count = pd.merge(group_count, hit_count, on=['PlayerSum', 'DealerCard', 'HasAce'])
    # print(state_hit_count)

    state_hit_count['State'] = list(zip(state_hit_count.PlayerSum, state_hit_count.DealerCard, state_hit_count.HasAce))

    # print(state_hit_count)

    return state_hit_count


if __name__ == "__main__":
    get_human_results()