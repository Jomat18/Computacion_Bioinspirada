import numpy as np
import copy

#del a[i] i indice
# a.pop(i) i indice
# a.remove(elemento) 
'''
distancias=[[0,12,3,23,1],
	    [12,0,9,18,3],
	    [3,9,0,89,56],
	    [23,18,89,0,87],
	    [1,3,56,87,0]]			

'''

distancias=[[0,12,3,23,1,5,23,56,12,11],
             [12,0,9,18,3,41,45,5,41,27],
             [3,9,0,89,56,21,12,48,14,29],
             [23,18,89,0,87,46,75,17,50,42],
             [1,3,56,87,0,55,22,86,14,33],
             [5,41,21,46,55,0,21,76,54,81],
             [23,45,12,75,22,21,0,11,57,48],
             [56,5,48,17,86,76,11,0,63,24],
             [12,41,14,50,14,54,57,63,0,9],
             [11,27,29,42,33,81,48,24,9,0]]
            

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


def calcular_ruta(ciudades_destino):
	ruta=[]
	ciudad_inicial='D' #ciudades[0]
	#ciudad_inicial=np.random.choice(ciudades)
	ruta.append(ciudad_inicial)
	ciudades_destino.remove(ciudad_inicial)
	while len(ciudades_destino)!=0:
		suma=0		
		size=len(ciudades_destino)
		probabilidad=[0.0]*size
		for i in range(size):
			t=feromona[ord(ciudad_inicial)%65][ord(ciudades_destino[i])%65]
			t=pow(t,alpha) 
			n=visibilidad[ord(ciudad_inicial)%65][ord(ciudades_destino[i])%65] 
			n=pow(n,beta) 
			probabilidad[i]=t*n
			suma+=t*n	
	
		hasta=len(probabilidad)
		suma_probabilidad=0
		for i in range(hasta):
			probabilidad[i]=(probabilidad[i]/suma)+suma_probabilidad
			suma_probabilidad+=probabilidad[i]


		aleatorio=np.random.uniform(0,1)
		
		for i in range(hasta):
			if aleatorio<probabilidad[i]:
				ciudad_inicial=ciudades_destino[i]
				ruta.append(ciudad_inicial)	
				ciudades_destino.remove(ciudad_inicial)
				break

				
	return ruta

def fitness(ruta):
	costo=0
	size=len(ruta)-1
	for i in range(size):
		costo+=distancias[ord(ruta[i])%65][ord(ruta[i+1])%65]	

	return costo

def actualizar_feromona(rutas, fitness_hormigas):
	size=len(distancias)
	sumas=[0.0]
	agregar=True
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=ciudades[i]
			fin=ciudades[j]
			suma_delta=p*feromona[ord(inicio)%65][ord(fin)%65]  #corregir
			sumas.append(suma_delta)			
			for k in range(n_hormigas):
			 	for r in range(len(rutas[k])-1):
					if inicio==rutas[k][r] or fin==rutas[k][r]:
						if  inicio==rutas[k][r+1] or fin==rutas[k][r+1]:
							temp=(1-p)*fitness_hormigas[k]  #corregir
							agregar=False
							sumas.append(temp)
							break
				
				if agregar:			
					sumas.append(0.0)
				
				agregar=True	
					
			#print(sumas)
			actualizar=sum(sumas)		
			print(inicio,fin,"valor: ",actualizar)
			del sumas[:]
			feromona[ord(inicio)%65][ord(fin)%65]=actualizar
			feromona[ord(fin)%65][ord(inicio)%65]=actualizar



def generaciones():
	rutas=[None]*n_hormigas
	for i in range(n_hormigas):
		rutas[i]=[None]*len(ciudades)

	fitness_hormigas=[0.0]*n_hormigas
	best_global=100000000	
	best_permutacion=[0]*len(ciudades)	
	
	for m in range(n_iteraciones):
		print("********************Iteracion: ",m+1,"**********************")
		for i in range(n_hormigas):
			ciudades_destino=copy.copy(ciudades)
			rutas[i]=calcular_ruta(ciudades_destino)
			fitness_hormigas[i]=fitness(rutas[i])
			print("Hormiga: ",i+1,rutas[i]," costo: ", fitness_hormigas[i])

		indices=np.argsort(fitness_hormigas)
		if fitness_hormigas[indices[0]]<best_global:
			best_global=fitness_hormigas[indices[0]]
			best_permutacion=rutas[indices[0]]

		print("Mejor hormiga global:",best_permutacion,"costo:",best_global)
		actualizar_feromona(rutas,fitness_hormigas)
	
	print("********************Final*********************")
	menor=np.argsort(fitness_hormigas)
	print(rutas[menor[0]],"Costo: ",fitness_hormigas[menor[0]])

#Parametros
p = 0.99
alpha = 1
beta = 1
q = 1.0
feromona_inicial = 0.1
n_hormigas = 3
n_iteraciones = 10
visibilidad = m_visibilidad()
feromona = m_feromonas()
ciudades=['A','B','C','D','E','F','G','H','I','J']
#ciudades=['A','B','C','D','E']
generaciones()



















