#!/usr/bin/env python3
"""
FATE'S GAMBIT - Simulador Estatístico Puro
Demonstra probabilidades com eventos aleatórios COMPLETOS
Você não escolhe qual dado rolar - o sistema escolhe aleatoriamente!
"""

import pygame
import sys
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import random

# Configurações
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
GAME_WIDTH = 700
STATS_WIDTH = 700
FPS = 60

# Cores
COLOR_BG = (15, 5, 30)
COLOR_PANEL = (50, 25, 75)
COLOR_GOLD = (255, 215, 0)
COLOR_RED = (220, 20, 60)
COLOR_GREEN = (50, 205, 50)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (180, 180, 180)
COLOR_BLUE = (100, 149, 237)
COLOR_ORANGE = (255, 140, 0)


class Weapon:
    """Arma com dados"""
    def __init__(self, name, dice_notation, num_dice, sides):
        self.name = name
        self.dice_notation = dice_notation
        self.num_dice = num_dice
        self.sides = sides
        self.min_damage = num_dice
        self.max_damage = num_dice * sides
        self.avg_damage = num_dice * (sides + 1) / 2
        self.variance = num_dice * (sides ** 2 - 1) / 12
        self.std_dev = np.sqrt(self.variance)
    
    def roll(self):
        total = sum(random.randint(1, self.sides) for _ in range(self.num_dice))
        is_max = (total == self.max_damage)
        return total, is_max
    
    def get_theoretical_distribution(self):
        if self.num_dice == 1:
            probs = {i: 1.0 / self.sides for i in range(self.min_damage, self.max_damage + 1)}
        else:
            probs = {}
            for val in range(self.min_damage, self.max_damage + 1):
                z = (val - self.avg_damage) / self.std_dev
                prob = np.exp(-0.5 * z ** 2) / (self.std_dev * np.sqrt(2 * np.pi))
                probs[val] = prob
            total = sum(probs.values())
            probs = {k: v / total for k, v in probs.items()}
        return probs


class Monster:
    """Monstro de dungeon"""
    def __init__(self, name, hp, num_dice, sides, room):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.num_dice = num_dice
        self.sides = sides
        self.room = room
        self.avg_damage = num_dice * (sides + 1) / 2
        self.is_boss = (room == 5)
        self.turn_count = 0
    
    def reset(self):
        self.current_hp = self.max_hp
        self.turn_count = 0
    
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        return self.is_alive()
    
    def is_alive(self):
        return self.current_hp > 0
    
    def attack(self):
        self.turn_count += 1
        if self.is_boss and self.turn_count % 3 == 0:
            damage = sum(random.randint(1, 4) for _ in range(5))
            return damage, True
        damage = sum(random.randint(1, self.sides) for _ in range(self.num_dice))
        return damage, False


# Armas disponíveis
WEAPONS = [
    Weapon("Adaga Rapida", "1d6", 1, 6),
    Weapon("Espada Comum", "2d6", 2, 6),
    Weapon("Martelo Pesado", "3d4", 3, 4),
    Weapon("Arco Longo", "1d12", 1, 12),
    Weapon("Cajado Magico", "4d3", 4, 3),
    Weapon("Critico Lendario", "1d20", 1, 20),
]

# Monstros das dungeons
MONSTERS = [
    Monster("Rato Gigante", 15, 1, 4, 0),
    Monster("Zumbi Podre", 30, 1, 6, 1),
    Monster("Esqueleto Guerreiro", 45, 2, 4, 2),
    Monster("Espectro Sombrio", 60, 1, 10, 3),
    Monster("Lobisomem Feroz", 80, 2, 6, 4),
    Monster("Dragao de Variancia", 150, 3, 6, 5),
]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fate's Gambit - Simulador Estatistico")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 36)
        self.font_huge = pygame.font.Font(None, 80)
        
        self.weapons = WEAPONS
        self.monsters = MONSTERS
        
        # Estado do jogo
        self.player_hp = 100
        self.max_hp = 100
        self.current_room = 0
        self.current_monster = None
        self.turn = 0
        self.game_over = False
        self.victory = False
        
        # Estatísticas
        self.damage_history = []
        self.weapon_usage = defaultdict(list)
        self.critical_hits = 0
        self.total_attacks = 0
        self.last_player_damage = None
        self.last_monster_damage = None
        self.last_weapon_used = None
        
        # Flash de animação
        self.flash_timer = 0
        
        # Inicia primeira dungeon
        self.start_room()
    
    def start_room(self):
        if self.current_room >= len(self.monsters):
            self.victory = True
            return
        self.current_monster = self.monsters[self.current_room]
        self.current_monster.reset()
    
    def attack(self):
        if not self.current_monster or not self.current_monster.is_alive():
            return
        
        # ESCOLHE ARMA ALEATORIAMENTE!
        weapon_idx = random.randint(0, len(self.weapons) - 1)
        weapon = self.weapons[weapon_idx]
        self.last_weapon_used = weapon
        
        # Ataque do jogador
        damage, is_critical = weapon.roll()
        self.current_monster.take_damage(damage)
        
        self.total_attacks += 1
        self.turn += 1
        self.last_player_damage = (damage, is_critical)
        self.flash_timer = 15 if is_critical else 8
        
        # Registra estatísticas
        self.damage_history.append(damage)
        self.weapon_usage[weapon_idx].append(damage)
        if is_critical:
            self.critical_hits += 1
        
        # Verifica se monstro morreu
        if not self.current_monster.is_alive():
            self.current_room += 1
            self.last_monster_damage = None
            if self.current_room < len(self.monsters):
                self.start_room()
            else:
                self.victory = True
            return
        
        # Contra-ataque do monstro
        monster_damage, is_special = self.current_monster.attack()
        self.player_hp -= monster_damage
        self.last_monster_damage = (monster_damage, is_special)
        
        if self.player_hp <= 0:
            self.player_hp = 0
            self.game_over = True
    
    def draw_text(self, text, x, y, color=COLOR_WHITE, font=None):
        if font is None:
            font = self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
    
    def draw_hp_bar(self, x, y, width, height, current, maximum, color):
        pygame.draw.rect(self.screen, COLOR_GRAY, (x, y, width, height))
        fill_width = int((current / maximum) * width)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, height))
        pygame.draw.rect(self.screen, COLOR_WHITE, (x, y, width, height), 2)
    
    def draw_game_panel(self):
        """Desenha painel do jogo (metade esquerda)"""
        # Painel do jogador
        pygame.draw.rect(self.screen, COLOR_PANEL, (20, 20, GAME_WIDTH - 40, 160))
        pygame.draw.rect(self.screen, COLOR_WHITE, (20, 20, GAME_WIDTH - 40, 160), 2)
        
        self.draw_text("AVENTUREIRO", 40, 35, COLOR_GOLD, self.font_large)
        self.draw_text(f"HP: {self.player_hp} / {self.max_hp}", 40, 75, COLOR_WHITE)
        self.draw_hp_bar(40, 105, GAME_WIDTH - 80, 25, self.player_hp, self.max_hp, COLOR_GREEN)
        self.draw_text(f"Turno: {self.turn} | Ataques: {self.total_attacks}", 40, 140, COLOR_GRAY, self.font_small)
        
        # Painel do monstro
        if self.current_monster:
            pygame.draw.rect(self.screen, COLOR_PANEL, (20, 200, GAME_WIDTH - 40, 140))
            pygame.draw.rect(self.screen, COLOR_WHITE, (20, 200, GAME_WIDTH - 40, 140), 2)
            
            boss_tag = " [CHEFE]" if self.current_monster.is_boss else ""
            self.draw_text(f"SALA {self.current_room + 1}/6", 40, 215, COLOR_GOLD, self.font_large)
            self.draw_text(f"{self.current_monster.name}{boss_tag}", 40, 255, COLOR_RED, self.font_large)
            self.draw_text(f"HP: {self.current_monster.current_hp} / {self.current_monster.max_hp}", 
                          40, 290, COLOR_WHITE)
            self.draw_hp_bar(40, 315, GAME_WIDTH - 80, 20, 
                           self.current_monster.current_hp, self.current_monster.max_hp, COLOR_RED)
        
        # PAINEL DE EVENTO ALEATÓRIO (resultado do último ataque)
        pygame.draw.rect(self.screen, COLOR_PANEL, (20, 360, GAME_WIDTH - 40, 240))
        pygame.draw.rect(self.screen, COLOR_WHITE, (20, 360, GAME_WIDTH - 40, 240), 2)
        
        self.draw_text("EVENTO ALEATORIO", 40, 375, COLOR_GOLD, self.font_large)
        
        if self.last_weapon_used and self.last_player_damage:
            damage, is_crit = self.last_player_damage
            
            # Nome da arma escolhida aleatoriamente
            self.draw_text(f"Arma Sorteada:", 40, 420, COLOR_WHITE)
            self.draw_text(f"{self.last_weapon_used.name}", 40, 445, COLOR_BLUE, self.font_large)
            self.draw_text(f"({self.last_weapon_used.dice_notation})", 40, 480, COLOR_GRAY)
            
            # Resultado do dado (GRANDE)
            result_color = COLOR_RED if is_crit and self.flash_timer % 4 < 2 else COLOR_GREEN
            self.draw_text("Dano:", 380, 420, COLOR_WHITE)
            self.draw_text(str(damage), 380, 450, result_color, self.font_huge)
            
            if is_crit:
                self.draw_text("CRITICO!", 360, 540, COLOR_RED, self.font_large)
            
            if self.flash_timer > 0:
                self.flash_timer -= 1
        else:
            self.draw_text("Clique para rolar os dados...", 180, 470, COLOR_GRAY, self.font_large)
        
        # Dano do monstro
        if self.last_monster_damage:
            dmg, is_special = self.last_monster_damage
            special_text = " [SOPRO DE CAOS!]" if is_special else ""
            color = COLOR_ORANGE if is_special else COLOR_RED
            self.draw_text(f"Monstro contra-atacou: -{dmg} HP{special_text}", 
                          40, 570, color, self.font_small)
        
        # BOTÃO GIGANTE: ROLAR DADOS
        button_color = COLOR_GREEN if self.flash_timer == 0 else COLOR_ORANGE
        pygame.draw.rect(self.screen, button_color, (20, SCREEN_HEIGHT - 120, GAME_WIDTH - 40, 100))
        pygame.draw.rect(self.screen, COLOR_WHITE, (20, SCREEN_HEIGHT - 120, GAME_WIDTH - 40, 100), 4)
        self.draw_text("ROLAR DADOS!", 200, SCREEN_HEIGHT - 90, COLOR_WHITE, self.font_huge)
        self.draw_text("(Arma sera escolhida aleatoriamente)", 150, SCREEN_HEIGHT - 40, COLOR_GRAY, self.font_small)
    
    def create_stats_graph(self):
        """Cria gráficos estatísticos"""
        fig = plt.figure(figsize=(7, 8), facecolor='#0f051e')
        
        if self.total_attacks == 0:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Aguardando primeiro ataque...', 
                   ha='center', va='center', color='white', fontsize=16)
            ax.set_facecolor('#32194b')
            ax.axis('off')
        else:
            # Gráfico 1: Distribuição (arma mais usada)
            most_used = max(self.weapon_usage.keys(), key=lambda k: len(self.weapon_usage[k]))
            weapon = self.weapons[most_used]
            damages = self.weapon_usage[most_used]
            
            ax1 = fig.add_subplot(3, 1, 1)
            ax1.set_facecolor('#32194b')
            ax1.set_title(f'Distribuicao: {weapon.name} ({len(damages)} usos)', 
                         color='gold', fontsize=12, fontweight='bold')
            
            bins = range(weapon.min_damage, weapon.max_damage + 2)
            ax1.hist(damages, bins=bins, alpha=0.6, color='cyan', 
                    edgecolor='white', label='Observado', density=True, linewidth=1.5)
            
            theo_probs = weapon.get_theoretical_distribution()
            theo_x = list(theo_probs.keys())
            theo_y = list(theo_probs.values())
            ax1.plot(theo_x, theo_y, 'r-', linewidth=3, label='Teorico', marker='o', markersize=8)
            
            ax1.set_xlabel('Dano', color='white', fontsize=10)
            ax1.set_ylabel('Probabilidade', color='white', fontsize=10)
            ax1.tick_params(colors='white', labelsize=9)
            ax1.legend(facecolor='#32194b', edgecolor='white', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Histórico
            ax2 = fig.add_subplot(3, 1, 2)
            ax2.set_facecolor('#32194b')
            ax2.set_title('Historico de Dano', color='gold', fontsize=12, fontweight='bold')
            
            ax2.plot(range(1, len(self.damage_history) + 1), self.damage_history, 
                    'g-', linewidth=1.5, marker='o', markersize=3, alpha=0.7)
            ax2.axhline(y=np.mean(self.damage_history), color='cyan', linestyle='--', 
                       linewidth=2, label=f'Media: {np.mean(self.damage_history):.2f}')
            ax2.set_xlabel('Ataque #', color='white', fontsize=10)
            ax2.set_ylabel('Dano', color='white', fontsize=10)
            ax2.tick_params(colors='white', labelsize=9)
            ax2.legend(facecolor='#32194b', edgecolor='white', fontsize=9)
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 3: Comparação
            ax3 = fig.add_subplot(3, 1, 3)
            ax3.set_facecolor('#32194b')
            ax3.set_title('Comparacao: Teorico vs Empirico', color='gold', fontsize=12, fontweight='bold')
            
            weapon_names = []
            theo_avgs = []
            obs_avgs = []
            
            for weapon_idx, damages in sorted(self.weapon_usage.items()):
                if len(damages) > 0:
                    weapon_names.append(self.weapons[weapon_idx].dice_notation)
                    theo_avgs.append(self.weapons[weapon_idx].avg_damage)
                    obs_avgs.append(np.mean(damages))
            
            if len(weapon_names) > 0:
                x = np.arange(len(weapon_names))
                width = 0.35
                
                ax3.bar(x - width/2, theo_avgs, width, label='Teorico', color='red', alpha=0.8)
                ax3.bar(x + width/2, obs_avgs, width, label='Observado', color='cyan', alpha=0.8)
                
                ax3.set_xlabel('Arma', color='white', fontsize=10)
                ax3.set_ylabel('Dano Medio', color='white', fontsize=10)
                ax3.set_xticks(x)
                ax3.set_xticklabels(weapon_names, rotation=0, ha='center', color='white', fontsize=9)
                ax3.tick_params(colors='white', labelsize=9)
                ax3.legend(facecolor='#32194b', edgecolor='white', fontsize=10)
                ax3.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(buf, size, "RGBA")
        plt.close(fig)
        
        return surf
    
    def draw_stats_panel(self):
        """Desenha painel de estatísticas (metade direita)"""
        graph_surface = self.create_stats_graph()
        self.screen.blit(graph_surface, (GAME_WIDTH, 0))
    
    def draw_game_over(self):
        """Tela de game over com estatísticas"""
        self.screen.fill(COLOR_BG)
        
        if self.victory:
            self.draw_text("VITORIA!", SCREEN_WIDTH // 2 - 100, 50, COLOR_GOLD, self.font_huge)
            self.draw_text("Voce derrotou o Dragao de Variancia!", 
                         SCREEN_WIDTH // 2 - 280, 140, COLOR_WHITE, self.font_large)
        else:
            self.draw_text("DERROTA!", SCREEN_WIDTH // 2 - 120, 50, COLOR_RED, self.font_huge)
            self.draw_text(f"Voce chegou ate a Sala {self.current_room + 1}/6", 
                         SCREEN_WIDTH // 2 - 200, 140, COLOR_WHITE, self.font_large)
        
        # Painel de estatísticas gerais
        panel_y = 200
        pygame.draw.rect(self.screen, COLOR_PANEL, (50, panel_y, 600, 280))
        pygame.draw.rect(self.screen, COLOR_WHITE, (50, panel_y, 600, 280), 2)
        
        self.draw_text("ESTATISTICAS DA AVENTURA", 70, panel_y + 20, COLOR_GOLD, self.font_large)
        
        y = panel_y + 70
        
        self.draw_text(f"Total de Ataques: {self.total_attacks}", 80, y, COLOR_WHITE)
        y += 30
        
        if self.total_attacks > 0:
            avg_damage = np.mean(self.damage_history)
            self.draw_text(f"Dano Medio Causado: {avg_damage:.2f}", 80, y, COLOR_WHITE)
            y += 30
            
            max_damage = max(self.damage_history)
            min_damage = min(self.damage_history)
            self.draw_text(f"Maior Dano: {max_damage}", 80, y, COLOR_GREEN)
            y += 30
            self.draw_text(f"Menor Dano: {min_damage}", 80, y, COLOR_ORANGE)
            y += 30
            
            crit_rate = (self.critical_hits / self.total_attacks) * 100
            self.draw_text(f"Criticos: {self.critical_hits} ({crit_rate:.1f}%)", 80, y, COLOR_RED)
            y += 30
            
            self.draw_text(f"HP Final: {self.player_hp}/{self.max_hp}", 80, y, COLOR_WHITE)
        
        # Painel de armas sorteadas
        panel2_y = 200
        panel2_x = 670
        pygame.draw.rect(self.screen, COLOR_PANEL, (panel2_x, panel2_y, 680, 280))
        pygame.draw.rect(self.screen, COLOR_WHITE, (panel2_x, panel2_y, 680, 280), 2)
        
        self.draw_text("ARMAS SORTEADAS", panel2_x + 20, panel2_y + 20, COLOR_GOLD, self.font_large)
        
        y = panel2_y + 70
        
        sorted_weapons = sorted(self.weapon_usage.items(), key=lambda x: len(x[1]), reverse=True)
        
        for weapon_idx, damages in sorted_weapons[:5]:
            weapon = self.weapons[weapon_idx]
            uses = len(damages)
            avg = np.mean(damages)
            theo_avg = weapon.avg_damage
            diff = avg - theo_avg
            diff_symbol = "+" if diff > 0 else ""
            
            self.draw_text(f"{weapon.name} ({weapon.dice_notation})", panel2_x + 30, y, COLOR_WHITE)
            y += 25
            self.draw_text(f"  Sorteios: {uses} | Media: {avg:.2f} (esperado: {theo_avg:.1f})", 
                         panel2_x + 30, y, COLOR_GRAY, self.font_small)
            
            diff_color = COLOR_GREEN if diff > 0 else COLOR_ORANGE if diff < 0 else COLOR_WHITE
            self.draw_text(f"  Diferenca: {diff_symbol}{diff:.2f}", 
                         panel2_x + 30, y + 20, diff_color, self.font_small)
            y += 50
        
        # Gráfico final
        graph_surface = self.create_final_stats_graph()
        self.screen.blit(graph_surface, (50, 500))
        
        self.draw_text("Pressione ESC para sair ou R para reiniciar", 
                     SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 40, COLOR_GRAY)
    
    def create_final_stats_graph(self):
        """Cria gráfico de estatísticas finais"""
        fig = plt.figure(figsize=(13, 2.8), facecolor='#0f051e')
        
        if self.total_attacks == 0:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Nenhum ataque realizado', 
                   ha='center', va='center', color='white', fontsize=14)
            ax.set_facecolor('#32194b')
            ax.axis('off')
        else:
            most_used = max(self.weapon_usage.keys(), key=lambda k: len(self.weapon_usage[k]))
            weapon = self.weapons[most_used]
            damages = self.weapon_usage[most_used]
            
            ax1 = fig.add_subplot(1, 3, 1)
            ax1.set_facecolor('#32194b')
            ax1.set_title(f'{weapon.name}\nTeorico vs Observado', 
                         color='gold', fontsize=11, fontweight='bold')
            
            bins = range(weapon.min_damage, weapon.max_damage + 2)
            ax1.hist(damages, bins=bins, alpha=0.6, color='cyan', 
                    edgecolor='white', label='Observado', density=True, linewidth=1.5)
            
            theo_probs = weapon.get_theoretical_distribution()
            theo_x = list(theo_probs.keys())
            theo_y = list(theo_probs.values())
            ax1.plot(theo_x, theo_y, 'r-', linewidth=3, label='Teorico', marker='o', markersize=6)
            
            ax1.set_xlabel('Dano', color='white', fontsize=9)
            ax1.set_ylabel('Probabilidade', color='white', fontsize=9)
            ax1.tick_params(colors='white', labelsize=8)
            ax1.legend(facecolor='#32194b', edgecolor='white', fontsize=8)
            ax1.grid(True, alpha=0.3)
            
            ax2 = fig.add_subplot(1, 3, 2)
            ax2.set_facecolor('#32194b')
            ax2.set_title('Todas as Armas\nMedia: Teorico vs Empirico', 
                         color='gold', fontsize=11, fontweight='bold')
            
            weapon_names = []
            theo_avgs = []
            obs_avgs = []
            
            for weapon_idx, damages in sorted(self.weapon_usage.items()):
                if len(damages) > 0:
                    weapon_names.append(self.weapons[weapon_idx].dice_notation)
                    theo_avgs.append(self.weapons[weapon_idx].avg_damage)
                    obs_avgs.append(np.mean(damages))
            
            x = np.arange(len(weapon_names))
            width = 0.35
            
            ax2.bar(x - width/2, theo_avgs, width, label='Teorico', color='red', alpha=0.8)
            ax2.bar(x + width/2, obs_avgs, width, label='Observado', color='cyan', alpha=0.8)
            
            ax2.set_xlabel('Arma', color='white', fontsize=9)
            ax2.set_ylabel('Dano Medio', color='white', fontsize=9)
            ax2.set_xticks(x)
            ax2.set_xticklabels(weapon_names, rotation=45, ha='right', color='white', fontsize=8)
            ax2.tick_params(colors='white', labelsize=8)
            ax2.legend(facecolor='#32194b', edgecolor='white', fontsize=8)
            ax2.grid(True, alpha=0.3, axis='y')
            
            ax3 = fig.add_subplot(1, 3, 3)
            ax3.set_facecolor('#32194b')
            ax3.set_title('Convergencia da Media\n(Lei dos Grandes Numeros)', 
                         color='gold', fontsize=11, fontweight='bold')
            
            cumulative_avg = []
            for i in range(1, len(self.damage_history) + 1):
                cumulative_avg.append(np.mean(self.damage_history[:i]))
            
            ax3.plot(range(1, len(cumulative_avg) + 1), cumulative_avg, 
                    'g-', linewidth=2, label='Media Acumulada')
            
            total_theo = sum(self.weapons[idx].avg_damage * len(dmgs) 
                           for idx, dmgs in self.weapon_usage.items())
            expected_avg = total_theo / self.total_attacks
            ax3.axhline(y=expected_avg, color='red', linestyle='--', 
                       linewidth=2, label=f'Esperado: {expected_avg:.2f}')
            
            ax3.set_xlabel('Numero de Ataques', color='white', fontsize=9)
            ax3.set_ylabel('Dano Medio', color='white', fontsize=9)
            ax3.tick_params(colors='white', labelsize=8)
            ax3.legend(facecolor='#32194b', edgecolor='white', fontsize=8)
            ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(buf, size, "RGBA")
        plt.close(fig)
        
        return surf
    
    def handle_events(self):
        """Processa eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.game_over or self.victory:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_r:
                        self.__init__()
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Clique no botão ROLAR DADOS
                if (20 <= mouse_x <= GAME_WIDTH - 20 and 
                    SCREEN_HEIGHT - 120 <= mouse_y <= SCREEN_HEIGHT - 20):
                    if self.current_monster and self.current_monster.is_alive():
                        self.attack()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.current_monster and self.current_monster.is_alive():
                        self.attack()
        
        return True
    
    def run(self):
        """Loop principal"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            
            self.screen.fill(COLOR_BG)
            
            if self.game_over or self.victory:
                self.draw_game_over()
            else:
                self.draw_game_panel()
                self.draw_stats_panel()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("=" * 60)
    print("FATE'S GAMBIT - Simulador Estatistico")
    print("=" * 60)
    print("A ARMA E ESCOLHIDA ALEATORIAMENTE A CADA ATAQUE!")
    print("Voce apenas rola os dados - o sistema escolhe qual dado usar.")
    print("=" * 60)
    print("Controles:")
    print("  CLIQUE ou ESPACO: Rolar dados (arma aleatoria)")
    print("  ESC: Sair (na tela final)")
    print("  R: Reiniciar (na tela final)")
    print("=" * 60)
    print("\nObserve os graficos em tempo real na metade direita!\n")
    
    game = Game()
    game.run()