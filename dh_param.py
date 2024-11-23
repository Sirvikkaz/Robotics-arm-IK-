import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
# Define DH parameters
#First row of the dh parameters 
theta1 = sp.symbols('theta1')  # Define theta1 as a symbolic variable
d1 = 0
a1 = 0
alpha1 = 0 
length=10
length2=5
# Calculate the first line of the transformation matrix
Inverse_formula = [[sp.cos(theta1), -sp.sin(theta1), 0, a1],
                 [sp.sin(theta1)*sp.cos(alpha1), sp.cos(theta1)*sp.cos(alpha1), -sp.sin(alpha1), -sp.sin(alpha1)*d1],
                 [sp.sin(theta1)*sp.sin(alpha1), sp.cos(theta1)*sp.sin(alpha1), sp.cos(alpha1), sp.cos(theta1)*d1],
                 [0,0,0,1]]
#Second row of the Dh parameter
theta2 = sp.symbols('theta2')  # Define theta1 as a symbolic variable
d2 = 0
a2 = length
alpha2 = 0 
# Calculate the second row of the transformation matrix 
Inverse_formula2 = [[sp.cos(theta2), -sp.sin(theta2), 0, a2],
                 [sp.sin(theta2)*sp.cos(alpha2), sp.cos(theta2)*sp.cos(alpha2), -sp.sin(alpha2), -sp.sin(alpha2)*d2],
                 [sp.sin(theta2)*sp.sin(alpha2), sp.cos(theta2)*sp.sin(alpha2), sp.cos(alpha2), sp.cos(theta2)*d2],
                 [0,0,0,1]]
#Third row of the dh parameter
theta3 = 0  
d3 = 0
a3 = length2
alpha3 = 0  # No need to convert since it’s already in radians
#Calculate the third row of the transformation matrix
Inverse_formula3 = [[sp.cos(theta3), -sp.sin(theta3), 0, a3],
                 [sp.sin(theta3)*sp.cos(alpha3), sp.cos(theta3)*sp.cos(alpha3), -sp.sin(alpha3), -sp.sin(alpha3)*d3],
                 [sp.sin(theta2)*sp.sin(alpha3), sp.cos(theta3)*sp.sin(alpha3), sp.cos(alpha3), sp.cos(theta3)*d3],
                 [0,0,0,1]]
#The end position of the end effectors
px = 12.99
py = 2.5
pz = sp.symbols('pz')
#converting the transformation to numpy array
consts  = np.array([[px, py, pz, 1]]).transpose()
x1 = np.array([Inverse_formula])
y1 = np.array([Inverse_formula2])
z1 = np.array([Inverse_formula3])
#performing the matrices operations
x1_mult_const = np.matmul(x1.swapaxes(1,2), consts)
y1_mult_z1 = np.matmul(y1, z1)
y1_T = np.array([y1_mult_z1[0, :, -1]])
solu1 = x1_mult_const-y1_T.T
solu2 = solu1[0, :2, :]
eq1 = solu2[0][0]
eq2 = solu2[1][0]
#solving for theta 1 and 2, answer in raadians
solution_new = sp.solve([eq1, eq2], [theta1, theta2])
#print(f"Solution: {solution_new}")
solutions = []
new_solution = []
#Converting theta back to radian and getting new solution as a set
for sol in solution_new:
    print(sol[0])
    print(sol[1],"Type sol",type(sol[1]))
    #theta1_deg = np.degrees(sol[0])
    theta1_deg = sol[0] *(180/np.pi)
    theta2_deg = sol[1] * (180/np.pi)
    '''
    print(f'Theta1 (radians): {sol[0]}, Theta1 (degrees): {theta1_deg}')
    print(f'Theta2 (radians): {sol[1]}, Theta2 (degrees): {theta2_deg}')
    print('---')
    '''
    new_solution.append((round(theta1_deg,1), round(theta2_deg,1)))
print(new_solution)
#Getting all the four possible solutions for the degrees
a=set()
b=set()
for i in new_solution:
    a.add(i[0])
    b.add(i[1])
t=[]
possibles_solutions = []
for i in a:
   for p in b:
        t.append(i)
        t.append(p)
        possibles_solutions.append(list(t))
        t=[]
   t=[]
#print(possibles_solutions)
#Plotting the datas and into four different subplots
fig, axs = plt.subplots(2,2, figsize=(10,8))
fig.suptitle("The Four position of the end effectors")
for j,i in enumerate(possibles_solutions):
    #angle_rad = np.radians(i[0])
    angle_rad = i[0] *(np.pi/180)
    angle_rad2 = (i[0]+i[1])*(np.pi/180)
    angle_rad_float = angle_rad.evalf()
    print(angle_rad_float, type(angle_rad_float))
    #angle_rad2 = np.radians(theta2)
    x0 = 0
    y0 = 0 
    dx = sp.cos(angle_rad)*length 
    dy = sp.sin(angle_rad) * length
    dpx = sp.cos(angle_rad2) * length2
    dpy = sp.sin(angle_rad2) * length2
    x1 = x0 + dx
    y1 = y0 + dy
    x2= x1+dpx
    y2= y1+dpy
    #print(i,j)
    if j < 2:
        axs[0,j].plot([x0, x1], [y0, y1], c="red", lw=3, label = "link1 = 10")
        axs[0,j].plot([x1, x2], [y1, y2], c="blue", lw=3, label = "link2 = 5")
        axs[0,j].plot(x2, y2, marker='s', markersize=5, color='red')
        axs[0,j].set_title(f"The position of the end effector when theta1 is {i[0]:.2f} and theta2 is {i[1]:.2f}", fontsize=10)
        axs[0,j].set_xlim(0, 15)
        axs[0,j].set_ylim(-10, 13)
        axs[0,j].grid(True)
        axs[0,j].axhline(0, color='black',linewidth=1)  # X-axis
        axs[0,j].axvline(0, color='black',linewidth=1)
        axs[0,j].legend()

    elif j == 2:
        axs[j-1,0].plot([x0, x1], [y0, y1], c="red", label ="link1 = 10", lw=3)
        axs[j-1,0].plot([x1, x2], [y1, y2], c="blue", label ="link2 = 5", lw=3)
        axs[j-1,0].plot(x2, y2, marker='s', markersize=5, color='red')
        # Adjust position as needed
        axs[j-1,0].set_title(f"The position of the end effector when theta1 is {i[0]:.2f} and theta2 is {i[1]:.2f}",fontsize=10)
        axs[j-1,0].set_xlim(0, 15)
        axs[j-1,0].set_ylim(-10, 13)
        axs[j-1,0].grid(True)
        axs[j-1,0].axhline(0, color='black',linewidth=1)  # X-axis
        axs[j-1,0].axvline(0, color='black',linewidth=1)
        axs[j-1,0].legend()
    else:
        axs[j-2,1].plot([x0, x1], [y0, y1], c="red", label ="link1 = 10",lw=3)
        axs[j-2,1].plot([x1, x2], [y1, y2], c="blue", label ="link2 = 5",lw=3)
        axs[j-2,1].plot(x2, y2, marker='s', markersize=5, color='red')
        axs[j-2,1].set_title(f"The position of the end effector when theta1 is {i[0]:.2f} and theta2 is {i[1]:.2f}", fontsize=10)
        axs[j-2,0].set_xlim(0, 15)
        axs[j-2,0].set_ylim(-10, 13)
        axs[j-2,0].grid(True)
        axs[j-2,0].axhline(0, color='black',linewidth=1)  # X-axis
        axs[j-2,0].axvline(0, color='black',linewidth=1)
plt.xlim(0, 15)
plt.ylim(-10, 13)
plt.grid(True)
#plt.xlabel("X-axis")
plt.tight_layout()
plt.legend()
plt.axhline(0, color='black',linewidth=1) 
plt.axvline(0, color='black',linewidth=1)  
plt.show()
plt.savefig("Figure of DH", dpi=300, bbox_inches="tight")
#Vikkaz says C'est finit