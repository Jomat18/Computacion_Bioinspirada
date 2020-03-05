
import numpy as np 
import sys  
import math 
import copy

def normal(x, desv): 
    retorno=-0.5*((x/desv)*(x/desv))
    retorno=pow(np.e,retorno)
    return float("%.5f"%(retorno/(desv*(np.sqrt(6.283184)))))


def valor_x(lim_inf, lim_sup, desviacion, delta, aleatorio):	
    area=0.0	
    aux = normal(lim_inf, desviacion)
    i=lim_inf+delta
    aux_suma=0.0	

    while i<lim_sup: 	
	aux_suma = normal(i,desviacion)
	area=area+(aux+aux_suma)
        if (area*(delta/2))>aleatorio:
		return float("%.5f"%i)

	aux=aux_suma
	i=i+delta

    return -1*(1.0)*(sys.maxint)	
#sys.maxint  

def fitness(ind1, ind2):
    return float("%.5f"%(100*(pow(pow(ind1,2)-ind2,2))+pow(1-ind1,2)))
    #return ind1+ind2	

def generacion(pob, desviacion):
    		
    n_exito=0
    hijo=pob.copy()	
    valor=0.0		
    valor_h=0.0
    ps=0.0
    r=0.0	    	    		
    
    for j in range(1000):
	print ("**************************Iteracion:", j+1 ,"************************************")
	print("Desviacion: ",desviacion)
			
	r=np.random.uniform(0,1)
	hijo[0] = pob[0] + valor_x(l_min, l_sup, desviacion[0], delta, r) 
	if hijo[0]>2.048:	hijo[0]=2.048
	if hijo[0]<-2.048: 	hijo[0]=-2.048

	r=np.random.uniform(0,1)
        hijo[1] = pob[1] + valor_x(l_min, l_sup, desviacion[1], delta, r)
	if hijo[1]>2.048:	hijo[1]=2.048
	if hijo[1]<-2.048: 	hijo[1]=-2.048

	valor=fitness(pob[0],pob[1])
	print("Aptitud Padre: ", valor)

	valor_h = fitness(hijo[0],hijo[1])
	print("Aptitud Hijo: ", valor_h)

	if valor<valor_h:
		print("Muto")
		pob[0]=hijo[0]
		pob[1]=hijo[1]
		n_exito=n_exito+1

	if j%mutaciones==0:
		ps = n_exito/(mutaciones)
		if ps<0.2:
			desviacion[0] = float("%.5f"%(desviacion[0]*0.817))
			desviacion[1] = float("%.5f"%(desviacion[1]*0.817))
			
		if ps>0.2:
			desviacion[0] = float("%.5f"%(desviacion[0]/0.817))
			desviacion[1] = float("%.5f"%(desviacion[1]/0.817))
	
		print("Exitos: ", n_exito)
		n_exito=0

    print(pob)


desviacion = [0.3,0.3]
l_min = -2.048
l_sup = 2.048
delta=0.01
mutaciones=10
pob_inicial=np.random.uniform(-2.048,2.048, size=2)
generacion(pob_inicial,desviacion)


