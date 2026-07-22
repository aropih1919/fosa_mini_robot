import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.scan_sub = self.create_subscription(
            LaserScan, '/dummy_scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.run_loop)
        self.latest_scan = None

    def scan_callback(self, msg):
        # on garde les distances pour compute_cmd
        self.latest_scan = msg.ranges

    def compute_cmd(self):
        if self.latest_scan is None:
            return Twist()
        min_dist = min(self.latest_scan)
        self.get_logger().info(f'distance min: {min_dist:.2f}')
        return Twist()

    def run_loop(self):
        cmd = self.compute_cmd()
        # toujours pas de publication réelle

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