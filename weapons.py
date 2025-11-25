"""
Sistema de Armas - Fate's Gambit
Define as armas disponíveis e suas características estatísticas
"""

import random
import numpy as np


class Weapon:
    """Representa uma arma no jogo"""
    
    def __init__(self, name, dice_notation, num_dice, sides):
        self.name = name
        self.dice_notation = dice_notation
        self.num_dice = num_dice
        self.sides = sides
        
        # Calcula estatísticas teóricas
        self.min_damage = num_dice
        self.max_damage = num_dice * sides
        self.avg_damage = num_dice * (sides + 1) / 2
        self.variance = num_dice * (sides ** 2 - 1) / 12
        self.std_dev = np.sqrt(self.variance)
        
        # Probabilidade de crítico (tirar máximo)
        if num_dice == 1:
            self.critical_prob = 1.0 / sides
        else:
            self.critical_prob = (1.0 / sides) ** num_dice
    
    def roll(self):
        """Rola os dados e retorna o dano"""
        total = sum(random.randint(1, self.sides) for _ in range(self.num_dice))
        is_critical = (total == self.max_damage)
        return total, is_critical
    
    def get_theoretical_distribution(self):
        """Retorna a distribuição teórica de probabilidades"""
        if self.num_dice == 1:
            # Distribuição uniforme
            probs = {i: 1.0 / self.sides for i in range(self.min_damage, self.max_damage + 1)}
        else:
            # Aproximação usando distribuição normal
            probs = {}
            for val in range(self.min_damage, self.max_damage + 1):
                # Probabilidade usando PDF da normal
                z = (val - self.avg_damage) / self.std_dev
                prob = np.exp(-0.5 * z ** 2) / (self.std_dev * np.sqrt(2 * np.pi))
                probs[val] = prob
            
            # Normalizar
            total = sum(probs.values())
            probs = {k: v / total for k, v in probs.items()}
        
        return probs
    
    def get_info(self):
        """Retorna informações formatadas da arma"""
        return {
            "name": self.name,
            "dice": self.dice_notation,
            "avg": self.avg_damage,
            "min": self.min_damage,
            "max": self.max_damage,
            "std": self.std_dev,
            "crit_prob": self.critical_prob * 100
        }
    
    def __str__(self):
        return f"{self.name} ({self.dice_notation}) - Avg: {self.avg_damage:.1f}"


# ==================== ARSENAL DE ARMAS ====================

WEAPONS = [
    Weapon(
        name="Adaga Rapida",
        dice_notation="1d6",
        num_dice=1,
        sides=6
    ),
    Weapon(
        name="Espada Comum",
        dice_notation="2d6",
        num_dice=2,
        sides=6
    ),
    Weapon(
        name="Martelo Pesado",
        dice_notation="3d4",
        num_dice=3,
        sides=4
    ),
    Weapon(
        name="Arco Longo",
        dice_notation="1d12",
        num_dice=1,
        sides=12
    ),
    Weapon(
        name="Cajado Magico",
        dice_notation="4d3",
        num_dice=4,
        sides=3
    ),
    Weapon(
        name="Critico Lendario",
        dice_notation="1d20",
        num_dice=1,
        sides=20
    ),
    Weapon(
        name="d100 do Caos",
        dice_notation="1d100",
        num_dice=1,
        sides=100
    ),
]


def get_weapon(index):
    """Retorna uma arma pelo índice"""
    if 0 <= index < len(WEAPONS):
        return WEAPONS[index]
    return None


def get_all_weapons():
    """Retorna lista de todas as armas"""
    return WEAPONS


def compare_weapons():
    """Compara estatísticas de todas as armas"""
    print("=" * 70)
    print("COMPARACAO DE ARMAS")
    print("=" * 70)
    print(f"{'Arma':<20} {'Dados':<8} {'Min':<5} {'Avg':<6} {'Max':<5} {'Std':<6} {'Crit%':<6}")
    print("-" * 70)
    
    for weapon in WEAPONS:
        info = weapon.get_info()
        print(f"{info['name']:<20} {info['dice']:<8} "
              f"{info['min']:<5} {info['avg']:<6.2f} {info['max']:<5} "
              f"{info['std']:<6.2f} {info['crit_prob']:<6.2f}")
    
    print("=" * 70)


if __name__ == "__main__":
    # Teste do módulo
    print("🗡️  TESTANDO MÓDULO DE ARMAS\n")
    
    compare_weapons()
    
    print("\n📊 TESTANDO ROLAGEM:")
    weapon = WEAPONS[1]  # Espada Comum
    print(f"\nArma: {weapon}")
    print("\n10 rolagens:")
    for i in range(10):
        damage, is_crit = weapon.roll()
        crit_text = " [CRÍTICO!]" if is_crit else ""
        print(f"  Ataque {i+1}: {damage} de dano{crit_text}")
    
    print("\n✅ Módulo funcionando corretamente!")