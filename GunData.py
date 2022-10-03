import imp
from random import choice
import pygame as pg
from UI import *
import win32api
from win32con import MOUSEEVENTF_MOVE

FIRECHECK = pg.USEREVENT + 1
RELOADCHECK = pg.USEREVENT + 2

gun_data = {
    "R-301": {
        "image": "R-301_Carbine_Icon.png",      # 槍枝圖片
        "fire_rate": 1 / 13.5,                  # 每發子彈發射時間 (每秒發射13.5發)
        "mag_size": 28,                         # 彈夾容量
                                                # 後座力表
        "recoil_pattern": [[0, 0, 0.0191], [-2, 3, 0.0191], [2, 1, 0.0191], [-1, 2, 0.0191], [-1, 1, 0.0191], [-2, 4, 0.0191], [2, 2, 0.0191], [1, 0, 0.0191], [-2, 3, 0.0191], [1, 0, 0.0191], [-2, 2, 0.0191], [0, 2, 0.0191], [1, 0, 0.0191], [-2, 2, 0.0191], [1, -1, 0.0191], [-1, 3, 0.0191], [1, 1, 0.0191], [2, 0, 0.0191], [-1, 2, 0.0191], [1, -1, 0.0191], [-1, 4, 0.0191], [1, 2, 0.0191], [0, 1, 0.0191], [0, 1, 0.0191], [-1, 2, 0.0191], [0, 1, 0.0191], [2, -1, 0.0191], [-2, 2, 0.0191], [1, -1, 0.0191], [-2, 2, 0.0191], [1, 0, 0.0191], [-1, 1, 0.0191], [-1, 1, 0.0191], [-2, 1, 0.0191], [1, -2, 0.0191], [-2, 2, 0.0191], [1, -1, 0.0191], [-2, 2, 0.0191], [1, 0, 0.0191], [-1, 1, 0.0191], [-1, 1, 0.0191], [-3, 1, 0.0191], [1, -2, 0.0191], [-2, 1, 0.0191], [1, -1, 0.0191], [-2, 2, 0.0191], [0, -1, 0.0191], [-1, 0, 0.0191], [-1, 0, 0.0191], [1, -1, 0.0191], [0, 3, 0.0191], [2, -1, 0.0191], [-1, 1, 0.0191], [2, 2, 0.0191], [2, 1, 0.0191], [1, 0, 0.0191], [0, 1, 0.0191], [1, 0, 0.0191], [0, 1, 0.0191], [2, -1, 0.0191], [1, 0, 0.0191], [-1, 1, 0.0191], [0, 2, 0.0191], [1, 0, 0.0191], [2, -2, 0.0191], [-1, 2, 0.0191], [2, -1, 0.0191], [1, 1, 0.0191], [2, -1, 0.0191], [1, 0, 0.0191], [1, -1, 0.0191], [0, 1, 0.0191], [2, -1, 0.0191], [-1, 1, 0.0191], [0, 2, 0.0191], [2, -1, 0.0191], [0, 1, 0.0191], [0, 1, 0.0191], [1, -1, 0.0191], [-3, 1, 0.0191], [1, -2, 0.0191], [-1, 0, 0.0191], [-1, 1, 0.0191], [-1, 0, 0.0191], [1, -1, 0.0191], [-3, 2, 0.0191], [0, -1, 0.0191], [-1, 1, 0.0191], [-2, 0, 0.0191], [1, -2, 0.0191], [-2, 1, 0.0191], [1, -1, 0.0191], [-2, 1, 0.0191], [-1, 0, 0.0191], [-1, 1, 0.0191], [0, -1, 0.0191], [-3, -1, 0.0191], [1, -2, 0.0191], [-1, 1, 0.0191], [-1, 0, 0.0191], [-2, 0, 0.0191], [0, -1, 0.0191], [1, -2, 0.0191], [-2, 1, 0.0191], [1, -1, 0.0191], [-1, 2, 0.0191], [1, -1, 0.0191], [-1, 1, 0.0191], [-1, 1, 0.0191], [1, -2, 0.0191], [-1, 1, 0.0191], [0, 1, 0.0191], [1, -1, 0.0191], [-1, 2, 0.0191]],
        "full_reload_time": 2880,              # 完全換子彈所需時間(包含上膛)
        "sounds": ['r301_1.wav', 'r301_2.wav']  # 開槍聲音檔案
    },
    "R99": {
        "image": "R-99_SMG_Icon.png",
        "mag_size": 27,
        "fire_rate": 1 / 18,
        "recoil_pattern": [[0, 0, 0.0144], [-1, 2, 0.0144], [0, 2, 0.0144], [1, 0, 0.0144], [-1, 1, 0.0144], [1, 3, 0.0144], [1, 0, 0.0144], [-1, 2, 0.0144], [0, -1, 0.0144], [2, 3, 0.0144], [1, 0, 0.0144], [-1, 1, 0.0144], [-1, 2, 0.0144], [1, 2, 0.0144], [-1, 1, 0.0144], [-1, 3, 0.0144], [0, 2, 0.0144], [1, 1, 0.0144], [-1, 1, 0.0144], [-3, 6, 0.0144], [-1, 2, 0.0144], [-2, 2, 0.0144], [-1, 2, 0.0144], [-1, 1, 0.0144], [-2, 2, 0.0144], [0, 1, 0.0144], [-1, 1, 0.0144], [-1, 3, 0.0144], [1, 0, 0.0144], [-1, 2, 0.0144], [2, 2, 0.0144], [2, 1, 0.0144], [0, 2, 0.0144], [2, 2, 0.0144], [2, 2, 0.0144], [0, 1, 0.0144], [0, 1, 0.0144], [1, 3, 0.0144], [0, 2, 0.0144], [1, 2, 0.0144], [2, 2, 0.0144], [-2, 2, 0.0144], [0, -2, 0.0144], [-1, 2, 0.0144], [1, 0, 0.0144], [-5, -2, 0.0144], [-2, 2, 0.0144], [-1, 0, 0.0144], [-2, 2, 0.0144], [0, -1, 0.0144], [-1, 1, 0.0144], [0, 1, 0.0144], [4, 1, 0.0144], [0, -1, 0.0144], [0, 2, 0.0144], [1, 0, 0.0144], [2, -2, 0.0144], [0, 1, 0.0144], [2, 2, 0.0144], [2, 0, 0.0144], [0, 1, 0.0144], [2, 2, 0.0144], [2, -2, 0.0144], [0, 1, 0.0144], [1, 3, 0.0144], [2, 0, 0.0144], [0, 1, 0.0144], [-1, 1, 0.0144], [-1, 1, 0.0144], [-2, -1, 0.0144], [-2, 0, 0.0144], [-3, 1, 0.0144], [-2, -2, 0.0144], [0, 2, 0.0144], [-1, 2, 0.0144], [1, -3, 0.0144], [-1, 1, 0.0144], [2, 2, 0.0144], [2, -1, 0.0144], [1, 2, 0.0144]],
        "full_reload_time": 2210,
        "sounds": ['r99_1.wav']
    },
    "Flatline": {
        "image": "VK-47_Flatline_Icon.png",
        "mag_size": 30,
        "fire_rate": 1 / 10,
        "recoil_pattern": [[0, 0, 0.0166], [2, 4, 0.0166], [-1, 3, 0.0166], [1, 1, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [1, -1, 0.0166], [1, -1, 0.0166], [-3, 5, 0.0166], [1, -1, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [1, -1, 0.0166], [1, 2, 0.0166], [1, 2, 0.0166], [1, 2, 0.0166], [1, 0, 0.0166], [-1, 1, 0.0166], [1, 0, 0.0166], [1, -1, 0.0166], [0, 2, 0.0166], [1, 2, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [0, 1, 0.0166], [2, 3, 0.0166], [0, 3, 0.0166], [2, -1, 0.0166], [-1, 2, 0.0166], [2, -1, 0.0166], [-1, 3, 0.0166], [0, 2, 0.0166], [1, -2, 0.0166], [2, -2, 0.0166], [-1, 2, 0.0166], [-1, 2, 0.0166], [0, -1, 0.0166], [-1, 2, 0.0166], [-1, 1, 0.0166], [-2, -1, 0.0166], [-1, 0, 0.0166], [0, -1, 0.0166], [-1, 0, 0.0166], [-1, -1, 0.0166], [-1, 2, 0.0166], [1, -3, 0.0166], [-1, 2, 0.0166], [0, -1, 0.0166], [1, -2, 0.0166], [0, 1, 0.0166], [-1, 1, 0.0166], [0, -1, 0.0166], [1, 0, 0.0166], [-2, 4, 0.0166], [1, -1, 0.0166], [0, -1, 0.0166], [-1, 2, 0.0166], [0, 1, 0.0166], [2, 1, 0.0166], [-1, 2, 0.0166], [2, -1, 0.0166], [-1, 1, 0.0166], [0, 1, 0.0166], [2, -1, 0.0166], [0, 3, 0.0166], [1, 2, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [1, -1, 0.0166], [1, -1, 0.0166], [-1, 4, 0.0166], [1, -1, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [1, -1, 0.0166], [1, 1, 0.0166], [1, 1, 0.0166], [1, -1, 0.0166], [1, 0, 0.0166], [1, -2, 0.0166], [0, 1, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [1, 1, 0.0166], [0, 5, 0.0166], [1, -1, 0.0166], [1, 0, 0.0166], [-1, 1, 0.0166], [1, 1, 0.0166], [1, 2, 0.0166], [1, 2, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [2, -2, 0.0166], [0, 2, 0.0166], [1, 1, 0.0166], [1, -1, 0.0166], [-1, 2, 0.0166], [2, -1, 0.0166], [0, 1, 0.0166], [0, 2, 0.0166], [0, 2, 0.0166], [2, -3, 0.0166], [0, 2, 0.0166], [1, -1, 0.0166], [1, 0, 0.0166], [0, 1, 0.0166], [0, 1, 0.0166], [1, -2, 0.0166], [-1, 1, 0.0166], [-1, 1, 0.0166], [1, -3, 0.0166], [-3, 2, 0.0166], [-1, 0, 0.0166], [0, -1, 0.0166], [-1, 2, 0.0166], [0, -1, 0.0166], [-2, 1, 0.0166], [-1, 0, 0.0166], [0, -1, 0.0166], [-1, 1, 0.0166], [-1, -1, 0.0166], [-3, 2, 0.0166], [0, -1, 0.0166], [-1, -1, 0.0166], [0, 1, 0.0166], [0, -1, 0.0166], [0, -2, 0.0166], [-3, 3, 0.0166], [0, -1, 0.0166], [0, -1, 0.0166], [-1, 1, 0.0166], [-3, 0, 0.0166], [-2, 2, 0.0166], [0, -3, 0.0166], [-1, 1, 0.0166], [-1, 1, 0.0166], [0, 1, 0.0166], [-1, 3, 0.0166], [1, 0, 0.0166], [0, -1, 0.0166], [0, 1, 0.0166], [0, -1, 0.0166], [-3, 4, 0.0166], [0, -2, 0.0166], [-1, 1, 0.0166], [0, 1, 0.0166], [0, -1, 0.0166], [1, 3, 0.0166], [0, 1, 0.0166], [1, -1, 0.0166], [-1, 3, 0.0166]],
        "full_reload_time": 2790,
        "sounds": ['flatline_1.wav', 'flatline_2.wav']
    },
}

class GUN():
    def __init__(self, screen: pg.Surface): # , recoil_pattern: list[float], reload_time: float, max_mag: int
        super().__init__()
        self.SCREEN = screen            # 主要繪製平面
        self.gun_name = ''              # 槍名
        self.recoil_pattern = []        # 後座力表
        self.full_reload_time = 0       # 裝填子彈時間
        self.mag_size = 0               # 彈夾容量
        self.crr_mag = 0                # 彈夾剩餘子彈
        self.reloading = False          # 是否正在裝填子彈
        self.crr_recoil = 0             # 當前後座力索引
        self.sounds = []                # 槍擊聲
        self.crr_recoil_pattern = []    # 當前射擊的後座力座標
        self.sensitive = 2.5            # 遊戲靈敏度
        self.fire_rate = 0              # 發射一顆子彈所需時間
        self.x_offset = None            # 最後一次開槍x控制後座力
        self.y_offset = None            # 最後一次開槍y控制後座力
        self.x_recoil = None            # 本次開槍x後座力
        self.y_recoil = None            # 本次開槍y後座力
        self.reload_progress = None            # 重新裝載子彈進度
        self.image = None               # 槍圖片
    
    def set_gun(self, gun_name: str) -> None:
        """設置當前槍種

        Args:
            gun_name (str): 槍名稱
        """
        if gun_name == '' or self.gun_name == gun_name:
            return
        gun_info = gun_data[gun_name]
        self.gun_name = gun_name
        self.fire_rate = gun_info['fire_rate']
        self.mag_size = gun_info['mag_size']
        self.crr_mag = gun_info['mag_size']
        self.recoil_pattern = gun_info['recoil_pattern']
        self.full_reload_time = gun_info['full_reload_time']
        self.reloading = False
        self.crr_recoil = 0
        self.sounds = []
        self.crr_recoil_pattern = []
        self.image = pg.image.load(f'./Assets/Guns/{gun_info["image"]}').convert_alpha()
        for sound in gun_info['sounds']:
            self.sounds.append(pg.mixer.Sound(f"./Audio/{sound}"))
    
    def draw_gun_info(self) -> None:
        """繪製槍枝資訊到UI
        """
        text_font = pg.font.SysFont(None, 24)
        gun_name_text = text_font.render(f'Gun Type: {self.gun_name}', True, (0, 0, 0))
        gun_crr_mag = text_font.render(f'Bullets Left: {self.crr_mag}', True, (0, 0, 0))
        self.SCREEN.blit(gun_name_text, (10, 650)) # 標靶提示文字
        self.SCREEN.blit(gun_crr_mag, (10, 680)) # 剩餘提示文字
        
        if self.reloading:
            if self.reload_pass_time - self.reload_at_time < self.full_reload_time:
                a = a+1
                draw_bar(self.SCREEN, (self.reload_pass_time - self.reload_at_time)/self.full_reload_time)
            else:
                reloading = False

        self.draw_bullet_track()
        cx, cy = 1100, 200  # 繪製箭頭的起始點
        if self.x_offset is not None:
            draw_arrow(self.SCREEN, pg.Vector2(cx, cy), pg.Vector2(cx + self.x_offset, cy + self.y_offset), pg.Color("dodgerblue"), 1, 4, 4)  # 繪製箭頭
        rx, ry = 1100, 550
        if self.x_recoil is not None:
            draw_arrow(self.SCREEN, pg.Vector2(rx, ry), pg.Vector2(rx - self.x_recoil, ry - self.y_recoil), pg.Color("red"), 1, 4, 4)  # 繪製箭頭
        
        # 如果有圖片就顯示圖片
        if self.image is not None:
            rect = self.image.get_rect()
            rect.topleft = (180, 10)
            self.SCREEN.blit(self.image, rect) # 槍圖片
            
        if self.reload_progress is not None:
            draw_bar(self.SCREEN, self.reload_progress)
        
    def start_fire(self) -> None:
        """開始開火, 在此執行計時器
        """
        self.first = True
        # 如果彈夾都打完了那就清理上次的彈孔
        if self.crr_mag == self.mag_size:
            self.crr_recoil_pattern = [] 
        self.fire()
    
    def fire(self) -> None:
        """開火
        """
        # 有選擇槍才開槍
        if self.gun_name == '':
            return
        
        # 換彈條件
        if self.crr_mag <= 0 and self.reload_progress is None:
            self.start_reload()
            return
        
        # 第一槍直接開槍
        if self.first:
            self.x_recoil, self.y_recoil = 0, 0 # 重置正確後座力
            self.time_passed, self.time_passed2 = 0, 0
            self.last_mouse_pos = pg.mouse.get_pos()
            self.do_fire() # 開第一槍
            self.do_recoil() # 開槍後的後座力
            pg.time.set_timer(FIRECHECK, 10) # 計時器開始
            self.first = False
        else:
            self.time_passed += (10 / 1000)
            self.time_passed2 += (10 / 1000)
            recoil_info = self.recoil_pattern[self.crr_recoil] # 取得當前後座力
            # 判斷是否執行後座力
            if self.time_passed >= recoil_info[2]:
                self.time_passed -= self.fire_rate # 計時器扣除耗時
                self.crr_recoil = (self.crr_recoil + 1) if self.crr_recoil < len(self.recoil_pattern) - 1 else 0 # 下一個後座力
                self.do_recoil() # 後座力
                self.time_passed = 0
            
            # 判斷是否執行開火
            if self.time_passed2 >= self.fire_rate:
                self.time_passed2 -= self.fire_rate # 計時器扣除耗時
                self.do_fire()
    
    def do_recoil(self) -> None:
        """執行後座力
        """
        recoil_info = self.recoil_pattern[self.crr_recoil]  # 取得當前後座力
        x_offset = int(-recoil_info[0] * self.sensitive)
        y_offset = int(-recoil_info[1] * self.sensitive)
        win32api.mouse_event(MOUSEEVENTF_MOVE, x_offset, y_offset, 0, 0)
        # 用來繪製正確後座力
        self.x_recoil += x_offset
        self.y_recoil += y_offset
    
    def do_fire(self) -> None:
        """執行開火功能
        """
        self.create_pattern()
        if self.sounds != []:
            sound = choice(self.sounds)
            pg.mixer.Sound.play(sound)

        self.crr_mouse_pos = pg.mouse.get_pos()  # 後座力之後的滑鼠座標
        self.x_offset = self.crr_mouse_pos[0] - self.last_mouse_pos[0]
        self.y_offset = self.crr_mouse_pos[1] - self.last_mouse_pos[1]
        self.x_recoil, self.y_recoil = 0, 0  # 重置正確後座力
        self.last_mouse_pos = self.crr_mouse_pos  # 更新最後滑鼠座標
        # 消耗子彈
        self.crr_mag -= 1
        
    def create_pattern(self) -> None:
        """製作當前滑鼠位置的彈孔
        """
        mouse_pos = list(pg.mouse.get_pos())
        self.crr_recoil_pattern.append(mouse_pos) # 增加彈孔
    
    def reset_fire(self) -> None:
        """自由開火結束
        """
        pg.time.set_timer(FIRECHECK, 0) # 停止計時器
        self.time_passed, self.time_passed2, self.crr_recoil = 0, 0, 0
        self.x_offset, self.y_offset = None, None
        self.x_recoil, self.y_recoil = None, None
    
    def set_sensitive(self, sen: float) -> None:
        """設置靈敏度

        Args:
            sen (float): 靈敏度
        """
        self.sensitive = sen
     
    def draw_bullet_track(self) -> None:  
        """繪製彈孔道

        Args:
            surface (pg.Surface): 要繪製的平面
            tracks (list[float, float]): 彈孔清單
        """ 
        # 繪製設定好的後座力表
        rx, ry = 633-450, 523
        for track in self.recoil_pattern:
            rx -= track[0] * self.sensitive
            ry -= track[1] * self.sensitive
            pg.draw.circle(self.SCREEN, (155, 155, 155), pg.Vector2(rx, ry), 2, 1)
        
        # 繪製玩家控制的後座力表
        if self.crr_recoil_pattern != []:
            for track in self.crr_recoil_pattern:
                pg.draw.circle(self.SCREEN, (155, 155, 155), pg.Vector2(track), 2, 1)
    
    def start_reload(self) -> None:
        """開始重新裝填子彈
        """
        pg.time.set_timer(FIRECHECK, 0) # 停止開火計時器
        pg.time.set_timer(RELOADCHECK, int(self.full_reload_time / 1000)) # 開始裝子彈計時器
        self.reload_progress = 0.
        self.reload()
    
    def reload(self) -> None:
        """重新裝填子彈
        """
        # 判斷是否已經裝好子彈了
        if self.reload_progress == None or self.reload_progress >= 1.:
            pg.time.set_timer(RELOADCHECK, 0)
            self.crr_mag = self.mag_size # 設置子彈數量為滿
            self.reload_progress = None # 重置裝子彈進度
            return
        self.reload_progress += 0.001
        