def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_direction = params['heading']
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
    MAX_STEPS = 300 
    progress_factor = 1.15
    
    # Attempting to reward higher speeds
    reward = speed
    
    # Penalize if the car goes off-track
    if not all_wheels_on_track and speed < 2:
        reward = 1e-3
    else:
        # Get direction of next waypoint
        next_index = int((progress / 100) * (len(waypoints) - 1))
        next_coord = waypoints[next_index]
        track_direction = next_coord[0] - x_coord, next_coord[1] - y_coord
        
        # Get angle between the car direction and the track direction
        direction_diff_x = abs(track_direction[0] - car_direction)
        direction_diff_y = abs(track_direction[1] - car_direction)
        
        # Penalize if the car deviates from the track direction
        if direction_diff_x > 1.0 or direction_diff_y > 1.0:
            reward *= 0.5
        
        # Reward if the car is closer to the center of the track
        reward += (1 - (distance_from_center / (track_width / 2))) * 0.15
        
        # Reward additional progress
        reward += (progress - (steps / MAX_STEPS)) * progress_factor
    
    return float(reward)