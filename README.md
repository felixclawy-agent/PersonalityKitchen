# The Scientific Kitchen (TIPI-D v3.0) 🍳🧬

A scientific instrument designed to determine your **Culinary Phenotype**. 

This app uses a shortened version of the **Ten-Item Personality Inventory (TIPI)** (adapted to 12 items for precision) to calculate your Big Five personality traits:
*   **O**penness
*   **C**onscientiousness
*   **E**xtraversion
*   **A**greeableness
*   **N**euroticism (Emotional Stability)

It then maps your psychometric profile to a specific dish that embodies your essence.

## 🚀 How to Run (Zero Dependencies)

This application is built with vanilla Python and HTML/JS. It requires **no external libraries** (no `pip install` needed).

### Prerequisites
*   Python 3.x installed

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/felixclawy-agent/PersonalityKitchen.git
    cd PersonalityKitchen
    ```

2.  **Run the server:**
    ```bash
    python3 server.py
    ```

3.  **Open your browser:**
    Go to `http://localhost:8091`

## 🛠 Configuration

You can change the port in `server.py`:
```python
PORT = 8091
```

## 📱 Features
*   **Scientific Scoring:** Uses standard TIPI reverse-scoring logic.
*   **Deterministic:** No AI/LLM queries. Runs 100% offline/locally.
*   **Responsive:** Works on mobile and desktop.
*   **Dark Mode:** Automatically respects system preferences.
