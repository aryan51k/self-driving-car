import pygame
from motor import Motor


def pygame_setup():
    '''This Function helps to setup the pygame'''
    pygame.init()
    win = pygame.display.set_mode((100,100))

def getKey(key):
    '''This helps to detect the key sent by user'''
    ans  = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    key_sent = getattr(pygame, 'K_{}'.format(key))
    if keyInput [key_sent]:
        ans = True    
    return ans
    
def main():
    '''This is used to drive the code'''
    motor1 = Motor(32, 33, 11, 13, 15, 16)
    
    if getKey('UP'):
        motor1.move(0.1,0,1)
        #print("HI")
    elif getKey('DOWN'):
        motor1.move(0.1,0,-1)
        #print("HI2")
    elif getKey('LEFT'):
        motor1.move(0.1,-0.5,0.5)
        #print("HI3")
    elif getKey('RIGHT'):
        motor1.move(0.1,0.5,0.5)
        #print("HI4")
        
    else:
        motor1.stop(0.1)
    

if __name__ == "__main__":
    pygame_setup()
    
    while True:
        main()
