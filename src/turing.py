import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class TuringMachine: #Inicia la clase
    states: set[str] #Declaramos estados
    symbols: set[str] #Declaramos el abecedario
    blank_symbol: str #Declaramos el simbolo para los espacios vacios
    input_symbols: set[str] #Declaramos la entrada
    initial_state: str #Declaramos el estado inicial
    accepting_states: set[str] #Declaramos el estado de aceptacion
    transitions: dict[tuple[str, str], tuple[str, str, int]]  
    # declaramos los "movidmientos" de la siguiente manera >>> state, symbol -> new state, new symbol, direction

    head: int = field(init=False) 
    tape: defaultdict[int, str] = field(init=False)
    current_state: str = field(init=False)
    halted: bool = field(init=False, default=True)

    def initialize(self, input_symbols: dict[int, str]): #Inicializamos la maquina
        self.head = 0 #el tamaño inicial en 0
        self.halted = False #Estado de final en falso
        self.current_state = self.initial_state #el estado actual igual al estado inicial
        self.tape = defaultdict(lambda: self.blank_symbol, input_symbols) #la funcion para llenar los espacios

    def step(self): #Instancia para los "pasos"
        if self.halted: #Si el estado es interumpido 
            raise RuntimeError('No se puede hacer este salto') #Tiramos este error

        try:
            state, symbol, direction = self.transitions[(self.current_state, self.tape[self.head])] #Entradas de "pasos"
        except KeyError:
            self.halted = True #Error haria que se detenga la ejecucion
            return
        self.tape[self.head] = symbol #Setteamos los valores 
        self.current_state = state    #Con los valores que se ingresan
        self.head += direction


    def accepted_input(self): #Entradas
        if not self.halted: #(Si) Negamos que haya terminado el programa 
            raise RuntimeError('La máquina sigue funcionando') #Pero encuentra un error de ejecucion mandara el mensaje
        return self.current_state in self.accepting_states 

    def print(self, window=10): #Formato de imprecion estilo:
        print('... ', end='')   #_____x_xx______
        print(' '.join(self.tape[i] for i in range(self.head - window, self.head + window + 1)), end='')
        print(f' ... estado={self.current_state}') #Agredando el estado en el que nos encontramos
        print(f'{" " * (2 * window + 4)}^')


if __name__ == '__main__':

    tm = TuringMachine(states={'a', 'b', 'c', 'd', 'e', 'f', 'H'}, #Estados de la maquina
                symbols={'0', '1', '_'}, #Diccionario
                blank_symbol='_', #Espacio en blanco
                input_symbols={'1', '_'}, #Entradas validas
                initial_state='a', #Estado en el que inicia
                accepting_states={'H'}, #Estado de aceptacion
                transitions={ #Todos los pasos declarados
                    ('a', '0'): ('a', '0', 1),
                    ('a', '1'): ('a', '1', 1),
                    ('a', '_'): ('b', '_', 1),
                    ('b', '0'): ('b', '0', 1),
                    ('b', '1'): ('b', '1', 1),
                    ('b', '_'): ('c', '_', -1),
                    ('c', '0'): ('c', '1', -1),
                    ('c', '1'): ('d', '0', -1),
                    ('c', '_'): ('f', '_', 1),
                    ('d', '0'): ('d', '0', -1),
                    ('d', '1'): ('d', '1', -1),
                    ('d', '_'): ('e', '_', -1),
                    ('e', '0'): ('a', '1', 1),
                    ('e', '1'): ('e', '0', -1),
                    ('e', '_'): ('a', '1', 1),
                    ('f', '1'): ('f', '_', 1),
                    ('f', '_'): ('H', '_', 1),                    
                })
    
    #Entradas al sistema (Ejemplos)
    #tm.initialize({0: '1', 1: '1', 2: '1', 3: '_', 4: '1', 5: '0', 6: '1'})
    #tm.initialize({0: '1', 1: '1', 2: '_', 3: '0', 4: '1'})
    #tm.initialize({0: '1', 1: '0', 2: '1', 3: '_', 4: '1', 5: '0', 6: '0'})
    tm.initialize({0: '1', 1: '_', 2: '1'})
    
    #Impreciones
    while not tm.halted:
        tm.print() 
        tm.step()
        time.sleep(1)

    print(tm.accepted_input())