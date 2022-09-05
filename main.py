import pygame
import sys
from pygame.locals import *
from dataclasses import dataclass

# ゲーム本編のスクリプトを格納する配列
# 章ごとなどに分けることが可能
TEXT = [
    []
]

# ライセンス画面に表示する文字列を格納する配列
# 1要素1行
LICENSE = [
]

# 背景の画像のパスを格納する配列
# 1要素1枚
BG = [
]

# キャラの立ち絵画像のパスを格納する配列
# 1要素1枚
CH0 = [
]

# 音声ファイルのパスを格納する配列
# 1要素1台詞
VOICE = [
]

# BGMのファイルパスを格納する配列
# 1要素1曲
BGM = [
]

# 効果音のファイルパスを格納する配列
# 1要素1音
SE = [
]

CAPTION = "サンプルゲーム"
CHOICE_FONT="./assets/font/x0y0pxFreeFont/x8y12pxTheStrongGamer.ttf"
TEXT_FONT="./assets/font/Kosugi/Kosugi-Regular.ttf"

# 座標を表すデータクラス
@dataclass
class Coordinate:
    x: int
    y: int

    def get(self):
        return self.x, self.y

# 各画像サーフェスを管理するデータクラス
@dataclass
class ImageSurfaces:
    images: list
    coordinate: Coordinate

    def __init__(self, image_path_list, coordinate=Coordinate(0, 0), size=None):
        self.images = []
        for image_path in image_path_list:
            if size is not None:
                self.images.append(pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size))
            else:
                self.images.append(pygame.image.load(image_path).convert_alpha())
        self.coordinate = coordinate

    def add_image(self, image_path, width=-1, height=-1):
        if width != -1 and height != 1:
            self.images.append(pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height)))
        else:
            self.images.append(pygame.image.load(image_path).convert_alpha())

    def get_length(self):
        return len(self.images)

    def get_coordinate(self):
        return self.coordinate

    def get_image_surface(self, image_number):
        return self.images[image_number]

    def show(self, surface, image_number):
        surface.blit(self.images[image_number], self.coordinate.get())

# 音を管理するデータクラス
@dataclass
class Sounds:
    sounds: list

    def __init__(self, sound_path_list):
        self.sounds = []
        for sound_path in sound_path_list:
            if sound_path is not None:
                self.sounds.append(pygame.mixer.Sound(sound_path))
            else:
                self.sounds.append(None)

    def set_volume(self, sound_number, volume):
        if sound_number < len(self.sounds) and self.sounds[sound_number] is not None:
            self.sounds[sound_number].set_volume(volume)

    def play(self, sound_number):
        if sound_number < len(self.sounds) and self.sounds[sound_number] is not None:
            self.sounds[sound_number].play()

    def stop(self, sound_number):
        if sound_number < len(self.sounds) and self.sounds[sound_number] is not None:
            self.sounds[sound_number].stop()

def main():
    # 定数
    CHOICE_FONT_SIZE = 70
    TEXT_FONT_SIZE = 40
    LINE_SPACING = 10
    LINE_SPACING_L = 30
    # 設定
    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(0)
    display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(CAPTION)
    screen_size = Coordinate(pygame.display.get_surface().get_size()[0], pygame.display.get_surface().get_size()[1])
    # フォント
    choice_font = pygame.font.Font(CHOICE_FONT, CHOICE_FONT_SIZE)
    text_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_SIZE)
    # 背景読み込み
    bg = ImageSurfaces(BG, size=screen_size.get())
    # キャラ読み込み
    ch_0 = ImageSurfaces(CH0, Coordinate(0, screen_size.y // 3),
                         (screen_size.x // 3.5, screen_size.y - screen_size.y // 3))
    # 音声読み込み
    voice = Sounds(VOICE)
    se = Sounds(SE)
    # その他画像
    text_window = pygame.transform.scale(pygame.image.load("./assets/graphic/item/text_window.png").convert_alpha(), (
    screen_size.x, screen_size.y - (screen_size.y // 2) - (screen_size.y // 4) + 20))
    # 効果用
    rect = pygame.Rect(0, 0, screen_size.x, screen_size.y)
    black = (0, 0, 0)
    white = (255, 255, 255)
    # 効率的描画用
    dr_CF = pygame.Rect(0, 0, CHOICE_FONT_SIZE, CHOICE_FONT_SIZE)
    dr_TF = pygame.Rect(0, 0, TEXT_FONT_SIZE, TEXT_FONT_SIZE)
    # タイトル
    choice_position_t = [
        Coordinate(screen_size.x // 6, screen_size.y * 3 // 5),
        Coordinate(screen_size.x // 8, screen_size.y * 3 // 5 + CHOICE_FONT_SIZE + LINE_SPACING),
        Coordinate(screen_size.x // 10, screen_size.y * 3 // 5 + CHOICE_FONT_SIZE * 2 + LINE_SPACING),
        Coordinate(screen_size.x // 15, screen_size.y * 3 // 5 + CHOICE_FONT_SIZE * 3 + LINE_SPACING)
    ]
    c_index = 0
    c_index_b = 0
    # エンジン用変数
    TEXT_LOAD_SPEED = 50
    STANDARD_TEXT_POSITION = Coordinate((screen_size.x // 2) - (screen_size.x // 4) - (screen_size.x // 6),
                                        (screen_size.y // 2) + (screen_size.y // 4))
    scene_number = -1
    text_number = 0
    bg_number = 0
    option_flag = False
    ch_0_style = 0
    ch_0_visible = False
    once = True
    text_state = 0
    text_index = 0
    frame = 1
    voice_number = 0
    display_covered = False
    while True:
        clock.tick(60)  # FPS上限固定
        if scene_number == -4: # 中断画面
            print("can't reach now")
        elif scene_number == -3: # らいせんす
            if once:
                display_surface.fill((255, 245, 170), rect)
                for i, text in enumerate(LICENSE):
                    display_surface.blit(text_font.render(text, True, (0, 0, 0)),
                                         (screen_size.x / 2 - text_font.render(text, True, (0, 0, 0)).get_width() / 2,
                                          (TEXT_FONT_SIZE + LINE_SPACING_L) * i + 100))
                pygame.display.update()
            for event in pygame.event.get(KEYDOWN):
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    se.play(1)
                    scene_number = -1
                    c_index = 0
                    c_index_b = 0
        elif scene_number == -2: # せってい
            print("can't reach now")
        elif scene_number == -1: # タイトル画面
            if once:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(BGM[0])
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(-1)
                bg.show(display_surface, bg_number)
                display_surface.blit(choice_font.render("はじめる", True, (0, 0, 0)), choice_position_t[0].get())
                display_surface.blit(choice_font.render("せってい", True, (100, 100, 100)), choice_position_t[1].get())
                display_surface.blit(choice_font.render("らいせんす", True, (0, 0, 0)), choice_position_t[2].get())
                display_surface.blit(choice_font.render("おわる", True, (0, 0, 0)), choice_position_t[3].get())
                once = False
                pygame.display.update()
            dirty_rects = [display_surface.blit(bg.get_image_surface(bg_number),
                                                (choice_position_t[c_index_b].x - CHOICE_FONT_SIZE,
                                                 choice_position_t[c_index_b].y),
                                                Rect(choice_position_t[c_index_b].x - CHOICE_FONT_SIZE,
                                                     choice_position_t[c_index_b].y, CHOICE_FONT_SIZE,
                                                     CHOICE_FONT_SIZE)),
                           display_surface.blit(choice_font.render("◆", True, (0, 0, 0)),
                                                (choice_position_t[c_index].x - CHOICE_FONT_SIZE,
                                                 choice_position_t[c_index].y))]
            pygame.display.update(dirty_rects)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if c_index < 3:
                            c_index_b = c_index
                            c_index += 1
                    elif event.key == K_UP:
                        if c_index > 0:
                            c_index_b = c_index
                            c_index -= 1
                    elif event.key == K_SPACE:
                        if c_index == 0:
                            scene_number = 0
                            se.play(0)
                            pygame.mixer.music.stop()
                            once = True
                        elif c_index == 1:
                            print("can't reach")
                            # scene_number = -2
                            # once = True
                        elif c_index == 2:
                            se.play(0)
                            scene_number = -3
                            once = True
                        else:
                            pygame.quit()
                            sys.exit()
        elif scene_number == 0: # ゲーム開始後
            if once and not display_covered:
                bg.show(display_surface, bg_number)
                if ch_0_visible:
                    ch_0.show(display_surface, ch_0_style)
                display_surface.blit(text_window, (0, STANDARD_TEXT_POSITION.y - 20))
                pygame.display.update()
                once = False
            elif (text_state == 0 or text_state == 2) and not display_covered:
                dirty_rects = []
                dirty_rects.append(display_surface.blit(bg.get_image_surface(bg_number),
                                                        (0, STANDARD_TEXT_POSITION.y - 20),
                                                        Rect(0, STANDARD_TEXT_POSITION.y - 20, screen_size.x,
                                                             screen_size.y + 20)))
                if ch_0_visible:
                    dirty_rects.append(display_surface.blit(ch_0.get_image_surface(ch_0_style),
                                                            (ch_0.get_coordinate().x, STANDARD_TEXT_POSITION.y - 20),
                                                            Rect(0, ch_0.get_image_surface(ch_0_style).get_height() - (
                                                                        screen_size.y - (screen_size.y // 2) - (
                                                                            screen_size.y // 4) + 20),
                                                                 ch_0.get_image_surface(ch_0_style).get_width(),
                                                                 ch_0.get_image_surface(ch_0_style).get_height())))
                dirty_rects.append(display_surface.blit(text_window, (0, STANDARD_TEXT_POSITION.y - 20)))
                pygame.display.update(dirty_rects)
            text = []
            text.extend(TEXT[scene_number][text_number])
            if text[0] == "@":
                if text[1] == "b":
                    bg_number = int(text[2])
                    once = True
                elif text[1] == "c":
                    if text[2] == "0":
                        if text[3] == "X":
                            ch_0_visible = False
                            once = True
                        else:
                            ch_0_style = int(text[3])
                            ch_0_visible = True
                            once = True
                elif text[1] == "f":
                    pygame.display.update(display_surface.fill(black, rect))
                    pygame.time.wait(100)
                    once = True
                elif text[1] == "s":
                    if text[2] == "0":
                        cover = pygame.Surface(display_surface.get_rect().size)
                        cover.fill(black)
                        for alpha in range(255):
                            bg.show(display_surface, bg_number)
                            if ch_0_visible:
                                ch_0.show(display_surface, ch_0_style)
                            cover.set_alpha(alpha, pygame.RLEACCEL)
                            display_surface.blit(cover, (0, 0))
                            pygame.display.update()
                        display_covered = True
                    if text[2] == "1":
                        cover = pygame.Surface(display_surface.get_rect().size)
                        cover.fill(black)
                        for alpha in reversed(range(255)):
                            bg.show(display_surface, bg_number)
                            if ch_0_visible:
                                ch_0.show(display_surface, ch_0_style)
                            cover.set_alpha(alpha, pygame.RLEACCEL)
                            display_surface.blit(cover, (0, 0))
                            pygame.display.update()
                        once = True
                        display_covered = False
                elif text[1] == "m":
                    if text[2] == "S":
                        pygame.mixer.music.play(-1)
                    elif text[2] == "P":
                        pygame.mixer.music.pause()
                    elif text[2] == "R":
                        pygame.mixer.music.unpause()
                    elif text[2] == "X":
                        pygame.mixer.music.stop()
                    elif text[2] == "F":
                        pygame.mixer.music.fadeout(500)
                    else:
                        pygame.mixer.music.load(BGM[int(text[2])])
                        pygame.mixer.music.set_volume(0.05)
                elif text[1] == "e":
                    if text[2] == "S":
                        se.stop(int(text[3]))
                    else:
                        se.set_volume(int(text[2]), 0.1)
                        se.play(int(text[2]))
                if text_number + 1 != len(TEXT[scene_number]):
                    text_number += 1
            else:
                if text_state == 0:
                    pygame.display.update(display_surface.blit(text_font.render(text[text_index], True, white), (
                        STANDARD_TEXT_POSITION.x + ((text_index - (text_index // 31 * 31)) * TEXT_FONT_SIZE),
                        STANDARD_TEXT_POSITION.y + (text_index // 31 * TEXT_FONT_SIZE))))
                    voice.set_volume(voice_number, 0.1)
                    voice.play(voice_number)
                    text_state = 1
                elif text_state == 1:
                    if text_index + 1 < len(text):
                        text_index += 1
                        pygame.display.update(display_surface.blit(text_font.render(text[text_index], True, white), (
                            STANDARD_TEXT_POSITION.x + ((text_index - (text_index // 31 * 31)) * TEXT_FONT_SIZE),
                            STANDARD_TEXT_POSITION.y + (text_index // 31 * TEXT_FONT_SIZE))))
                    else:
                        text_state = 3
                elif text_state == 2:
                    for index, char in enumerate(text):
                        pygame.display.update(display_surface.blit(text_font.render(char, True, white), (
                            STANDARD_TEXT_POSITION.x + ((index - (index // 31 * 31)) * TEXT_FONT_SIZE),
                            STANDARD_TEXT_POSITION.y + (index // 31 * TEXT_FONT_SIZE))))
                    text_state = 3
                for event in pygame.event.get(KEYDOWN):
                    if event.key == K_SPACE:
                        if text_state == 0 or text_state == 1:
                            text_state = 2
                        elif text_state == 3:
                            if text_number + 1 != len(TEXT[scene_number]):
                                voice.stop(voice_number)
                                text_number += 1
                                voice_number += 1
                                text_index = 0
                                text_state = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        frame += 1
        if frame == 61:
            frame = 1


if __name__ == "__main__":
    main()
