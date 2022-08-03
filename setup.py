from setuptools import setup

package_name = 'dvrk_python'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anton Deguet',
    maintainer_email='anton.deguet@jhu.edu',
    description='dVRK Python client for ROS2',
    license='MIT',
    entry_points={
        'console_scripts': [
            'dvrk_arm_test = dvrk_python.dvrk_arm_test:main'
        ],
    },
)
