def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_direction = params['heading']
    car_is_offtrack = params['is_offtrack']
    distance_from_center = params['distance_from_center']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_width = params['track_width']
    waypoints = params['waypoints']
    x_coord = params['x']
    y_coord = params['y']
    
    # Max steps b4 episode is terminated (avoids running indefinitely)
    MAX_STEPS = 275 
    PROGRESS_FACTOR = 1.25
    
    # Attempting to reward higher speeds
    reward = speed
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Penalize if the car goes off-track
    if not all_wheels_on_track and car_is_offtrack: return 1e-3
    
    # Get direction of next waypoint
    next_index = int((progress / 100) * (len(waypoints) - 1))
    next_coord = waypoints[next_index]
    track_direction = next_coord[0] - x_coord, next_coord[1] - y_coord
    
    # Get angle between the car direction and the track direction
    direction_diff_x = abs(track_direction[0] - car_direction)
    direction_diff_y = abs(track_direction[1] - car_direction)
    
    # Penalize if the car deviates from the track direction
    if direction_diff_x > 1.0 or direction_diff_y > 1.0: reward *= 0.5
    else: reward *= 1.25
    
    # Reward if the car is closer to the center of the track
    reward += (1 - (distance_from_center / marker_3)) * 0.2
    
    # Reward additional progress
    reward += (progress - (steps / MAX_STEPS)) * PROGRESS_FACTOR

    if (marker_3 - distance_from_center) >= 0.1: reward *= 1.5
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1: reward *= 2
    elif distance_from_center <= marker_2: reward *= 1.5
    elif distance_from_center <= marker_3: reward *= 1.25
    else: reward = 1e-3
    
    return float(reward)