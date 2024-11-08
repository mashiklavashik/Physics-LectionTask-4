import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

mass1 = float(input("Масса первого тела в килограммах: "))
mass2 = float(input("Масса второго тела в килограммах: "))
speed1 = float(input("Модуль скорости первого тела (м/с): "))
speed2 = float(input("Модуль скорости второго тела (м/с): "))
direction1 = np.array(list(map(float, input("Направление скорости первого тела вектор (x, y): ").split(','))))
direction2 = np.array(list(map(float, input("Направление скорости второго тела вектор (x, y): ").split(','))))
box_height = float(input("Высота оболочки: "))
box_width = float(input("Ширина оболочки: "))

v1_initial = direction1 / np.linalg.norm(direction1) * speed1
v2_initial = direction2 / np.linalg.norm(direction2) * speed2


position1_initial = np.array([1.0, 1.0])
position2_initial = np.array([box_width - 1.0, box_height - 1.0])


time_step = 0.01  
total_time = 10


positions = [position1_initial, position2_initial]
velocities = [v1_initial, v2_initial]
masses = [mass1, mass2]


def resolve_collision(v1, v2, m1, m2, pos1, pos2):
    normal = (pos2 - pos1) / np.linalg.norm(pos2 - pos1)
    p = 2 * (v1 @ normal - v2 @ normal) / (m1 + m2)
    v1_new = v1 - p * m2 * normal
    v2_new = v2 + p * m1 * normal
    return v1_new, v2_new


def update_positions():
    global positions, velocities

    for i in range(2):
        
        positions[i] += velocities[i] * time_step

        
        if positions[i][0] <= 0 or positions[i][0] >= box_width:
            velocities[i][0] = -velocities[i][0]
        if positions[i][1] <= 0 or positions[i][1] >= box_height:
            velocities[i][1] = -velocities[i][1]

    
    distance = np.linalg.norm(positions[0] - positions[1])
    if distance < 0.5:  
        velocities[0], velocities[1] = resolve_collision(
            velocities[0], velocities[1], masses[0], masses[1], positions[0], positions[1]
        )


fig, ax = plt.subplots()
ax.set_xlim(0, box_width)
ax.set_ylim(0, box_height)
circle1 = plt.Circle(positions[0], 0.25, fc='#cc8ff7')
circle2 = plt.Circle(positions[1], 0.25, fc='#8ddce3')
ax.add_patch(circle1)
ax.add_patch(circle2)


text1 = ax.text(positions[0][0], positions[0][1], f'{mass1:.1f} kg', ha='center', va='center', color='black')
text2 = ax.text(positions[1][0], positions[1][1], f'{mass2:.1f} kg', ha='center', va='center', color='black')


speed_text1 = ax.text(positions[0][0], positions[0][1] - 0.3, f'{np.linalg.norm(velocities[0]):.2f} m/s', ha='center', va='center', color='black')
speed_text2 = ax.text(positions[1][0], positions[1][1] - 0.3, f'{np.linalg.norm(velocities[1]):.2f} m/s', ha='center', va='center', color='black')


arrow1 = ax.quiver(positions[0][0], positions[0][1], velocities[0][0], velocities[0][1], color='#cc8ff7', scale=2)
arrow2 = ax.quiver(positions[1][0], positions[1][1], velocities[1][0], velocities[1][1], color='#8ddce3', scale=2)

def animate(frame):
    update_positions()
    circle1.set_center(positions[0])
    circle2.set_center(positions[1])
    text1.set_position(positions[0])
    text2.set_position(positions[1])
    speed_text1.set_position((positions[0][0], positions[0][1] - 0.3))
    speed_text2.set_position((positions[1][0], positions[1][1] - 0.3))
    speed_text1.set_text(f'{np.linalg.norm(velocities[0]):.2f} m/s')
    speed_text2.set_text(f'{np.linalg.norm(velocities[1]):.2f} m/s')
    arrow1.set_offsets(positions[0])
    arrow1.set_UVC(velocities[0][0], velocities[0][1])
    arrow2.set_offsets(positions[1])
    arrow2.set_UVC(velocities[1][0], velocities[1][1])
    return circle1, circle2, text1, text2, speed_text1, speed_text2, arrow1, arrow2


anim = FuncAnimation(fig, animate, frames=int(total_time / time_step), interval=20, blit=True)
anim.save("simulation.gif", dpi=80, writer='pillow')
plt.close()
