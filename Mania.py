# #Keenan H
# #5/6/19
# #V 1.0.0
# #I now have a select screen that works properly, one finished song, and an end screen

"""Mania is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Mania is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

# #Notes - time delta

import pygame, sys, math
# from pygame.locals import *
import random

pygame.init()

# #Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)

# #Speed of the notes
Note_Speed = 0

# #Makes the screen
info_object = pygame.display.Info()

screen_width = 1500
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mania")

# #Sprite groups
ALL_SPRITES_LIST = pygame.sprite.Group()
ALL_NOTES = pygame.sprite.Group()

clock = pygame.time.Clock()
clock_display = clock.get_fps()

SONG_BEAT_MAP = pygame.sprite.Group()

HIGH_SCORE = 0
SCORE = 0

end = 0

# #Screen images
outline = pygame.image.load("Boarder.png").convert_alpha()
background = "WP_1.png"

beat_map_file = ""

song_file = "Sword Art Online Alicization.mp3"  # #Song file


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Game:
    def __init__(self):
        global ALL_SPRITES_LIST
        global SONG_BEAT_MAP
        global SCORE
        global background
        global beat_map_file

        # #Screens  0 is false and 1 is true
        self.intro = 1
        self.select = 0
        self.game = 0

        self.window_height = screen_height
        self.note_distance = screen_width / 20  # #distance between notes

        self.note_hit_box_1 = self.window_height - self.window_height / 3.6
        self.note_hit_box_2 = self.window_height - self.window_height / 6

        self.start = screen_width / 6  # #Start is where the first note will be placed

        self.logo_clicked = 0

        while True:
            for eventG in pygame.event.get():  # #"G" stands for game
                if eventG.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # #-----------------------------------------------------------

                elif eventG.type == pygame.MOUSEBUTTONDOWN:
                    if self.intro == 1 and self.select == 0 and self.game == 0:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        sqx = (x - screen_width / 2) ** 2
                        sqy = (y - screen_height / 2) ** 2

                        if math.sqrt(sqx + sqy) < 300:
                            # print('inside')
                            self.logo_clicked = 1

                            self.intro = 0
                            self.select = 1
                            self.game = 0

                            # #Calls background, song, and clears the Group
                            '''ALL_SPRITES_LIST = pygame.sprite.Group()
                            self.intro = 0
                            self.select = 1
                            self.game = 0
                            StartGame().make_song_map()  # #Did this so it only reads it once
                            print("HEHEHE")
                            background_load = pygame.image.load(background)

                            pygame.mixer_music.load(file)
                            pygame.mixer_music.play()

                            screen.blit(background_load, (0, 0))'''

                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            # print(ALL_SPRITES_LIST)
                            # print("hdsajidhgasjghdfjksahgjkfhasjkhfjkashfjkhdgsjkgreuiwhfksdbfuidsbknvbweuivbhjgweuyfg")

                            background = chose_wallpaper()
                            background_load = pygame.image.load("Wallpapers/%s" % background)

                            screen.blit(background_load, (0, 0))

                    elif self.intro == 0 and self.select == 1 and self.game == 0:  # #self.intro == 0 and self.select == 1 and self.game == 0
                        global beat_map_file

                        ALL_SPRITES_LIST = pygame.sprite.Group()

                        pos = pygame.mouse.get_pos()

                        x = 30
                        y = 30  # #30 + 120*i + 30*i
                        width = 400
                        height = 120

                        if x + width > pos[0] > x and y + 120 * 0 + 30 * 0 + height > pos[1] > y:
                            self.intro = 0
                            self.select = 0
                            self.game = 1

                            song = "SAO Alicization"
                            beat_map_file = song
                            # print(beat_map_file)
                            start_game()

                    if self.intro == 0 and self.select == 0 and self.game == 1:
                        pass

                # #-----------------------------------------------------------

                elif eventG.type == pygame.KEYDOWN:
                    if self.intro == 1 and self.select == 0 and self.game == 0:
                        pass

                    if self.intro == 0 and self.select == 1 and self.game == 0:
                        pass

                    if self.intro == 0 and self.select == 0 and self.game == 1:

                        def kill(note_num):
                            global SCORE
                            global HIGH_SCORE

                            for notes in SONG_BEAT_MAP:  # #Goes through all of the notes that are in the list
                                # #checks the x position of the note, and if it equals start, then it will kill the note
                                if notes.x == self.start + self.note_distance * note_num:
                                    # print(notes.rect.y)
                                    # #----------Checks if the note is between the two different values----------
                                    if self.note_hit_box_1 < notes.rect.y < self.note_hit_box_2:
                                        notes.kill()
                                        if SCORE >= HIGH_SCORE:
                                            SCORE += 1
                                            HIGH_SCORE = SCORE
                                        elif SCORE < HIGH_SCORE:
                                            SCORE += 1
                                            print(HIGH_SCORE)
                                            pass

                        if eventG.key == pygame.K_d:
                            kill(0)

                        if eventG.key == pygame.K_f:
                            kill(1)

                        if eventG.key == pygame.K_j:
                            kill(2)

                        if eventG.key == pygame.K_k:
                            kill(3)

                # #-----------------------------------------------------------

                elif eventG.type == pygame.KEYUP:

                    if self.intro == 1 and self.select == 0 and self.game == 0:
                        if eventG.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                        if eventG.key == pygame.K_RETURN:  # #Enters the game (Will change to the click)
                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            self.intro = 0
                            self.select = 1
                            self.game = 0

                            # print(self.intro)
                            # print(self.select)
                            # print(self.game)

                            background = chose_wallpaper()

                            background_load = pygame.image.load("Wallpapers/%s" % background)
                            screen.blit(background_load, (0, 0))

                    if self.intro == 0 and self.select == 1 and self.game == 0:
                        if eventG.key == pygame.K_ESCAPE:
                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            # print(self.intro)
                            # print(self.select)
                            # print(self.game)
                            self.intro = 1
                            self.select = 0
                            self.game = 0
                            background = chose_wallpaper()

                        if eventG.key == pygame.K_RETURN:
                            pass
                            # self.intro = 0
                            # self.select = 0
                            # self.game = 1

                            # StartGame().make_song_map()  # #Did this so it only reads it once
                            # print("HEHEHE")

                            # background_load = pygame.image.load("Wallpapers/$s" % background)

                            # StartGame().make_song_map()  # #Did this so it only reads it once

                            # pygame.mixer_music.load(file)
                            # pygame.mixer_music.play()

                            # screen.blit(background_load, (0, 0))

                    if self.intro == 0 and self.select == 0 and self.game == 1:
                        if eventG.key == pygame.K_ESCAPE:
                            ALL_SPRITES_LIST = pygame.sprite.Group()

                            self.intro = 0
                            self.select = 1
                            self.game = 0

                            # print(self.intro)
                            # print(self.select)
                            # print(self.game)

                            pygame.mixer_music.stop()
                            background = chose_wallpaper()
                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            SONG_BEAT_MAP = pygame.sprite.Group()

                            background_load = pygame.image.load("Wallpapers/%s" % background)
                            screen.blit(background_load, (0, 0))

                            SCORE = 0
                            HIGH_SCORE = 0

            # #-----------------------------------------------------------

            if self.intro == 1 and self.select == 0 and self.game == 0:  # #self.intro == 1 and self.game == 0:
                #global SCORE
                ALL_SPRITES_LIST = pygame.sprite.Group()
                SONG_BEAT_MAP = pygame.sprite.Group()

                background_load = pygame.image.load("Wallpapers/%s" % background)

                SCORE = 0

                screen.blit(background_load, (0, 0))
                IntroScreen(self.logo_clicked).update()
                # SelectScreen().update()

            if self.intro == 0 and self.select == 1 and self.game == 0:  # #Select screen
                # ####TEST if (the pos of the mouse is clicked):
                # ####         self.intro = 0 self.secect = 0 se;f/game = 1
                SelectScreen().update()

            if self.intro == 0 and self.select == 0 and self.game == 1:  # #self.intro == 0 and self.game == 1:
                # if end == 0:
                StartGame().update()
                # else:
                #    End().update()


def chose_wallpaper():
    random_wallpaper = random.randrange(1, 7)

    background_wp = "WP_%s.png" % random_wallpaper

    return background_wp


def start_game():
    StartGame().make_song_map()  # #Did this so it only reads it once
    background_load = pygame.image.load(background)

    pygame.mixer_music.load(song_file)
    pygame.mixer_music.play()

    screen.blit(background_load, (0, 0))


# #The screens
# #-Logo/Intro
class IntroScreen:
    def __init__(self, click):
        # pygame.draw.circle(screen, BLACK, (int(screen_width / 2), int(screen_height / 2)), 300)

        # self.logo = pygame.image.load("Mania_Title.png")
        # self.logo = pygame.transform.scale(self.logo, (600, 600))

        # self.rect = self.logo.get_rect()

        self.clicked = click

        self.move = click  # #If self.move = 0, then it will not move, if self.move = 1 it will move

    def update(self):
        num = 3.33333333333333333333333333333333333
        logo = Logo(int(screen_width / num), int(screen_height / 8), 600, 600, self.clicked)
        # ALL_SPRITES_LIST.add(logo)
        logo.update()

        # ALL_SPRITES_LIST.update()
        # print("IT WORKS")
        # num = 3.33333333333333333333333333333333333
        # screen.blit(self.logo, (int(screen_width / num), int(screen_height / 8)))

        ALL_SPRITES_LIST.draw(screen)
        # pygame.display.flip()

        font_obj = pygame.font.SysFont('comicsansms', 30)
        text_surface_obj = font_obj.render(str(int(clock_display)), True, BLACK)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (100, 10)

        screen.blit(text_surface_obj, text_rect_obj)

        pygame.display.flip()

        # print("OWOWOWOWOWOPWOWOWOWOWOIOIJDKLSJHKHSKJHKSJH")


class Logo(Entity):
    def __init__(self, x, y, width, height, move):
        super(Logo, self).__init__(x, y, width, height)

        self.image_decide = "Mania_Title.png"

        self.image = pygame.image.load(self.image_decide)

    def update(self):
        # self.rect.move_ip(self.x_change, self.y_change)
        # print(self.move)
        # pass

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        sqx = (x - screen_width / 2) ** 2
        sqy = (y - screen_height / 2) ** 2

        if math.sqrt(sqx + sqy) < 300:
            self.image_decide = "Mania_Title_2.png"
        else:
            self.image_decide = "Mania_Title.png"

        self.image = pygame.image.load(self.image_decide)
        self.image = pygame.transform.scale(self.image, (600, 600))

        screen.blit(self.image, (self.x, self.y))


# #-Select screen
class SelectScreen:
    def __init__(self):
        self.image = pygame.image.load("Button_1.png")
        self.rect = self.image.get_rect()

        self.click = 0

    def update(self):
        text = ""
        for i in range(5):
            if i == 0:
                text = "SAO Alicization"
            elif i == 1:
                text = ""
            elif i == 2:
                text = ""
            elif i == 3:
                text = ""
            elif i == 4:
                text = ""
            song_button = Button(int(30), int(30 + 120 * i + 30 * i), 400, 120, text)
            screen.blit(song_button.update()[0], song_button.update()[1])

        pygame.display.flip()


class Button(Entity):
    def __init__(self, x, y, width, height, text):
        super(Button, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_text = text

        self.image = pygame.image.load("Button_1.png")

    def update(self):
        pos = pygame.mouse.get_pos()

        if self.x + self.width > pos[0] > self.x and self.y + self.height > pos[1] > self.y:
            self.image = pygame.image.load("Button_2.png")
        else:
            self.image = pygame.image.load("Button_1.png")

        screen.blit(self.image, (self.x, self.y))

        # #-----------------------
        # Makes the text that will go in the button
        font_obj = pygame.font.SysFont('comicsansms', 30)
        text_surface_obj = font_obj.render(self.button_text, True, BLACK)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (self.x + (self.width / 2), self.y + (self.height / 2))

        return text_surface_obj, text_rect_obj

        # screen.blit(text_surface_obj, text_rect_obj)


# #-Game Screen
class StartGame:
    def __init__(self):
        self.color = GREEN

        self.start = screen_width / 6  # #Start is where the first note will be placed
        self.note_width = screen_width / 22  # #note width
        self.note_height = screen_height / 33  # #note height
        self.note_distance = screen_width / 20  # #distance between notes
        self.window_width = screen_width
        self.window_height = screen_height

        # ###test song will change later on when I have a menu where you can select songs
        self.song = open("%s/Beat_Map.txt" % beat_map_file, "r")
        # ###############################################

        self.counter = 0
        self.data = 0

        self.note_hit_box_2 = self.window_height - self.window_height / 5.5

        self.end = 0

        self.background = chose_wallpaper()

    def make_song_map(self):
        global background
        global song_file
        global Note_Speed
        global end

        for notes in self.song:
            read_line = notes.replace("\n", "")
            note_with_no_space = read_line.split()

            if self.data <= 3:
                if self.data == 0:
                    song_file = read_line
                if self.data == 1:
                    background = read_line
                    print(background)
                elif self.data == 2:
                    Note_Speed = float(read_line)
                elif self.data == 3:
                    pass
                self.data += 1

            else:
                if read_line == "end":
                    end = 1
                    break
                # #-------------------------------------------------------------------------------------------------------------------------------------
                if read_line == "_______":
                    pass
                else:
                    self.counter += 1
                    # print(self.counter)
                # #------------------------- | Makes the position of the block | -------------------------
                y = 0 - self.note_height * ((self.counter - 1) * 2)

                for note in note_with_no_space:

                    if note == "1":
                        make = MakeNotes(self.start + self.note_distance * 0, y, self.note_width, self.note_height)
                        ALL_SPRITES_LIST.add(make)
                        SONG_BEAT_MAP.add(make)
                    if note == "2":
                        make = MakeNotes(self.start + self.note_distance * 1, y, self.note_width, self.note_height)
                        ALL_SPRITES_LIST.add(make)
                        SONG_BEAT_MAP.add(make)
                    if note == "3":
                        make = MakeNotes(self.start + self.note_distance * 2, y, self.note_width, self.note_height)
                        ALL_SPRITES_LIST.add(make)
                        SONG_BEAT_MAP.add(make)
                    if note == "4":
                        make = MakeNotes(self.start + self.note_distance * 3, y, self.note_width, self.note_height)
                        ALL_SPRITES_LIST.add(make)
                        SONG_BEAT_MAP.add(make)

        self.song.close()

    def update(self):
        global SCORE
        global ALL_SPRITES_LIST
        global SONG_BEAT_MAP

        if self.end == 0:
            score = ShowScore()
            surface = score.textSurface
            rect = score.textRect

            ALL_SPRITES_LIST.update()

            for notes in SONG_BEAT_MAP:
                if notes.rect.y > self.note_hit_box_2:
                    notes.kill()
                    SCORE = 0

            screen.blit(surface, rect)

            ALL_SPRITES_LIST.draw(screen)
            pygame.display.flip()

            screen.blit(outline, (0, 0))

            if pygame.mixer_music.get_busy() == 1:
                self.end = 0
            elif pygame.mixer_music.get_busy() == 0:
                self.end = 1

            # print(self.end)

        if self.end == 1:
            ALL_SPRITES_LIST = pygame.sprite.Group()
            pygame.mixer_music.stop()

            SONG_BEAT_MAP = pygame.sprite.Group()

            background_load = pygame.image.load("Wallpapers/%s" % self.background)
            screen.blit(background_load, (0, 0))
            # screen.fill(BLACK)
            pygame.display.flip()


# #Text
# # - Score
class ShowScore:
    def __init__(self):
        self.font = pygame.font.SysFont('comicsansms', 100)
        self.textSurface = self.font.render(str(SCORE), True, MAGENTA)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (screen_width - 1100, 300)


# #Make and hit notes
class MakeNotes(Entity):
    def __init__(self, x, y, width, height):
        super(MakeNotes, self).__init__(x, y, width, height)

        self.window_width = screen_width
        self.window_height = screen_height

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.x_change = 0
        self.y_change = Note_Speed

    def update(self):
        self.rect.move_ip(self.x_change, self.y_change)

        if self.rect.y > self.window_height:
            MakeNotes.kill(self)


Game()
clock.tick(60)
