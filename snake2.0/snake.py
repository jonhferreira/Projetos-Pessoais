import pygame
from pygame.locals import *
import pygame_menu
import sys
import time
import random





class snake():
    
    # são as cordenadas dos pixeis referente a snake na tela

    snake_cord = []

    # objetos relacionados a cada pixel, nesse caso retangulos
    snake_obj = []

    def __init__(self):

        x,y = 125,125
        cabeca = pygame.Rect(x,y,10,10)
        
        self.snake_cord = [[x,y]]
        self.snake_obj = [cabeca]

    # atualiza todas as posições dos pixeis relacionado a snake(move ela na tela)
    # se a snake se alimentar(colision = True) ocorre o aumento dela

    def updatesnake(self,ant_block,colision):
        
        for i in range(1,len(self.snake_cord)):
            self.snake_cord[i],ant_block = ant_block, self.snake_cord[i]

            x,y = self.snake_cord[i]
            self.snake_obj[i].update(x,y,10,10)
            
        if(colision):
            self.snake_cord.append(ant_block)
            x,y = ant_block
            novo_ret = pygame.Rect(x,y,10,10)
            self.snake_obj.append(novo_ret)

class game():

    # define o eixo que vai ser alterado 0(x) e 1(y)
    ind = 0
    # define a quantidade de pixel a ser avançado pela snake
    acres = 10

    colision = False
    cor = (0,255,0)

    # tamanho da tela
    tamanho = [250,250]

    def __init__(self):

        pygame.init()
        time.sleep(0.2)
        
        # cria tela e define seu (1)tamanho e sua (2)cor de fundo
        self.tela = pygame.display.set_mode((self.tamanho[0],self.tamanho[1]))
        self.tela.fill((0,0,0))

        # vai ser utilizado para controle de FPS
        self.frame = pygame.time.Clock()
        
        # posições aleatória dos obstaculos(alimento da snake)
        self.obs_x = random.randint(0,230)
        self.obs_y = random.randint(0,230)

        # instanciamento de snake
        self.snake = snake()
        self.snake_cord = self.snake.snake_cord
        self.snake_obj = self.snake.snake_obj

    # realiza a detecção de colisao entre a snake e o alimento
    def detect_colision(self,snk_x, snk_y, obs_x, obs_y):

        if ( ((snk_x >= obs_x) and (snk_x <= obs_x+10)) or ((snk_x <= obs_x ) and (snk_x >= obs_x-10))):
            if ( ((snk_y >= obs_y ) and (snk_y <= obs_y+10)) or ((snk_y <= obs_y ) and (snk_y >= obs_y-10))):
                return True

        return False

    def sair(self):
         pygame.quit()
         sys.exit()

    def menu_run(self):
        tema = pygame_menu.themes.THEME_GREEN
        menu = pygame_menu.Menu(200,200,"Menu",theme = tema)
        menu.add_button("Jogar", self.game_run)
        menu.add_button("Sair", self.sair)
        menu.mainloop(self.tela)
        

    def game_run(self):
        sec = 0.07
        cont = 1
        while(True):

            # se a snake comeu entao crie outro alimento aleatório
            # senão comeu permanece o mesmo
            if (self.colision):
                self.obs_x = random.randint(0,230)
                self.obs_y = random.randint(0,230)
                self.colision = False
                cont += 1
    
            obs = pygame.draw.rect(self.tela,(255,0,0),(self.obs_x,self.obs_y,10,10))

            for partes in self.snake_obj:
                pygame.draw.rect(self.tela, self.cor,partes)
                
            for evento in pygame.event.get():

                if evento.type == QUIT:
                   self.sair()
                    
                if evento.type == pygame.KEYDOWN:
                    
                    if (evento.key == pygame.K_RIGHT and self.ind!= 0):
                        self.ind = 0
                        self.acres = 10
        
                    elif (evento.key == pygame.K_LEFT and self.ind!= 0):
                        self.ind = 0
                        self.acres = -10
        
                    elif (evento.key == pygame.K_UP and self.ind!= 1):
                        self.ind = 1
                        self.acres = -10

                    elif (evento.key == pygame.K_DOWN and self.ind!= 1):
                        self.ind = 1
                        self.acres = 10


            # detecta colisão da snake com a borda obs: -5 por conta do tamanho do retangulo
            if (self.snake_cord[0][self.ind]+ self.acres <= self.tamanho[self.ind] and self.snake_cord[0][self.ind] >= -5):
                # ant_block guarda a cabeça da snake
                ant_block = self.snake_cord[0].copy()

                # acrecenta/reduz n pixel na posição da cabeça da snake
                self.snake_cord[0][self.ind]  += self.acres

                snk_x = self.snake_cord[0][0]
                snk_y = self.snake_cord[0][1]

                self.snake_obj[0].update(snk_x,snk_y,10,10)
                
                self.colision = self.detect_colision(snk_x, snk_y, self.obs_x, self.obs_y)
                
                self.snake.updatesnake(ant_block, self.colision)
        
                # detecta a colisão da snake com ela mesma
                if self.snake_cord[0] in self.snake_cord[1::]:
                    self.menu_run()
            else:
                self.menu_run()

            pygame.display.update()
            self.tela.fill((0,0,0))
            self.frame.tick(60)

            # aumenta a velocidade da snake após ela comer 10 alimentos
            if (cont%10 == 0 and sec != 0.02):
                sec = float("%.2f" %(sec - 0.01))
                print(sec)
                cont = 1
            time.sleep(sec)
   
jogo_snake = game()
jogo_snake.menu_run()
    
