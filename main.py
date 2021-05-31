#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 22:35:41 2021

@author: Amin Henteti
"""
from mower import Mower
def cast_elt(elt):
    """
    transform a char to int when possible
    """
    try:
        x=int(elt)
    except:
        x=elt #leave it as char
    return x
def cast_list(l):
    """
    transform a list of chars to int when possible
    """    
    return list(map(cast_elt,l))

if __name__=='__main__':
    file_name="input.txt"
    with open(file_name,'r') as f: #close automatically the file afterwards
        Lines=f.readlines(); n=len(Lines)
    L = [li[:-1] if li.endswith('\n') else li for li in Lines] #avoid \n in each line; maybe the last line dont have it
    nb_mowers = (n-1)//2 # first line IN the definition of a mower is dedicated for the initial state and the following line for its commands
    R_corner=cast_list(L[0].split(' '))
    mowers_simul=[]; commands=[]; 
    maxi=1
    print('Input : ')
    for i in range(nb_mowers):
        init_state = cast_list(L[1+2*i].split(" "))
        m=Mower(init_state,R_corner)
        mowers_simul.append(m)
        cmnd=list(L[2+2*i])#dissociate each character in the string
        commands.append(cmnd) # will have the same order as mowers_simul
        print('Initially', m, 'with commands :', ''.join(cmnd))
        maxi=max(maxi, len(cmnd)) # used to adjust the length of all commands
    for i in range(nb_mowers):
        commands[i]=commands[i]+(maxi-len(commands[i]))*[' '] # command ' ' don nothingfor the state of the mower
    for ind in range(maxi):
        # the simulaneous group of mowers is int fully clear so i imagined that 
        # the first mower does first cmnd then the second mower does its first command 
        # then we pass to the next command
        # this has an impact for the admissibility of every command
        for i in range(nb_mowers):
            m=mowers_simul[i]#take advantage of the mutability of the list
            c = commands[i][ind]
            m.execute_command(c)
#            print(f"After the command {c} on {m.name}")
#            print(m)
    #output final state
    print(f"Output : ")
    for m in mowers_simul: print(m)
    with open("output.txt",'w') as f: 
        for m in mowers_simul:
            f.write(' '.join(map(str,m.get_state()))+'\n'); 
