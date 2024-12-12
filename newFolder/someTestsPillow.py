from PIL import Image, ImageDraw

# Define the pixel art grid
pixel_art_grid = [
    "RRGG",
    "RGGR",
    "GRRG",
    "GRGR"
]

# Define the color mapping
color_mapping = {
    'R': (255, 0, 0),   # Red
    'G': (0, 255, 0),   # Green
    'B': (0, 0, 255),   # Blue
    'Y': (255, 255, 0), # Yellow
    'W': (255, 255, 255), # White
    'K': (0, 0, 0)      # Black
}

# Define the size of each pixel
pixel_size = 50

# Calculate the dimensions of the image
width = len(pixel_art_grid[0]) * pixel_size
height = len(pixel_art_grid) * pixel_size

# Create a new image
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Fill the image with pixels based on the grid
for y, row in enumerate(pixel_art_grid):
    for x, char in enumerate(row):
        if char in color_mapping:
            draw.rectangle(
                [x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size],
                fill=color_mapping[char]
            )

# Save the image
image.save('pixel_art.png')
image.show()
