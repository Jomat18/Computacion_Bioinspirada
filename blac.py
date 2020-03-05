
import numpy as np
import copy

#del a[i] i indice
# a.pop(i) i indice
# a.remove(elemento) 

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
			inicio=ciudades[i]
			fin=ciudades[j]	
			if encontrar_arco(inicio,fin,permutacion_global): 	
				suma_delta=p*feromona[ord(inicio)%65][ord(fin)%65]
				sumas.append(suma_delta)									
				temp=(1.0/best_global)
				sumas.append(temp)
				actualizar=sum(sumas)
				del sumas[:]
				feromona[ord(inicio)%65][ord(fin)%65]=float("%.5f"%(actualizar))
				feromona[ord(fin)%65][ord(inicio)%65]=float("%.5f"%(actualizar))	
			


def actualizar_feromona(rutas, fitness_hormigas):
	size=len(distancias)
	sumas=[0.0]
	agregar=True
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=ciudades[i]
			fin=ciudades[j]
			suma_delta=p*feromona[ord(inicio)%65][ord(fin)%65]  
			sumas.append(suma_delta)			
			for k in range(n_hormigas):
			 	for r in range(len(rutas[k])-1):
					if inicio==rutas[k][r] or fin==rutas[k][r]:
						if  inicio==rutas[k][r+1] or fin==rutas[k][r+1]:
							temp=q/fitness_hormigas[k]  
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
			rutas[i],fitness_hormigas[i]=escalada(rutas[i],n_escaladas,fitness_hormigas[i],n_hijos)
			print("Hormiga escalonada: ",i+1,rutas[i]," costo escalonado: ", fitness_hormigas[i])
			actualizar_arcos(rutas[i],fitness_hormigas[i])
			

		menor=np.argsort(fitness_hormigas)
		if fitness_hormigas[menor[0]]<best_global:
			best_global=fitness_hormigas[menor[0]]
			best_permutacion=rutas[menor[0]]
		print("Mejor hormiga global:",best_permutacion,"costo:", best_global)
		actualizar_feromona(rutas,fitness_hormigas)
	
	print("********************Final*********************")
	print("Mejor hormiga global:",best_permutacion,"costo:", best_global)

#Parametros
p = 0.99
alpha = 1
beta = 1
q = 1.0
feromona_inicial = 0.1
n_hormigas = 3
n_iteraciones = 100
n_escaladas = 10
n_hijos = 10
visibilidad = m_visibilidad()
feromona = m_feromonas()
ciudades=['A','B','C','D','E','F','G','H','I','J','K','L','M']
#ciudades=['A','B','C','D','E']
generaciones()



















