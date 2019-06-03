
import PythonLibMightyZap as mighty
def zap(length):
    value = 3863.2 * length
    print(value)
    servo_id=0
    #mighty.CloseMightyZap
    mighty.OpenMightyZap('/dev/ttyUSB0',200000)
    mighty.goalPosition(servo_id, int(value))
   

    return()
if __name__ == "__main__":
    zap(0)
    
    
