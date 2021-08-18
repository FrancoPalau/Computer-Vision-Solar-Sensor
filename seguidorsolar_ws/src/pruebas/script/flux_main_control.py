#!/usr/bin/env python
# coding=utf-8

# INPUTS: SETS_POINTS FROM BOTH OPENLOOP OR CLOSELOOP
# OUTPUTS: NUMS_STEPS TO ROSSERIAL 

import threading
from pruebas.msg import numsteps
import rospy
import smach
from smach import user_data
import smach_ros

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
        if(not loopstatus):
            msg = self.waitForMsg()
            if(msg == 'to_close_loop'):
                return 'to_close_loop'
            if msg != None:
                pub_num_steps_to_uC.publish(msg)
                return 'succeeded'

            else:
                return 'aborted'
        elif(loopstatus):
            return 'to_close_loop'

class CloseLoopState(smach.State):
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

    def waitForMsg(self):
        print('Waiting for setpoint...')
        timeout_time = rospy.Time.now() + rospy.Duration.from_sec(self.timeout)
        while rospy.Time.now() < timeout_time:
            if(~(rospy.get_param("/close_loop_flag"))):
                return 'to_open_loop'
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
        if(loopstatus):
            msg = self.waitForMsg()
            if(msg == 'to_open_loop'):
                return 'to_open_loop'
            if msg != None:
                return 'succeeded'
            else:
                return 'aborted'
        elif(not loopstatus):
            return 'to_open_loop'



def main():

    rospy.init_node('SolarStateMachine')


    sm = smach.StateMachine(outcomes=['ShottingDown','WaringMode'])

    with sm:
      
        smach.StateMachine.add('INITSTATE',InitState(),
                                transitions={'to_open_loop':'OPENLOOPSTATE',
                                             'not_ready_to_start':'INITSTATE',
                                              })
        smach.StateMachine.add('OPENLOOPSTATE', OpenLoopState(), 
                               transitions={'succeeded':'OPENLOOPSTATE',
                                            'to_close_loop': 'CLOSELOOPSTATE', 
                                            'aborted':'WaringMode'})
        smach.StateMachine.add('CLOSELOOPSTATE', CloseLoopState(), 
                        transitions={'succeeded':'CLOSELOOPSTATE',
                                    'to_open_loop': 'OPENLOOPSTATE', 
                                    'aborted':'WaringMode'})


    outcome = sm.execute()


if __name__ == '__main__':
    main()



