import open3d as o3d
import numpy as np
import random


def main():
    # read PLY file    
    pcd = read_data()

    # segment plane to detect table surface
    plane_model, inlier_cloud, outlier_cloud = segment_table(pcd)

    # segment points on table
    above_plane_cloud = segment_above_plane(outlier_cloud, plane_model)

    # apply dbscan to detect each balls and banks
    cluster_points = above_plane_cloud.cluster_dbscan(0.010, min_points=100)

    print(f"{len(np.unique(cluster_points)) - 1} clusters found")

    # color each clusters
    cluster_cloud_list = []
    for idx in np.unique(cluster_points):
        # generate random color for each cluster
        color = [0, random.randint(0, 10) / 10, random.randint(0, 10) / 10]
        cluster_cloud = above_plane_cloud.select_down_sample(np.where(cluster_points == idx)[0].tolist())
        cluster_cloud.paint_uniform_color(color)
        cluster_cloud_list.append(cluster_cloud)

    geometries = []
    geometries.append(inlier_cloud)
    geometries.extend(cluster_cloud_list)
    o3d.visualization.draw_geometries(geometries)


def segment_above_plane(outlier_cloud, plane_model):
    pcd_np = np.asarray(outlier_cloud.points)
    # apply plane_model to each points
    pcd_np_plane_model = np.apply_along_axis(plane_equation_func(plane_model), 1, pcd_np)
    # retrieve points above the table by thresholding
    indices_above_plane = np.where(pcd_np_plane_model > 0.005)[0]
    return outlier_cloud.select_down_sample(indices_above_plane.tolist())


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