#!/usr/bin/env python
import rospy
import cv2
import tkinter as tk
from tkinter import ttk
from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        vertex, path = queue.popleft()
        if vertex == goal:
            return path
        if vertex not in visited:
            visited.add(vertex)
            neighbors = graph[vertex]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return "Tidak ditemukan jalur"



# Contoh penggunaan
graph = {
    'A1': ['A2', 'B1'],
    'A2': ['A1', 'A3','B2'],
    'A3': ['A2','A4','B3'],
    'A4': ['A3','A5','B4'],
    'A5': ['A4','B5'],
    'B1': ['A1','B2','C1'],
    'B2': ['A2','B1','B3','C2'],
    'B3': ['A3','B2','B4','C3'],
    'B4': ['A4','B3','B5','C4'],
    'B5': ['A5','B4','C5'],
    'C1': ['C2','B1','D1'],
    'C2': ['C1','B2','C3','D2'],
    'C3': ['C2','B3','C4','D3'],
    'C4': ['C3','B4','C5','D4'],
    'C5': ['C4','B5','D5',],
    'D1': ['D2','C1','E1'],
    'D2': ['D1','C2','D3','E2'],
    'D3': ['D2','C3','D4','E3'],
    'D4': ['D3','C4','D5','E4'],
    'D5': ['D4','C5','E5'],
    'E1' : ['D1','E2','F1'],
    'E2' : ['D2','E1','E3','F2'],
    'E3' : ['D3','E2','E4','F3'],
    'E4' : ['D4','E3','E5','F4'],
    'E5' : ['D5','E4','F5'],
    'F1' : ['E1','F2','G1'],
    'F2' : ['E2','F1','F3','G2'],
    'F3' : ['E3','F2','F4','G3'],
    'F4' : ['E4','F3','F5','G4'],
    'F5' : ['E5','F4','G5'],
    'G1' : ['F1','G2','H1'],
    'G2' : ['F2','G1','G3','H2'],
    'G3' : ['F3','G2','G4','H3'],
    'G4' : ['F4','G3','G5','H4'],
    'G5' : ['F5','G4','H5'],
    'H1' : ['G1','H2','I1'],
    'H2' : ['G2','H1','H3','I2'],
    'H3' : ['G3','H2','H4','I3'],
    'H4' : ['G4','H3','H5','I4'],
    'H5' : ['G5','H4','I5'],
    'I1' : ['H1','I2','J1'],
    'I2' : ['H2','I1','I3','J2'],
    'I3' : ['H3','I2','I4','J3'],
    'I4' : ['H4','I3','I5','J4'],
    'I5' : ['H5','I4','J5'],
    'J1' : ['I1','J2'],
    'J2' : ['I2','J1','J3'],
    'J3' : ['I3','J2','J4'],
    'J4' : ['I4','J3','J5'],
    'J5' : ['I5','J4']
    
}
# Fungsi yang akan dijalankan saat tombol "Cari Jalur" ditekan
def cari_jalur():
    start = start_entry.get()
    goal = goal_entry.get()
    

    if start not in graph or goal not in graph:
        hasil_label.config(text="Simpul tidak ditemukan")
        return
    
    hasil_jalur = bfs(graph, start, goal)
    
    if hasil_jalur:
        hasil_label.config(text=f"Jalur dari {start} ke {goal} adalah: {' -> '.join(hasil_jalur)}")
    else:
        hasil_label.config(text=f"Tidak ada jalur dari {start} ke {goal}")



# Membuat jendela Tkinter
root = tk.Tk()
root.title("Pencarian Jalur dengan BFS")

# Membuat label dan input untuk simpul awal
start_label = ttk.Label(root, text="Simpul Awal:")
start_label.pack()
start_entry = ttk.Entry(root)
start_entry.pack()

# Membuat label dan input untuk simpul tujuan
goal_label = ttk.Label(root, text="Simpul Tujuan:")
goal_label.pack()
goal_entry = ttk.Entry(root)
goal_entry.pack()

# Tombol "Cari Jalur"
cari_button = ttk.Button(root, text="Cari Jalur", command=cari_jalur)
cari_button.pack()

# Label untuk menampilkan hasil pencarian jalur
hasil_label = ttk.Label(root, text="")
hasil_label.pack()


if __name__ == '__main__':
    try:
        rospy.init_node('bfs', anonymous=True)
        root.mainloop()
    except rospy.ROSInterruptException:
        pass

