import random
import time
import os
import json
from datetime import datetime

# НАСТРОЙКИ
TICK_TIME = 0.8
INITIAL_HEALTH = 3
MAX_HEALTH = 5  # Максимум жизней
INITIAL_WATER_TANKS = 5
POINTS_PER_TREE_SAVED = 10
PENALTY_PER_BURNED = -5
HOSPITAL_COST = 15
UPGRADE_COST = 25

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
width, height = 10, 10
trees = []
rivers = []
fires = []
clouds = []
helicopter = {'x': 0, 'y': 0, 'water': 0, 'health': INITIAL_HEALTH, 'points': 0, 'tanks': INITIAL_WATER_TANKS}
weather = 'sunny'
game_over = False
tick_count = 0
was_on_fire = False

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_inside(x, y):
    return 0 <= x < width and 0 <= y < height

# ГЕНЕРАЦИЯ МИРА
def generate_rivers(count=3):
    rivers.clear()
    for _ in range(count):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        rivers.append((x, y))

def generate_trees(count=25):
    trees.clear()
    while len(trees) < count:
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        if (x, y) not in rivers and (x, y) not in trees:
            trees.append((x, y))

def generate_random_fire():
    if trees:
        idx = random.randint(0, len(trees)-1)
        if trees[idx] not in fires:
            fires.append(trees[idx])
            return True
    return False

def generate_clouds():
    global clouds
    clouds.clear()
    for _ in range(random.randint(3, 7)):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        clouds.append((x, y))

def init_game():
    global trees, rivers, fires, helicopter, weather, game_over, tick_count, clouds, was_on_fire
    generate_rivers()
    generate_trees()
    fires.clear()
    helicopter = {'x': width//2, 'y': height//2, 'water': 0, 'health': INITIAL_HEALTH, 
                  'points': 0, 'tanks': INITIAL_WATER_TANKS}
    weather = 'sunny'
    game_over = False
    tick_count = 0
    was_on_fire = False
    generate_clouds()
    for _ in range(3):
        generate_random_fire()

# ЦИКЛ ОТРИСОВКИ
def draw_game():
    clear_screen()
    print(f"🌟 ОЧКИ: {helicopter['points']}  ❤️ ЗДОРОВЬЕ: {helicopter['health']}/{MAX_HEALTH}  💧 ВОДА: {helicopter['water']}/{helicopter['tanks']}  ☁️ ПОГОДА: {weather.upper()}")
    print(f"📍 ПОЗИЦИЯ: ({helicopter['x']},{helicopter['y']})  🌲 ДЕРЕВЬЕВ: {len(trees)}  🔥 ПОЖАРОВ: {len(fires)}  🌀 ХОД: {tick_count}")
    print("=" * (width * 2 + 2))
    
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) == (helicopter['x'], helicopter['y']):
                line += "🚁 "
            elif (x, y) in fires:
                line += "🔥 "
            elif (x, y) in trees:
                line += "🌲 "
            elif (x, y) in rivers:
                line += "💧 "
            elif weather == 'rain' and (x, y) in clouds:
                line += "☁️ "
            elif weather == 'thunderstorm' and (x, y) in clouds:
                line += "⛈️ "
            else:
                line += "⬜ "
        print(line)
    print("=" * (width * 2 + 2))
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ W/A/S/D - движение │ E - тушить │ R - вода │ H - госпиталь │")
    print("│ U - магазин (улучшение бака) │ F5 - сохранить │ F6 - загрузить │ Q - выход │")
    print("└─────────────────────────────────────────────────────────────────┘")

# ==================== ПОГОДА ====================
def update_weather():
    global weather, clouds
    r = random.random()
    if r < 0.1:
        weather = 'thunderstorm'
        generate_clouds()
    elif r < 0.3:
        weather = 'rain'
        generate_clouds()
    else:
        weather = 'sunny'
        clouds.clear()

def apply_weather_effects():
    global helicopter
    if weather == 'rain':
        for fire in fires[:]:
            if random.random() < 0.3:
                fires.remove(fire)
                helicopter['points'] += POINTS_PER_TREE_SAVED // 2
                print("🌧️ Дождь потушил пожар! +5 очков")
                time.sleep(0.3)
    elif weather == 'thunderstorm':
        if random.random() < 0.15:
            helicopter['health'] -= 1
            print("⚡⚡⚡ МОЛНИЯ УДАРИЛА В ВЕРТОЛЁТ! -1 ЗДОРОВЬЕ ⚡⚡⚡")
            time.sleep(0.5)

# ==================== МЕХАНИКА ПОЖАРОВ ====================
def spread_fire():
    global fires
    new_fires = []
    
    for fx, fy in fires:
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = fx + dx, fy + dy
            if is_inside(nx, ny) and (nx, ny) in trees and (nx, ny) not in fires and (nx, ny) not in new_fires:
                new_fires.append((nx, ny))
                print(f"  🔥 Огонь перекинулся на ({nx},{ny})!")
                time.sleep(0.2)
    
    for fire in new_fires:
        if fire not in fires:
            fires.append(fire)
    
    return len(new_fires)

def burn_trees():
    global helicopter, trees, fires
    burned = 0
    
    for fire in fires[:]:
        if fire in trees:
            trees.remove(fire)
            helicopter['points'] += PENALTY_PER_BURNED
            burned += 1
            print(f"  💀 Дерево {fire} сгорело! {PENALTY_PER_BURNED} очков")
            time.sleep(0.3)
    
    return burned

def check_fire_damage():
    global was_on_fire, helicopter
    
    current_pos = (helicopter['x'], helicopter['y'])
    is_on_fire_now = current_pos in fires
    
    if was_on_fire and not is_on_fire_now:
        helicopter['health'] -= 1
        print(f"💔 ВЫ УШЛИ С ПОЖАРА НЕ ПОТУШИВ ЕГО! -1 ЗДОРОВЬЕ (осталось {helicopter['health']}) 💔")
        time.sleep(0.5)
        was_on_fire = False
        return True
    
    was_on_fire = is_on_fire_now
    return False

# ==================== ВЕРТОЛЁТ ====================
def take_water():
    pos = (helicopter['x'], helicopter['y'])
    if pos in rivers:
        helicopter['water'] = helicopter['tanks']
        print(f"💧💧💧 ВОДА ЗАЛИТА! Теперь {helicopter['water']}/{helicopter['tanks']} 💧💧💧")
    else:
        print("❌ Здесь нет воды! Найдите реку (💧)")

def extinguish():
    global was_on_fire
    pos = (helicopter['x'], helicopter['y'])
    
    if pos in fires and helicopter['water'] > 0:
        fires.remove(pos)
        helicopter['water'] -= 1
        helicopter['points'] += POINTS_PER_TREE_SAVED
        was_on_fire = False
        print(f"✅✅✅ ПОЖАР ПОТУШЕН! +{POINTS_PER_TREE_SAVED} ОЧКОВ! ✅✅✅")
        return True
    elif pos in fires and helicopter['water'] == 0:
        print("❌ Нет воды! Заберите воду из реки (R)")
    else:
        print("❌ Здесь нет пожара!")
    return False

def hospital():
    """Госпиталь - лечение за очки"""
    if helicopter['health'] >= MAX_HEALTH:
        print(f"❌ У вас уже максимальное здоровье! ({helicopter['health']}/{MAX_HEALTH})")
        return
    
    if helicopter['points'] >= HOSPITAL_COST:
        helicopter['points'] -= HOSPITAL_COST
        helicopter['health'] += 1
        print(f"🏥🏥🏥 ВЫЛЕЧИЛИСЬ! +1 ЗДОРОВЬЕ (теперь {helicopter['health']}/{MAX_HEALTH}) 🏥🏥🏥")
        print(f"💰 Осталось очков: {helicopter['points']}")
    else:
        print(f"❌ Не хватает очков! Нужно {HOSPITAL_COST}, у вас {helicopter['points']}")
        print(f"   Нужно потушить {HOSPITAL_COST // POINTS_PER_TREE_SAVED + 1} пожар(ов)")

def shop():
    if helicopter['points'] >= UPGRADE_COST:
        helicopter['points'] -= UPGRADE_COST
        helicopter['tanks'] += 1
        print(f"🛒🛒🛒 РЕЗЕРВУАР УВЕЛИЧЕН! Теперь {helicopter['tanks']} 💧 🛒🛒🛒")
        print(f"💰 Осталось очков: {helicopter['points']}")
    else:
        print(f"❌ Не хватает очков! Нужно {UPGRADE_COST}, у вас {helicopter['points']}")

# СОХРАНЕНИЕ / ЗАГРУЗКА
def save_game():
    data = {
        'width': width, 'height': height,
        'trees': trees, 'rivers': rivers, 'fires': fires,
        'helicopter': helicopter, 'weather': weather,
        'tick_count': tick_count,
        'was_on_fire': was_on_fire,
        'timestamp': str(datetime.now())
    }
    try:
        with open('savegame.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾💾💾 ИГРА СОХРАНЕНА! 💾💾💾")
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

def load_game():
    global width, height, trees, rivers, fires, helicopter, weather, tick_count, was_on_fire
    try:
        with open('savegame.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        width, height = data['width'], data['height']
        trees = [tuple(t) for t in data['trees']]
        rivers = [tuple(r) for r in data['rivers']]
        fires = [tuple(f) for f in data['fires']]
        helicopter = data['helicopter']
        weather = data['weather']
        tick_count = data.get('tick_count', 0)
        was_on_fire = data.get('was_on_fire', False)
        print("📀📀📀 ИГРА ЗАГРУЖЕНА! 📀📀📀")
        print(f"❤️ Здоровье: {helicopter['health']}/{MAX_HEALTH}")
        print(f"💧 Вода: {helicopter['water']}/{helicopter['tanks']}")
        time.sleep(1)
    except FileNotFoundError:
        print("❌ Нет сохранённой игры!")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")

# ТИК ИГРЫ
def tick():
    global game_over, tick_count
    tick_count += 1
    
    print("\n" + "="*45)
    print(f"🔄 ХОД ИГРЫ #{tick_count} 🔄")
    print("="*45)
    
    check_fire_damage()
    new_fires = spread_fire()
    burned = burn_trees()
    apply_weather_effects()
    update_weather()
    
    if random.random() < 0.15 and len(trees) > 0:
        if generate_random_fire():
            print("  🔥🔥🔥 НОВЫЙ СЛУЧАЙНЫЙ ПОЖАР! 🔥🔥🔥")
    
    print(f"\n📊 ИТОГ ТИКА: +{new_fires} пожаров, сгорело {burned} деревьев")
    print(f"🌲 Деревьев: {len(trees)} | 🔥 Пожаров: {len(fires)} | ❤️ Здоровье: {helicopter['health']}/{MAX_HEALTH}")
    print("="*45)
    
    if helicopter['health'] <= 0:
        game_over = True
        print("\n" + "="*50)
        print("💀💀💀 ИГРА ОКОНЧЕНА! ВЕРТОЛЁТ РАЗБИЛСЯ 💀💀💀")
        print("="*50)
        print(f"💰 ФИНАЛЬНЫЙ СЧЁТ: {helicopter['points']} ОЧКОВ")

# ГЛАВНЫЙ ЦИКЛ
def main():
    global game_over, width, height
    
    print("="*55)
    print("     🚁 ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ЛЕСНОЙ ПАТРУЛЬ' 🚁")
    print("="*55)
    
    size = input("🎮 Выберите размер поля (5-20, Enter=10): ")
    if size.isdigit() and 5 <= int(size) <= 20:
        width = height = int(size)
    
    init_game()
    print("\n🎬 ИГРА НАЧАЛАСЬ! 🚁")
    print("⚠️ ПРАВИЛО: Если встали на пожар и НЕ потушили - при уходе потеряете жизнь!")
    print("✅ Если потушили - жизни НЕ теряете!")
    print(f"💧 Начальный резервуар: {helicopter['tanks']}")
    print(f"🏥 Госпиталь (H): +1 жизнь за {HOSPITAL_COST} очков (максимум {MAX_HEALTH} жизней)")
    print(f"🛒 Магазин (U): +1 к баку за {UPGRADE_COST} очков")
    time.sleep(3)
    
    while not game_over:
        draw_game()
        action = input("\n👉 ВАШ ХОД: ").lower().strip()
        
        if action == 'w':
            if is_inside(helicopter['x'], helicopter['y'] - 1):
                helicopter['y'] -= 1
                print(f"⬆️ Вверх → ({helicopter['x']},{helicopter['y']})")
            else:
                print(f"❌ НЕЛЬЗЯ! Вы у ВЕРХНЕЙ границы!")
                
        elif action == 's':
            if is_inside(helicopter['x'], helicopter['y'] + 1):
                helicopter['y'] += 1
                print(f"⬇️ Вниз → ({helicopter['x']},{helicopter['y']})")
            else:
                print(f"❌ НЕЛЬЗЯ! Вы у НИЖНЕЙ границы!")
                
        elif action == 'a':
            if is_inside(helicopter['x'] - 1, helicopter['y']):
                helicopter['x'] -= 1
                print(f"⬅️ Влево → ({helicopter['x']},{helicopter['y']})")
            else:
                print(f"❌ НЕЛЬЗЯ! Вы у ЛЕВОЙ границы!")
                
        elif action == 'd':
            if is_inside(helicopter['x'] + 1, helicopter['y']):
                helicopter['x'] += 1
                print(f"➡️ Вправо → ({helicopter['x']},{helicopter['y']})")
            else:
                print(f"❌ НЕЛЬЗЯ! Вы у ПРАВОЙ границы!")
        
        elif action == 'e':
            extinguish()
        elif action == 'r':
            take_water()
        elif action == 'h':
            hospital()
        elif action == 'u':
            shop()
        elif action == 'f5':
            save_game()
        elif action == 'f6':
            load_game()
        elif action == 'q':
            print("\n👋 Выход из игры... До свидания!")
            break
        else:
            print("❌ Неверная команда!")
            continue
        
        tick()
        time.sleep(TICK_TIME)
    
    print(f"\n🎮 Игра завершена! Результат: {helicopter['points']} очков")

if __name__ == "__main__":
    main()