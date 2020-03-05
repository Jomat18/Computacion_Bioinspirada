import numpy
import copy

def fitness(x1,x2):
	fx=float("%.4f"%(pow(x1,2)+pow(x2,2)))
	if fx>=0:
		fit=float("%.4f"%(1.0/(1+fx)))
	else:
		fit=float("%.4f"%(1.0+abs(fx)))
	
	return fx,fit 	

def crear_soluciones(sol,xi,xf,yi,yf):
	print "************************ Fuente de Alimentos Iniciales ********************************"		
	poblacion=[]
	mejor=[0,0,0,-100000]
	for i in range(sol):	
		x_=[]		
		x_.append(float("%.4f"%(numpy.random.uniform(xi,xf))))
		x_.append(float("%.4f"%(numpy.random.uniform(yi,yf))))
		fx,fit=fitness(x_[0],x_[1])
		x_.append(fx)
		x_.append(fit)
		if x_[3]>mejor[3]:
			mejor[0]=x_[0]
			mejor[1]=x_[1]
			mejor[2]=x_[2]
			mejor[3]=x_[3]

		x_.append('')
		x_.append(0)
		poblacion.append(x_)
		
		print i+1," x1=",poblacion[i][0],"x2=",poblacion[i][1],"fx=",poblacion[i][2],"fit=",poblacion[i][3],"cont=",poblacion[i][5]
	print "Mejor Fuente: ","x1=",mejor[0],"x2=",mejor[1],"fx=",mejor[2],"fit=",mejor[3]
	print 
	
	return poblacion,mejor

def explorar(i,soluciones,mejor):
	cand=copy.copy(soluciones[i])
	fi=float("%.4f"%(numpy.random.uniform(-1,1)))
	temp=range(n_sol)
	temp.remove(i)
	k=numpy.random.choice(temp)
	j=numpy.random.randint(d)

	cand[j]=float("%.4f"%(soluciones[i][j]+fi*(soluciones[i][j]-soluciones[k][j])))	
	fx,fit=fitness(cand[0],cand[1])
	cand[2]=float("%.4f"%(fx))
	cand[3]=float("%.4f"%(fit))
	if cand[3]>soluciones[i][3]:
		cand[4]='Si'
		cand[5]=0
		soluciones[i]=cand
		if soluciones[i][3]>mejor[3]:
			mejor[0]=soluciones[i][0]
			mejor[1]=soluciones[i][1]						
			mejor[2]=soluciones[i][2]
			mejor[3]=soluciones[i][3]
			#print "Mejor:", mejor
			
	else:
		cand[4]='No'
		soluciones[i][5]=soluciones[i][5]+1
				
	print i+1," k:",k+1,"j:",j,"fi:",fi," x1=",cand[0],"x2=",cand[1],"fx=",cand[2],"fit=",cand[3],"M=",cand[4],"cont=",soluciones[i][5]	
	print "x1=",soluciones[k][0] ," x2=", soluciones[k][1]


def nuevas_soluciones(soluciones,mejor):
	print 
	print "************************ Soluciones Candidatas ********************************"
	for i in range(n_sol):
		explorar(i,soluciones,mejor)


def probabilidades(sol):
	suma=0
	probabilidad=[0.0]*n_sol
	for i in range(n_sol):	
		probabilidad[i]=sol[i][3]
		suma+=probabilidad[i]

	suma_probabilidad=0.0
	print 
	print "************************* Mejores Soluciones *********************************"

	for i in range(n_sol):
		probabilidad[i]=float("%.4f"%(((1.0)*probabilidad[i]/suma)))	
		suma_probabilidad+=probabilidad[i]
		probabilidad[i]=suma_probabilidad
		print i+1," x1=",sol[i][0],"x2=",sol[i][1],"fx=",sol[i][2],"fit=",sol[i][3],"Prob=",probabilidad[i],"cont=",sol[i][5]
	print "Sum=",suma
	
	print 
	return probabilidad

def observadoras_soluciones(sol,mejor):
	for i in range(n_sol):
		probabilidad=probabilidades(sol)
		print "************************ Observadora ",i+1,"********************************"
		aleatorio=numpy.random.uniform(0,1)
		print "Aleatorio: ",aleatorio
		pos=-1
		for i in range(n_sol):
			if aleatorio<probabilidad[i]:	
				pos=i	
				break

		explorar(pos,sol,mejor)

	probabilidad=probabilidades(sol)


def fuentes_abandonadas(sol):
	print
	print "***************************** Reemplazo Fuentes Abandonadas ***********************************"
	for i in range(n_sol):		
		if sol[i][5]>limite:
			r=numpy.random.uniform(0,1)
			sol[i][0]=float("%.4f"%(xmin+r*(xmax-xmin)))
			r=numpy.random.uniform(0,1)
			sol[i][1]=float("%.4f"%(ymin+r*(ymax-ymin)))
			sol[i][2],sol[i][3]=fitness(sol[i][0],sol[i][1])
			sol[i][4]=''
			sol[i][5]=0
			print i+1," x1=",sol[i][0],"x2=",sol[i][1],"fx=",sol[i][2],"fit=",sol[i][3],"cont=",sol[i][5]

	probabilidad=probabilidades(sol)
	

def abc(iteraciones):
	soluciones,mejor=crear_soluciones(n_sol,xmin,xmax,ymin,ymax)
	for i in range(iteraciones):		
		print "*************************Iteracion ",i+1,"***************************************"
		nuevas_soluciones(soluciones,mejor)
		observadoras_soluciones(soluciones,mejor)
		fuentes_abandonadas(soluciones)
		print "Memorizado ", "x1=",mejor[0],"x2=",mejor[1],"fx=",mejor[2],"fit=",mejor[3]
		print 
		

n_sol=10
xmax=5
xmin=-5
ymax=5
ymin=-5
size=6
d=2
limite=(size*d)/2
iteraciones=5
abc(iteraciones)


