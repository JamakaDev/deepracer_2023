def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_is_offtrack = params['is_offtrack']
    reward = speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_reversed = params['is_reversed']
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if not all_wheels_on_track or car_is_offtrack or is_reversed: return 1e-4
    if   distance_from_center <= marker_1: reward += 2
    elif distance_from_center <= marker_2: reward += 1.5
    elif distance_from_center <= marker_3: reward += 1.25
    else: return 1e-3
    
    return float(reward)
