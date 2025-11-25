import random


class Monster:
    """Representa um monstro no jogo"""
    
    def __init__(self, name, hp, num_dice, sides, room, is_boss=False, description=""):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.num_dice = num_dice
        self.sides = sides
        self.room = room
        self.is_boss = is_boss
        self.description = description
        
        self.avg_damage = num_dice * (sides + 1) / 2
        self.min_damage = num_dice
        self.max_damage = num_dice * sides
        
        self.turn_count = 0
    
    def reset(self):
        """Reseta o HP do monstro"""
        self.current_hp = self.max_hp
        self.turn_count = 0
    
    def take_damage(self, damage):
        """Aplica dano ao monstro"""
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        return self.is_alive()
    
    def is_alive(self):
        """Verifica se o monstro está vivo"""
        return self.current_hp > 0
    
    def attack(self):
        """Monstro ataca e retorna dano"""
        self.turn_count += 1
        
        if self.is_boss and self.turn_count % 3 == 0:
            return self.special_attack()
        
        damage = sum(random.randint(1, self.sides) for _ in range(self.num_dice))
        return damage, False
    
    def special_attack(self):
        """Ataque especial do chefe (Sopro de Caos)"""
        damage = sum(random.randint(1, 4) for _ in range(5))
        return damage, True  # True indica ataque especial
    
    def get_hp_percentage(self):
        """Retorna porcentagem de HP"""
        return (self.current_hp / self.max_hp) * 100
    
    def get_info(self):
        """Retorna informações do monstro"""
        return {
            "name": self.name,
            "hp": self.current_hp,
            "max_hp": self.max_hp,
            "hp_percent": self.get_hp_percentage(),
            "room": self.room,
            "is_boss": self.is_boss,
            "avg_damage": self.avg_damage,
            "description": self.description
        }
    
    def __str__(self):
        status = "MORTO" if not self.is_alive() else f"HP: {self.current_hp}/{self.max_hp}"
        boss_text = " [CHEFE]" if self.is_boss else ""
        return f"{self.name}{boss_text} - {status}"



MONSTERS = [
    Monster(
        name="Rato Gigante",
        hp=15,
        num_dice=1,
        sides=4,
        room=1,
        description="Um rato do tamanho de um cachorro. Facil, mas cuidado!"
    ),
    Monster(
        name="Zumbi Podre",
        hp=30,
        num_dice=1,
        sides=6,
        room=2,
        description="Lento mas resistente. Escolha sua arma com sabedoria."
    ),
    Monster(
        name="Esqueleto Guerreiro",
        hp=45,
        num_dice=2,
        sides=4,
        room=3,
        description="Armadura ossea. Ataques consistentes sao eficazes."
    ),
    Monster(
        name="Espectro Sombrio",
        hp=60,
        num_dice=1,
        sides=10,
        room=4,
        description="Imprevisivel e perigoso. A probabilidade esta contra voce."
    ),
    Monster(
        name="Lobisomem Feroz",
        hp=80,
        num_dice=2,
        sides=6,
        room=5,
        description="Rapido e agressivo. Prepare-se para o chefe!"
    ),
    Monster(
        name="Dragao de Variancia",
        hp=150,
        num_dice=3,
        sides=6,
        room=6,
        is_boss=True,
        description="O guardiao final. Usa Sopro de Caos a cada 3 turnos!"
    ),
]


def get_monster(room):
    """Retorna um monstro pela sala (0-indexed)"""
    if 0 <= room < len(MONSTERS):
        return MONSTERS[room]
    return None


def get_all_monsters():
    """Retorna lista de todos os monstros"""
    return MONSTERS


def get_total_rooms():
    """Retorna número total de salas"""
    return len(MONSTERS)


def monster_info_table():
    """Imprime tabela de informações dos monstros"""
    print("=" * 80)
    print("BESTIÁRIO - MASMORRAS DA PROBABILIDADE")
    print("=" * 80)
    print(f"{'Sala':<6} {'Monstro':<25} {'HP':<8} {'Dano':<12} {'Avg':<6} {'Tipo':<10}")
    print("-" * 80)
    
    for i, monster in enumerate(MONSTERS):
        tipo = "CHEFE" if monster.is_boss else "Normal"
        dano_info = f"{monster.num_dice}d{monster.sides}"
        print(f"{i+1:<6} {monster.name:<25} {monster.max_hp:<8} "
              f"{dano_info:<12} {monster.avg_damage:<6.1f} {tipo:<10}")
    
    print("=" * 80)
    print(f"\nTotal de Salas: {len(MONSTERS)}")
    print(f"HP Total dos Monstros: {sum(m.max_hp for m in MONSTERS)}")


if __name__ == "__main__":
    print("👹 TESTANDO MÓDULO DE MONSTROS\n")
    
    monster_info_table()
    
    print("\n⚔️  SIMULANDO COMBATE:\n")
    
    monster = get_monster(0)
    print(f"Lutando contra: {monster.name}")
    print(f"HP inicial: {monster.current_hp}/{monster.max_hp}\n")
    
    print("Jogador ataca:")
    for i in range(3):
        dano = random.randint(3, 8)
        still_alive = monster.take_damage(dano)
        print(f"  Ataque {i+1}: {dano} de dano - {monster}")
        if not still_alive:
            print("  💀 Monstro derrotado!")
            break
    
    if monster.is_alive():
        print(f"\nMonstro contra-ataca:")
        for i in range(2):
            dano, is_special = monster.attack()
            special_text = " [ESPECIAL!]" if is_special else ""
            print(f"  Ataque {i+1}: {dano} de dano{special_text}")
    
    print("\n✅ Módulo funcionando corretamente!")