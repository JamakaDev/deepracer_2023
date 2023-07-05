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
    reward = speed
    
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    DIRECTION_THRESHOLD = 15.0
    SPEEDING_THRESHOLD = 2.2
    STEPS_THRESHOLD = 300 
    PROGRESS_FACTOR = 1.25
        

    # Penalize if the car goes off-track
    if not all_wheels_on_track or car_off_track:
        return 1e-3
    
    # Get direction of next waypoint
    prev_waypoint = waypoints[closest_waypoints[0]]
    next_waypoint = waypoints[closest_waypoints[1]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.degrees(math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0]))

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - car_direction)
    if direction_diff > 180:
        direction_diff -= 360

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
    reward += (1 - (distance_from_center / (track_width / 2))) * 0.2
    
    # Reward additional progress
    reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR

    if (abs(steering_angle) <= 5.0) and (speed >= SPEEDING_THRESHOLD) and direction_diff < DIRECTION_THRESHOLD:
        reward *= 2.5
    
    if (marker_3 - distance_from_center) >= 0.05: 
        reward *= 1.75
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward *= 2.25
    elif distance_from_center <= marker_2:
        reward *= 1.5
    elif distance_from_center <= marker_3:
        reward *= 1.1
    else:
        reward = 1e-3

    
    return float(reward)
