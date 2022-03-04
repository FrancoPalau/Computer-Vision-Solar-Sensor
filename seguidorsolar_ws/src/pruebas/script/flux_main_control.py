#!/usr/bin/env python
# coding=utf-8

""" Actualmente migrando el proyecto a ROS
    Autores:
    - Lautaro Delgado
    - Franco Palau
    - Gonzalo Fernández

    Migracion y adaptacion a ROS:
    - Corteggiano Tomas
"""  

from pickle import TRUE
import threading
from pruebas.msg import numsteps
import rospy
import smach
from smach import user_data
import smach_ros

# Flag to start system
rospy.set_param('start_system_flag',False)

#Create publisher to send number of steps to uC
pub_num_steps_to_uC = rospy.Publisher('num_steps_to_uC',numsteps)

# States definition for states machine

# Each state is defined by a class, which is inherited from smach's classes library
class InitState(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['to_open_loop','not_ready_to_start'])

    def execute(self,ud):
        loopstatus = rospy.get_param("/start_system_flag")
        if(loopstatus):
            return 'to_open_loop'
        else:
            return 'not_ready_to_start'

# Open Loop Class  
class OpenLoopState(smach.State):
    # Constructor
    def __init__(self, msg_cb=None, output_keys=[], latch=False, timeout=10):
        # IMPORTANT, outcomes: Define the posibles output status of the state, they are used to evaluate de transitions
        smach.State.__init__(self, outcomes=['succeeded', 'to_close_loop', 'aborted'],  output_keys=output_keys)
        self.latch = latch
        self.timeout = timeout
        self.mutex = threading.Lock()
        self.msg = numsteps()
        self.msg_cb = msg_cb
        # Subcript to the topic from the open loop node.
        self.subscriber = rospy.Subscriber("/num_steps_open_loop", numsteps, self._callback, queue_size=1)

    def _callback(self, msg):
        self.mutex.acquire()
        self.msg = msg
        self.mutex.release()

    def waitForMsg(self):
        print('Waiting for setpoint...')
        timeout_time = rospy.Time.now() + rospy.Duration.from_sec(self.timeout)
        while rospy.Time.now() < timeout_time:
            if(rospy.get_param("/close_loop_flag")):
                return 'to_close_loop'
            self.mutex.acquire()
            if self.msg != None:
                print('Got message.')
                message = self.msg
                
                rospy.loginfo("Az number of steps %d",message.az)
                rospy.loginfo("Al number of steps %d",message.al)
                
                if not self.latch:
                    self.msg = None

                self.mutex.release()
                return message
            self.mutex.release()
        print('Timeout!')
        return None

    def execute(self, ud):
        loopstatus = rospy.get_param("/close_loop_flag")
        warn = rospy.get_param("/romper_sistema")
        if(warn):
            return 'aborted'
        if(not loopstatus):
            while(True):
                msg = self.waitForMsg()
                if(msg == 'to_close_loop'):
                    return 'to_close_loop'
                if msg != None:
                    pub_num_steps_to_uC.publish(msg)
                else:
                    return 'aborted'
        elif(loopstatus):
            return 'to_close_loop'

# Close Loop Class 
class CloseLoopState(smach.State):
    
    # Constructor
    def __init__(self, msg_cb=None, output_keys=[], latch=False, timeout=10):
        smach.State.__init__(self, outcomes=['succeeded','to_open_loop','aborted'],  output_keys=output_keys)
        self.latch = latch
        self.timeout = timeout
        self.mutex = threading.Lock()
        self.msg = numsteps()
        self.msg_cb = msg_cb
        self.subscriber = rospy.Subscriber("/num_steps_close_loop", numsteps, self._callback, queue_size=1)

    def _callback(self, msg):
        self.mutex.acquire()
        self.msg = msg
        self.mutex.release()

    # Function to get a message from topic
    def waitForMsg(self):
        print('Waiting for setpoint...')
        timeout_time = rospy.Time.now() + rospy.Duration.from_sec(self.timeout)
        while rospy.Time.now() < timeout_time:
            self.mutex.acquire()
            if self.msg != None:
                print('Got message.')
                message = self.msg
                
                rospy.loginfo("Az number of steps %d",message.az)
                rospy.loginfo("Al number of steps %d",message.al)
                pub_num_steps_to_uC.publish(message)
                if not self.latch:
                    self.msg = None

                self.mutex.release()
                return message
            self.mutex.release()
            if(~(rospy.get_param("/close_loop_flag"))):
                return 'to_open_loop'
        print('Timeout!')
        return None

    # execute() What is done in the state. Careful with the return of state.
    def execute(self, ud):
        loopstatus = rospy.get_param("/close_loop_flag")
        if(loopstatus):
            while(True):
                msg = self.waitForMsg()
                if(msg == 'to_open_loop'):
                    return 'to_open_loop'
                if msg != None:
                    pub_num_steps_to_uC.publish(msg)
                    return 'succeeded'
                else:
                    return 'aborted'
        elif(not loopstatus):
            return 'to_open_loop'




def main():

    rospy.init_node('SolarStateMachine')


    # Top level state machine
    level1_state_machine = smach.StateMachine(outcomes=['ShottingDown','WaringMode'])

    with level1_state_machine:
      
        # Must add homming state inside INIT_STATE
        smach.StateMachine.add('INITSTATE',InitState(),
                                transitions={'to_open_loop':'OPENLOOPSTATE',
                                             'not_ready_to_start':'INITSTATE',
                                              })

        # Open loop state. System start in this state until, camera detect the sun.
        smach.StateMachine.add('OPENLOOPSTATE', OpenLoopState(), 
                               transitions={'succeeded':'OPENLOOPSTATE',
                                            'to_close_loop': 'CLOSELOOPSTATE', 
                                            'aborted':'WaringMode'})

        # Close loop state. System enter this state if camera detect the sun. Refresh every 5s the loop.
        smach.StateMachine.add('CLOSELOOPSTATE', CloseLoopState(), 
                        transitions={'succeeded':'CLOSELOOPSTATE',
                                    'to_open_loop': 'OPENLOOPSTATE', 
                                    'aborted':'WaringMode'})

        # If the wind speed exceed the maximun value, the system transist to other machine state (Level 0)
  


    outcome = level1_state_machine.execute()



if __name__ == '__main__':
    main()



