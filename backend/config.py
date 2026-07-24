"""
MuleTrace — Configuration & Database Connection Settings

Dataset design decisions:
- NUM_ACCOUNTS: 1200 accounts (larger pool for realistic 1-2% mule prevalence)
- NUM_MULE_RINGS: 12 rings total (7 fraud + 5 false positive)
  → At ring size 3-5, this yields ~18-35 mule accounts = ~1.5-2.9% prevalence
  → Matches SAML-D / AMLNet industry baseline of 0.5-3%
- GNN_EPOCHS: 60 with early stopping (patience=15) — faster convergence
"""
import os

# ─── Neo4j Configuration ────────────────────────────────────────────
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "chainvigil")

# ─── Data Generation Defaults ───────────────────────────────────────
NUM_ACCOUNTS = int(os.getenv("NUM_ACCOUNTS", "1200"))
NUM_TRANSACTIONS = int(os.getenv("NUM_TRANSACTIONS", "5000"))
# 12 rings: 7 fraud typologies + 5 false positives
# Ring size 3-5 → ~18-35 true mule accounts (~1.5-2.9% of 1200 base accounts)
NUM_MULE_RINGS = int(os.getenv("NUM_MULE_RINGS", "12"))
MULE_RING_SIZE_RANGE = (3, 5)   # Smaller, realistic ring sizes

# ─── Channels ───────────────────────────────────────────────────────
CHANNELS = ["UPI", "ATM", "WEB", "MOBILE_APP"]

# ─── GNN Configuration ─────────────────────────────────────────────
GNN_HIDDEN_DIM = 64    # slightly larger to handle new features
GNN_NUM_LAYERS = 3     # 3-hop aggregation for ring detection
GNN_LEARNING_RATE = 0.003
GNN_EPOCHS = 60        # reduced; early stopping at patience=15 will stop earlier
GNN_DROPOUT = 0.4      # slightly higher dropout for realistic AUC
RISK_THRESHOLD = 0.50  # balanced threshold

# ─── Paths ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "sample_data")
MODEL_DIR = os.path.join(BASE_DIR, "gnn", "saved_models")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
