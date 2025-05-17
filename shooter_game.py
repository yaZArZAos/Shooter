import pygame
from random import randint

# Инициализация Pygame
pygame.init()
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 60)
win_text = font_large.render('You win! Press R to restart', True, (0, 255, 0))
lose_text = font_large.render('You lose! Press R to restart', True, (255, 0, 0))
clock = pygame.time.Clock()
mixer = pygame.mixer
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')

# Настройки окна
window = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Shooter')
background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (700, 500))

# Переменные игры
lost = 0
killed = 0
health = 11 # Здоровье игрока
level = 1   # Уровень игры
player_speed = 5 #Начальная скорость игрока 
game_running = True
game_over = False

# Переменные для стрельбы
fire_rate = 500  # Время между выстрелами в миллисекундах (500 мс)
last_fire_time = pygame.time.get_ticks()  # Время последнего выстрела

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), (w,h))
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x,y))

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 0:  
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < 450:  
            self.rect.y += self.speed

    def fire(self):
        global last_fire_time
        current_time = pygame.time.get_ticks()
        if current_time - last_fire_time >= fire_rate:
            bullet = Bullet('bullet.png', 5 ,10 ,5 ,self.rect.centerx ,self.rect.top)
            bullets.add(bullet)
            fire_sound.play()
            last_fire_time = current_time

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed 
        if self.rect.y >= 500:
            lost += 1 
            self.reset_position()

    def reset_position(self):
        self.rect.y = -50
        self.rect.x = randint(50 ,650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y <= 0:
            self.kill()

def init_game():
    global lost, killed, health, level, game_running, game_over 
    global fire_rate, last_fire_time
    
    lost = killed = health = level = 0
    
    fire_rate = 500
    last_fire_time = pygame.time.get_ticks()   
    
    game_running = True
    game_over = False
    
    player_group.empty()
    player_group.add(Player('rocket.png.png', 50, 50, 5, 350, 425))
    
    enemies.empty()
    for _ in range(5 + level): 
        enemy_speed = randint(1 + level - 1, level + 2) 
        enemy_new= Enemy('ufo.png',50 ,50 ,enemy_speed ,randint(50 ,650) ,-50)
        enemies.add(enemy_new)
    
    bullets.empty()

def draw_texts():
    text_lost = font.render(f'Missed: {lost}', True,(255 ,255 ,255))
    text_killed= font.render(f'Killed: {killed}', True,(255 ,255 ,255))
    text_health= font.render(f'Health: {health}', True,(255 ,255 ,255)) 
    text_level= font.render(f'Level: {level}', True,(255 ,255 ,255)) 
    
    window.blit(text_lost,(10 ,10))
    window.blit(text_killed,(10 ,40))
    window.blit(text_health,(10 ,70)) 
    window.blit(text_level,(10 ,100)) 

def handle_collisions():
    global killed
    
    hit_enemies = pygame.sprite.groupcollide(enemies ,bullets ,True ,True)
    
    for hit in hit_enemies:
        killed += 1
        
        new_enemy= Enemy('ufo.png',50 ,50 ,
                          randint(1 + level - 1, level + 2), 
                          randint(50 ,650) ,-50) 
        enemies.add(new_enemy)

def check_game_over():
    global game_over
    
    if health <= 0:
        game_over=True 
        window.blit(lose_text,(100 ,250))

def check_win_condition():
    global level, health, fire_rate, player_speed
    
    if killed >= level * 10:    
        level += 1   
        health +=1
        player_speed += 1

        if level % 2 == 0 and fire_rate > 100:  
            fire_rate -= 50

        for _ in range(level): 
            enemy_speed=randint(1 + level -1, level +2) 
            enemy_new=Enemy('ufo.png',50 ,50 ,
                            enemy_speed,
                            randint(50 ,650) ,-50) 
            enemies.add(enemy_new)

def show_menu():
    menu_running=True
    while menu_running:
        window.fill((0,0,0))
        
        title_text= font_large.render("Shooter Game", True,(255,255,255))
        start_text= font.render("Press ENTER to Start", True,(255,255,255))
        
        window.blit(title_text,(200,150))
        window.blit(start_text,(220,250))

       # Обработка событий в меню.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running=False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    init_game()  
                    menu_running=False  

       # Обновление экрана.
        pygame.display.update()

# Создание групп спрайтов
player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Показать начальное меню перед началом игры.
show_menu()

while game_running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game_running=False
            
        if game_over and event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_r:  
                init_game()

    
    if not game_over:  
        
        window.blit(background,(0 ,0))
        
        draw_texts()

        
        player_group.update()
        
        enemies.update()
        
       # Проверка состояния клавиши K_SPACE для стрельбы по зажатию кнопки.
       # Если клавиша зажата и не произошло слишком много времени с последнего выстрела,
       # то вызываем метод fire у игрока.
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_group.sprites()[0].fire()

        
        handle_collisions()

        check_win_condition()

       # Проверка на столкновения между игроком и врагами
        if pygame.sprite.spritecollideany(player_group.sprites()[0], enemies):  
            health -= 1   
            for enemy in enemies:
                enemy.reset_position()

            check_game_over()

        
        bullets.update()     
        bullets.draw(window)

         # Обновление экрана после всех отрисовок и логики игры.
         
         # Обновление экрана после всех отрисовок и логики игры.
        player_group.draw(window)   # Отображение игрока на экране.
        enemies.draw(window)         # Отображение врагов на экране.

         # Обновление экрана после всех отрисовок и логики игры.
        pygame.display.update()

    clock.tick(60)

pygame.quit()