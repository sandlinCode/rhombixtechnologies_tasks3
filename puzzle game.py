import tkinter as tk
from tkinter import messagebox
import random
import time

# --- CONFIG ---
CARD_BACK = "❓"
CARDS = ["🐶", "🐱", "🐰", "🦊", "🐻", "🐼", "🐨", "🐸"]
TIME_LIMIT = 60  # seconds

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Memory Puzzle Game")
        self.root.geometry("400x500")
        self.root.configure(bg="#f8f9fa")

        self.cards = CARDS * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.flipped = []
        self.matched = set()
        self.start_time = time.time()
        self.remaining_time = TIME_LIMIT

        # Header
        self.title_label = tk.Label(
            root, text="Match the Pairs!", font=("Arial", 20, "bold"), bg="#f8f9fa"
        )
        self.title_label.pack(pady=10)

        self.timer_label = tk.Label(
            root, text=f"Time: {self.remaining_time}s", font=("Arial", 14), bg="#f8f9fa"
        )
        self.timer_label.pack()

        # Game Grid
        self.frame = tk.Frame(root, bg="#f8f9fa")
        self.frame.pack(pady=20)

        for i in range(4):
            row = []
            for j in range(4):
                idx = i * 4 + j
                btn = tk.Button(
                    self.frame,
                    text=CARD_BACK,
                    font=("Arial", 20),
                    width=4,
                    height=2,
                    command=lambda idx=idx: self.flip_card(idx),
                    bg="#e9ecef",
                    activebackground="#dee2e6",
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        self.update_timer()

    def flip_card(self, idx):
        if idx in self.matched:
            return
        row, col = divmod(idx, 4)
        btn = self.buttons[row][col]

        if len(self.flipped) < 2 and idx not in [f[0] for f in self.flipped]:
            btn.config(text=self.cards[idx])
            self.flipped.append((idx, btn))

            if len(self.flipped) == 2:
                self.root.after(800, self.check_match)

    def check_match(self):
        (idx1, btn1), (idx2, btn2) = self.flipped
        if self.cards[idx1] == self.cards[idx2]:
            self.matched.add(idx1)
            self.matched.add(idx2)
            btn1.config(bg="#c3f3c0")
            btn2.config(bg="#c3f3c0")
        else:
            btn1.config(text=CARD_BACK)
            btn2.config(text=CARD_BACK)
        self.flipped = []

        if len(self.matched) == len(self.cards):
            messagebox.showinfo("🎉 You Win!", "Congratulations! You matched all pairs!")
            self.root.destroy()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.remaining_time = TIME_LIMIT - elapsed
        self.timer_label.config(text=f"Time: {self.remaining_time}s")

        if self.remaining_time <= 0:
            messagebox.showwarning("⏰ Time's Up!", "Game Over! Try again.")
            self.root.destroy()
        else:
            self.root.after(1000, self.update_timer)

# --- Run Game ---
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
