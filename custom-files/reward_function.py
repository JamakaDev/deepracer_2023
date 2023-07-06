import math

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
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    reward = speed

    DIRECTION_THRESHOLD = 10.0
    MAX_STEPS = 300 
    PROGRESS_FACTOR = 1.15
    SPEED_THRESHOLD = 3.0
    
    # Penalize if the car goes off-track
    if not all_wheels_on_track and car_is_offtrack:
        return 1e-3

    if distance_from_center <= marker_1:
        reward *= 2
    elif distance_from_center <= marker_2:
        reward *= 1.5
    elif distance_from_center <= marker_3:
        reward *= 1.25
    else:
        return 1e-3

    # Get direction of next waypoint
    next_point = waypoints[params['closest_waypoints'][1]]
    track_direction = math.atan2(next_point[0] - x_coord, next_point[1] - y_coord)
    track_direction = math.degrees(track_direction)
    
    # Get angle between the car direction and the track direction
    direction_diff = abs(track_direction - car_direction)
    if direction_diff > 180: direction_diff = 360 - direction_diff
    
    # Penalize if the diff too large
    if direction_diff > DIRECTION_THRESHOLD: reward *= 0.5
    else: reward *= 1.25
    
    # Reward if the car is closer to the center of the track
    reward += (1 - (distance_from_center / (track_width / 2))) * 0.15
    
    # Reward additional progress
    reward += (progress - (steps / MAX_STEPS)) * PROGRESS_FACTOR
    
    if speed > SPEED_THRESHOLD and distance_from_center <= (track_width*.25): reward *= 2.5
    
    return float(reward)