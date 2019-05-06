# #Keenan H
# #5/6/19
# #V 0.8.0
# #Have it where there is a home screen and one playable song

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

SONG_BEAT_MAP = pygame.sprite.Group()
SCORE = 0

end = 0

# #Screen images
outline = pygame.image.load("Boarder.png").convert_alpha()
background = "WP_1.png"

file = "Sword Art Online Alicization.mp3"  # #Song file


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
                    if self.intro == 1 and self.game == 0:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        sqx = (x - screen_width / 2) ** 2
                        sqy = (y - screen_height / 2) ** 2

                        if math.sqrt(sqx + sqy) < 300:
                            # print('inside')
                            self.logo_clicked = 1

                            # #Calls background, song, and clears the Group
                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            self.intro = 0
                            # self.select = 1
                            self.game = 1
                            StartGame().make_song_map()  # #Did this so it only reads it once
                            print("HEHEHE")
                            background_load = pygame.image.load(background)

                            pygame.mixer_music.load(file)
                            pygame.mixer_music.play()

                            screen.blit(background_load, (0, 0))

                    if self.intro == 0 and self.game == 0:  # #self.intro == 0 and self.select == 1 and self.game == 0
                        pass

                    if self.intro == 0 and self.game == 1:
                        pass

                # #-----------------------------------------------------------

                elif eventG.type == pygame.KEYDOWN:
                    '''if self.intro == 1 and self.select == 0 and self.game == 0:
                        pass

                    if self.intro == 0 and self.select == 1 and self.game == 0:
                        pass'''

                    if self.intro == 0 and self.game == 1:  # #self.intro == 0 and self.select == 0 and self.game == 1

                        def kill(note_num):
                            global SCORE
                            for notes in SONG_BEAT_MAP:  # #Goes through all of the notes that are in the list
                                # #checks the x position of the note, and if it equals start, then it will kill the note
                                if notes.x == self.start + self.note_distance * note_num:
                                    # print(notes.rect.y)
                                    # #----------Checks if the note is between the two different values----------
                                    if self.note_hit_box_1 < notes.rect.y < self.note_hit_box_2:
                                        notes.kill()
                                        SCORE += 1

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
                            # self.select = 1
                            self.game = 1
                            StartGame().make_song_map()  # #Did this so it only reads it once
                            print("HEHEHE")
                            background_load = pygame.image.load(background)

                            pygame.mixer_music.load(file)
                            pygame.mixer_music.play()

                            screen.blit(background_load, (0, 0))

                    '''if self.intro == 0 and self.select == 1 and self.game == 0:
                        if eventG.key == pygame.K_ESCAPE:
                            self.intro = 1
                            self.select = 0
                            self.game = 0
                            #background = chose_wallpaper()'''

                    if self.intro == 0 and self.game == 1:  # #self.intro == 0 and self.select == 0 and self.game == 1
                        if eventG.key == pygame.K_ESCAPE:
                            self.intro = 1  # #self.intro = 0
                            # self.select = 1
                            self.game = 0
                            pygame.mixer_music.stop()
                            background = chose_wallpaper()
                            ALL_SPRITES_LIST = pygame.sprite.Group()
                            SONG_BEAT_MAP = pygame.sprite.Group()

            # #-----------------------------------------------------------

            if self.intro == 1 and self.game == 0:  # #Intro screen  self.intro == 1 and self.select == 0 and self.game == 0
                global SCORE
                ALL_SPRITES_LIST = pygame.sprite.Group()
                SONG_BEAT_MAP = pygame.sprite.Group()

                background_load = pygame.image.load("Wallpapers/%s" % background)

                SCORE = 0

                screen.blit(background_load, (0, 0))
                IntroScreen(self.logo_clicked).update()
                #SelectScreen().update()

            '''if self.intro == 0 and self.select == 1 and self.game == 0:  # #Select screen
                # ####TEST if (the pos of the mouse is clicked):
                # ####         self.intro = 0 self.secect = 0 se;f/game = 1
                pass'''

            if self.intro == 0 and self.game == 1:  # #Game screen  self.intro == 0 and self.select == 0 and self.game == 1
                #if end == 0:
                StartGame().update()
                #else:

                #    End().update()


def chose_wallpaper():
    random_wallpaper = random.randrange(1, 11)

    background_wp = "WP_%s.png" % random_wallpaper

    return background_wp


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
        ALL_SPRITES_LIST.add(logo)

        # ALL_SPRITES_LIST.update()
        # print("IT WORKS")
        # num = 3.33333333333333333333333333333333333
        # screen.blit(self.logo, (int(screen_width / num), int(screen_height / 8)))

        ALL_SPRITES_LIST.draw(screen)
        pygame.display.flip()


class Logo(Entity):
    def __init__(self, x, y, width, height, move):
        super(Logo, self).__init__(x, y, width, height)

        self.image = pygame.image.load("Mania_Title.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.move = move

        self.x_change = -2
        self.y_change = 0

    def update(self):
        # self.rect.move_ip(self.x_change, self.y_change)
        # print(self.move)
        pass


# #-Select screen
class SelectScreen:
    def __init__(self):
        self.image = pygame.image.load("Button_1.png")
        self.rect = self.image.get_rect()

        self.click = 0

    def update(self):
        print(self.rect)
        song_1 = Button(int(30), int(30), 400, 120)
        ALL_SPRITES_LIST.add(song_1)

        song_2 = Button(int(30), int(30 + 120 + 30), 400, 120)
        ALL_SPRITES_LIST.add(song_2)

        ALL_SPRITES_LIST.update()
        ALL_SPRITES_LIST.draw(screen)
        pygame.display.flip()


class Button(Entity):
    def __init__(self, x, y, width, height):
        super(Button, self).__init__(x, y, width, height)
        self.x = x
        self.y = y

        self.image = pygame.image.load("Button_1.png")

        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        print(pos)  # #X, Y
        # print(self.image.get_rect())
        if self.image.get_rect().collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.image.load("Button_2.png")
            # print("OWOWOWOWOWOWOWOWOWOW")
        else:
            self.image = pygame.image.load("Button_1.png")

        screen.blit(self.image, (self.x, self.y))

        '''# #-----------------------
        # Makes the text that will go in the button
        fontObj = pygame.font.SysFont('comicsansms', 20)
        textSurfaceObj = fontObj.render(self.button_text, True, BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.x + (self.w / 2), self.y + (self.h / 2))'''


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
        self.song = open("SAO Alicization/SAO_Alicization_Beat_map.txt", "r")
        # ###############################################

        self.counter = 0
        self.data = 0

        self.note_hit_box_2 = self.window_height - self.window_height / 5.5

    def make_song_map(self):
        global background
        global file
        global Note_Speed
        global end

        for notes in self.song:
            read_line = notes.replace("\n", "")
            note_with_no_space = read_line.split()

            if self.data <= 2:
                if self.data == 0:
                    file = read_line
                if self.data == 1:
                    background = read_line
                    print(background)
                elif self.data == 2:
                    Note_Speed = float(read_line)
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
        # for ent in ALL_SPRITES_LIST:  # #Updates the notes so they move down
        #    self.counter += 1
        #    if self.counter == 4:
        #        self.counter = 0
        #    if self.counter != 4:
        #        ent.update()

        # #Scores the visuals
        score = ShowScore()
        surface = score.textSurface
        rect = score.textRect

        ALL_SPRITES_LIST.update()

        for notes in SONG_BEAT_MAP:
            if notes.rect.y > self.note_hit_box_2:
                notes.kill()
                SCORE = 0

        screen.blit(surface, rect)

        # Keys(self.start, screen_height - self.note_height * 5, self.note_width, self.note_height * 4)

        ALL_SPRITES_LIST.draw(screen)
        pygame.display.flip()

        # pygame.draw.rect(screen, (0, 0, 0), (screen_width - 350, 10, 300, 50))

        screen.blit(outline, (0, 0))

        # screen.blit(surface, rect)

        # screen.blit(background, (0, 0))
        # screen.fill(self.color)
        # screen.blit(outline, (0, 0))


# #End Screen
class End:
    def __init__(self):
        self.color = BLACK

    def update(self):
        screen.fill(self.color)


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
