
import PythonLibMightyZap as mighty
servo_id=0
mighty.CloseMightyZap
mighty.OpenMightyZap('/dev/ttyUSB1',200000)
baud=mighty.read_Addr(0,0x04,1)
print(baud)
##mighty.write_Addr(0,0x04,1,8)
mighty.goalPosition(0,0)
