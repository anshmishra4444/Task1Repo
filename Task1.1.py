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

# --- 2. FIND OPTIMAL DIMENSIONS (Simplified from previous search) ---
# Let's assume our previous search found this to be a near-optimal candidate.
# It's very close to 10,000 bricks and has a large internal volume.
L_opt, W_opt, H_opt = 4300, 4300, 4200  # mm

def calculate_brick_count(L, W, H, t=WALL_THICKNESS):
    outer_vol = L * W * H
    inner_vol = (L - 2*t) * (W - 2*t) * (H - 2*t)
    return (outer_vol - inner_vol) / BRICK_VOLUME

n_bricks_opt = calculate_brick_count(L_opt, W_opt, H_opt)
print(f"Using dimensions: {L_opt}x{W_opt}x{H_opt} mm")
print(f"Calculated number of bricks: {n_bricks_opt:.2f}")
print(f"Deviation from target: {n_bricks_opt - TOTAL_BRICKS:.2f} bricks\n")

# --- 3. DATA STRUCTURE FOR BRICK INFORMATION ---
# We will define a class to hold the position and orientation of each brick.
class Brick:
    def __init__(self, brick_id, center_x, center_y, center_z, orientation):
        """
        Represents a single brick.
        :param brick_id: Unique identifier for the brick.
        :param center_x, center_y, center_z: Coordinates of the brick's center (mm).
        :param orientation: A string defining how the brick's L, W, H are aligned with the world's X, Y, Z axes.
                            'LXY' = Brick's Length is along world X, Width along Y, Height along Z.
                            'LXZ' = Brick's Length is along world X, Width along Z, Height along Y.
                            etc.
        """
        self.id = brick_id
        self.center = np.array([center_x, center_y, center_z])
        self.orientation = orientation

        # Determine effective dimensions based on orientation
        if orientation == 'LXY': # Standard for horizontal courses
            self.dims = np.array([BRICK_L, BRICK_W, BRICK_H])
        elif orientation == 'LYX': # Rotated 90 degrees in the horizontal plane
            self.dims = np.array([BRICK_W, BRICK_L, BRICK_H])
        elif orientation == 'LXZ': # For vertical placement, length along X, height along Z
            self.dims = np.array([BRICK_L, BRICK_H, BRICK_W])
        elif orientation == 'LYZ': # For vertical placement, length along Y, height along Z
            self.dims = np.array([BRICK_H, BRICK_L, BRICK_W])
        else:
            # Default orientation
            self.dims = np.array([BRICK_L, BRICK_W, BRICK_H])

        # Calculate the min and max corners of the brick's bounding box
        self.bbox_min = self.center - self.dims / 2.0
        self.bbox_max = self.center + self.dims / 2.0

    def to_dict(self):
        """Converts the Brick object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'center': self.center.tolist(),
            'orientation': self.orientation,
            'bbox_min': self.bbox_min.tolist(),
            'bbox_max': self.bbox_max.tolist()
        }

# --- 4. ALGORITHM TO GENERATE BRICK LAYOUT (CONCEPTUAL) ---
# This is a simplified version that generates bricks for one wall.
# A full solution would involve complex logic for all 6 walls and corners.

def generate_bricks_for_xz_wall(y_position, is_inner_wall=False, start_id=0):
    """
    Generates bricks for a wall in the X-Z plane at a fixed Y coordinate.
    This is a simplified example for one wall segment, not handling corners.
    """
    bricks = []
    current_id = start_id
    course_height = 200  # mm (2 bricks high)
    brick_length = 200   # mm

    # Determine the start and end of the wall in X and Z
    wall_x_start = 0
    wall_x_end = L_opt
    wall_z_start = 0
    wall_z_end = H_opt

    num_courses = int(H_opt / course_height)
    bricks_per_course = int(L_opt / brick_length)

    for course in range(num_courses):
        z_pos = course * course_height + course_height / 2.0 # Center of the course
        is_offset_course = (course % 2 == 1)
        offset = brick_length / 2.0 if is_offset_course else 0.0

        for i in range(bricks_per_course + 1): # +1 to account for the offset half-brick
            x_pos = i * brick_length + offset + brick_length / 2.0
            # Check if this brick's position is within the wall boundaries
            if x_pos - brick_length/2.0 < wall_x_end:
                # Determine orientation: 'LXY' if flat, 'LXZ' if on side
                orientation = 'LXY'
                # Create the brick
                new_brick = Brick(
                    brick_id=current_id,
                    center_x=x_pos,
                    center_y=y_position,
                    center_z=z_pos,
                    orientation=orientation
                )
                bricks.append(new_brick)
                current_id += 1
            else:
                # This brick would be outside, skip it.
                pass

    return bricks, current_id

# --- 5. GENERATE A SAMPLE OF BRICKS ---
print("Generating a sample of brick data for the front wall (Y=0)...")
# Let's generate bricks for the outer front wall (Y = 0)
sample_bricks, next_id = generate_bricks_for_xz_wall(y_position=0, start_id=0)

print(f"Generated {len(sample_bricks)} bricks for the sample wall.")
print("First 5 bricks:")

# Print details for the first 5 bricks
for i, brick in enumerate(sample_bricks[:5]):
    print(f"  Brick {brick.id}: Center={brick.center}, Orientation='{brick.orientation}'")

# --- 6. OUTPUT BRICK DATA TO JSON ---
# Convert the list of Brick objects to a list of dictionaries
bricks_data = [brick.to_dict() for brick in sample_bricks]

# Save to a JSON file
output_filename = "brick_locations_sample.json"
with open(output_filename, 'w') as f:
    json.dump(bricks_data, f, indent=4)

print(f"\nSample brick data saved to '{output_filename}'.")

# --- 7. 3D VISUALIZATION (Simplified, shows outer box and sample bricks) ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('3D Visualization of Cuboid and Sample Bricks\n(Shows front wall at Y=0)')
ax.set_xlabel('X (Length)')
ax.set_ylabel('Y (Width)')
ax.set_zlabel('Z (Height)')
ax.set_xlim(0, L_opt)
ax.set_ylim(0, W_opt)
ax.set_zlim(0, H_opt)

# Draw the outer cuboid (wireframe)
def plot_cuboid(ax, origin, size, color='b', alpha=0.1, linewidth=1):
    """Plots a wireframe cuboid."""
    ox, oy, oz = origin
    l, w, h = size
    # List of vertices for the cuboid
    verts = [
        [ox, oy, oz], [ox+l, oy, oz], [ox+l, oy+w, oz], [ox, oy+w, oz], # bottom
        [ox, oy, oz+h], [ox+l, oy, oz+h], [ox+l, oy+w, oz+h], [ox, oy+w, oz+h]  # top
    ]
    # List of faces by connecting vertices
    faces = [
        [verts[0], verts[1], verts[2], verts[3]], # bottom
        [verts[4], verts[5], verts[6], verts[7]], # top
        [verts[0], verts[1], verts[5], verts[4]], # front
        [verts[2], verts[3], verts[7], verts[6]], # back
        [verts[1], verts[2], verts[6], verts[5]], # right
        [verts[0], verts[3], verts[7], verts[4]]  # left
    ]
    # Plot each face
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=linewidth, edgecolors='k', alpha=alpha))

# Plot the outer shell (hollow)
plot_cuboid(ax, (0, 0, 0), (L_opt, W_opt, H_opt), color='cyan', alpha=0.05)
# Plot the inner void
plot_cuboid(ax, (WALL_THICKNESS, WALL_THICKNESS, WALL_THICKNESS),
            (L_opt-2*WALL_THICKNESS, W_opt-2*WALL_THICKNESS, H_opt-2*WALL_THICKNESS),
            color='red', alpha=0.05)

# Plot a subset of the sample bricks (for clarity, not all 10,000!)
print("\nPlotting a subset of bricks for visualization...")
for brick in sample_bricks[::5]:  # Plot every 5th brick to avoid clutter
    plot_cuboid(ax, brick.bbox_min, brick.dims, color='#C2B280', alpha=0.7, linewidth=0.5)

plt.tight_layout()
plt.show()