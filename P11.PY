
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


def fitness(ind1, ind2):
	return float("%.5f"%(-1*np.cos(ind1)*np.cos(ind2)*np.exp(-1*pow((ind1-pi),2)-pow(ind2-pi,2))))


def vector_fitness(pob):
	vector=[0]*size
	for i in range(size):
		vector[i]=fitness(pob[i][0],pob[i][1])

	return vector
 
def poblacion(size_):
	pob = np.random.uniform(-10,10, size=(size_,2))
	desv=[0]*size
	
	for i in range(size_):
		desv[i]=[0]*2
		desv[i]=[desv_ini,desv_ini]
		
	return pob, desv


def torneo(pob, desv):	

	padres_=[0]*2
	for i in range(2):
                padres_[i]=[0]*2

	desv_=[0]*2
	for i in range(2):
                desv_[i]=[0]*2
	
        menor=1000000
	pos=0

	for i in range(2):
        	for j in range(n_concursantes):
                	n = np.random.randint(size)
                	valor=fitness(pob[n][0],pob[n][1])
                	if valor<menor:  
                	        menor=valor 
                	        pos=n
				

		padres_[i]=pob[n]
		desv_[i]=desv[n]
			

        return padres_[0], padres_[1], desv_[0], desv_[1]
 

def cruzamiento(padre1, padre2, desv1_,desv2_):
	hijo = [0.0,0.0]
	desv = [0.0,0.0]

	hijo[0]=float("%.5f"%(0.5*(padre1[0]+padre2[0])))
	hijo[1]=float("%.5f"%(0.5*(padre1[1]+padre2[1])))

	desv[0]=float("%.5f"%(np.sqrt(desv1_[0]+desv2_[0])))
	desv[1]=float("%.5f"%(np.sqrt(desv1_[1]+desv2_[1])))
		
	return hijo, desv


def mutacion(hijo, desv):
	variacion=float("%.5f"%(1/(np.sqrt(2*np.sqrt(size)))))
	r=np.random.uniform(0,1)	
	desv[0]=float("%.5f"%(desv[0]*np.exp(valor_x(l_min, l_sup, variacion, delta, r))))
	r=np.random.uniform(0,1)
	hijo[0]=float("%.5f"%(hijo[0]+valor_x(l_min, l_sup, desv[0], delta, r)))
	if hijo[0]>10:		hijo[0]=10
	if hijo[0]<-10: 	hijo[0]=-10

	r=np.random.uniform(0,1)
	desv[1]=float("%.5f"%(desv[1]*np.exp(valor_x(l_min, l_sup, variacion, delta, r))))
	r=np.random.uniform(0,1)
	hijo[1]=float("%.5f"%(hijo[1]+valor_x(l_min, l_sup, desv[1], delta, r))) 		
	if hijo[1]>10:		hijo[1]=10
	if hijo[1]<-10:  	hijo[1]=-10
	
	return hijo, desv


def determinista(hijo, desvh, pob, desvp):
	
	pob=np.append([hijo],pob, axis=0)
	desvp=np.append([desvh],desvp,axis=0)	
	vector=vector_fitness(pob)
	vector_copy=copy.copy(vector)
	indice = np.argsort(vector_copy)
	pob = np.delete(pob,indice[size-1],0)
	desvp = np.delete(desvp,indice[size-1],0)
	return pob, desvp	


def generaciones():
	pob,desv =poblacion(size)
	for i in range(1000):
		print("**************Iteracion: ", i+1, "*******************")
		p1, p2, desv1, desv2= torneo(pob, desv)
		hijo, desvh = cruzamiento(p1, p2, desv1, desv2)
		hijo, desvh = mutacion(hijo, desvh)
		print("*******************Poblacion***************************")
		print(pob)
		print("*******************Desviacion***************************")
		print(desv)
		print("*******************Fitness***************************")
		print(vector_fitness(pob))
		pob, desv = determinista(hijo, desvh, pob, desv)
			
	print("*************************Poblacion Final*********************")	
	print(pob)

pi=3.141592
size=10
l_min = -10
l_sup = 10
n_concursantes=10
desv_ini=0.3
delta=0.01
generaciones()

	








