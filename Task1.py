# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib.patches import Rectangle
# #
# # # --- 1. BRICK AND PROBLEM CONSTANTS ---
# # BRICK_VOLUME = 200 * 100 * 100  # mm³
# # TOTAL_BRICKS = 10000
# # WALL_THICKNESS = 200  # mm
# # TARGET_VOLUME = TOTAL_BRICKS * BRICK_VOLUME  # mm³, volume occupied by bricks
# #
# #
# # # --- 2. DEFINE THE CRITICAL EQUATION ---
# # def calculate_brick_volume(L, W, H, t=WALL_THICKNESS):
# #     """
# #     Calculates the total volume of bricks used for a hollow cuboid.
# #     L, W, H: Outer dimensions (mm).
# #     t: Wall thickness (mm).
# #     """
# #     inner_vol = (L - 2 * t) * (W - 2 * t) * (H - 2 * t)
# #     outer_vol = L * W * H
# #     brick_vol = outer_vol - inner_vol
# #     return brick_vol
# #
# #
# # def calculate_brick_count(L, W, H, t=WALL_THICKNESS):
# #     """Calculates the number of bricks used for given dimensions."""
# #     brick_vol = calculate_brick_volume(L, W, H, t)
# #     return brick_vol / BRICK_VOLUME
# #
# #
# # # --- 3. FIND OPTIMAL DIMENSIONS (NEAR-CUBE) ---
# # # Solve S³ - (S-400)³ = 20,000,000,000 for S
# # # This is the equation for a perfect cube. We know S ~ 4280.9mm.
# # # We will search for integer dimensions (multiples of 100mm) around this value.
# #
# # # Define search space: dimensions must be multiples of 100 and >= 400.
# # min_dim = 400
# # max_dim = 5000
# # step = 100  # mm
# #
# # best_config = None
# # best_internal_volume = 0
# # best_brick_diff = float('inf')  # Difference from 10,000 bricks
# #
# # # Iterate through possible dimensions. Assume L <= W <= H to avoid duplicates.
# # print("Searching for optimal dimensions near a cube...")
# # for L in range(min_dim, max_dim + 1, step):
# #     for W in range(L, max_dim + 1, step):  # Start W from L to avoid symmetric duplicates
# #         for H in range(W, max_dim + 1, step):  # Start H from W
# #             # Calculate brick count for this configuration
# #             n_bricks = calculate_brick_count(L, W, H)
# #
# #             # Check if it's a valid candidate (uses all bricks or very close)
# #             brick_diff = abs(n_bricks - TOTAL_BRICKS)
# #             # We are looking for configurations that use *exactly* or very nearly 10,000 bricks.
# #             if brick_diff < 50:  # Look within a tolerance of 50 bricks
# #                 internal_vol = (L - 2 * WALL_THICKNESS) * (W - 2 * WALL_THICKNESS) * (H - 2 * WALL_THICKNESS)
# #
# #                 # Check if this is the best candidate so far
# #                 # Priority 1: Uses exactly 10,000 bricks (or closest)
# #                 # Priority 2: If tie, largest internal volume
# #                 if (brick_diff < best_brick_diff or
# #                         (brick_diff == best_brick_diff and internal_vol > best_internal_volume)):
# #                     best_config = (L, W, H)
# #                     best_internal_volume = internal_vol
# #                     best_brick_diff = brick_diff
# #                     print(f"New best candidate: L={L}, W={W}, H={H}, "
# #                           f"Bricks={n_bricks:.2f}, Diff={brick_diff:.2f}, "
# #                           f"Internal Vol={internal_vol / 1e9:.2f} billion mm³")
# #
# # # Output the final best configuration
# # L_opt, W_opt, H_opt = best_config
# # n_bricks_opt = calculate_brick_count(L_opt, W_opt, H_opt)
# # internal_vol_opt = (L_opt - 2 * WALL_THICKNESS) * (W_opt - 2 * WALL_THICKNESS) * (H_opt - 2 * WALL_THICKNESS)
# #
# # print("\n" + "=" * 50)
# # print("OPTIMAL SOLUTION FOUND")
# # print("=" * 50)
# # print(f"Outer Dimensions (L x W x H): {L_opt} mm x {W_opt} mm x {H_opt} mm")
# # print(f"Inner Dimensions: {L_opt - 400} mm x {W_opt - 400} mm x {H_opt - 400} mm")
# # print(f"Number of Bricks Used: {n_bricks_opt:.2f}")
# # print(f"Internal Volume: {internal_vol_opt / 1e9:.3f} billion mm³")
# # print(f"Deviation from Target: {n_bricks_opt - TOTAL_BRICKS:.2f} bricks")
# #
# #
# # # --- 4. VISUALIZATION (Top View and Side View) ---
# # def draw_brick_course(ax, start_x, start_y, width_mm, height_mm, brick_length, brick_height, is_offset=False):
# #     """
# #     Draws a single horizontal course of bricks on a matplotlib axis.
# #     """
# #     brick_color = '#C2B280'  # Sand color
# #     mortar_color = 'gray'
# #     mortar_thickness = 2  # mm for drawing
# #
# #     current_x = start_x
# #     bricks_in_course = width_mm / brick_length
# #     # If there's an offset, start with a half-brick
# #     if is_offset:
# #         brick_width = brick_length / 2
# #         rect = Rectangle((current_x, start_y), brick_width - mortar_thickness, brick_height - mortar_thickness,
# #                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
# #         ax.add_patch(rect)
# #         current_x += brick_width
# #
# #     # Draw all full bricks
# #     while current_x < start_x + width_mm - brick_length:
# #         rect = Rectangle((current_x, start_y), brick_length - mortar_thickness, brick_height - mortar_thickness,
# #                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
# #         ax.add_patch(rect)
# #         current_x += brick_length
# #
# #     # Draw the last brick (might be a half-brick if the course ended with an offset start)
# #     remaining_width = (start_x + width_mm) - current_x
# #     if remaining_width > 0:
# #         rect = Rectangle((current_x, start_y), remaining_width - mortar_thickness, brick_height - mortar_thickness,
# #                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
# #         ax.add_patch(rect)
# #
# #
# # # Create the figure
# # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
# # fig.suptitle(f'Optimal Cuboid Construction\n(L={L_opt}mm, W={W_opt}mm, H={H_opt}mm, Bricks used={n_bricks_opt:.1f})',
# #              fontsize=16)
# #
# # # --- TOP VIEW (L-W Plane) ---
# # ax1.set_title('Top View (shows one course of the 200mm thick wall)')
# # ax1.set_xlabel('Length (mm)')
# # ax1.set_ylabel('Width (mm)')
# # ax1.set_xlim(0, L_opt)
# # ax1.set_ylim(0, W_opt)
# # ax1.set_aspect('equal')
# #
# # # Draw the outer and inner boundaries
# # outer_rect = Rectangle((0, 0), L_opt, W_opt, linewidth=2, edgecolor='k', facecolor='none', label='Outer Edge')
# # inner_rect = Rectangle((WALL_THICKNESS, WALL_THICKNESS), L_opt - 2 * WALL_THICKNESS, W_opt - 2 * WALL_THICKNESS,
# #                        linewidth=2, edgecolor='r', linestyle='--', facecolor='none', label='Inner Edge')
# # ax1.add_patch(outer_rect)
# # ax1.add_patch(inner_rect)
# #
# # # Draw the bricks for the TOP wall segment.
# # # We visualize one 200mm "slice" of the wall at the top.
# # wall_segment_thickness = 200  # mm
# # draw_brick_course(ax1, 0, W_opt - wall_segment_thickness, L_opt, wall_segment_thickness,
# #                   brick_length=200, brick_height=100, is_offset=False)
# # ax1.legend()
# #
# # # --- SIDE VIEW (L-H Plane) ---
# # ax2.set_title('Side View (shows brick courses)')
# # ax2.set_xlabel('Length (mm)')
# # ax2.set_ylabel('Height (mm)')
# # ax2.set_xlim(0, L_opt)
# # ax2.set_ylim(0, H_opt)
# # ax2.set_aspect('equal')
# #
# # # Draw the outer and inner boundaries for the side
# # outer_rect_side = Rectangle((0, 0), L_opt, H_opt, linewidth=2, edgecolor='k', facecolor='none', label='Outer Edge')
# # inner_rect_side = Rectangle((WALL_THICKNESS, WALL_THICKNESS), L_opt - 2 * WALL_THICKNESS, H_opt - 2 * WALL_THICKNESS,
# #                             linewidth=2, edgecolor='r', linestyle='--', facecolor='none', label='Inner Edge')
# # ax2.add_patch(outer_rect_side)
# # ax2.add_patch(inner_rect_side)
# #
# # # Draw multiple courses for the side wall.
# # # Each course is 200mm tall (2 bricks high). The pattern alternates.
# # course_height = 200  # mm
# # num_courses = int(H_opt / course_height)
# # for i in range(num_courses):
# #     y_pos = i * course_height
# #     is_offset_course = (i % 2 == 1)  # Alternate courses are offset for bond
# #     draw_brick_course(ax2, 0, y_pos, L_opt, course_height,
# #                       brick_length=200, brick_height=course_height, is_offset=is_offset_course)
# # ax2.legend()
# #
# # plt.tight_layout()
# # plt.show()
#
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
#
# # --- 1. BRICK AND PROBLEM CONSTANTS ---
# BRICK_VOLUME = 200 * 100 * 100  # mm³
# TOTAL_BRICKS = 10000
# WALL_THICKNESS = 200  # mm
# TARGET_VOLUME = TOTAL_BRICKS * BRICK_VOLUME  # mm³, volume occupied by bricks
#
# # --- 2. DEFINE THE CRITICAL EQUATION ---
# def calculate_brick_volume(L, W, H, t=WALL_THICKNESS):
#     """
#     Calculates the total volume of bricks used for a hollow cuboid.
#     L, W, H: Outer dimensions (mm).
#     t: Wall thickness (mm).
#     """
#     inner_vol = (L - 2*t) * (W - 2*t) * (H - 2*t)
#     outer_vol = L * W * H
#     brick_vol = outer_vol - inner_vol
#     return brick_vol
#
# def calculate_brick_count(L, W, H, t=WALL_THICKNESS):
#     """Calculates the number of bricks used for given dimensions."""
#     brick_vol = calculate_brick_volume(L, W, H, t)
#     return brick_vol / BRICK_VOLUME
#
# # --- 3. FIND OPTIMAL DIMENSIONS (NEAR-CUBE) ---
# min_dim = 400
# max_dim = 5000
# step = 100  # mm
#
# best_config = None
# best_internal_volume = 0
# best_brick_diff = float('inf')  # Difference from 10,000 bricks
#
# # Iterate through possible dimensions. Assume L <= W <= H to avoid duplicates.
# print("Searching for optimal dimensions near a cube...")
# for L in range(min_dim, max_dim + 1, step):
#     for W in range(L, max_dim + 1, step):  # Start W from L to avoid symmetric duplicates
#         for H in range(W, max_dim + 1, step):  # Start H from W
#             # Calculate brick count for this configuration
#             n_bricks = calculate_brick_count(L, W, H)
#
#             # Check if it's a valid candidate (uses all bricks or very close)
#             brick_diff = abs(n_bricks - TOTAL_BRICKS)
#             if brick_diff < 50:  # Look within a tolerance of 50 bricks
#                 internal_vol = (L - 2 * WALL_THICKNESS) * (W - 2 * WALL_THICKNESS) * (H - 2 * WALL_THICKNESS)
#
#                 # Check if this is the best candidate so far
#                 if (brick_diff < best_brick_diff or
#                         (brick_diff == best_brick_diff and internal_vol > best_internal_volume)):
#
#                     best_config = (L, W, H)
#                     best_internal_volume = internal_vol
#                     best_brick_diff = brick_diff
#                     print(f"New best candidate: L={L}, W={W}, H={H}, "
#                           f"Bricks={n_bricks:.2f}, Diff={brick_diff:.2f}, "
#                           f"Internal Vol={internal_vol / 1e9:.2f} billion mm³")
#
# # Output the final best configuration
# L_opt, W_opt, H_opt = best_config
# n_bricks_opt = calculate_brick_count(L_opt, W_opt, H_opt)
# internal_vol_opt = (L_opt - 2 * WALL_THICKNESS) * (W_opt - 2 * WALL_THICKNESS) * (H_opt - 2 * WALL_THICKNESS)
#
# print("\n" + "=" * 50)
# print("OPTIMAL SOLUTION FOUND")
# print("=" * 50)
# print(f"Outer Dimensions (L x W x H): {L_opt} mm x {W_opt} mm x {H_opt} mm")
# print(f"Inner Dimensions: {L_opt - 400} mm x {W_opt - 400} mm x {H_opt - 400} mm")
# print(f"Number of Bricks Used: {n_bricks_opt:.2f}")
# print(f"Internal Volume: {internal_vol_opt / 1e9:.3f} billion mm³")
# print(f"Deviation from Target: {n_bricks_opt - TOTAL_BRICKS:.2f} bricks")
#
# # --- 4. VISUALIZATION (Top View and Side View) ---
# def draw_brick_course(ax, start_x, start_y, width_mm, height_mm, brick_length, brick_height, is_offset=False, brick_data=None):
#     """
#     Draws a single horizontal course of bricks on a matplotlib axis and records brick locations.
#     """
#     brick_color = '#C2B280'  # Sand color
#     mortar_color = 'gray'
#     mortar_thickness = 2  # mm for drawing
#
#     current_x = start_x
#     bricks_in_course = width_mm / brick_length
#     # If there's an offset, start with a half-brick
#     if is_offset:
#         brick_width = brick_length / 2
#         rect = Rectangle((current_x, start_y), brick_width - mortar_thickness, brick_height - mortar_thickness,
#                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
#         ax.add_patch(rect)
#         brick_data.append((current_x, start_y, 'Offset'))  # Record location and orientation
#         current_x += brick_width
#
#     # Draw all full bricks
#     while current_x < start_x + width_mm - brick_length:
#         rect = Rectangle((current_x, start_y), brick_length - mortar_thickness, brick_height - mortar_thickness,
#                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
#         ax.add_patch(rect)
#         brick_data.append((current_x, start_y, 'Aligned'))  # Record location and orientation
#         current_x += brick_length
#
#     # Draw the last brick (might be a half-brick if the course ended with an offset start)
#     remaining_width = (start_x + width_mm) - current_x
#     if remaining_width > 0:
#         rect = Rectangle((current_x, start_y), remaining_width - mortar_thickness, brick_height - mortar_thickness,
#                          linewidth=1, edgecolor=mortar_color, facecolor=brick_color)
#         ax.add_patch(rect)
#         brick_data.append((current_x, start_y, 'Aligned'))  # Record location and orientation
#
# # Store brick data: [(x, y, orientation), ...]
# brick_data = []
#
# # Create the figure
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
# fig.suptitle(f'Optimal Cuboid Construction\n(L={L_opt}mm, W={W_opt}mm, H={H_opt}mm, Bricks used={n_bricks_opt:.1f})', fontsize=16)
#
# # --- TOP VIEW (L-W Plane) ---
# ax1.set_title('Top View (shows one course of the 200mm thick wall)')
# ax1.set_xlabel('Length (mm)')
# ax1.set_ylabel('Width (mm)')
# ax1.set_xlim(0, L_opt)
# ax1.set_ylim(0, W_opt)
# ax1.set_aspect('equal')
#
# # Draw the outer and inner boundaries
# outer_rect = Rectangle((0, 0), L_opt, W_opt, linewidth=2, edgecolor='k', facecolor='none', label='Outer Edge')
# inner_rect = Rectangle((WALL_THICKNESS, WALL_THICKNESS), L_opt - 2 * WALL_THICKNESS, W_opt - 2 * WALL_THICKNESS,
#                        linewidth=2, edgecolor='r', linestyle='--', facecolor='none', label='Inner Edge')
# ax1.add_patch(outer_rect)
# ax1.add_patch(inner_rect)
#
# # Draw the bricks for the TOP wall segment.
# wall_segment_thickness = 200  # mm
# draw_brick_course(ax1, 0, W_opt - wall_segment_thickness, L_opt, wall_segment_thickness,
#                   brick_length=200, brick_height=100, is_offset=False, brick_data=brick_data)
# ax1.legend()
#
# # --- SIDE VIEW (L-H Plane) ---
# ax2.set_title('Side View (shows brick courses)')
# ax2.set_xlabel('Length (mm)')
# ax2.set_ylabel('Height (mm)')
# ax2.set_xlim(0, L_opt)
# ax2.set_ylim(0, H_opt)
# ax2.set_aspect('equal')
#
# # Draw the outer and inner boundaries for the side
# outer_rect_side = Rectangle((0, 0), L_opt, H_opt, linewidth=2, edgecolor='k', facecolor='none', label='Outer Edge')
# inner_rect_side = Rectangle((WALL_THICKNESS, WALL_THICKNESS), L_opt - 2 * WALL_THICKNESS, H_opt - 2 * WALL_THICKNESS,
#                             linewidth=2, edgecolor='r', linestyle='--', facecolor='none', label='Inner Edge')
# ax2.add_patch(outer_rect_side)
# ax2.add_patch(inner_rect_side)
#
# # Draw multiple courses for the side wall.
# course_height = 200  # mm
# #


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json

# --- 1. CONSTANTS ---
BRICK_L, BRICK_W, BRICK_H = 200, 100, 100  # mm (Standard Orientation)
WALL_THICKNESS = 200  # mm
TOTAL_BRICKS = 10000
BRICK_VOLUME = BRICK_L * BRICK_W * BRICK_H
TARGET_VOLUME = TOTAL_BRICKS * BRICK_VOLUME

# Optimal dimensions (example)
L_opt, W_opt, H_opt = 4300, 4300, 4200  # mm


# --- 2. BRICK CLASS ---
class Brick:
    def __init__(self, brick_id, center_x, center_y, center_z, orientation):
        self.id = brick_id
        self.center = np.array([center_x, center_y, center_z])
        self.orientation = orientation

        # Dimensions depend on orientation
        if orientation == 'LXY':
            self.dims = np.array([BRICK_L, BRICK_W, BRICK_H])
        elif orientation == 'LYX':
            self.dims = np.array([BRICK_W, BRICK_L, BRICK_H])
        elif orientation == 'LXZ':
            self.dims = np.array([BRICK_L, BRICK_H, BRICK_W])
        elif orientation == 'LYZ':
            self.dims = np.array([BRICK_W, BRICK_H, BRICK_L])
        else:
            self.dims = np.array([BRICK_L, BRICK_W, BRICK_H])

        self.bbox_min = self.center - self.dims / 2.0
        self.bbox_max = self.center + self.dims / 2.0

    def to_dict(self):
        return {
            'id': self.id,
            'center': self.center.tolist(),
            'orientation': self.orientation,
            'bbox_min': self.bbox_min.tolist(),
            'bbox_max': self.bbox_max.tolist()
        }


# --- 3. WALL BRICK GENERATOR ---
def generate_bricks_for_wall(axis, fixed_value, length, height, start_id=0):
    """
    Generate bricks for a wall aligned with given axis.
    axis: 'X', 'Y' -> which axis is fixed
    fixed_value: the fixed coordinate (wall plane)
    length, height: dimensions of the wall
    """
    bricks = []
    current_id = start_id

    course_height = BRICK_H
    brick_length = BRICK_L

    num_courses = int(height / course_height)
    bricks_per_course = int(length / brick_length)

    for course in range(num_courses):
        z_pos = course * course_height + course_height / 2.0
        is_offset_course = (course % 2 == 1)
        offset = brick_length / 2.0 if is_offset_course else 0.0

        for i in range(bricks_per_course + 1):
            pos = i * brick_length + offset + brick_length / 2.0
            if pos - brick_length / 2.0 < length:
                if axis == 'Y':  # Wall in XZ plane (front/back)
                    brick = Brick(current_id, pos, fixed_value, z_pos, 'LXY')
                else:  # Wall in YZ plane (left/right)
                    brick = Brick(current_id, fixed_value, pos, z_pos, 'LYX')
                bricks.append(brick)
                current_id += 1
    return bricks, current_id


# --- 4. GENERATE ALL WALLS ---
all_bricks = []
next_id = 0

# Front wall (Y=0)
front_wall, next_id = generate_bricks_for_wall('Y', 0, L_opt, H_opt, next_id)
all_bricks.extend(front_wall)

# Back wall (Y=W_opt)
back_wall, next_id = generate_bricks_for_wall('Y', W_opt, L_opt, H_opt, next_id)
all_bricks.extend(back_wall)

# Left wall (X=0)
left_wall, next_id = generate_bricks_for_wall('X', 0, W_opt, H_opt, next_id)
all_bricks.extend(left_wall)

# Right wall (X=L_opt)
right_wall, next_id = generate_bricks_for_wall('X', L_opt, W_opt, H_opt, next_id)
all_bricks.extend(right_wall)

print(f"Generated {len(all_bricks)} bricks in total.")

# --- 5. SAVE TO JSON ---
bricks_data = [b.to_dict() for b in all_bricks]
with open("brick_locations_full.json", "w") as f:
    json.dump(bricks_data, f, indent=4)

print("Brick data saved to 'brick_locations_full.json'.")


# --- 6. VISUALIZATION ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D Visualization of All Walls with Bricks")
ax.set_xlabel("X (Length)")
ax.set_ylabel("Y (Width)")
ax.set_zlabel("Z (Height)")
ax.set_xlim(0, L_opt)
ax.set_ylim(0, W_opt)
ax.set_zlim(0, H_opt)


def plot_cuboid(ax, origin, size, color='b', alpha=0.2, linewidth=0.5):
    ox, oy, oz = origin
    l, w, h = size
    verts = [
        [ox, oy, oz], [ox+l, oy, oz], [ox+l, oy+w, oz], [ox, oy+w, oz],
        [ox, oy, oz+h], [ox+l, oy, oz+h], [ox+l, oy+w, oz+h], [ox, oy+w, oz+h]
    ]
    faces = [
        [verts[0], verts[1], verts[2], verts[3]],
        [verts[4], verts[5], verts[6], verts[7]],
        [verts[0], verts[1], verts[5], verts[4]],
        [verts[2], verts[3], verts[7], verts[6]],
        [verts[1], verts[2], verts[6], verts[5]],
        [verts[0], verts[3], verts[7], verts[4]]
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=linewidth, edgecolors='k', alpha=alpha))


# Outer shell
plot_cuboid(ax, (0, 0, 0), (L_opt, W_opt, H_opt), color='cyan', alpha=0.05)

# Plot subset of bricks for clarity
for b in all_bricks[::50]:  # every 50th brick
    plot_cuboid(ax, b.bbox_min, b.dims, color='#C2B280', alpha=0.7, linewidth=0.2)

plt.show()
