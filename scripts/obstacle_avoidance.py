import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidance(Node):
    """Nœud de contrôle et évitement d'obstacles (logique réactive, sans SLAM)."""

    def __init__(self):
        super().__init__('obstacle_avoidance')

        self.declare_parameter('distance_seuil', 0.5)
        self.declare_parameter('distance_ralentissement', 1.0)
        self.declare_parameter('vitesse_lineaire', 0.2)
        self.declare_parameter('vitesse_angulaire', 0.5)

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.run_loop)

        self.latest_scan = None

    def scan_callback(self, msg):
        # stocke les distances brutes du dernier scan
        self.latest_scan = msg.ranges

    def _distance_min(self):
        # ignore les valeurs invalides (0 ou infini)
        valides = [d for d in self.latest_scan if d > 0.0]
        return min(valides) if valides else None

    def compute_cmd(self):
        cmd = Twist()
        if self.latest_scan is None:
            return cmd

        seuil = self.get_parameter('distance_seuil').value
        seuil_ralenti = self.get_parameter('distance_ralentissement').value
        v_lin = self.get_parameter('vitesse_lineaire').value
        v_ang = self.get_parameter('vitesse_angulaire').value

        min_dist = self._distance_min()
        if min_dist is None:
            return cmd

        if min_dist < seuil:
            # obstacle proche : rotation sur place
            cmd.angular.z = v_ang
        elif min_dist < seuil_ralenti:
            # zone d'approche : ralentissement progressif
            facteur = (min_dist - seuil) / (seuil_ralenti - seuil)
            cmd.linear.x = v_lin * facteur
        else:
            # voie libre : vitesse de croisière
            cmd.linear.x = v_lin

        return cmd

    def run_loop(self):
        self.cmd_pub.publish(self.compute_cmd())


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