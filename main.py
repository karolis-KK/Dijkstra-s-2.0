import pygame
import heapq
import sys
import customtkinter as ctk

pygame.init()

# const
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# spalvos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SEARCH = (163, 160, 160)
GRAY = (71, 68, 68)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm")

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# taskeliai
waypoints = []

# algo
def dijkstra(start, end):
    def single_target_dijkstra(start, end):
        distances = {(r, c): float('inf') for r in range(ROWS) for c in range(COLS)}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()
        path = {}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end:
                return reco(path, start, end)

            if current_node in visited:
                continue

            visited.add(current_node)

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                r, c = current_node[0] + dr, current_node[1] + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != 1:
                    distance = current_distance + 1
                    if distance < distances[(r, c)]:
                        distances[(r, c)] = distance
                        path[(r, c)] = current_node
                        heapq.heappush(pq, (distance, (r, c)))
                        if show_visualization.get():
                            pygame.draw.rect(screen, SEARCH, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                            pygame.display.flip()
                            pygame.time.delay(10)

        return None

    if waypoints:
        path = []
        current_start = start
        for wp in waypoints:
            segment_path = single_target_dijkstra(current_start, wp)
            if not segment_path:
                print(f"No valid path between {current_start} and {wp}")
                return None
            path.extend(segment_path[:-1])
            current_start = wp
        final_segment = single_target_dijkstra(current_start, end)
        if final_segment:
            path.extend(final_segment)
        else:
            print(f"No valid path between {current_start} and {end}")
            return None
        return path
    else:
        return single_target_dijkstra(start, end)

def reco(path, start, end):
    current = end
    full_path = []
    while current != start:
        full_path.append(current)
        current = path[current]
    full_path.append(start)
    return full_path[::-1]

# ctk
root = ctk.CTk()
root.title("CTK")
root.geometry("300x200")

start_frame = ctk.CTkFrame(root)
start_frame.pack(pady=10)

start_label = ctk.CTkLabel(start_frame, text="0 =< Start < 40:")
start_label.pack(side=ctk.LEFT)

start_x = ctk.CTkEntry(start_frame, width=50)
start_x.pack(side=ctk.LEFT, padx=5)

start_y = ctk.CTkEntry(start_frame, width=50)
start_y.pack(side=ctk.LEFT, padx=5)

end_frame = ctk.CTkFrame(root)
end_frame.pack(pady=10)

end_label = ctk.CTkLabel(end_frame, text="0 <= End <40:")
end_label.pack(side=ctk.LEFT)

end_x = ctk.CTkEntry(end_frame, width=50)
end_x.pack(side=ctk.LEFT, padx=5)

end_y = ctk.CTkEntry(end_frame, width=50)
end_y.pack(side=ctk.LEFT, padx=5)

show_visualization = ctk.CTkCheckBox(root, text="Show Visualization")
show_visualization.pack(pady=10)

start_button = ctk.CTkButton(root, text="Start Visualization", command=lambda: None)
start_button.pack(pady=10)

start_pos = None
end_pos = None
shortest_path = None

# main loopas
def main():
    global start_pos, end_pos, shortest_path, waypoints
    drawing = False
    erasing = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LEFT
                    drawing = True
                elif event.button == 3:  # RIGHT
                    erasing = True
                elif event.button == 2:  # MIDDLE taskeliai
                    x, y = pygame.mouse.get_pos()
                    r, c = y // GRID_SIZE, x // GRID_SIZE
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if (r, c) in waypoints:
                            waypoints.remove((r, c))
                        else:
                            waypoints.append((r, c))
                        shortest_path = None # resetint, kai taskeliai pasikeicia
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    erasing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if start_pos and end_pos:
                        shortest_path = dijkstra(start_pos, end_pos)

        if drawing or erasing:
            x, y = pygame.mouse.get_pos()
            r, c = y // GRID_SIZE, x // GRID_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r][c] = 1 if drawing else 0
                shortest_path = None # resetint, kai pasikeicia kelias

        screen.fill(WHITE)

        # grid draw
        for r in range(ROWS):
            for c in range(COLS):
                color = BLACK if grid[r][c] == 1 else WHITE
                pygame.draw.rect(screen, color, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, (200, 200, 200), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # TASKAI
        for wp in waypoints:
            pygame.draw.rect(screen, ORANGE, (wp[1] * GRID_SIZE, wp[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (255, 140, 0), (wp[1] * GRID_SIZE, wp[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

        # trumpiausias kelias
        if shortest_path:
            for i, (r, c) in enumerate(shortest_path):
                if i == 0 or i == len(shortest_path) - 1: # pradzia ir pabaiga skip
                    continue 
                pygame.draw.rect(screen, GRAY, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # startas ir pabaiga
        if start_pos:
            pygame.draw.rect(screen, GREEN, (start_pos[1] * GRID_SIZE, start_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (0, 100, 0), (start_pos[1] * GRID_SIZE, start_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

        if end_pos:
            pygame.draw.rect(screen, RED, (end_pos[1] * GRID_SIZE, end_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (100, 0, 0), (end_pos[1] * GRID_SIZE, end_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

        pygame.display.flip()
        clock.tick(60)

        root.update()

def start_visualization():
    global start_pos, end_pos, shortest_path
    try:
        start_pos = (int(start_y.get()), int(start_x.get()))
        end_pos = (int(end_y.get()), int(end_x.get()))
        shortest_path = None # resetint, kai pasikeicia s/e
    except ValueError:
        print("Enter valid coordinates")

start_button.configure(command=start_visualization)

if __name__ == "__main__":
    main()
