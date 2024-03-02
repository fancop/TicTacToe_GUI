import pygame
import sys


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 50
NUM_CELLS = 9
WINNING_COMBINATIONS = [
    # Горизонтальные линии
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    # Вертикальные линии
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    # Диагональные линии
    [0, 4, 8], [2, 4, 6]
]


class Field:
    ''' Класс, представляющий игровое поле. '''

    def __init__(self, screen):
        ''' Инициализация поля. '''

        self.screen = screen
        self.cells = [''] * NUM_CELLS

    def render(self, offset_x, offset_y):
        ''' Отображение игрового поля на экране. '''

        for i in range(NUM_CELLS):
            cell_x = (i % 3) * CELL_SIZE
            cell_y = (i // 3) * CELL_SIZE

            cell_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            cell_surface.fill((255, 255, 255))
            pygame.draw.rect(cell_surface, (0, 255, 0), cell_surface.get_rect(), 2)

            cell_rect = cell_surface.get_rect(
                topleft=(offset_x + cell_x, offset_y + cell_y)
            )

            self.screen.blit(cell_surface, cell_rect.topleft)

            font = pygame.font.Font(None, 36)
            text = font.render(self.cells[i], True, (0, 0, 255) if self.cells[i] == 'O' else (255, 0, 0))
            text_rect = text.get_rect(center=cell_rect.center)
            self.screen.blit(text, text_rect)

    def check_winner(self):
        ''' Проверка наличия выигрышной комбинации на поле. '''

        for combination in WINNING_COMBINATIONS:
            if self.cells[combination[0]] == self.cells[combination[1]] == self.cells[combination[2]] != '':
                return self.cells[combination[0]]
        return None


class Player:
    ''' Класс, представляющий игрока. '''

    def __init__(self):
        ''' Инициализация игрока. '''

        self.current_player = 1

    def switch_player(self):
        ''' Смена текущего игрока. '''

        self.current_player = 2 if self.current_player == 1 else 1


class Window:
    ''' Класс, представляющий игровое окно. '''

    def __init__(self):
        ''' Инициализация игрового окна. '''

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.field = Field(self.screen)
        self.player = Player()
        self.winner = None
        self.tie = False

    def run(self):
        ''' Запуск игры. '''

        while self.is_running:
            self.update()
            self.render()

    def update(self):
        ''' Обновление состояния игры. '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.winner is not None or self.tie:
                    self.handle_end_game_click()
                else:
                    self.handle_click()

    def handle_click(self):
        ''' Обработка нажатия кнопки мыши. '''

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell_x = (mouse_x - (self.screen.get_width() - 3 * CELL_SIZE) // 2) // CELL_SIZE
        cell_y = (mouse_y - (self.screen.get_height() - 3 * CELL_SIZE) // 2) // CELL_SIZE
        index = cell_x + cell_y * 3
        if 0 <= index < NUM_CELLS:
            if self.field.cells[index] == '':
                self.field.cells[index] = 'X' if self.player.current_player == 1 else 'O'
                self.player.switch_player()
                self.winner = self.field.check_winner()
                if all(cell != '' for cell in self.field.cells) and not self.winner:
                    self.tie = True

    def handle_end_game_click(self):
        ''' Обработка нажатия кнопок в конце игры. '''

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.screen.get_width() // 2 - 100 < mouse_x < self.screen.get_width() // 2 - 20 and
            self.screen.get_height() // 2 + 50 < mouse_y < self.screen.get_height() // 2 + 90):
            self.restart_game()
        elif (self.screen.get_width() // 2 + 20 < mouse_x < self.screen.get_width() // 2 + 100 and
              self.screen.get_height() // 2 + 50 < mouse_y < self.screen.get_height() // 2 + 90):
            self.quit_game()

    def render(self):
        ''' Отображение игры на экране. '''

        self.screen.fill((255, 255, 255))
        offset_x = (self.screen.get_width() - 3 * CELL_SIZE) // 2
        offset_y = (self.screen.get_height() - 3 * CELL_SIZE) // 2

        if self.winner:
            font = pygame.font.Font(None, 48)
            text = font.render(f'Игрок {self.winner} победил!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)
            self.render_end_game_buttons()
        elif self.tie:
            font = pygame.font.Font(None, 48)
            text = font.render('Ничья!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)
            self.render_end_game_buttons()
        else:
            font = pygame.font.Font(None, 36)
            current_player_text = 'Ходит игрок X' if self.player.current_player == 1 else 'Ходит игрок O'
            text = font.render(current_player_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, offset_y - 50))
            self.screen.blit(text, text_rect)
            self.field.render(offset_x, offset_y)

        pygame.display.flip()

    def render_end_game_buttons(self):
        ''' Отображение кнопок в конце игры. '''

        font = pygame.font.Font(None, 36)
        text_question = font.render('Хотите сыграть ещё?', True, (0, 0, 0))
        text_yes = font.render('Да', True, (0, 0, 0))
        text_no = font.render('Нет', True, (0, 0, 0))

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        text_rect_question = text_question.get_rect(center=(
            screen_width // 2, screen_height // 2 - 50))
        text_rect_yes = text_yes.get_rect(center=(
            screen_width // 2 - 100, screen_height // 2 + 70))
        text_rect_no = text_no.get_rect(center=(
            screen_width // 2 + 100, screen_height // 2 + 70))

        rect_offset = 10
        rect_question = (text_rect_question.left - rect_offset,
                        text_rect_question.top - rect_offset,
                        text_rect_question.width + 2 * rect_offset,
                        text_rect_question.height + 2 * rect_offset)
        rect_yes = (text_rect_yes.left - rect_offset,
                    text_rect_yes.top - rect_offset,
                    text_rect_yes.width + 2 * rect_offset,
                    text_rect_yes.height + 2 * rect_offset)
        rect_no = (text_rect_no.left - rect_offset,
                text_rect_no.top - rect_offset,
                text_rect_no.width + 2 * rect_offset,
                text_rect_no.height + 2 * rect_offset)

        pygame.draw.rect(self.screen, (255, 255, 0), rect_question)
        pygame.draw.rect(self.screen, (0, 255, 0), rect_yes)
        pygame.draw.rect(self.screen, (255, 0, 0), rect_no)

        self.screen.blit(text_question, text_rect_question)
        self.screen.blit(text_yes, text_rect_yes)
        self.screen.blit(text_no, text_rect_no)

    def restart_game(self):
        ''' Перезапуск игры. '''

        self.field.cells = [''] * NUM_CELLS
        self.player.current_player = 1
        self.winner = None
        self.tie = False

    def quit_game(self):
        ''' Выход из игры. '''

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Window()
    game.run()