# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

       

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        if random.random() < self.clearProb:
            return True
        else:
            return False

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if random.random() < (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()        
                            



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)     


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        clearNum = 0
        newViruses = []
        for virus in self.viruses:
            if virus.doesClear() == True:
                clearNum += 1
            else:
                popDensity = (float(self.getTotalPop())/self.maxPop)
                try:
                    newViruses.append(virus.reproduce(popDensity))
                except:
                    continue
                    
                            

        for i in range(clearNum):
            self.viruses.pop()

        #print newViruses
        self.viruses += newViruses
            
        #print "updated"

        return len(self.viruses)
            
                

        



#
# PROBLEM 2
#
##maxPop = 1000
##numStartViruses = 100
##Virus_maxBirthProb = .4
##Virus_clearProb = .1
##num_of_time_steps = 300
##
##                            
##viruses = []
##for i in range(numStartViruses):
##    viruses.append(SimpleVirus(Virus_maxBirthProb, Virus_clearProb))


def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    maxPop = 1000
    numStartViruses = 100
    Virus_maxBirthProb = .1
    Virus_clearProb = .05
    num_of_time_steps = 300

                            
    viruses = []
    for i in range(numStartViruses):
        viruses.append(SimpleVirus(Virus_maxBirthProb, Virus_clearProb))
    patient = SimplePatient(viruses, maxPop)
    virus_pop = []
    for i in range(num_of_time_steps):
        virus_pop.append(patient.update())
    return virus_pop[:]
    #pylab.plot(virus_pop, 'r+')
    #pylab.title('Virus Population over Time')
    #pylab.ylabel('Virus Population')
    #pylab.xlabel('Time (Hours)')
    #pylab.show()


def Trials():
    numTrials = 1000    
    trials = []                   
    for i in range(numTrials):
        trials.append(simulationWithoutDrug())

    total = [(sum(a)/float(numTrials)) for a in zip(*trials)]
    ##totals = []
    ##zipped = zip(trials)
    ##for i in range(len(zipped)):
    ##    totals.append(sum(zipped[i][0])/numTrials)

    pylab.plot(total)
    pylab.title('Virus Population over Time')
    pylab.ylabel('Virus Population')
    pylab.xlabel('Time (Hours)')
    pylab.show()

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/float(len(X)))**0.5



def roll(numTrials):
    y = 0
    for i in range(numTrials):
        d1 = random.randrange(1,7)
        d2 = random.randrange(1,7)
        d3 = random.randrange(1,7)
        d4 = random.randrange(1,7)
        d5 = random.randrange(1,7)
        if d1 == d2 == d3 == d4 == d5:
            y += 1
    return float(y)/numTrials

def rollSim(nt, nrpt):
    fracY = []
    for i in range(nt):
        fracY.append(roll(nrpt))
    return fracY

def plots(nr1, nr2, nt):
    fracY1 = rollSim(nt, nr1)
    #print fracY1
    mean1 = sum(fracY1)/float(len(fracY1))
    std1 = stdDev(fracY1)
    pylab.hist(fracY1, bins = 20)
    xmin,xmax = pylab.xlim()
    ymin,ymax = pylab.ylim()
    pylab.xlabel('Fraction of Yahtzees')
    pylab.ylabel('Triala')
    pylab.title(str(nt) + "trials of " + str(nr1) + 'rolls each')
    pylab.figure()
    fracY2 = rollSim(nt, nr2)
    mean2 = sum(fracY2)/float(len(fracY2))
    std2 = stdDev(fracY2)
    pylab.hist(fracY2, bins = 20)
    xmin,xmax = pylab.xlim()
    ymin,ymax = pylab.ylim()
    pylab.xlabel('Fraction of Yahtzees')
    pylab.ylabel('Triala')
    pylab.title(str(nt) + "trials of " + str(nr2) + 'rolls each')
    pylab.show()

print roll(10000000)

    


        
    
    
