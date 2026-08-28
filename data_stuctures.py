#--------------------------------------Imports------------------------------------#
from macros import *


#-------------------------------------Classes---------------------------------------#
class Circular_Queue:
    def __init__(self, _size):
        self.array = []
        self.size = _size
        for i in range(self.size):
            self.array.append(None)
        self.start_ptr = None
        self.end_ptr = 0


    #end pointer points to next available space, and None if the queue is full
    #start pointer points to the next item to be dequeued and None if queue if empty

    def enqueue(self, _item): # Returns true if successful, false if unsuccessful

        #if full
        if self.end_ptr == None:
            return False

        #Actually adding item to array
        self.array[self.end_ptr] = _item
        
        #--------Adjusting pointers---------#

        #Adjusing start pointer
        if self.start_ptr == None:
            self.start_ptr = self.end_ptr

        #Adjusting end pointer
        #if one away from being full
        if INCREMENT_CIRCULAR(self.end_ptr, self.size) == self.start_ptr:
            self.end_ptr = None
        #if not full and not close to being full
        else: 
            self.end_ptr = INCREMENT_CIRCULAR(self.end_ptr, self.size)
        return True
    

    def dequeue(self): # Returns item if successful, false if unsuccessful

        #if empty
        if self.start_ptr == None:
            return False
        
        #Setting item to return
        item_to_return = self.array[self.start_ptr]

        
        #---------Adjusting Pointers------#

        #Adjusting end pointer
        if self.end_ptr == None:
            self.end_ptr = self.start_ptr

        #Adjusting start pointer
        #if one away from being empty
        if INCREMENT_CIRCULAR(self.start_ptr, self.size) == self.end_ptr:
            self.start_ptr = None
        #if not empty and not close to being empty
        else:
            self.start_ptr = INCREMENT_CIRCULAR(self.start_ptr, self.size)

        
        return  item_to_return
    


    def get_array_of_items(self): #Returns array of items, with the first index of this new array representing the space where the start ptr is in the real array
                                  #Note that it will not include items available for cleanup

        #If empty
        if self.start_ptr == None:
            return []  

        #-------Initializing variables-----#
        array_to_return = []
        if self.end_ptr == None: #if full
            num_of_items = self.size
        else: #if not full
            num_of_items = (self.end_ptr - self.start_ptr + self.size) % self.size 
        # num_of_items is number of items in queue (excluding items in clearance)
        
        #setting starting index to look at
        if self.end_ptr == None:
            index_to_look = DECREMENT_CIRCULAR(self.start_ptr, self.size)
        else:
            index_to_look = DECREMENT_CIRCULAR(self.end_ptr, self.size)

        #--------main loop---------#
        for i in range(num_of_items):
            array_to_return.append(self.array[index_to_look])            
            index_to_look = DECREMENT_CIRCULAR(index_to_look, self.size)

        return array_to_return
    
    def get_is_full(self):
        return (self.end_ptr == None)
    
    def get_is_empty(self):
        return (self.start_ptr == None)
