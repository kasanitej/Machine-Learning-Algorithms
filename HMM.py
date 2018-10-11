import numpy as np
import numpy.ma as ma
from numpy.ma import filled
from numpy import log

def HMMViterbi(ESeq,T,E): #List,np.ndarray,np.ndarray
    logT=ma.log(np.matrix(T)).filled(np.NINF).T;#to avoid log(0) convert to -inf
    logE=ma.log(np.matrix(E)).filled(np.NINF).T;#to avoid log(0) convert to -inf
    No_ofStates=len(T);Seq_Lenth=len(ESeq);
    V=np.full((No_ofStates,1),np.NINF); V[0,0]=0;V1=np.copy(V);
    PTr=np.zeros((No_ofStates,Seq_Lenth));SSeq=[-1]*Seq_Lenth;
    for Idx,Ems in enumerate(ESeq):
        for Id,Tc in enumerate(logT):
            VTemp=np.copy(V1+Tc.T);
            V[Id]=max(VTemp);
            PTr[Id,Idx]=np.argmax(VTemp);
        V=V+logE[Ems].T;
        V1=np.copy(V);
    SSeq[Idx]=np.argmax(V1);
    #BackTracking
    for Idx in range(Seq_Lenth-2,-1,-1):
        SSeq[Idx]=int(PTr[SSeq[Idx+1]][Idx+1])
    return SSeq

def probability(Matrix):
    for a,b in enumerate(Matrix):
        Add=sum(b)
        if Add!=0:                                                #Sum up the entire row
            for i in range(len(b)):
                Matrix[a][i]=Matrix[a][i]/Add                         #divide each entry with sum
    return Matrix

def HmmEstimate(StateSignal,EmissionSignal):    #Only takes lists
    if(len(StateSignal)==len(EmissionSignal)):  #Comparing the size of Emission and Transisition Matrix

        #Emission Matrix creation
        Ematrix=np.zeros((max(StateSignal)+1,max(EmissionSignal)+1)) #Initiation of Emission Matrix
        for i in list(zip(StateSignal,EmissionSignal)):                 #clubbed both State & Emission signal for easy access
            Ematrix[i[0]][i[1]]+=1                                      #count the no.of entries per each state in the respective place
        Ematrix=probability(Ematrix)                                    #calling probability function

        #Transistion Matrix creation
        Tmatrix=np.zeros((max(StateSignal)+1,max(StateSignal)+1)) #Initiation of State Matrix
        for i in range(len(StateSignal)-1):
            Tmatrix[int(StateSignal[i])][int(StateSignal[i+1])]+=1      #count the each transistion in their respective place.
        Tmatrix=probability(Tmatrix)                                    #calling probability function
    else:
        Error('State Signal and Emission signal should be of same length')
        exit()
    return [Tmatrix,Ematrix]
