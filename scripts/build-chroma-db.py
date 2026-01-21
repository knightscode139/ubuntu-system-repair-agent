# scripts/build_chroma_db.py
import json
from pathlib import Path
import chromadb
from chromadb.config import Settings

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "src" / "data"
SOLUTIONS_FILE = DATA_DIR / "solutions.json"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

print(f"📂 Loading solutions from: {SOLUTIONS_FILE}")
print(f"💾 Will save ChromaDB to: {CHROMA_DB_PATH}")

# Initialize ChromaDB with disk persistence
print("🔧 Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH),
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Delete old collection if exists (fresh start)
try:
    chroma_client.delete_collection("ubuntu_solutions")
    print("🗑️  Deleted old collection")
except:
    pass

# Create new collection
collection = chroma_client.create_collection(
    name="ubuntu_solutions",
    metadata={"description": "Ubuntu system repair solutions"}
)
print("✅ Created new collection")

# Load solutions from JSON
print(f"📖 Reading {SOLUTIONS_FILE}...")
with open(SOLUTIONS_FILE, 'r') as f:
    solutions = json.load(f)

print(f"✅ Loaded {len(solutions)} solutions")

# Prepare data for ChromaDB
print("🔄 Preparing data for embedding...")
documents = []
metadatas = []
ids = []

for idx, solution in enumerate(solutions):
    # Combine error_trigger + context + solution_explanation for embedding
    doc_text = f"{solution['error_trigger']}\n{solution['context']}\n{solution['solution_explanation']}"
    documents.append(doc_text)

    # Store full solution as metadata
    metadatas.append({
        "category": solution['category'],
        "error_trigger": solution['error_trigger'],
        "risk_level": solution['risk_level'],
        "steps": json.dumps(solution['steps']),
        "backup_required": solution['backup_required'],
        "requires_reboot": solution['requires_reboot'],
        "validation_command": solution['validation_command'],
        "alternative_solution": solution['alternative_solution']
    })

    ids.append(f"solution_{idx}")

print(f"✅ Prepared {len(documents)} documents for embedding")

# Add all solutions to ChromaDB
print("🚀 Creating embeddings and adding to ChromaDB...")
print("   (This may take 10-30 seconds for 150 solutions)")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("✅ Successfully built ChromaDB!")
print(f"📍 Database saved to: {CHROMA_DB_PATH}")
print(f"📊 Total solutions indexed: {len(solutions)}")
