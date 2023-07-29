def reward_function(params):

    center_variance = params["distance_from_center"] / params["track_width"]

    left_lane = [
        24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,66,67,
        68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88
    ]
    center_lane = [
        0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,44,45,
        46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,89,90,91,
        92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,
        111,112,113,114,115,116,117,118
    ]  
    
    fast = [
        0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,46,47,
        48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,
        72,73,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,
        100,101,102,103,104,105,106,107,108,109,110,111,112,113,117,118
    ]
    slow = [
        25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45
    ]
    
    reward = 42.0

    if params["all_wheels_on_track"] or not params["is_offtrack"] or not params["is_reversed"]: reward += 10.0
    else: return 1e-4

    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]: reward += 10.0
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.5: reward += 10.0
    else: reward -= 10.0
    
    if params["closest_waypoints"][1] in fast:
        if params["speed"] >= 3 : reward += 20.0
        elif params["speed"] >= 2 : reward += 10.0
        else: reward -= 10.0
    elif params["closest_waypoints"][1] in slow:
        if params["speed"] <= 2 : reward += 10.0
        else: reward -= 10.0

    if not params["waypoints"][params["closest_waypoints"][1]] in list(range(20,105)) and params["speed"] > 3: reward += 100.0

    return float(reward) if reward > 0 else 1e-3