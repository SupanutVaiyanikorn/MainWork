import simpy
import random, itertools

simulation_time = 1000
CPU_size = 100
THRESHOLD = 30
CONSUMING_CPU_LEVEL = [1, 2]  # Min/max levels of fuel tanks (in liters)
RANDOM1 = [30, 300]
RECOVER_SPEED = 2 # second
PROCESS_TAKING_TIME = 100
# Yeah Yeah
#OKOKOKOKOKOKOKOK
#OKOKOKOKOKOKOKOK
#OKOKOKOKOKOKOKOK
#OKOKOKOKOKOKOKOK
#OKOKOKOKOKOKOKOK
#OKOKOKOKOKOKOKOK
def Packet(name, env, SERVER_SPACE, CPU):
    consuming_cpu_level = random.randint(*CONSUMING_CPU_LEVEL)
    print('%s arriving at SERVER_SPACE at %.1f' % (name, env.now))
    with SERVER_SPACE.request() as req:
        start = env.now
        # Request one of the gas pumps
        yield req

        # Get the required amount of fuel
        CPU_required = CPU_size - consuming_cpu_level #หาจำนวน
        yield CPU.get(CPU_required)

        # The "actual" refueling process takes some time
        # #เวลาที่รถเติมน้ำมัน  โดยการจำนวนน้ำมันที่เติม Litters_requred มาหาร 2 กับสปิดในการเติม จะได้เวลาในการเติม
        yield env.timeout(CPU_required / RECOVER_SPEED)

        print('%s finished refueling in %.1f seconds.' % (name, env.now - start))

def GeneratePacket(env, SERVER_SPACE, CPU):
    for i in itertools.count():
        yield env.timeout(random.randint(*RANDOM1))
        env.process(Packet('Packet %d' % i, env, SERVER_SPACE, CPU))

def CallingSERVER(env, CPU):
    while True:
        if CPU.level / CPU.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Refiling CPU at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(RecoverProcess(env, CPU))

        yield env.timeout(10)

def RecoverProcess(env, CPU):
# should cosider in case of CPU, 'cause in this case, it's designed for gas station.
# CPU always recovers its process. That process is recovered from Packet in which would come to consume the CPU resource

    yield env.timeout(PROCESS_TAKING_TIME) #300
    print('CPU finished consuming CPU process at %d' % env.now)
    amount = CPU.capacity - CPU.level
    print('T refuelling %.1f liters.' % amount)
    yield CPU.put(amount) #เติมน้ำมันลงคอนเ

random.seed(42)

env = simpy.Environment()
SERVER_SPACE = simpy.Resource(env, 100) # 100 = amount of packet 
CPU = simpy.Container(env, CPU_size, init=CPU_size)
# Memory = simpy.Container(env, Memor)

env.process(CallingSERVER(env, CPU))
env.process(GeneratePacket(env, SERVER_SPACE, CPU))
env.run(until=simulation_time)