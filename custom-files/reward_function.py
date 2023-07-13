import math
def reward_function(params):
    
    all_wheels_on_track = params['all_wheels_on_track']
    car_direction = params['heading']
    car_off_track = params['is_offtrack']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_width = params['track_width']
    waypoints = params['waypoints']
    x_coord = params['x']
    y_coord = params['y']
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    reward = speed
    
    
    DIRECTION_THRESHOLD = 10.0
    SPEEDING_THRESHOLD = 2.0
    STEPS_THRESHOLD = 275 
    PROGRESS_FACTOR = 1.25
        

    if not all_wheels_on_track or car_off_track: return 1e-3
    
    prev_waypoint = waypoints[closest_waypoints[0]]
    next_waypoint = waypoints[closest_waypoints[1]]

    track_direction = math.degrees(math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0]))

    direction_diff = abs(track_direction - car_direction)
    if direction_diff > 180: direction_diff -= 360

    if direction_diff > DIRECTION_THRESHOLD: reward *= 0.5
    else: reward *= 1.25
    
    reward += (1 - (distance_from_center / marker_3)) * 0.2
    reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR

    if (abs(steering_angle) <= 5.0) and (speed >= SPEEDING_THRESHOLD) and (marker_3 - distance_from_center) >= 0.1: reward *= 3  
    
    if distance_from_center <= marker_1: reward = reward * 3 if speed >= SPEEDING_THRESHOLD else reward * 2
    elif distance_from_center <= marker_2: reward *= 1.5
    elif distance_from_center <= marker_3: reward *= 1.1
    else: reward = 1e-3
     
    
    return float(reward)