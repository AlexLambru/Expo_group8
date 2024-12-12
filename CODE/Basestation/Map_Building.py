import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
def head_direction(head,inputs):
    


# state format{
#     "axes": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],(left stick(x,y),right stick(x,y),l2,r2)
#     "buttons": [0, 0, 0,0](square,x,circle,triangle)
# }




# Convert to float arrays

# Scatter plot
ax.scatter(x, s, zs=t, s=200, label='True Position')



# Connect the points with a line
ax.plot(x, s, t, color='b', label='Connecting Line')

# Set labels
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")



plt.show()
