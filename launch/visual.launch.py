from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # declare arguments
    arguments = []
    arguments.append(
        DeclareLaunchArgument(
            "using_left_arm",
            default_value="true",
            description="Arguement to determine wether to use left arm.",
        )
    )
    arguments.append(
        DeclareLaunchArgument(
            "using_right_arm",
            default_value="true",
            description="Arguement to determine wether to use right arm.",
        )
    )
    arguments.append(
        DeclareLaunchArgument(
            "using_gazebo",
            default_value="false",
            description="Arguement to determine wether to parse car_description with gazebo.",
        )
    )

    # initialize arguments
    using_left_arm = LaunchConfiguration("using_left_arm")
    using_right_arm = LaunchConfiguration("using_right_arm")
    using_gazebo = LaunchConfiguration("using_gazebo")

    # variables
    robot_description_package = FindPackageShare("separable_jaws_description")
    robot_description_file = PathJoinSubstitution([
        robot_description_package,
        "urdf",
        "separable_jaws.xacro"
    ])
    rviz_config_file = PathJoinSubstitution([
        robot_description_package,
        "config",
        "urdf.rviz"
    ])
    # convert xacro into urdf
    robot_description = Command([
        PathJoinSubstitution([
            FindExecutable(name="xacro")
        ]),
        " ",
        robot_description_file,
        " ",
        "using_left_arm:=",
        using_left_arm,
        " ",
        "using_right_arm:=",
        using_right_arm,
        " ",
        "using_gazebo:=",
        using_gazebo,
    ])

    # declare nodes
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[
            {"robot_description" : robot_description}
        ],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    nodes = [
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ]

    return LaunchDescription(arguments + nodes)
