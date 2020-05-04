import open3d as o3d
import numpy as np


def main():
    device = 0
    config = o3d.io.AzureKinectSensorConfig()
    sensor = o3d.io.AzureKinectSensor(config)

    if not sensor.connect(device):
        raise RuntimeError('Failed to connect to sensor')

    while True:
        rgbd_image = sensor.capture_frame(True)
        if rgbd_image is None:
            continue
        print(rgbd_image)
        break

    # depth image should be converted to meter scale
    # ref. https://github.com/intel-isl/Open3D/issues/1437
    color, depth = np.asarray(rgbd_image.color).astype(np.uint8), np.asarray(rgbd_image.depth).astype(np.float32) / 1000.0
    detph = o3d.geometry.Image(depth)
    color = o3d.geometry.Image(color)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color, detph, depth_scale=1.0, convert_rgb_to_intensity=False)

    intrinsic = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        intrinsic)

    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    # save as PLY file
    o3d.io.write_point_cloud("data/billiard_table.ply", pcd)


if __name__ == "__main__":
    main()