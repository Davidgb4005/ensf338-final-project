import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import DataStructures.Deque as dq


class SerivceInfo():
    def __init__(self,name,contact_number,description):
        self.name = name
        self.contact_number = contact_number
        self.description = description
        pass



class ServiceQue:
    def __init__(self):
        self.buffer = [dq.Deque]
        self.prio= {"High":0,"Med":1,"Low":2}
        for i in len(self.prio):
            self.buffer.append(dq.Deque())
        pass

    def append_service(self,service_info:SerivceInfo,prio):
        self.buffer[prio].append_tail(service_info)
    
    def pop_service(self):
        top_prio = None
        for i in self.buffer:
            if i.get_len()>0:
                top_prio = i
                break
        
        if top_prio:
            return [i,top_prio.pop_head()]
        else:
            print("Services Buffer Empty")
            return None
        