import pygame as pg
import time

FPS = 60

WIDTH, HEIGHT = 1280, 800
RESOLUTION = (WIDTH, HEIGHT)

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

def mouse_inside_valid_area(mx: int, my: int) -> bool:
    """判斷滑鼠是否在開火區域

    Args:
        mx (int): 滑鼠x座標
        my (int): 滑鼠y座標

    Returns:
        bool: 滑鼠是否在開火區域
    """
    x, y, w, h = WIDTH/2-200, 100, 400, 600
    return x < mx < x + w and y < my < y + h


def draw_valid_area(surface: pg.Surface, x: int, y: int, w: int, h: int) -> None:
    """繪製有效開火區域

    Args:
        surface (pg.Surface): 要繪製的平面
        x (int): 左上x座標
        y (int): 左上y座標
        w (int): 寬度
        h (int): 長度
    """
    rect = pg.Rect(x, y, w, h)
    pg.draw.rect(surface, (185, 185, 185), rect, 1)
    
class DropDown:
    def __init__(self, screen, x, y, w, h, font, main, options):
        self.screen = screen
        self.color_menu = [COLOR_INACTIVE, COLOR_ACTIVE]
        self.color_option = [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE]
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
    
    def draw(self):
        """繪製下拉選單
        """
        pg.draw.rect(self.screen, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        self.screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(self.screen, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                self.screen.blit(msg, msg.get_rect(center = rect.center))
        
    def update(self, event_list) -> int:
        """更新選項

        Args:
            event_list (_type_): 事件清單

        Returns:
            int: 新選項索引
        """
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1

class InputBox:

    def __init__(self, screen: pg.Surface, x, y, w, h, text=''):
        self.screen = screen
        self.rect = pg.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = text
        self.text_font = pg.font.SysFont(None, 24)
        self.txt_surface = self.text_font.render(text, True, self.color)
        self.active = False
        self.score = 1
        # Cursor declare
        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pg.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))

    def get_float_value(self) -> float:
        if self.text == '':
            return 0.
        return float(self.text)
    
    def handle_event(self, event) -> None:
        """接收輸入事件

        Args:
            event (_type_): _description_
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                # 只接收浮點數
                elif(event.unicode in map(str, range(9 + 1)) or (event.unicode == '.' and '.' not in self.text)):
                    self.text += event.unicode
                    # Cursor
                    self.txt_rect.size = self.txt_surface.get_size()
                    self.cursor.topleft = self.txt_rect.topright
                    # Limit characters           -20 for border width
                    if self.txt_surface.get_width() > self.rect.w - 15:
                        self.text = self.text[:-1]
    
    def draw(self):
        """繪製輸入欄位
        """
        self.txt_surface = self.text_font.render(self.text, True, self.color)
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        pg.draw.rect(self.screen, self.color, self.rect, 1)
        if time.time() % 1 > 0.5:
            # bounding rectangle of the text
            text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 5, self.rect.y + 10))
            # set cursor position
            self.cursor.midleft = text_rect.midright
            pg.draw.rect(self.screen, self.color, self.cursor)

def draw_gamepad(screen: pg.Surface) -> None:
    """繪製後座力表

    Args:
        screen (pg.Surface): 要繪製的平面
    """
    for i in range(5):
        c = (207, 207, 207) if (i % 2) == 0 else (155, 155, 155)
        r = 25 * (i + 1)
        pg.draw.circle(screen, c, [1100, 200], r, 2)

    text_font = pg.font.SysFont(None, 24)
    rg_text = text_font.render("Your Recoil", True, (0, 0, 0))
    screen.blit(rg_text, (1050, 350)) # 標靶提示文字
    
    
    for i in range(5):
        c = (207, 207, 207) if (i % 2) == 0 else (155, 155, 155)
        r = 25 * (i + 1)
        pg.draw.circle(screen, c, [1100, 550], r, 2)

    text_font = pg.font.SysFont(None, 24)
    rg_text = text_font.render("Correct Recoil", True, (0, 0, 0))
    screen.blit(rg_text, (1050, 700)) # 標靶提示文字

def draw_red_dot(surface: pg.Surface) -> None:
    """繪製紅點

    Args:
        surface (pg.Surface): 要繪製的平面
    """
    pg.draw.circle(surface, pg.Color("red"), [633, 523], 3, 3)

def draw_bullet_track(surface: pg.Surface, tracks: list[float, float]) -> None:
    """繪製彈孔道

    Args:
        surface (pg.Surface): 要繪製的平面
        tracks (list[float, float]): 彈孔清單
    """
    for track in tracks:
        pg.draw.circle(surface, (155, 155, 155), pg.Vector2(track), 3, 1)

def draw_arrow(surface: pg.Surface, start: pg.Vector2, end: pg.Vector2, color: pg.Color = pg.Color("dodgerblue"), body_width: int = 2, head_width: int = 4, head_height: int = 2):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pg.Surface): The surface to draw on
        start (pg.Vector2): Start position
        end (pg.Vector2): End position
        color (pg.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pg.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pg.Vector2(0, head_height / 2),  # Center
        pg.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pg.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pg.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pg.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pg.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pg.Vector2(body_width / 2, body_length / 2),  # Topright
            pg.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pg.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pg.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pg.draw.polygon(surface, color, body_verts)

def draw_mouse_pos(screen: pg.Surface, x: int, y: int) -> None:
    """繪製滑鼠目前位置文本

    Args:
        screen (pg.Surface): 要繪製的平面
        x (int): 滑鼠x座標
        y (int): 滑鼠y座標
    """
    text_font = pg.font.SysFont(None, 24)
    mouse_pos_text = text_font.render(f'Mouse X: {x}   Y: {y}', True, (0, 0, 0))
    screen.blit(mouse_pos_text, (10, 710)) # 標靶提示文字

def draw_bar(surface: pg.Surface, progress: float) -> None:
    """繪製讀取條

    Args:
        surface (pg.Surface): 要繪製的平面
        progress (float): 讀取條進度
    """
    pos = (WIDTH/2-200, 660)
    size = (400, 30)
    borderC, barC = (0, 0, 0), (0, 128, 0)
    pg.draw.rect(surface, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    pg.draw.rect(surface, barC, (*innerPos, *innerSize))

class Target(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('./Assets/target.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WIDTH-76)/2, 500)
        text_font = pg.font.SysFont(None, 24)
        self.distance_text = text_font.render('Distance 40m', True, (0, 0, 0))
    
    def draw(self, surface: pg.Surface) -> None:
        """繪製敵人圖示

        Args:
            surface (pg.Surface): 要繪製的平面
        """
        surface.blit(self.image, self.rect) # 標靶圖
        surface.blit(self.distance_text, (WIDTH/2-50, 710)) # 標靶提示文字

class UI():
    def __init__(self, screen: pg.Surface, guns: list[str]):
        super().__init__()
        self.SCREEN = screen
        self.dd_guns = DropDown(screen, 10, 10, 150, 40, pg.font.SysFont(None, 20), "Select Gun", guns)
        self.target = Target()
        self.input_sensitive = InputBox(screen, 100, 610, 50, 36, '2.5')
        text_font = pg.font.SysFont(None, 24)
        self.sensitive_text = text_font.render('Sensitive: ', True, (0, 0, 0))
        
    
    def update_drop_down(self, events: list[pg.event.Event]) -> str:
        """更新下拉選單

        Args:
            events (list[pg.event.Event]): 視窗事件清單

        Returns:
            str: 有更新就回傳選擇的選項反之空字串
        """
        option_index = self.dd_guns.update(events)
        if option_index >= 0:
            if(self.dd_guns.main != self.dd_guns.options[option_index]):
                self.dd_guns.main = self.dd_guns.options[option_index]
                return self.dd_guns.options[option_index]
        return ''

    def draw(self) -> None:
        """繪製UI
        """
        self.SCREEN.fill((255, 255, 255))
        self.dd_guns.draw()
        draw_gamepad(self.SCREEN)
        draw_valid_area(self.SCREEN, WIDTH/2-200, 100, 400, 600)
        self.target.draw(self.SCREEN)
        draw_red_dot(self.SCREEN)
        
        
        self.SCREEN.blit(self.sensitive_text, (10, 620)) # 標靶提示文字
        # 輸入靈敏度
        self.input_sensitive.draw()