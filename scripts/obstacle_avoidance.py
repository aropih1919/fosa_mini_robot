import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.declare_parameter('distance_seuil', 0.5)
        self.declare_parameter('vitesse_lineaire', 0.2)
        self.declare_parameter('vitesse_angulaire', 0.5)

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.run_loop)
        self.latest_scan = None

    def scan_callback(self, msg):
        self.latest_scan = msg.ranges

    def compute_cmd(self):
        cmd = Twist()
        if self.latest_scan is None:
            return cmd

        seuil = self.get_parameter('distance_seuil').value
        v_lin = self.get_parameter('vitesse_lineaire').value
        v_ang = self.get_parameter('vitesse_angulaire').value

        min_dist = min(self.latest_scan)
        if min_dist < seuil:
            # obstacle proche : on tourne
            cmd.linear.x = 0.0
            cmd.angular.z = v_ang
        else:
            # rien devant : on avance
            cmd.linear.x = v_lin
            cmd.angular.z = 0.0
        return cmd

    def run_loop(self):
        cmd = self.compute_cmd()
        self.cmd_pub.publish(cmd)

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