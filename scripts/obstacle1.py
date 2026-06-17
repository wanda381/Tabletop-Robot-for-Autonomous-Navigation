#!/usr/bin/env python3

#This program does the Canny edge detection on the live camera feed
 
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

# Initialize the CvBridge
bridge = CvBridge()

# Initialize the publisher for robot movement
cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def image_callback(msg):
    try:
        # Convert ROS Image message to OpenCV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        # Convert to grayscale
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Canny Edge Detection
        edges = cv2.Canny(gray_image, 100, 200)

        # Display the edges
        cv2.imshow("Edge Detection", edges)
        
        # Check the lower part of the image for edges
        height, width = edges.shape
        lower_half = edges[int(height/20):, :]  # Get the lower parts of the image
        
        # Count the non-zero edge pixels in the lower part
        edge_count = np.count_nonzero(lower_half)

        # If the number of edges in the lower part is greater than 3700 stop, move back and rotate
        if edge_count >= 3700:  
            rospy.loginfo("Edge Value: {}".format(edge_count))
            rospy.loginfo("Object too close.")
            
            # Stop the robot
            stop_cmd = Twist()
            rotate_cmd = Twist()
            move_cmd = Twist()
            
            cmd_pub.publish(stop_cmd)            
            
            move_cmd.linear.x = -0.2 # Move back
            cmd_pub.publish(move_cmd)
       
            rotate_cmd.angular.z = 0.10  # Rotate at a speed of 0.2 rad/s
            cmd_pub.publish(rotate_cmd)

         # If the number of edges in the lower part is between 700 and 3700 stop, move forward  
        elif edge_count< 3700 and edge_count>= 700:
            rospy.loginfo("Edge Value : {}".format(edge_count))
            rospy.loginfo("Moving Forward.")
            
            stop_cmd = Twist()
            rotate_cmd = Twist()
            move_cmd = Twist()
            
            cmd_pub.publish(stop_cmd)            
            
            move_cmd.linear.x = .2 # Move forward
            cmd_pub.publish(move_cmd)
            
        # If the number of edges in the lower part is between 400 and 700 stop, move forward      
        elif edge_count< 700 and edge_count>= 400:
            rospy.loginfo("Edge Value: {}".format(edge_count))
            rospy.loginfo("Edge Detected. Moving Forward.")
            
            move_cmd = Twist()
            
            move_cmd.linear.x = 0.25 # Move froward
            cmd_pub.publish(move_cmd)
        # If the number of edges in the lower part is between 400 and 100 stop, move back, rotate 
        elif edge_count< 400 and edge_count >=100:
            rospy.loginfo("Edge Value: {}".format(edge_count))
            rospy.loginfo("Edge too close.")
            
            # Stop the robot
            stop_cmd = Twist()
            rotate_cmd = Twist()
            move_cmd = Twist()
            
            cmd_pub.publish(stop_cmd)            
            
            move_cmd.linear.x = -0.2 # Move back
            cmd_pub.publish(move_cmd)
       
            rotate_cmd.angular.z = 0.20  # Rotate at a speed of 0.2 rad/s
            cmd_pub.publish(rotate_cmd)    
        #else stop, move back and rotate completely        
        else : 
            # Stop the robot
            rospy.loginfo("Edge Value: {}".format(edge_count))
            rospy.loginfo("Robot stopping")
            stop_cmd = Twist()
            
            cmd_pub.publish(stop_cmd)
            
            move_cmd = Twist()
            move_cmd.linear.x = -0.5 # Move back
            cmd_pub.publish(move_cmd)
            
            rotate_cmd = Twist()
            rotate_cmd.angular.z = 6  # Rotate at a speed of 0.2 rad/s
            cmd_pub.publish(rotate_cmd) 
        
        cv2.waitKey(1)
        #rospy.sleep(1)

    except Exception as e:
        rospy.logerr(f"Error processing image: {e}")

def main():
    rospy.init_node('edge_detection', anonymous=True)

    # Subscribe to the RGB image topic
    rospy.Subscriber('/camera/rgb/image_raw', Image, image_callback)

    # Keep the node running
    rospy.spin()

if __name__ == "__main__":
    main()

rospy.sleep(1)
