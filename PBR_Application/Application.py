import sys
import pygame
import asyncio
import csv
import os
import pygame.font
import random
from pygame.locals import *

from BT import BT
from button import Button

pygame.init()
clock = pygame.time.Clock()
main_win = pygame.display.set_mode((1440, 900), pygame.RESIZABLE)
pygame.display.set_caption('Liquid level measurement system')
BG = pygame.image.load("assets/Background2.png")
BG2 = pygame.image.load("assets/Background4.png")
bt = BT()
global liquid_level
global bt_status

DISCONNECTED = "disconnected"
CONNECT = "connected"
GREEN = "Green"
RED = "Red"


def save_value_to_csv(value, file_number,st):
    filename = f"sensor_data_{file_number}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow([st])
            writer.writerow(["Value"])

        writer.writerow([value])



async def read_sensor_data():
    global value
    while True:
        value = await bt.readData()
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Domelen.ttf", size)


class Application:

    def __init__(self):
        self.bt_status = CONNECT
        self.color = GREEN
    async def main_menu(self):
        while True:
            main_win.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            pygame.draw.rect(main_win, "#000000", pygame.Rect(300, 45, 850, 85))
            MENU_TEXT1 = get_font(58).render("Liquid                  ", True, "#0080FF")
            MENU_TEXT2 = get_font(58).render("       Detection System", True, "#FF3333")
            MENU_RECT1 = MENU_TEXT1.get_rect(center=(720, 80))
            MENU_RECT2 = MENU_TEXT2.get_rect(center=(720, 80))

            MAIN_MENU_BT_TEXT_DEFAULT = get_font(24).render("Bluetooth status: ", True, "White")
            MAIN_MENU_BT_TEXT_DEFAULT_POS = MAIN_MENU_BT_TEXT_DEFAULT.get_rect(center=(1120, 15))
            main_win.blit(MAIN_MENU_BT_TEXT_DEFAULT, MAIN_MENU_BT_TEXT_DEFAULT_POS)

            MAIN_MENU_BT_TEXT_STATUS = get_font(24).render(self.bt_status, True, self.color)
            MAIN_MENU_BT_TEXT_STATUS_POS = MAIN_MENU_BT_TEXT_STATUS.get_rect(center=(1330, 15))
            main_win.blit(MAIN_MENU_BT_TEXT_STATUS, MAIN_MENU_BT_TEXT_STATUS_POS)

            MEASUREMENT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(720, 250),
                                        text_input="MEASUREMENT", font=get_font(42), base_color="#FFFFFF",
                                        hovering_color="#0080FF")

            CONNECT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(720, 400),
                                    text_input="CONNECT", font=get_font(42), base_color="#FFFFFF",
                                    hovering_color="#0080FF")

            DISCONNECT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(720, 550),
                                       text_input="DISCONNECT", font=get_font(42), base_color="#FFFFFF",
                                       hovering_color="#0080FF")

            QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(720, 705),
                                 text_input="QUIT", font=get_font(42), base_color="#FFFFFF",
                                 hovering_color="#0080FF")

            main_win.blit(MENU_TEXT1, MENU_RECT1)
            main_win.blit(MENU_TEXT2, MENU_RECT2)

            for button in [MEASUREMENT_BUTTON, DISCONNECT_BUTTON, CONNECT_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(main_win)

            CONNECT_BUTTON.changeColor(MENU_MOUSE_POS)
            DISCONNECT_BUTTON.changeColor(MENU_MOUSE_POS)
            CONNECT_BUTTON.update(main_win)
            DISCONNECT_BUTTON.update(main_win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MEASUREMENT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if self.bt_status == CONNECT:
                            sensor_type = 4
                            #bt.write_sensor(sensor_type)
                            await Application.sensor_screen(self)
                        else:
                            await Application.no_connection(self)
                    if CONNECT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        try:
                            if bt.bt_serial():
                                self.bt_status = CONNECT
                                self.color = GREEN
                                bt.write_one()
                                break
                        except Exception as e:
                            print(e)
                    if DISCONNECT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        try:
                            bt.write_zero()
                            self.bt_status = DISCONNECTED
                            self.color = RED
                            bt.disconect()
                            break
                        except Exception as e:
                            print(e)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        try:
                            bt.write_zero()
                            self.bt_status = DISCONNECTED
                            self.color = RED
                            bt.disconect()
                            break
                        except Exception as e:
                            print(e)
                        pygame.quit()
                        sys.exit()
            pygame.display.update()


    # main_menu()
    async def sensor_screen(self):
        try:
            #moving_sprites = pygame.sprite.Group()
            #sensor = Sensor(1200, 450)
            #moving_sprites.add(sensor)

            MOVEEVENT, t = pygame.USEREVENT + 1, 1000
            pygame.time.set_timer(MOVEEVENT, t)
            turn_on_measurement = 0
            file_number = 0
            value=0

            measurements = [1,2,3]  # Lista przechowująca pomiary
            max_measurements = 50  # Maksymalna liczba pomiarów do wyświetlenia
            bar_width = 10  # Szerokość słupka na wykresie
            bar_spacing = 3  # Odstęp między słupkami
            chart_x = 135  # Początkowa pozycja X wykresu
            chart_y = 620  # Początkowa pozycja Y wykresu
            axis_color = (255, 255, 255)  # Kolor osi
            font = pygame.font.Font(None, 20)  # Inicjalizacja obiektu czcionki
            font2 = pygame.font.Font(None, 30)  # Inicjalizacja obiektu czcionki
            #font_meas = pygame.font.Font(None, 18)  # Inicjalizacja obiektu czcionki
            x_labels = list(range(1, max_measurements + 1))
            min_value = 0
            max_value = 0

            chart_height = 300
            main_win.blit(BG2, (0, 0))

            y_min = 0
            y_max = 5

            while True:
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                main_win.blit(BG2, (0, 0))
                #clock.tick(10)
                #moving_sprites.draw(main_win)
                #moving_sprites.update()

                NAME_TEXT = get_font(70).render("Measurement Type:", True, "#0080FF")
                NAME_RECT = NAME_TEXT.get_rect(topleft=(15, 10))
                main_win.blit(NAME_TEXT, NAME_RECT)

                TYPE_TEXT = get_font(70).render("Optical Fiver Liquid Sensor", True, "#FF3333")
                TYPE_RECT = NAME_TEXT.get_rect(topleft=(15, 100))
                main_win.blit(TYPE_TEXT, TYPE_RECT)

                VALUE_TEXT = get_font(78).render("Generated Voltage:" + "      V", True, "#0080FF")
                VALUES_TEXT = get_font(78).render(str(value), True, "#FF3333")
                VALUE_RECT = NAME_TEXT.get_rect(topleft=(15, 190))
                VALUES_RECT = NAME_TEXT.get_rect(topleft=(900, 190))
                main_win.blit(VALUE_TEXT, VALUE_RECT)
                main_win.blit(VALUES_TEXT, VALUES_RECT)

                OPTIONS_MM = Button(image=pygame.image.load("assets/Rect.png"), pos=(300, 810),
                                    text_input="MAIN MENU", font=get_font(65), base_color="White",
                                    hovering_color="#0080FF")
                OPTIONS_QUIT = Button(image=pygame.image.load("assets/Rect.png"), pos=(780, 810),
                                      text_input="QUIT", font=get_font(65), base_color="White",
                                      hovering_color="#0080FF")

                if turn_on_measurement == 0:
                    START_M = Button(image=pygame.image.load("assets/Rect.png"), pos=(300, 728),
                                     text_input="START MEAS", font=get_font(30), base_color="White",
                                     hovering_color="#0080FF")
                    SAVE_M = Button(image=pygame.image.load("assets/Rect.png"), pos=(780, 728),
                                    text_input="SAVE MEAS", font=get_font(30), base_color="#666666",
                                    hovering_color="#666666")
                elif turn_on_measurement == 1:
                    START_M = Button(image=pygame.image.load("assets/Rect.png"), pos=(300, 728),
                                     text_input="START MEAS", font=get_font(30), base_color="#666666",
                                     hovering_color="#666666")
                    SAVE_M = Button(image=pygame.image.load("assets/Rect.png"), pos=(780, 728),
                                    text_input="SAVE MEAS", font=get_font(30), base_color="White",
                                    hovering_color="#0080FF")

                    if value < min_value:
                        min_value = value
                    elif value > max_value:
                        max_value = value

                    Y_AXIS_TEXT = get_font(24).render("Generated voltage [V]", True, "#0080FF")
                    X_AXIS_TEXT = get_font(24).render("No. of measurement", True, "#FF3333")
                    Y_AXIS_RECT = NAME_TEXT.get_rect(topleft=(36, 320))
                    X_AXIS_RECT = NAME_TEXT.get_rect(topleft=(350, 650))
                    ROT_Y = pygame.transform.rotate(Y_AXIS_TEXT, 90)
                    main_win.blit(ROT_Y, Y_AXIS_RECT)
                    main_win.blit(X_AXIS_TEXT, X_AXIS_RECT)

                    # Rysowanie osi X
                    pygame.draw.line(main_win, axis_color, (chart_x, chart_y),
                                     (chart_x + max_measurements * (bar_width + bar_spacing)+10, chart_y), 2)

                    # Rysowanie osi Y
                    pygame.draw.line(main_win, axis_color, (chart_x, chart_y), (chart_x, chart_y - chart_height), 2)

                    # Wyświetlanie podziałek na osi Y
                    for i in range(0, chart_height + 1, 30):  # Zmniejszamy odstęp między podziałkami
                        pygame.draw.line(main_win, axis_color, (chart_x - 5, chart_y - i), (chart_x + 5, chart_y - i),2)
                        label_value = i / chart_height * (y_max - y_min) + y_min  # Obliczamy wartość podziałki
                        label = font2.render(f"{label_value:.1f}", True,axis_color)  # Formatujemy liczbę z jednym miejscem po przecinku
                        label_rect = label.get_rect(center=(chart_x - 45, chart_y - i))
                        main_win.blit(label, label_rect)

                    # Przycinanie listy, jeśli przekroczy maksymalną liczbę pomiarów
                    if len(measurements) > max_measurements:
                        measurements = measurements[1:]  # Usuń pierwszy pomiar
                        x_labels = x_labels[1:]  # Usuń pierwszy numer
                    x_labels.append(x_labels[-1] + 1)  # Dodaj kolejny numer

                    # Wyświetlanie wykresu słupkowego
                    x = chart_x
                    prev_bar_height = None
                    for j, (measurement, label) in enumerate(zip(measurements, x_labels), start=1):
                        if min_value != max_value:
                            bar_height = int((measurement - y_min) / (y_max - y_min) * chart_height)
                            #bar_height = int((chart_height*value)/y_max)
                        else:
                            bar_height = chart_height // 2

                        if bar_height > chart_height:
                            bar_height = chart_height+10
                            bar_rect = pygame.Rect(x+20, chart_y-bar_height, bar_width, bar_height)
                            pygame.draw.rect(main_win, (255, 0, 0), bar_rect)
                            #value_label = font_meas.render(str(measurement), True, axis_color)
                            #value_label_rect = value_label.get_rect()
                            #value_label_rect.midbottom = (x + 20 + bar_width // 2, chart_y - bar_height - 5)
                            #main_win.blit(value_label, value_label_rect)
                        elif bar_height < 0:
                            bar_rect = pygame.Rect(x+20, chart_y-bar_height+5, bar_width, 5)
                            pygame.draw.rect(main_win, (255, 0, 0), bar_rect)
                            #value_label = font_meas.render(str(measurement), True, axis_color)
                            #value_label_rect = value_label.get_rect()
                            #value_label_rect.midbottom = (x + 20 + bar_width // 2, chart_y - 5)
                            #main_win.blit(value_label, value_label_rect)
                        else:
                            bar_rect = pygame.Rect(x+20, chart_y-bar_height, bar_width, 3)  # Tworzenie prostokąta dla słupka
                            pygame.draw.rect(main_win, (255, 255, 255), bar_rect)
                            #value_label = font_meas.render(str(measurement), True, axis_color)
                            #value_label_rect = value_label.get_rect()
                            #value_label_rect.midbottom = (x + 20 + bar_width // 2, chart_y - bar_height - 5)
                            #main_win.blit(value_label, value_label_rect)

                        if label % 2 != 0:
                            label = font.render(str(label), True, axis_color)
                            label_rect = label.get_rect()
                            label_rect.midtop = ((x + 20 + bar_width // 2), chart_y + 10)
                            main_win.blit(label, label_rect)

                        if prev_bar_height is not None:
                            line_start = (x + 10 + bar_width // 2, chart_y - prev_bar_height)  # Punkt początkowy linii
                            line_end = (x + 10 + bar_width // 2, chart_y - bar_height)  # Punkt końcowy linii
                            pygame.draw.line(main_win, (255, 255, 255), line_start, line_end, 3)  # Rysowanie linii

                        prev_bar_height = bar_height
                        x += bar_width + bar_spacing

                START_M.changeColor(OPTIONS_MOUSE_POS)
                START_M.update(main_win)
                SAVE_M.changeColor(OPTIONS_MOUSE_POS)
                SAVE_M.update(main_win)

                OPTIONS_MM.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_MM.update(main_win)
                OPTIONS_QUIT.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_QUIT.update(main_win)

                for event in pygame.event.get():
                    if event.type == MOVEEVENT:  # is called every 't' milliseconds
                        value = round(random.uniform(2.2, 3.3),2)
                        # await bt.readData()/100
                        if turn_on_measurement == 1:
                            save_value_to_csv(value, file_number, "Fiber")
                            measurements.append(value)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if START_M.checkForInput(OPTIONS_MOUSE_POS) & turn_on_measurement == 0:
                            turn_on_measurement = 1
                            min_value = value
                            max_value = value
                        if SAVE_M.checkForInput(OPTIONS_MOUSE_POS) & turn_on_measurement == 1:
                            turn_on_measurement = 0
                            measurements.clear()
                            measurements = []
                            file_number += 1
                        if OPTIONS_MM.checkForInput(OPTIONS_MOUSE_POS):
                            try:
                                bt.write_zero()
                                self.bt_status = DISCONNECTED
                                self.color = RED
                                turn_on_measurement = 0
                                measurements.clear()
                                measurements = []
                                file_number += 1
                                bt.disconect()
                                await Application.main_menu(self)
                                break
                            except Exception as e:
                                print(e)
                        if OPTIONS_QUIT.checkForInput(OPTIONS_MOUSE_POS):
                            try:
                                bt.write_zero()
                                self.bt_status = DISCONNECTED
                                self.color = RED
                                file_number = 0
                                bt.disconect()
                                pygame.quit()
                                sys.exit()
                                break
                            except Exception as e:
                                print(e)

                pygame.display.update()
        except Exception as e:
            print("Wystąpił błąd podczas obsługi ekranu czujnika:", str(e))

    async def no_connection(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            main_win.blit(BG, (0, 0))

            pygame.draw.rect(main_win, "#000000", pygame.Rect(140, 165, 1160, 85))
            pygame.draw.rect(main_win, "#000000", pygame.Rect(50, 370, 1345, 72))
            NAME_TEXT1 = get_font(80).render("No Bluetooth Connection", True, "#0080FF")
            NAME_TEXT2 = get_font(60).render("Please connect the APP to the device", True, "#FF3333")
            NAME_RECT1 = NAME_TEXT1.get_rect(center=(720, 200))
            NAME_RECT2 = NAME_TEXT2.get_rect(center=(720, 400))
            main_win.blit(NAME_TEXT1, NAME_RECT1)
            main_win.blit(NAME_TEXT2, NAME_RECT2)

            OPTIONS_MM = Button(image=pygame.image.load("assets/Rect.png"), pos=(500, 650),
                                text_input="BACK", font=get_font(70), base_color="White",
                                hovering_color="#0080FF")
            OPTIONS_QUIT = Button(image=pygame.image.load("assets/Rect.png"), pos=(940, 650),
                                  text_input="QUIT", font=get_font(70), base_color="White",
                                  hovering_color="#0080FF")

            OPTIONS_MM.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_MM.update(main_win)
            OPTIONS_QUIT.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_QUIT.update(main_win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_MM.checkForInput(OPTIONS_MOUSE_POS):
                        await Application.main_menu(self)
                    if OPTIONS_QUIT.checkForInput(OPTIONS_MOUSE_POS):
                        bt.disconect()
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
