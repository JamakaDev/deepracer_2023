#Bytesize-Base-v1 - Successful 20.926 sec lap
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
    
    
    DIRECTION_THRESHOLD = 10.0
    SPEEDING_THRESHOLD = 2.25
    STEPS_THRESHOLD = 250 
    PROGRESS_FACTOR = 1.25
        

    # Penalize if the car goes off-track
    if not all_wheels_on_track or car_off_track:
        reward = 1e-3
    else:
        # Get direction of next waypoint
        prev_waypoint = waypoints[closest_waypoints[0]]
        next_waypoint = waypoints[closest_waypoints[1]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.degrees(math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0]))

        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - car_direction)
        if direction_diff > 180:
            direction_diff -= 360

        # Penalize the reward if the difference is too large
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.5
        
        # Reward if the car is closer to the center of the track
        reward += (1 - (distance_from_center / (track_width / 2))) * 0.1
        
        # Reward additional progress
        reward += (progress - (steps / STEPS_THRESHOLD)) * PROGRESS_FACTOR

        if speed >= SPEEDING_THRESHOLD:
            reward *= 1.5

        if (-5.0 <= steering_angle <= 5.0) and (speed >= SPEEDING_THRESHOLD):
            reward *= 2

        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center   <= 0.1 * track_width: reward *= 2
        elif distance_from_center <= 0.25 * track_width: reward *= 1.25
        elif distance_from_center <= 0.5 * track_width: reward *= 1.1
        else: reward = 1e-3
       
    
    return float(reward)

