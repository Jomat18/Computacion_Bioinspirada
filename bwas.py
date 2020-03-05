import numpy as np
import copy 
import sys 

'''
distancias=[[0,50,50,94,50],
	    [50,0,22,50,36],
	    [50,22,0,44,14],
	    [94,50,44,0,50],
	    [50,36,14,50,0]]			


flujo=[[0,0,2,0,3],
       [0,0,0,3,0],
       [2,0,0,0,0],
       [0,3,0,0,1],
       [3,0,0,1,0]]
'''
'''
distancias=[[0,12,6,4],
	    [12,0,6,8],
	    [6,6,0,7],
	    [4,8,7,0]]			


flujo=[[0,3,8,3],
       [3,0,2,4],
       [8,2,0,5],
       [3,4,5,0]]

'''

distancias=[[0,35,71,99,71,75,41],
	    [35,0,42,80,65,82,47],
	    [71,42,0,45,49,79,55],
	    [99,80,45,0,36,65,65],
	    [71,65,49,36,0,31,32],			
	    [75,82,79,65,31,0,36],
	    [41,47,55,65,32,36,0]]	
	    		

flujo=[[0,2,0,0,0,0,2],
       [2,0,3,0,0,1,0],
       [0,3,0,0,0,1,0],
       [0,0,0,0,3,0,1],
       [0,0,0,3,0,0,0],
       [0,1,1,0,0,0,0],
       [2,0,0,1,0,0,0]]			

orden=['A','B','C','D','E','F','G']
#orden=['A','B','C','D']
#orden=['A','B','C','D','E']

	

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


def producto_punto(f, d, size):
	resultado=0;	
	for i in range(size):
		resultado+=f[i]*d[i]		
			
	return resultado

def columna_fila(index,size):
	fila=[]
	for i in range(size):
		fila.append(distancias[i][index])
	
	return fila

def m_visibilidad():
	size=len(distancias)
	visibilidad=[0]*size
	for i in range(size):
		visibilidad[i]=[0]*size
		for j in range(size):
			e_ij = producto_punto(flujo[i],columna_fila(j,size),size)
			if e_ij==0:
				visibilidad[i][j]=float("%.5f"%(1.0/0.01))#0.0		
			else: 
				visibilidad[i][j]=float("%.5f"%(1.0/e_ij))
			

	return visibilidad


def m_feromonas():
	size=len(distancias)
	feromonas=[0]*size
	for i in range(size):
		feromonas[i]=[0]*size
		for j in range(size):
			if i!=j:
				feromonas[i][j]=feromona_inicial
			else:
				feromonas[i][j]=0

	return feromonas


def fitness(permutacion):
	costo=0
	size=len(permutacion)
	
	for i in range(size):
		fila=ord(permutacion[i])%65
		permutacion_copy=copy.copy(permutacion)
		a=range(size)
		a.remove(i)
		permutacion_copy.pop(i)
		for j,k in zip(a,permutacion_copy): 				
			costo+=flujo[i][j]*distancias[fila][ord(k)%65]	

	return costo



def diversificacion(permutacion,permutacion_i,valor_inicial):
	valor_temp=valor_inicial
	suma=0		
	size=len(permutacion)
	probabilidad=[0.0]*size
	for i in range(size):
		t=feromona[ord(valor_inicial)%65][ord(permutacion[i])%65]
		t=pow(t,alpha) 
		n=visibilidad[ord(valor_inicial)%65][ord(permutacion[i])%65] 
		n=pow(n,beta) 
		probabilidad[i]=t*n	
		suma+=t*n	
			
	suma_probabilidad=0.0
	for i in range(size):
		if suma==0.0:		
			probabilidad[i]=float("%.5f"%((probabilidad[i]/0.01)+suma_probabilidad))
		else:
			probabilidad[i]=float("%.5f"%((probabilidad[i]/suma)+suma_probabilidad))

		suma_probabilidad+=probabilidad[i]
	
	aleatorio=np.random.uniform(0,1)
	
	for i in range(size):
		if aleatorio<probabilidad[i]:
			valor_inicial=permutacion[i]
			permutacion_i.append(valor_inicial)	
			permutacion.remove(valor_inicial)
			break

	temp=(1-fi)*(feromona[ord(valor_temp)%65][ord(valor_inicial)%65])	
	actualizar_feromona=temp+fi*feromona_inicial
	feromona[ord(valor_temp)%65][ord(valor_inicial)%65]=float("%.5f"%(actualizar_feromona))
	feromona[ord(valor_inicial)%65][ord(valor_temp)%65]=float("%.5f"%(actualizar_feromona))
	return valor_inicial


def intensificacion(permutacion,permutacion_i,valor_inicial):
	valor_temp=valor_inicial
	argmax=[]
	size=len(permutacion)
	for i in range(size):
		t=feromona[ord(valor_inicial)%65][ord(permutacion[i])%65]
		t=pow(t,alpha) 
		n=visibilidad[ord(valor_inicial)%65][ord(permutacion[i])%65] 
		n=pow(n,beta) 
		argmax.append(t*n)

	mayor=np.argsort(argmax)
	valor_inicial=permutacion[mayor[size-1]]
	permutacion_i.append(valor_inicial)
	permutacion.remove(valor_inicial)

	temp=(1-fi)*(feromona[ord(valor_temp)%65][ord(valor_inicial)%65])	
	actualizar_feromona=temp+fi*feromona_inicial
	feromona[ord(valor_temp)%65][ord(valor_inicial)%65]=float("%.5f"%(actualizar_feromona))
	feromona[ord(valor_inicial)%65][ord(valor_temp)%65]=float("%.5f"%(actualizar_feromona))
	return valor_inicial


def calcular_permutacion_i(permutacion):
	permutacion_i=[]
	#valor_inicial=orden[1]
	valor_inicial=np.random.choice(orden)
	permutacion_i.append(valor_inicial)
	permutacion.remove(valor_inicial)
	while len(permutacion)!=0:
		q=np.random.uniform(0,1)
		if q>q0:
			valor_inicial=diversificacion(permutacion,permutacion_i,valor_inicial)	
		if q<=q0:
			valor_inicial=intensificacion(permutacion,permutacion_i,valor_inicial)
				
	return permutacion_i


def encontrar_arco(inicio, fin, permutacion):
	for r in range(len(permutacion)-1):
		if inicio==permutacion[r] or fin==permutacion[r]:
			if  inicio==permutacion[r+1] or fin==permutacion[r+1]:
				return True
							
	return False



def mutacion(inicio, fin, list_feromonas):
	umbral=(sum(list_feromonas))/n_hormigas
	aleatorio=np.random.uniform(0,1)
	if umbral==0:  umbral=0.01	
	mutacion=feromona[ord(inicio)%65][ord(fin)%65]+valor_x(-1.0*umbral, umbral, umbral, delta, aleatorio)
	if mutacion>umbral:
		mutacion=umbral
	if mutacion<(-1.0)*umbral:
		mutacion=(-1.0)*umbral
	feromona[ord(inicio)%65][ord(fin)%65]=float("%.5f"%(mutacion))
	feromona[ord(fin)%65][ord(inicio)%65]=float("%.5f"%(mutacion))	


def actualizar_feromona(permutacion_global, best_global):
	size=len(orden)
	sumas=[0.0]
	list_feromonas=[]
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=orden[i]
			fin=orden[j]				
			
			if encontrar_arco(inicio,fin,permutacion_global): 	
				suma_delta=(1-p)*feromona[ord(inicio)%65][ord(fin)%65]
				sumas.append(suma_delta)
				temp=(1.0/best_global)*100
				sumas.append(temp)
				list_feromonas.append(sum(sumas))
				
			else: 	
				suma_delta=(1-p)*feromona[ord(inicio)%65][ord(fin)%65]
				sumas.append(suma_delta)			
				sumas.append(0.0)	
				
			actualizar=sum(sumas)
			print(inicio,fin,"valor: ",actualizar)
			del sumas[:]
			feromona[ord(inicio)%65][ord(fin)%65]=float("%.5f"%(actualizar))
			feromona[ord(fin)%65][ord(inicio)%65]=float("%.5f"%(actualizar))

	
			r=np.random.uniform(0,1)	
			if r<0.2:
				mutacion(inicio, fin, list_feromonas)

	del list_feromonas[:]


def generaciones():
	contador=0
	fitness_temp=0.0
	
	permutacion_hormigas=[0]*n_hormigas
	for i in range(n_hormigas):
		permutacion_hormigas[i]=[0]*len(orden)

	fitness_hormigas=[0.0]*n_hormigas
	best_global=100000000	
	best_permutacion=[0]*len(orden)
	
	for j in range(n_iteraciones):
		print("********************Iteracion: ",j+1,"**********************")
		for i in range(n_hormigas):
			permutacion=copy.copy(orden)
			permutacion_hormigas[i]=calcular_permutacion_i(permutacion)
			fitness_hormigas[i]=fitness(permutacion_hormigas[i])
			print("Hormiga: ",i+1,permutacion_hormigas[i]," Costo: ", fitness_hormigas[i])

		indices=np.argsort(fitness_hormigas)
		if fitness_hormigas[indices[0]]<best_global:
			best_global=fitness_hormigas[indices[0]]
			best_permutacion=permutacion_hormigas[indices[0]]

		if j%(n_iteraciones/5)==0:
			if fitness_hormigas[indices[0]]>best_global:
				feromona = m_feromonas()			

		print("Mejor hormiga global:",best_permutacion,"costo:", best_global)
		actualizar_feromona(best_permutacion, best_global)
		


#Parametros
p=0.99
q0=0.7
alpha = 1
beta = 1
fi=0.05
q=1
delta=0.01
feromona_inicial = 0.1
n_hormigas = 6
n_iteraciones = 100
visibilidad = m_visibilidad()
feromona = m_feromonas()
generaciones()


















