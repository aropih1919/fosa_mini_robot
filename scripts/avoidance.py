
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance')

        # topic factice pour le moment (sera remplacé par /scan au J2/J3)
        self.scan_sub = rospy.Subscriber('/dummy_scan', LaserScan, self.scan_callback)

        # publisher cmd_vel non branché encore (J3)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.rate = rospy.Rate(10)  # 10 Hz

    def scan_callback(self, msg):
        # lecture des données LiDAR : sera implémentée au J2
        pass

    def compute_cmd(self):
        # logique d'évitement : sera implémentée au J3/J4
        return Twist()

    def run(self):
        while not rospy.is_shutdown():
            cmd = self.compute_cmd()
            # pas de publication réelle encore, juste la structure
            self.rate.sleep()


if __name__ == '__main__':
    node = ObstacleAvoidance()
    try:
        node.run()
    except rospy.ROSInterruptException:
        pass