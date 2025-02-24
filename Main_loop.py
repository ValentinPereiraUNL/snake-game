import pygame  
from pygame.locals import *
import random

#Menu
class Boton:
    def __init__(self,x,y,altura,ancho,texto,color_claro,color_fondo,accion = None):
         #Constructor del rectangulo
        self.rectangulo = pygame.Rect(x,y,altura,ancho)
        self.texto = texto
        self.color_claro = color_claro
        self.color_fondo = color_fondo
        self.accion = accion    
    
    def draw(self,pantalla,font):
        mouse_pos = pygame.mouse.get_pos() #toma la posicion del mouse
        color = self.color_claro if self.rectangulo.collidepoint(mouse_pos) else self.color_fondo
       
        pygame.draw.rect(pantalla,color,self.rectangulo, border_radius=10) #Dibuja el boton
        
        texto = font.render(self.texto, True, (255,255,255))
        pantalla.blit(texto, (self.rectangulo.x + 20, self.rectangulo.y + 10)) #centra el texto

    
        
    def check_click(self,evento):
        if evento.type == MOUSEBUTTONDOWN and self.rectangulo.collidepoint(evento.pos):
            if self.accion:
                self.accion() #llama a la funcion definida

#Serpiente
class Snake:
    def __init__(self,pos, dir):
        self.snake_head = pos
        self.snake_pos = [pos]
        self.snake_dir = dir

    def set_head(self,head):
        self.snake_head = head
    def move(self):
        """Mueve la serpiente en la dirección actual."""
          # La cabeza de la serpiente
        new_head = [self.snake_head[0] + self.snake_dir[0], self.snake_head[1] + self.snake_dir[1]]
        self.set_head(new_head)
        self.snake_pos.insert(0, new_head)  # Agrega la nueva cabeza
        self.snake_pos.pop()  # Elimina la última parte (para moverse)

    def crecer(self):
        #Crece al comer
        self.snake_pos.append(self.snake_pos[-1]) #agrega al final de la cola


#Comida
class Comida:
    def __init__(self):
        self.pos = [random.randrange(10,630,10), random.randrange(10,390,10)]

    def new_pos(self):
        self.pos = [random.randrange(10,630,10), random.randrange(10,390,10)]

#Main class
class App:           
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 1024
        pygame.display.set_caption("La serpiente loca")
        
        self.snake = Snake([400,200],[-10,0])
        self.snake2 = Snake([100,50],[10,0]) 
        self.comida = Comida()
        self.comida2 = Comida()        
         
        self.estado = "menu"

    def on_init(self):  #Ejecucion de la pantalla
        pygame.init()
        self._display_surf=pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.font =  pygame.font.Font(None, 36)

        #Botones
        self.button_start = Boton(220, 150, 200, 50, "JUGAR", (0, 128, 0), (0, 180, 0), self.start_game)
        self.button_exit = Boton(220, 260, 200, 50, "SALIR", (200, 0, 0), (255, 0, 0), self.on_cleanup)
        self.button_versus = Boton(220,205,200,50, "VERSUS",(200,200,0),(255,255,0),self.start_versus)

    def start_game(self):
        self.estado = "clasico"
    
    def start_versus(self):
        self.estado = "versus"

    def start_challenge(self):
        self.estado = "challenge"
    def on_event(self, event): #Ejecucion de cada evento
        if event.type == pygame.QUIT:
            self._running = False
        if self.estado == "menu":
            self.button_start.check_click(event)
            self.button_versus.check_click(event)
            self.button_exit.check_click(event)
        elif self.estado == "clasico":
        #Manejo del teclado
            if event.type == KEYDOWN:
                if event.key == K_UP and self.snake.snake_dir != [0,10]:
                    self.snake.snake_dir = [0,-10]
                elif event.key == K_DOWN and self.snake.snake_dir != [0,-10]:
                    self.snake.snake_dir = [0,10]
                elif event.key == K_LEFT and self.snake.snake_dir != [10,0]:
                    self.snake.snake_dir = [-10,0]
                elif event.key == K_RIGHT and self.snake.snake_dir != [-10,0]:
                    self.snake.snake_dir = [10,0]
                elif event.key == K_ESCAPE:
                    self.estado = "menu"
        elif self.estado == "versus":
        #Manejo del teclado
            if event.type == KEYDOWN:
                if event.key == K_UP and self.snake.snake_dir != [0,10]:
                    self.snake.snake_dir = [0,-10]
                elif event.key == K_DOWN and self.snake.snake_dir != [0,-10]:
                    self.snake.snake_dir = [0,10]
                elif event.key == K_LEFT and self.snake.snake_dir != [10,0]:
                    self.snake.snake_dir = [-10,0]
                elif event.key == K_RIGHT and self.snake.snake_dir != [-10,0]:
                    self.snake.snake_dir = [10,0]
                elif event.key == K_w and self.snake2.snake_dir != [0,10]:
                    self.snake2.snake_dir = [0,-10]
                elif event.key == K_s and self.snake2.snake_dir != [0,-10]:
                    self.snake2.snake_dir = [0,10]
                elif event.key == K_a and self.snake2.snake_dir != [10,0]:
                    self.snake2.snake_dir = [-10,0]
                elif event.key == K_d and self.snake2.snake_dir != [-10,0]:
                    self.snake2.snake_dir = [10,0]
                elif event.key == K_ESCAPE:
                    self.estado = "menu"
    def on_loop(self):
        """Lógica del juego: mueve la serpiente y detecta colisiones."""
        if self.estado == "clasico":
            #Movimiento
            self.snake.move()
            #Chocarse contra pared
            if self.snake.snake_head[0]==0 or self.snake.snake_head[1]==0 or self.snake.snake_head[0]==self.weight-10 or self.snake.snake_head[1]==self.height-10:
                self.on_cleanup()
            #Chocarse a si mismo
            for segmento in self.snake.snake_pos[1::]:
                if segmento == self.snake.snake_head:
                    self.on_cleanup()
            # Verifica si la serpiente come la comida
            if self.snake.snake_head == self.comida.pos:
                self.snake.crecer()
                self.comida.new_pos()  # Genera nueva comida
        if self.estado == "versus":
            #Movimiento
            self.snake.move()
            self.snake2.move()
            #Chocarse contra pared
            if self.snake.snake_head[0]==0 or self.snake.snake_head[1]==0 or self.snake.snake_head[0]==630 or self.snake.snake_head[1]==390:
                self.on_cleanup()
            if self.snake2.snake_head[0]==0 or self.snake2.snake_head[1]==0 or self.snake2.snake_head[0]==630 or self.snake2.snake_head[1]==390:
                self.on_cleanup()
            #Chocarse a si mismo
            for segmento in self.snake.snake_pos[1::]:
                if segmento == self.snake.snake_head:
                    self.on_cleanup()
                if segmento == self.snake2.snake_head:
                    self.on_cleanup()
            for segmento2 in self.snake2.snake_pos[1::]:
                if segmento2 == self.snake2.snake_head:
                    self.on_cleanup()
                if segmento2 == self.snake.snake_head:
                    self.on_cleanup()
            # Verifica si la serpiente come la comida
            if self.snake.snake_head == self.comida.pos:
                self.snake.crecer()
                self.comida.new_pos()  # Genera nueva comida
            if self.snake2.snake_head == self.comida2.pos:
                self.snake2.crecer()
                self.comida2.new_pos()  # Genera nueva comida


    def on_render(self): #Dibuja lo que se encuentra en la pantalla
        self._display_surf.fill((65,125,125))
         #bordes
        pygame.draw.rect(self._display_surf,(1,1,1),(0,0,10,self.height))
        pygame.draw.rect(self._display_surf,(1,1,1),(0,self.height-10,self.weight,10))
        pygame.draw.rect(self._display_surf,(1,1,1),(self.weight-10,0,10,self.height))
        pygame.draw.rect(self._display_surf,(1,1,1),(0,0,self.weight,10))
        if self.estado == "menu":
            pygame.draw.rect(self._display_surf,(0,0,0),(220,60,210,50))
            titulo = self.font.render("La serpiente loca", True, (255, 255, 255))
            
            self._display_surf.blit(titulo,(self.weight//2 - 100, 80))
            self.button_start.draw(self._display_surf,self.font)
            self.button_versus.draw(self._display_surf,self.font)
            self.button_exit.draw(self._display_surf,self.font)
            
        elif self.estado == "clasico":
            #comida
            pygame.draw.circle(self._display_surf,(255,0,0),self.comida.pos,5)
            #cabeza
            pygame.draw.rect(self._display_surf,(0,100,0),(self.snake.snake_head[0],self.snake.snake_head[1],10,10))
            #cuerpo
            for segment in self.snake.snake_pos:
                pygame.draw.rect(self._display_surf, (0, 100, 0), (segment[0], segment[1], 10, 10))

        elif self.estado == "versus":
            #comida
            pygame.draw.circle(self._display_surf,(0,255,0),self.comida.pos,5)
            pygame.draw.circle(self._display_surf,(0,0,255),self.comida2.pos,5)
            #bordes
            pygame.draw.rect(self._display_surf,(1,1,1),(0,0,10,400))
            pygame.draw.rect(self._display_surf,(1,1,1),(0,390,640,10))
            pygame.draw.rect(self._display_surf,(1,1,1),(630,0,10,400))
            pygame.draw.rect(self._display_surf,(1,1,1),(0,0,640,10))
            #cabezaS
            pygame.draw.rect(self._display_surf,(0,100,0),(self.snake.snake_head[0],self.snake.snake_head[1],10,10))
            pygame.draw.rect(self._display_surf,(0,0,100),(self.snake2.snake_head[0],self.snake2.snake_head[1],10,10))
            #cuerpoS
            for segment in self.snake.snake_pos:
                pygame.draw.rect(self._display_surf, (0, 100, 0), (segment[0], segment[1], 10, 10))
            for segment2 in self.snake2.snake_pos:
                pygame.draw.rect(self._display_surf, (0, 0, 100), (segment2[0], segment2[1], 10, 10))
        pygame.display.flip() 

    def on_cleanup(self): #Lo que sucede al limpiar la pantalla 
        pygame.quit()        

    def on_execute(self):  #Main loop
        if self.on_init () == False:
            self._running = False
        clock = pygame.time.Clock()    
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            clock.tick(10)

        self.on_cleanup()



if __name__ == "__main__" :
    onApp = App()
    onApp.on_execute()
