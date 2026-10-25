from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone
import re, os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./realitylens.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class ReviewRecord(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    place_name = Column(String(200), nullable=False)
    project = Column(String(30), nullable=False)
    perspective = Column(String(100), default="General customer")
    review = Column(Text, nullable=False)
    sentiment = Column(String(30), nullable=False)
    aspects_json = Column(Text, nullable=False)
    claims_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FACT CHECK | RealityLensAI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","),
    allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)

class ReviewInput(BaseModel):
    project: str = Field(pattern="^(places|delivery_apps)$")
    place_name: str = Field(min_length=1, max_length=200)
    perspective: str = Field(default="General customer", max_length=100)
    review: str = Field(min_length=3, max_length=5000)

POSITIVE = {"good","great","excellent","clean","friendly","helpful","delicious","fresh","comfortable","fast","quick","affordable","perfect","beautiful","easy","amazing","love"}
NEGATIVE = {"bad","poor","dirty","rude","slow","late","delay","expensive","stale","broken","wrong","missing","damaged","leaking","terrible","worst","uncomfortable","overpriced"}

PLACE_ASPECTS = {
 "cleanliness":["clean","dirty","hygiene","neat"],
 "staff_and_service":["staff","employee","service","rude","helpful","waiter"],
 "food_quality":["food","taste","fresh","stale","delicious","meal"],
 "price":["price","cost","expensive","cheap","affordable","value"],
 "comfort":["comfort","comfortable","noisy","quiet","room","bed"],
 "waiting_time":["wait","waiting","delay","slow","quick"],
 "location":["location","parking","nearby","distance","accessible"],
}
DELIVERY_ASPECTS = {
 "delivery_time":["delivery","late","delay","fast","quick","arrived"],
 "packaging":["packaging","package","leaking","damaged","wrapped"],
 "item_condition":["fresh","stale","broken","cold","quality","expired"],
 "price_and_fees":["price","cost","fee","expensive","cheap","charge"],
 "customer_support":["support","refund","help","complaint","agent"],
 "order_accuracy":["wrong","missing","incorrect","order","item"],
}

def analyze_sentiment(text):
    words = re.findall(r"\b[a-z']+\b", text.lower())
    pos = sum(w in POSITIVE for w in words)
    neg = sum(w in NEGATIVE for w in words)
    label = "Positive" if pos > neg else "Negative" if neg > pos else "Mixed or Neutral"
    return {"label": label, "positive_terms": pos, "negative_terms": neg,
            "method": "Transparent keyword baseline; not a trained ML model"}

def analyze_aspects(text, dictionary):
    lower = text.lower()
    found = []
    for aspect, keywords in dictionary.items():
        hits = [kw for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", lower)]
        if hits:
            found.append({"aspect": aspect.replace("_", " ").title(), "matched_terms": hits,
                          "sentiment": analyze_sentiment(text)["label"],
                          "note": "Review mention; not independently verified"})
    return found

def extract_claims(text):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if len(s.strip()) >= 8]
    return [{"text": s, "status": "Insufficient evidence",
             "explanation": "A review alone is not independent evidence. Attach a reliable source before making a verification decision."}
            for s in sentences]

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/")
def root():
    return {"name":"FACT CHECK | RealityLensAI", "status":"running", "docs":"/docs"}

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.post("/api/analyze")
def analyze(payload: ReviewInput, db: Session = Depends(get_db)):
    project = payload.project
    dictionary = PLACE_ASPECTS if project == "places" else DELIVERY_ASPECTS
    sentiment = analyze_sentiment(payload.review)
    aspects = analyze_aspects(payload.review, dictionary)
    claims = extract_claims(payload.review)
    row = ReviewRecord(place_name=payload.place_name, project=project,
        perspective=payload.perspective, review=payload.review, sentiment=sentiment["label"],
        aspects_json=json.dumps(aspects), claims_json=json.dumps(claims))
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id, "project":project, "place_name":payload.place_name,
        "perspective":payload.perspective, "review":payload.review,
        "sentiment":sentiment, "aspects":aspects, "claims":claims,
        "disclaimer":"Prototype analysis only. Sentiment is keyword-based and claims are not externally verified."}

@app.get("/api/reviews")
def reviews(project: str = "places", db: Session = Depends(get_db)):
    if project not in ("places","delivery_apps"):
        raise HTTPException(status_code=400, detail="project must be places or delivery_apps")
    rows = db.query(ReviewRecord).filter_by(project=project).order_by(ReviewRecord.id.desc()).limit(100).all()
    return [{"id":r.id,"place_name":r.place_name,"project":r.project,"perspective":r.perspective,
        "review":r.review,"sentiment":r.sentiment,"aspects":json.loads(r.aspects_json),
        "claims":json.loads(r.claims_json),"created_at":r.created_at.isoformat()} for r in rows]

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    row = db.query(ReviewRecord).filter_by(id=review_id).first()
    if not row: raise HTTPException(status_code=404, detail="Review not found")
    db.delete(row); db.commit()
    return {"deleted": review_id}
