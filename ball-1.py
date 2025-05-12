import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Square")

# Colors
black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

# Ball properties
ball_radius = 15
# Start the ball in the center of the screen/square
ball_x = width // 2
ball_y = height // 2
ball_speed_x = random.uniform(-5, 5)
ball_speed_y = random.uniform(-5, 5)

# Square properties, center it
square_size = 200
square_x = width // 2 - square_size // 2
square_y = height // 2 - square_size // 2
square_rotation = 0  # Initial rotation
rotation_speed = 0.5  # Rotation speed


# Game loop
running = True
clock = pygame.time.Clock()

def reflect_vector(vx, vy, nx, ny):
    # Reflect a vector (vx, vy) across a normal vector (nx, ny)
    dot_product = vx * nx + vy * ny
    rx = vx - 2 * dot_product * nx
    ry = vy - 2 * dot_product * ny
    return rx, ry

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotation_speed -= 0.1
            if event.key == pygame.K_RIGHT: rotation_speed += 0.1

    # Rotate the square
    square_rotation += rotation_speed

    # Calculate rotated square corners
    center_x = width // 2
    center_y = height // 2
    corners = []
    for i in range(4):
        angle = math.radians(square_rotation + i * 90)
        x = center_x + (square_size // 2) * math.cos(angle)
        y = center_y + (square_size // 2) * math.sin(angle)
        corners.append((x, y))

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision detection and response with rotated square
    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]  # Next corner (loop back to first)

        # Calculate the distance from the ball's center to the line segment
        dx = x2 - x1  # Vector from x1,y1 to x2,y2
        dy = y2 - y1
        a = dx * dx + dy * dy  # Squared length of the line segment

        if a == 0:  # If the line segment is a point (shouldn't happen, but handle it)
            continue

        # Project the ball's center onto the line segment
        t = ((ball_x - x1) * dx + (ball_y - y1) * dy) / a
        if t < 0:  # Closest point is x1,y1
            closest_x, closest_y = x1, y1
        elif t > 1:  # Closest point is x2,y2
            closest_x, closest_y = x2, y2
        else:  # Closest point is on the line segment
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

        # Calculate the distance from the ball's center to the closest point
        distance = math.sqrt((ball_x - closest_x) ** 2 + (ball_y - closest_y) ** 2)

        if distance < ball_radius:  # Collision detected
            # Calculate the normal vector (perpendicular to the line segment)
            # The normal to a line segment (dx, dy) is (-dy, dx) or (dy, -dx)
            nx = -dy
            ny = dx
            norm = math.sqrt(nx * nx + ny * ny)
            if norm > 0:  # Avoid division by zero
                nx /= norm
                ny /= norm
            ball_speed_x, ball_speed_y = reflect_vector(ball_speed_x, ball_speed_y, nx, ny)


    # Keep ball within screen bounds (simple bounce)
    if ball_x + ball_radius > width or ball_x - ball_radius < 0:
        ball_speed_x = -ball_speed_x
    if ball_y + ball_radius > height or ball_y - ball_radius < 0:
        ball_speed_y = -ball_speed_y

    # Drawing

    screen.fill(black)
    pygame.draw.polygon(screen, yellow, corners, 2)  # Draw rotated square
    pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)  # Draw ball
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
