import open3d as o3d
import numpy as np


def main():
    pcd = read_data()
    
    plane_model, inlier_cloud, outlier_cloud = segment_table(pcd)

    pcd_np = np.asarray(pcd.points)

    # apply plane_model to each points
    pcd_np_new = np.apply_along_axis(plane_equation_func(plane_model), 1, pcd_np)
    # retrieve points above the table.
    indices_above_plane = np.where(pcd_np_new > 0.005)[0]
    above_plane_cloud = pcd.select_down_sample(indices_above_plane.tolist())
    # draw points on the table by green color
    above_plane_cloud.paint_uniform_color([0.0, 1.0, 0])

    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud, above_plane_cloud])


def plane_equation_func(plane_model):
    return lambda a: (plane_model[0] * a[0]) + (plane_model[1] * a[1]) + plane_model[2] * a[2] + plane_model[3]


def segment_table(pcd):
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.005,
                                            ransac_n=50,
                                            num_iterations=100)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = pcd.select_down_sample(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_down_sample(inliers, invert=True)

    return  plane_model, inlier_cloud, outlier_cloud


def read_data():
    pts_path = "data/billiard_table.ply"
    pcd = o3d.io.read_point_cloud(pts_path)
    return pcd


if __name__ == "__main__":
    main()