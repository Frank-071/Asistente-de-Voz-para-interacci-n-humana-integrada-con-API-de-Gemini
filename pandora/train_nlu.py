# train_nlu.py
import json, random
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

DATA = Path("data/nlu_es.jsonl")
OUT  = Path("models"); OUT.mkdir(parents=True, exist_ok=True)

def load_dataset():
    rows = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        rows.append(json.loads(line))
    random.shuffle(rows)
    X = [r["text"]   for r in rows]
    y = [r["intent"] for r in rows]
    return X, y

def main():
    X, y = load_dataset()
    clf = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            analyzer="char_wb",
            ngram_range=(3,5),
            min_df=1
        )),
        ("lr", LogisticRegression(max_iter=300, n_jobs=None))
    ])
    clf.fit(X, y)
    joblib.dump(clf, OUT / "nlu_intents.joblib")
    print("✅ Modelo entrenado. Intents:", sorted(set(y)))
    # Prueba rápida:
    tests = ["Lila qué hora es", "abre yutube", "googlea clima lima", "hola", "Lila salir"]
    for t in tests:
        pred = clf.predict([t])[0]
        proba = max(clf.predict_proba([t])[0])
        print(f"  • {t!r} → {pred} ({proba:.2f})")

if __name__ == "__main__":
    main()
