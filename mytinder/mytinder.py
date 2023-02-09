import sys
import funciones

dades=funciones.llegirDades("./dades")

comanda=sys.argv[1]
if len(sys.argv)>2:
    par1=sys.argv[2]
if len(sys.argv)>3:
    par2=sys.argv[3]

if comanda == 'list':
    print(list("./dades"))
if comanda == 'affinity':
    print(funciones.affinity(par1, par2))
if comanda == 'best':
    print(funciones.best(par1))
if comanda == 'worse':
    print(funciones.worse(par1))