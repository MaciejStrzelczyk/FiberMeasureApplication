import asyncio
import pygame
from Application import Application

pygame.init()
main = Application()
loop = asyncio.get_event_loop()
loop.run_until_complete(main.main_menu())