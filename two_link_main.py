import time
import grid

if __name__ == "__main__":
        print(grid.num_pts(18,24,200))



def two_link_grid(panel_size, points):

    # xoffset, is the distance where the center of the MX-64 is, measured off the inside aluminum frame on the side where
    # the panels sit up against, believe that would be the 28 inch side
    xoffset = 14
    # yoffset, is the distance where the center of the MX-64 is, measured off the inside aluminum frame on the side where
    # the panels sit up against, believe that would be the 31 inch side
    yoffset = 3

    # when running the code for the servo values for the three panels comment out the ones that you are not getting values
    # from.
    # Just highlight and press Ctrl+/ to comment and uncomment out
    # Small panel grid, lines 39-41
    if panel_size == 0:
        x, y = np.meshgrid(((np.linspace(2, 23, 5))), np.linspace(2, 17, 4))
        X = xoffset - x
        Y = yoffset + y


    # # # Medium panel grid, lines 44-46
    elif panel_size == 1:
        x, y = np.meshgrid(((np.linspace(2, 23, 5))), np.linspace(2, 21, 4))
        X = xoffset - x
        Y = yoffset + y

    # # Large panel grid, lines 48-51
    elif panel_size == 2:
        x, y = np.meshgrid(((np.linspace(2, 27, 5))), np.linspace(2, 23, 4))
        X = xoffset - x
        Y = yoffset + y

    ikin(X, Y)


def ikin(X, Y):
    # Arm Link Lengths: change theses as needed
    a1 = 16
    a2 = 14.5

    beta = np.degrees(np.arccos(((a1**2 + a2**2 - X[:]**2 - Y[:]**2)/ (2 * a1 * a2))))
    alpha = np.degrees(np.arccos((X[:]**2 + Y[:]**2 + a1**2 - a2**2) / (2 * a1 * np.sqrt(X[:]**2 + Y[:]**2))))
    gamma = np.degrees(np.arctan2(Y[:], X[:]))
    theta1r = gamma - alpha
    theta2r = 180 - beta
    theta1l = gamma + alpha
    theta2l = beta - 180
    # Ratio for MX
    r = 4095/360
    # Servo values for left and right elbow orientations based on calculated theta's
    v1l = (theta1l + 90) * r
    v2r = (180 + theta2r) * r
    v1r = (theta1r + 90) * r
    v2l = (180 - abs(theta2l)) * r
    # the values are than rounded to whole number integers
    v1l = np.around(v1l, decimals=0)
    v2r = np.around(v2r, decimals=0)
    v1r = np.around(v1r, decimals=0)
    v2l = np.around(v2l, decimals=0)
    # Every other column is flipped starting with the second to provide better effeciency of robot arm movement
    v1l[:, 1::2] = v1l[::-1, 1::2]
    v2r[:, 1::2] = v2r[::-1, 1::2]
    v1r[:, 1::2] = v1r[::-1, 1::2]
    v2l[:, 1::2] = v2l[::-1, 1::2]
    # The flipped arrays are transformed to a list in order of indexing
    v1l_flat = v1l.flatten('F')
    v2r_flat = v2r.flatten('F')
    v1r_flat = v1r.flatten('F')
    v2l_flat = v2l.flatten('F')
    # this returns indices of the max element, in this case 3000, so the arm can remain in the parameters of the PCB's
    idx = np.argmax(v1l_flat>=3000)
    # those values in V1LA >= 3000 are exchanged for the corresponding values in V1RA
    v1l_flat[idx:] = v1r_flat[idx:]
    v2l_flat[idx:] = v2r_flat[idx:]
    # V1LA and V2LA reshaped to original order with replaced values creating SV1 (Servo Value 1) and SV2
    sv1 = np.reshape(v1l_flat, v1l.shape, order='F')
    sv2 = np.reshape(v2l_flat, v2l.shape, order='F')
    # Servo values are transformed to a list in order to communicate the values appropriately to the Arduino
    sv1 = sv1.flatten('F')
    sv2 = sv2.flatten('F')
    s_values = (sv1, sv2)
    print(sv1)
    print(sv2)

