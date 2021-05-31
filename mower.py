#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 22:32:05 2021

@author: Amin Henteti
"""

class Mower():
  #class attributes 
  Rcorner=(1,1)
  Lcorner=(0,0) # fixed
  orientations=("N", "E", "S", "W") # must be in circular order
  busy_lawn_coord=[] # contain the occupied coord inside the lawn, its structures is list of tuples
  mowers=[]#list of the working mowers
  def __init__(self, init_state, R_corner, L_corner=(0,0), name='m'):
    self.X, self.Y, self.O = init_state #unpack the list of arg
    Mower.Rcorner = R_corner
    Mower.Lcorner = L_corner
    self.name=name+'_'+str(len(Mower.mowers)+1)# len(Mower.mowers) play the role of an identifier
    Mower.mowers.append(self.name)
    Mower.occupy_coord(self.X,self.Y)
  def __str__(self):
      return f"The mower {self.name} is at {' '.join(map(str,self.get_state()))}"
  @classmethod
  def occupy_coord(cls,X,Y):
      cls.busy_lawn_coord.append((X,Y))
  @classmethod
  def release_coord(cls,X,Y):
      cls.busy_lawn_coord.remove((X,Y))
  def Fcommand(self):
    """
    move forward with the present orientation
    """
    X,Y = self.X, self.Y
#    print(X); print(Y)
    Mower.release_coord(X,Y)
    state_copy=[X,Y,self.O]#save the old state, maybe used afterwards for non-admissible command
    if self.O=='N':
      self.Y+=1
    if self.O=='E':
      self.X+=1
    if self.O=='W':
      self.X-=1
    if self.O=='S':
      self.Y-=1
    if self.admissible_command():
        Mower.occupy_coord(self.X,self.Y)
    else:
        self.X, self.Y, self.O=state_copy # discard the move
        Mower.occupy_coord(X,Y)
    #the orientation remains inchanged
  def Lcommand(self):
    """
    turn 90° to the left so 'N' becomes 'W'
    """
    o_ind=Mower.orientations.index(self.O)
    self.O = Mower.orientations[o_ind-1] # No need to test the range thnaks to python indexing logic
    #X,Y coordinates remains inchanged
  def Rcommand(self):
    """
    turn 90° to the right so 'N' becomes 'E'
    """
    o_ind=Mower.orientations.index(self.O)
    self.O = Mower.orientations[o_ind+1] if o_ind+1 < 4 else Mower.orientations[0]  # otherwise we would have out of range error
    #X,Y coordinates remains inchanged
  def admissible_command(self):
      #check if out of out_of_boundaries
      if self.X > Mower.Rcorner[0] or self.Y > Mower.Rcorner[1]:
          print('exceeding right boundaries of the lawn')
          return False
      if self.X < Mower.Lcorner[0] or self.Y < Mower.Lcorner[1]:
          print('exceeding left boundaries of the lawn')
          return False
      #availibiblity of the coord
      if (self.X, self.Y) in Mower.busy_lawn_coord:
          print('confronting an existing mower')
          return False
#      print('admissible_command')
      return True
  def execute_command(self, command):
      if command=='F':
          self.Fcommand()
      if command=='L':
          self.Lcommand()
      if command=='R':
          self.Rcommand()
      if command==" ": #artificial case to deal with different lengths of cammands for multiple mowers
          pass #state won't change
  def get_state(self):
      return [self.X, self.Y, self.O]
if __name__=='__main__':
    from main import cast_list, cast_elt # import here to avoid circular import 
    R_corner=cast_list("5 5".split(' '))
    init_state1 = cast_list("1 2 N".split(" "))
    m1=Mower(init_state1,R_corner)
    init_state2 = cast_list("3 3 E".split(" "))
    m2=Mower(init_state2,R_corner)   
    print(m1); print(m2)
    commands1=list('LFLFLFLFF')#dissociate each character in the string
    commands2=list('EFFRFFRFRRF')# i think must have the same numbers of commands for all the mowers
    #otherwise we should the commands should have the time of execution
    maxi=max(len(commands1), len(commands2))
    commands1=commands1+(maxi-len(commands1))*[' ']
    commands2=commands2+(maxi-len(commands2))*[' ']
    for c1,c2 in zip(commands1,commands2):
        print(f"After the command {c1} on {m1.name}")
        m1.execute_command(c1)
        print(m1)
        print(f"After the command {c2} on {m2.name}")
        m2.execute_command(c2)
        print(m2)    
        print(50*'_')