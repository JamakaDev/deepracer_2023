def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_is_offtrack = params['is_offtrack']
    speed = params['speed']
    next_step = params['closest_waypoints'][1]
    is_reversed = params['is_reversed']

    if not all_wheels_on_track or car_is_offtrack or is_reversed: return 1e-4
    if next_step in list(range(20, 40)) and speed > 2: return 1e-3
    return float(speed)