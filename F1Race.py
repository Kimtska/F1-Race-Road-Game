import pygame
import time
import random
import os
import math

pygame.init()

screen_width = 800
screen_height = 900

btn_starting_x = (screen_width - 213) // 2
nw_gm_y = 610
exit_y = 680
btn_width = 213
btn_height = 57

black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 30, 0)
green_color = (80, 222, 25)
blue_color = (0, 85, 255)
dark_bg = (15, 15, 20)
accent_color = (220, 38, 38)

car_names = ["Ryuzin", "Mikson", "Sakura", "Nanashi"]
car_files = ["car", "car_blue", "car_pink", "car_yellow"]

selected_car_index = 0

game_layout_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('F1 Race Road Game')
time_clock = pygame.time.Clock()

# ── Pre-load assets ──
car_photos = [pygame.image.load(os.getcwd() + f'\\images\\{name}.png') for name in car_files]
left_cs = [pygame.image.load(os.getcwd() + f'\\images\\{name}_left.png') for name in car_files]
right_cs = [pygame.image.load(os.getcwd() + f'\\images\\{name}_right.png') for name in car_files]

car_photo = car_photos[selected_car_index]
left_c = left_cs[selected_car_index]
right_c = right_cs[selected_car_index]

photo_obstacle = pygame.image.load(os.getcwd() + '\\images/obstacle.png')
texture_photo = pygame.image.load(os.getcwd() + '\\images/texture.png')
(c_width, c_height) = car_photo.get_rect().size
(t_width, t_height) = photo_obstacle.get_rect().size
(txtwidth, txtheight) = texture_photo.get_rect().size

icon = pygame.image.load(os.getcwd() + '\\images/logo.png')
pygame.display.set_icon(icon)

# Scale background to fit screen
image_background = pygame.image.load(os.getcwd() + '\\images/background.png')
image_background = pygame.transform.scale(image_background, (screen_width, screen_height))
image_background_still = pygame.image.load(os.getcwd() + '\\images/background_inv.png')
image_background_still = pygame.transform.scale(image_background_still, (screen_width, screen_height))

start_btn_img = pygame.image.load(os.getcwd() + '\\images\\start_button.png')
quit_btn_img = pygame.image.load(os.getcwd() + '\\images\\quit_button.png')
restart_btn_img = pygame.image.load(os.getcwd() + '\\images\\restart_button.png')
mainmenu_btn_img = pygame.image.load(os.getcwd() + '\\images\\mainmenu_button.png')
introtext_img = pygame.image.load(os.getcwd() + '\\images\\introtext.png')
introtext_rect = introtext_img.get_rect(center=(screen_width // 2, screen_height // 3))
img_3 = pygame.image.load(os.getcwd() + '\\images\\3.png')
img_2 = pygame.image.load(os.getcwd() + '\\images\\2.png')
img_1 = pygame.image.load(os.getcwd() + '\\images\\1.png')
img_go = pygame.image.load(os.getcwd() + '\\images\\GO!.png')
count_imgs = {3: img_3, 2: img_2, 1: img_1}
game_over_bg = pygame.image.load(os.getcwd() + '\\images\\game_over_layout.png')
game_over_bg = pygame.transform.scale(game_over_bg, (screen_width, screen_height))
pause_layout_bg = pygame.image.load(os.getcwd() + '\\images\\pause_layout.png')
pause_layout_bg = pygame.transform.scale(pause_layout_bg, (screen_width, screen_height))

welcome_1 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro1.wav')
welcome_2 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro2.wav')
audio_crash = pygame.mixer.Sound(os.getcwd() + '\\audio/car_crash.wav')
audio_ignition = pygame.mixer.Sound(os.getcwd() + '\\audio/ignition.wav')
intro_running = pygame.mixer.Sound(os.getcwd() + '\\audio\\intro_running.mp3')
point_sound = pygame.mixer.Sound(os.getcwd() + '\\audio\\point_record.mp3')
racetrack_music = os.getcwd() + '\\audio\\Racetrackbackground_sound.mp3'
pygame.mixer.music.load(racetrack_music)
selection_sound = pygame.mixer.Sound(os.getcwd() + '\\audio\\selection_sound_effect.mp3')
selected_sound = pygame.mixer.Sound(os.getcwd() + '\\audio\\selected_sound_effect.mp3')

# ── Pre-cache fonts ──
FONT_16 = pygame.font.Font('freesansbold.ttf', 16)
FONT_20 = pygame.font.Font('freesansbold.ttf', 20)
FONT_22 = pygame.font.Font('freesansbold.ttf', 22)
FONT_30 = pygame.font.Font('freesansbold.ttf', 30)
FONT_50 = pygame.font.Font('freesansbold.ttf', 50)
FONT_55 = pygame.font.Font('freesansbold.ttf', 55)
FONT_60 = pygame.font.Font('freesansbold.ttf', 60)
FONT_70 = pygame.font.Font('freesansbold.ttf', 70)

# ── Pre-render welcome background ──
welcome_bg = pygame.image.load(os.getcwd() + '\\images\\main_menu_layout.png')

# ── Pre-render pause overlay ──
pause_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
pause_overlay.fill((0, 0, 0, 150))


# ── Fast UI Helpers ──

def draw_rounded_rect(surface, color, rect, radius=12):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

def draw_modern_button(surface, text, x, y, w, h, base_color, hover_color, hovered=False):
    color = hover_color if hovered else base_color
    draw_rounded_rect(surface, color, (x, y, w, h), radius=14)
    txt = FONT_20.render(text, True, white_color)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(txt, txt_rect)

def draw_text_centered(text, y, font_size, color):
    if font_size == 60:
        txt = FONT_60.render(text, True, color)
    elif font_size == 55:
        txt = FONT_55.render(text, True, color)
    elif font_size == 50:
        txt = FONT_50.render(text, True, color)
    elif font_size == 30:
        txt = FONT_30.render(text, True, color)
    elif font_size == 22:
        txt = FONT_22.render(text, True, color)
    elif font_size == 20:
        txt = FONT_20.render(text, True, color)
    else:
        txt = FONT_16.render(text, True, color)
    rect = txt.get_rect(center=(screen_width // 2, y))
    game_layout_display.blit(txt, rect)

def is_hovered(x, y, w, h):
    mx, my = pygame.mouse.get_pos()
    return x <= mx <= x + w and y <= my <= y + h

def is_clicked():
    return pygame.mouse.get_pressed()[0] == 1


# ── Game Functions ──

def things_dodged(counting, highest_score):
    score = FONT_30.render("Dodged: " + str(counting), True, white_color)
    h_score = FONT_30.render("High Score: " + str(highest_score), True, white_color)
    game_layout_display.blit(score, (20, 10))
    game_layout_display.blit(h_score, (10, 45))

def high_score_update(dodged):
    with open(os.getcwd() + '\\textfile/high_score.txt', 'w') as f:
        f.write(str(dodged))

def things(th_x, th_y, img):
    game_layout_display.blit(img, (th_x, th_y))

def car(x, y, direction):
    if direction == 0:
        game_layout_display.blit(car_photo, (x, y))
    elif direction == -1:
        game_layout_display.blit(left_c, (x, y))
    elif direction == 1:
        game_layout_display.blit(right_c, (x, y))

def text_objects(text, font, color):
    txtSurf = font.render(text, True, color)
    return txtSurf, txtSurf.get_rect()

def message_display_screen(txt, sh_x, sh_y, color, time_sleeping):
    txtSurf, TxtRect = text_objects(txt, FONT_50, color)
    TxtRect.center = ((screen_width / 2 - sh_x), (screen_height / 2 - sh_y))
    game_layout_display.blit(txtSurf, TxtRect)
    pygame.display.update()
    time.sleep(time_sleeping)

def title_message_display(sh_x, sh_y, color):
    txtSurf, TxtRect = text_objects("F1 RaceRoad", FONT_70, color)
    TxtRect.center = ((screen_width / 2 - sh_x), (screen_height / 3 - sh_y))
    game_layout_display.blit(txtSurf, TxtRect)
    time.sleep(0.15)
    pygame.display.update()

def title_msg():
    animation_height = screen_height
    pygame.mixer.Sound.play(audio_ignition)
    while animation_height > -c_height - 100:
        game_layout_display.blit(image_background, (0, 0))
        car(screen_width / 2 - c_width / 2, animation_height, 0)
        animation_height -= 8
        pygame.display.update()
    game_layout_display.blit(introtext_img, introtext_rect)
    pygame.display.update()
    time.sleep(0.8)

def motion_texture(offset):
    y = offset - txtheight
    while y < screen_height + txtheight:
        game_layout_display.blit(texture_photo, (0, y))
        y += txtheight


# ── Welcome Screen ──

def welcome_gameplay():
    global selected_car_index, car_photo, left_c, right_c

    game_layout_display.blit(image_background, (0, 0))
    title_msg()
    welcome_2.play(-1)

    car_gap = 40
    car_start_x = (screen_width - (len(car_names) * 93 + (len(car_names) - 1) * car_gap)) // 2
    car_y = 310

    car_locked = False
    active_button = 0

    while True:
        game_layout_display.blit(welcome_bg, (0, 0))

        for i, name in enumerate(car_names):
            cx = car_start_x + i * (93 + car_gap)
            cy = car_y
            is_selected = (i == selected_car_index)
            hovered = is_hovered(cx, cy, 93, 248)

            if not car_locked and hovered and is_clicked():
                selected_car_index = i
                car_photo = car_photos[i]
                left_c = left_cs[i]
                right_c = right_cs[i]
                selection_sound.play()
                pygame.time.wait(200)

            if is_selected:
                pulse = 3 + abs(math.sin(pygame.time.get_ticks() * 0.003)) * 3
                color = green_color if car_locked else accent_color
                pygame.draw.rect(game_layout_display, color, (cx - pulse, cy - pulse, 93 + pulse * 2, 248 + pulse * 2), width=3, border_radius=6)

            game_layout_display.blit(car_photos[i], (cx, cy))

            name_txt = FONT_16.render(name, True, white_color)
            game_layout_display.blit(name_txt, name_txt.get_rect(center=(cx + 46, cy + 248 + 12)))

        nw_hov = is_hovered(btn_starting_x, nw_gm_y, btn_width, btn_height)
        exit_hov = is_hovered(btn_starting_x, exit_y, btn_width, btn_height)

        game_layout_display.blit(start_btn_img, (btn_starting_x, nw_gm_y))
        game_layout_display.blit(quit_btn_img, (btn_starting_x, exit_y))

        pulse = 3 + abs(math.sin(pygame.time.get_ticks() * 0.003)) * 3
        if car_locked and active_button == 0:
            pygame.draw.rect(game_layout_display, green_color,
                             (btn_starting_x - pulse, nw_gm_y - pulse, btn_width + pulse * 2, btn_height + pulse * 2),
                             width=3, border_radius=8)
        elif nw_hov:
            pygame.draw.rect(game_layout_display, green_color,
                             (btn_starting_x - pulse, nw_gm_y - pulse, btn_width + pulse * 2, btn_height + pulse * 2),
                             width=3, border_radius=8)
        if car_locked and active_button == 1:
            pygame.draw.rect(game_layout_display, green_color,
                             (btn_starting_x - pulse, exit_y - pulse, btn_width + pulse * 2, btn_height + pulse * 2),
                             width=3, border_radius=8)
        elif exit_hov:
            pygame.draw.rect(game_layout_display, green_color,
                             (btn_starting_x - pulse, exit_y - pulse, btn_width + pulse * 2, btn_height + pulse * 2),
                             width=3, border_radius=8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if not car_locked:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        selected_car_index = (selected_car_index - 1) % len(car_names)
                        car_photo = car_photos[selected_car_index]
                        left_c = left_cs[selected_car_index]
                        right_c = right_cs[selected_car_index]
                        selection_sound.play()
                        pygame.time.wait(100)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        selected_car_index = (selected_car_index + 1) % len(car_names)
                        car_photo = car_photos[selected_car_index]
                        left_c = left_cs[selected_car_index]
                        right_c = right_cs[selected_car_index]
                        selection_sound.play()
                        pygame.time.wait(100)
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        car_locked = True
                        active_button = 0
                        selected_sound.play()
                        pygame.time.wait(100)
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_a or event.key == pygame.K_w:
                        active_button = 0
                        selection_sound.play()
                        pygame.time.wait(100)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_d or event.key == pygame.K_s:
                        active_button = 1
                        selection_sound.play()
                        pygame.time.wait(100)
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if active_button == 0:
                            pygame.mixer.stop()
                            title_msg()
                            pygame.time.wait(100)
                            return
                        else:
                            pygame.quit()
                            quit()

        if nw_hov and is_clicked():
            if car_locked:
                pygame.mixer.stop()
                title_msg()
                pygame.time.wait(150)
                return
        if exit_hov and is_clicked():
            pygame.quit()
            quit()

        pygame.display.update()
        time_clock.tick(60)


# ── Crash Screen ──

def draw_gaming_button(surface, text, x, y, w, h, base_color, hover_color, hovered=False):
    """Gaming-style button with glow border and gradient feel."""
    # Glow border when hovered
    if hovered:
        glow = pygame.Surface((w + 8, h + 8), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*hover_color, 60), (0, 0, w + 8, h + 8), border_radius=16)
        surface.blit(glow, (x - 4, y - 4))

    # Button background with darker border
    border_color = tuple(min(c + 40, 255) for c in base_color)
    draw_rounded_rect(surface, border_color, (x - 2, y - 2, w + 4, h + 4), radius=16)

    color = hover_color if hovered else base_color
    draw_rounded_rect(surface, color, (x, y, w, h), radius=14)

    # Inner highlight line at top
    highlight = tuple(min(c + 60, 255) for c in color)
    pygame.draw.line(surface, highlight, (x + 16, y + 3), (x + w - 16, y + 3), 1)

    # Text
    txt = FONT_20.render(text, True, white_color)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(txt, txt_rect)

def crash_function(score=0):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(audio_crash)

    restart_y = 500
    menu_y = 570
    quit_y = 640
    btn_w = restart_btn_img.get_width()
    btn_h = restart_btn_img.get_height()
    btn_x = (screen_width - btn_w) // 2

    active_button = 0
    btn_count = 3

    while True:
        game_layout_display.blit(game_over_bg, (0, 0))

        # Score
        score_num = FONT_55.render(str(score), True, white_color)
        score_y = 370
        game_layout_display.blit(score_num, score_num.get_rect(center=(screen_width // 2, score_y)))

        # Best score
        best = "0"
        try:
            with open(os.getcwd() + '/textfile/high_score.txt', 'r') as f:
                best = f.read().strip()
        except:
            pass
        best_label = FONT_22.render("BEST: " + best, True, (220, 180, 50))
        game_layout_display.blit(best_label, best_label.get_rect(center=(screen_width // 2, score_y + 80)))

        # Buttons with images
        btn_images = [restart_btn_img, mainmenu_btn_img, quit_btn_img]
        btn_ys = [restart_y, menu_y, quit_y]

        for i in range(btn_count):
            game_layout_display.blit(btn_images[i], (btn_x, btn_ys[i]))
            if active_button == i:
                pulse = 3 + abs(math.sin(pygame.time.get_ticks() * 0.003)) * 3
                pygame.draw.rect(game_layout_display, green_color,
                                 (btn_x - pulse, btn_ys[i] - pulse, btn_w + pulse * 2, btn_h + pulse * 2),
                                 width=3, border_radius=8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    active_button = (active_button - 1) % btn_count
                    selection_sound.play()
                    pygame.time.wait(100)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    active_button = (active_button + 1) % btn_count
                    selection_sound.play()
                    pygame.time.wait(100)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if active_button == 0:
                        looping_gameplay()
                    elif active_button == 1:
                        welcome_gameplay()
                        looping_gameplay()
                    else:
                        pygame.quit()
                        quit()

        mx, my = pygame.mouse.get_pos()
        for i in range(btn_count):
            if btn_x <= mx <= btn_x + btn_w and btn_ys[i] <= my <= btn_ys[i] + btn_h:
                active_button = i
                if is_clicked():
                    pygame.time.wait(150)
                    if active_button == 0:
                        looping_gameplay()
                    elif active_button == 1:
                        welcome_gameplay()
                        looping_gameplay()
                    else:
                        pygame.quit()
                        quit()

        pygame.display.update()
        time_clock.tick(60)


# ── Countdown ──

def counting_three_two_one():
    counting = 3
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(audio_ignition)
    while counting >= 0:
        game_layout_display.blit(image_background, (0, 0))
        car(screen_width * 0.40, screen_height * 0.75, 0)
        if counting == 0:
            intro_running.play()
            game_layout_display.blit(img_go, img_go.get_rect(center=(screen_width // 2, screen_height // 2)))
            pygame.display.update()
            time.sleep(0.75)
            pygame.mixer.music.unpause()
        else:
            game_layout_display.blit(count_imgs[counting], count_imgs[counting].get_rect(center=(screen_width // 2, screen_height // 2)))
            pygame.display.update()
            time.sleep(0.75)
        counting -= 1
    time_clock.tick(15)


# ── Pause ──

def gameplay_paused():
    pygame.mixer.music.pause()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.unpause()
                return

        game_layout_display.blit(pause_layout_bg, (0, 0))
        pygame.display.update()
        time_clock.tick(30)


# ── Main Gameplay ──

def looping_gameplay():
    global selected_car_index, car_photos

    obstacle_cars = [car_photos[i] for i in range(len(car_photos)) if i != selected_car_index]
    current_obstacle = random.choice(obstacle_cars)
    obs_w, obs_h = current_obstacle.get_rect().size

    width_x = (screen_width * 0.4)
    height_y = (screen_height * 0.75)
    ch_x = 0

    th_st_x = random.randrange(8, screen_width - obs_w - 8)
    th_st_y = -800
    th_speed = 8

    dodg = 0
    direction = 0
    road_offset = 0

    with open(os.getcwd() + '/textfile/high_score.txt', 'r') as f:
        high_score = f.read()

    game_layout_display.blit(image_background, (0, 0))
    car(screen_width / 2 - c_width / 2, height_y, 0)
    pygame.display.update()

    pygame.mixer.music.play(-1)
    counting_three_two_one()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ch_x = -10
                    direction = -1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ch_x = 10
                    direction = 1
                if event.key == pygame.K_SPACE:
                    gameplay_paused()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    ch_x = 0
                    direction = 0

        width_x += ch_x
        game_layout_display.blit(image_background, (0, 0))

        road_offset += th_speed
        if road_offset > txtheight:
            road_offset -= txtheight
        motion_texture(road_offset)
        things(th_st_x, th_st_y, current_obstacle)
        th_st_y += th_speed
        car(width_x, height_y, direction)

        things_dodged(dodg, high_score)

        if th_st_y > screen_height:
            th_st_y = 0 - obs_h - 200
            th_st_x = random.randrange(0, screen_width - obs_w)
            current_obstacle = random.choice(obstacle_cars)
            dodg += 1
            point_sound.play()
            th_speed += 1

        if dodg > int(high_score):
            high_score_update(dodg)

        if height_y < th_st_y + obs_h - 15 and width_x > th_st_x - c_width - 5 and width_x < th_st_x + obs_w - 5:
            crash_function(dodg)

        pygame.display.update()
        time_clock.tick(60)


welcome_gameplay()
looping_gameplay()
pygame.quit()
quit()
