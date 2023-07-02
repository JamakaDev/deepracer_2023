def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_direction = params['heading']
    distance_from_center = params['distance_from_center']
    progress = params['progress']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_width = params['track_width']
    waypoints = params['waypoints']
    x_coord = params['x']
    y_coord = params['y']
    
    reward = speed

    SPEEDING_THRESHOLD = 2.0
    STEERING_THRESHOLD = 15.0
    STEPS_THRESHOLD = 300.0 
    PROGRESS_FACTOR = 1.25
    
    
    # Attempting to reward higher speeds when going straight
    if steering_angle == 0 and speed > SPEEDING_THRESHOLD:
        reward *= speed
    
    # Reduce reward if the car is steering too much
    if steering > STEERING_THRESHOLD:
        reward *= 0.9
    
    # Reduce reward if the car is going slow
    if speed < SPEEDING_THRESHOLD:
        reward *= 0.9
    
    # Penalize if the car goes off-track
    if not all_wheels_on_track:
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
        reward += (1 - (distance_from_center / (track_width / 2))) * 0.1
        
        # Reward additional progress
        reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR
    
    return float(reward)

