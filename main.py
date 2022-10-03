import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # 關閉不必要的訊息
from UI import *
from GunData import *
import pygame as pg
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP

guns = list(gun_data.keys())

pg.init()
CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode(RESOLUTION)
SHOOT_WINDOW = ([400, 50], [700, 900])
pg.display.set_caption('Apex 後座力練習工具')

ui = UI(SCREEN, guns)
gun = GUN(SCREEN)

pg.mixer.set_num_channels(30) # 設置 20 個音軌以避免音軌被占用

try:
    while True:
        CLOCK.tick(FPS)
        # 取得滑鼠座標
        x, y = pg.mouse.get_pos()
        
        # 事件處理
        events = pg.event.get()
        for event in events:
            # 結束視窗
            if event.type == QUIT:
                print("quit")
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and mouse_inside_valid_area(x, y):
                    gun.start_fire()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    gun.reset_fire()
            elif event.type == FIRECHECK and mouse_inside_valid_area(x, y):
                gun.fire()
            elif event.type == RELOADCHECK:
                gun.reload()
        
            # 更新輸入欄位與靈敏度設定
            ui.input_sensitive.handle_event(event)
            gun.set_sensitive(ui.input_sensitive.get_float_value())
        
        crr_gun_name = ui.update_drop_down(events) # 取得當前選取的槍枝名稱
        gun.set_gun(crr_gun_name) # 設置槍枝
        
        # 繪製 UI
        ui.draw()
        gun.draw_gun_info()
        draw_mouse_pos(ui.SCREEN, x, y)
        pg.display.flip()
except Exception as e:
    print(e)