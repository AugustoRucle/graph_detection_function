#-----------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

# A simple visitor for FuncDef nodes that prints the names and
# locations of function definitions.
listaDeclaracionesFunciones=[]
listaLlamadasFunciones=[]
class FuncDefVisitor(c_ast.NodeVisitor):
    def visit_FuncDef(self, node):
        filename = 'hash.c'
        #print('%s at %s' % (node.decl.name, node.decl.coord))
        nombre = '%s' % (node.decl.name)
        cordenada = '%s' % (node.decl.coord)
        tupla=(nombre,cordenada)
        listaDeclaracionesFunciones.append(tupla)
        show_func_calls(filename, node.decl.name)

def encontrarFunciones(filename):
    # Note that cpp is used. Provide a path to your own cpp or
    # make sure one exists in PATH.
    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-Iutils/fake_libc_include')

    nodoVisitaorDefiniciones = FuncDefVisitor()
    nodoVisitaorDefiniciones.visit(ast)

class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self, funcname):
        self.funcname = funcname
    
    def visit_FuncCall(self, node):
        if node.name.name == self.funcname:
            #print('%s called at %s' % (self.funcname, node.name.coord))
            nombre = '%s' % (self.funcname)
            cordenada = '%s' % (node.name.coord)
            tupla=(nombre,cordenada)
            listaLlamadasFunciones.append(tupla)
        # Visit args in case they contain more func calls.
        if node.args:
            self.visit(node.args)


def show_func_calls(filename, funcname):
    ast = parse_file(filename, use_cpp=True)
    v = FuncCallVisitor(funcname)
    v.visit(ast)

class funcionesLocalizacion(object):
    listaDefinicion=[]
    listaLlamadas=[]
    listaFunciones=[]
    def __init__(self,listaDefinicion,listaLlamadas):
        self.listaDefinicion=listaDefinicion
        self.listaLlamadas=listaLlamadas
    def agregarNombrePosicionFuncion(self, nombre, posicion):
        self.listaDefinicion.append(nombre)
        self.listaLlamadas.append(posicion)
    def contenidoLista(self):
        for posicion in range (0,len(self.listaDefinicion)) :
            nombre , llamado = self.listaDefinicion[posicion]
            inicioFuncion= self.obtenerNumero(llamado)
            finFuncion=99999
            if posicion+1<len(self.listaDefinicion):
                nombreTemp, llamadoTemp= self.listaDefinicion[posicion+1]
                finFuncion=self.obtenerNumero(llamadoTemp)-1
            listaTemp=[]
            for posicionListaLlamadas in range(0, len(self.listaLlamadas)):
                nombreFuncionLlamada, posicionFuncionLlamada = self.listaLlamadas[posicionListaLlamadas]
                posicionFuncionLlamada= self.obtenerNumero(posicionFuncionLlamada)
                
                if posicionFuncionLlamada>inicioFuncion and posicionFuncionLlamada<finFuncion: 
                    listaTemp.append(nombreFuncionLlamada)
            tupla=(nombre,listaTemp)
            self.listaFunciones.append(tupla)

        return self.listaFunciones
            
    def encontrarFuncionesLlamadas(self):
        pass

    def obtenerNumero(self,cadena):
        contador=0
        numero=""
        for posicion in range(0,len(cadena)):
            if cadena[posicion]==":" :
                contador=contador+1
            if contador==1:
                if cadena[posicion]!=":":
                    numero=numero+cadena[posicion]
            if contador==2:
                return int(numero)

class FunctionDetector:
    @staticmethod
    def start():
        filename = 'hash.c'
        encontrarFunciones(filename)
        funciones = funcionesLocalizacion(listaDeclaracionesFunciones,listaLlamadasFunciones)
        listaCorrecta=funciones.contenidoLista()
        return listaCorrecta
    