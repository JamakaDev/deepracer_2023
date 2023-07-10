def reward_function(params):
    # Penalize if the car goes off-track
    if not params['all_wheels_on_track'] or params['is_offtrack']: return 1e-4
    else: return float(params['speed'])