import numpy as np
import copy 

distancias=[[0,12,3,23,1,5,23,56,12,11,89,97,52],
            [12,0,9,18,3,41,45,5,41,27,16,76,56],
             [3,9,0,89,56,21,12,48,14,29,5,91,8],
             [23,18,89,0,87,46,75,17,50,42,100,70,15],
             [1,3,56,87,0,55,22,86,14,33,31,84,21],
             [5,41,21,46,55,0,21,76,54,81,92,37,22],
             [23,45,12,75,22,21,0,11,57,48,39,59,22],
             [56,5,48,17,86,76,11,0,63,24,55,58,98],
             [12,41,14,50,14,54,57,63,0,9,44,18,52],
             [11,27,29,42,33,81,48,24,9,0,64,65,82],		
	     [89,16,5,100,31,92,39,55,44,64,0,9,70],
	     [97,76,91,70,84,37,59,58,18,65,9,0,50],
             [52,56,8,15,21,22,22,98,52,82,70,50,0]]				

def permutacion(lista, size):
	a=np.random.randint(size)
	b=np.random.randint(size)
	while(a==b):
		b=np.random.randint(size)
	
	temp=lista[a]
	lista[a]=lista[b]
	lista[b]=temp
	return lista

def m_visibilidad():
	size=len(distancias)
	visibilidad=[0]*size
	for i in range(size):
		visibilidad[i]=[0]*size
		for j in range(size):
			if i!=j:
				visibilidad[i][j]=float("%.5f"%(1.0/distancias[i][j]))
			else:
				visibilidad[i][j]=0

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


def fitness(ruta):
	costo=0
	size=len(ruta)-1
	for i in range(size):
		costo+=distancias[ord(ruta[i])%65][ord(ruta[i+1])%65]	

	return costo



def diversificacion(permutacion,permutacion_i,valor_inicial):
	valor_temp=valor_inicial
	suma=0.0		
	size=len(permutacion)
	probabilidad=[None]*size
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
	valor_inicial='D'  #orden[1]
	#valor_inicial=np.random.choice(orden)
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


def mutacion(solucion, n_hijos, fit_solucion):
	temp=copy.copy(solucion)
	size=len(solucion)	
	for i in range(n_hijos):
		temp=permutacion(temp,size)
		valor=fitness(temp)
		if valor<fit_solucion:
			solucion=temp
			fit_solucion=valor

	return solucion, fit_solucion


def escalada(solucion, n_escaladas, fit_solucion, n_hijos):
	for i in range(n_escaladas):
		solucion, fit_solucion=mutacion(solucion,n_hijos,fit_solucion)

	return solucion, fit_solucion

def actualizar_arcos(permutacion_global, best_global):
	size=len(distancias)
	sumas=[0.0]
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=orden[i]
			fin=orden[j]	
			if encontrar_arco(inicio,fin,permutacion_global): 	
				suma_delta=p*feromona[ord(inicio)%65][ord(fin)%65]
				sumas.append(suma_delta)									
				temp=(1.0/best_global)
				sumas.append(temp)
				actualizar=sum(sumas)
				del sumas[:]
				feromona[ord(inicio)%65][ord(fin)%65]=float("%.5f"%(actualizar))
				feromona[ord(fin)%65][ord(inicio)%65]=float("%.5f"%(actualizar))


def actualizar_feromona(permutacion_global, best_global):
	size=len(orden)
	sumas=[0.0]
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=orden[i]
			fin=orden[j]	
			suma_delta=p*feromona[ord(inicio)%65][ord(fin)%65]
			sumas.append(suma_delta)			
			
			if encontrar_arco(inicio,fin,permutacion_global): 	
				temp=(1-p)*(1.0/best_global)*100
				sumas.append(temp)
				
			else: 				
				sumas.append(0.0)	
				
			actualizar=sum(sumas)
			print(inicio,fin,"valor: ",actualizar)
			del sumas[:]
			feromona[ord(inicio)%65][ord(fin)%65]=float("%.5f"%(actualizar))
			feromona[ord(fin)%65][ord(inicio)%65]=float("%.5f"%(actualizar))



def generaciones():
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
			permutacion_hormigas[i],fitness_hormigas[i]=escalada(permutacion_hormigas[i],n_escaladas,fitness_hormigas[i],n_hijos)
			print("Hormiga escalonada: ",i+1,permutacion_hormigas[i]," costo escalonado: ", fitness_hormigas[i])
			actualizar_arcos(permutacion_hormigas[i],fitness_hormigas[i])

		indices=np.argsort(fitness_hormigas)
		if fitness_hormigas[indices[0]]<best_global:
			best_global=fitness_hormigas[indices[0]]
			best_permutacion=permutacion_hormigas[indices[0]]

		print("Mejor hormiga global:",best_permutacion,"costo:", best_global)
		actualizar_feromona(best_permutacion, best_global)

	print("********************Final*********************")
	print("Mejor hormiga global:",best_permutacion,"costo:", best_global)
		


#Parametros
p=0.99 
q0=0.7
alpha = 1
beta = 1
fi=0.05
q=1
feromona_inicial = 0.1
n_hormigas = 3
n_escaladas = 10
n_hijos = 10
n_iteraciones = 10
visibilidad = m_visibilidad()
feromona = m_feromonas()
orden=['A','B','C','D','E','F','G','H','I','J','K','L','M']
generaciones()










