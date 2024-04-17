import math

#placeholder variables representing the robot's state
current_orientation = 0  #current orientation in degrees (0 is the original direction)
current_position = (0, 0)  #current position using (x, y) coordinates, start at origin
target_position = (0, 500)  #target position (end point)

#turn the robot by a certain angle (in degrees)
def turn(angle):
    global current_orientation
    current_orientation = (current_orientation + angle) % 360
    #placeholder for actual turn command to the robot
    print(f"Turning {angle} degrees")

#move the robot forward a certain distance
def move_forward(distance):
    global current_position, current_orientation
    # Calculate new position based on current orientation and distance moved
    rad = math.radians(current_orientation)
    delta_x = distance * math.cos(rad)
    delta_y = distance * math.sin(rad)
    current_position = (current_position[0] + delta_x, current_position[1] + delta_y)
    #placeholder for actual move command to the robot
    print(f"Moving forward {distance} units to position {current_position}")

# navigate around the obstacle and return to the path
def avoid_obstacle_and_return():
    distance=10
    #turn 90 degrees right to avoid the obstacle
    #depending if object is on left or right we can change where it turns
    turn(90)
    move_forward(distance)  #move forward an arbitrary distance to clear the obstacle

    #turn left to face the original direction
    #make it turn opposite way it turned before
    turn(-90)
    move_forward(distance)  #move forward the arbitrary distance to continue to clear obstacle
 

    #turn left to face the original path
    #make it turn same way as before
    turn(-90)
    #move forward until back on the original path
    #calculate distance to the original path
    distance_to_path = abs(current_position[0]-target_position[0])
    move_forward(distance_to_path)
 
    
    #turn right to face the original direction towards the target
    turn(90)

def check_for_obstacle():
        return True #obstacle spotted
        return False  #no obstacle
    
def main():
    while current_position[1] < target_position[1]:
        # check for an obstacle
        obstacle_detected = check_for_obstacle()
        
        if not obstacle_detected: #no object
            #move towards the target, but check for obstacles after every small step
            while current_position[1] < target_position[1] and not obstacle_detected:
                small_step = 1
                move_forward(small_step)
                obstacle_detected = check_for_obstacle()
        else: #if obstacle is detected

            avoid_obstacle_and_return() #navigate around the object, and should return to the path
            
            #avoided object, so set to false
            obstacle_detected = False
if __name__ == "__main__":
    main()
