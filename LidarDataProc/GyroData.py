from turtle import st


class GyroData:
    '''
    Gyro Data
    '''

    def __init__(self, line) -> None:
        self.timestamp= line[0]
        self.north_vel	= line[1]
        self.east_vel	= line[2]
        self.down_vel	= line[3]
        self.north_vel_dev	= line[4]
        self.east_vel_dev	= line[5]
        self.down_vel_dev	= line[6]
        self.lat	= line[7]
        self.long	= line[8]
        self.alt	= line[9]
        self.undulation	= line[10]
        self.lat_dev	= line[11]
        self.long_dev	= line[12]
        self.alt_dev	= line[13]
        self.accel_x	= line[14]
        self.accel_y	= line[15]
        self.accel_z	= line[16]
        self.gyro_x	= line[17]
        self.gyro_y	= line[18]
        self.gyro_z	= line[19]
        self.temp	= line[20]
        self.delta_vel_x	= line[21]
        self.delta_vel_y	= line[22]
        self.delta_vel_z	= line[23]
        self.delta_angle_x	= line[24]
        self.delta_angle_y	= line[25]
        self.delta_angle_z	= line[26]
        self.mag_x	= line[27]
        self.mag_y	= line[28]
        self.mag_z	= line[29]
        self.accel_x= line[30]
        self.accel_y= line[31]
        self.accel_z= line[32]
        self.roll	= line[33]
        self.pitch	= line[34]
        self.yaw	= line[35]
        self.roll_dev	= line[36]
        self.pitch_dev	= line[37]
        self.yaw_dev	= line[38]
        self.w_quat	= line[39]
        self.x_quat	= line[40]
        self.y_quat	= line[41]
        self.z_quat	= line[42]
        self.roll_dev= line[43]
        self.pitch_dev	= line[44]
        self.yaw_dev= line[45]
        self.heave_period	= line[46]
        self.surge_motion	= line[47]
        self.sway_motion	= line[48]
        self.heave_motion	= line[49]
        self.surge_accel	= line[50]
        self.sway_accel	= line[51]
        self.heave_accel	= line[52]
        self.surge_vel	= line[53]
        self.sway_vel	= line[54]
        self.heave_vel	= line[55]
        self.wave_angle= line[56]

    def __str__(self) -> str:
        st_retour: str = self.timestamp

        return st_retour