#Bytesize-Jon-v1-070323 - Successful 25.536 sec lap down from 20.926
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
    
    # Max steps b4 episode is terminated (avoids running indefinitely)
    SPEEDING_THRESHOLD = 2.0
    STEERING_THRESHOLD = 15.0
    STEPS_THRESHOLD = 300.0 
    PROGRESS_FACTOR = 1.25
    
    # Attempting to reward higher speeds
    if speed > SPEEDING_THRESHOLD:
        reward = speed 
    else:
        speed * 0.5
    
    # Reduce reward if the car is steering too much
    if steering > STEERING_THRESHOLD:
        reward *= 0.9
    
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
        reward += (1 - (distance_from_center / (track_width / 2))) * 0.1
        
        # Reward additional progress
        reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR
    
    return float(reward)


# Bytesize-Jon-v2 
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
    
    SPEEDING_THRESHOLD = 2.0
    STEERING_THRESHOLD = 15.0
    STEPS_THRESHOLD = 300 
    PROGRESS_FACTOR = 1.1
    
    # Attempting to reward higher speeds
    reward = speed
    
    # Penalize if the car goes off-track
    if not all_wheels_on_track or speed < SPEEDING_THRESHOLD:
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
        else:
            reward *= 1.25
        
        # Reward if the car is closer to the center of the track
        reward += (1 - (distance_from_center / (track_width / 2))) * 0.1
        
        # Reward additional progress
        reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR
    
    return float(reward)

def reward_function(params):

    center_variance = params["distance_from_center"] / params["track_width"]

    left_lane = [24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88]
    
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118]
    
    right_lane = []
    
    fast = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,117,118]
    slow = [25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
    
    reward = 21

    if params["all_wheels_on_track"]:
        reward += 10
    else:
        reward -= 10

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]: reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]: reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.4: reward += 10
    else: reward -= 10
    
    if params["closest_waypoints"][1] in fast:
        if params["speed"] >= 2 : reward += 10
        else: reward -= 10
    elif params["closest_waypoints"][1] in slow:
        if params["speed"] <= 2 : reward += 10
        else: reward -= 10
            
    return float(reward)
