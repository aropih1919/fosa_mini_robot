import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        # topic factice, sera remplacé par /scan au J3
        self.scan_sub = self.create_subscription(
            LaserScan, '/dummy_scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.run_loop)

    def scan_callback(self, msg):
        pass

    def compute_cmd(self):
        return Twist()

    def run_loop(self):
        cmd = self.compute_cmd()
        # pas de publication réelle encore

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()