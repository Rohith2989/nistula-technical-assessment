import os
import uuid
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv


from app.services.anthropic_service import get_ai_draft
from app.services.scoring_service import calculate_confidence, get_action

load_dotenv()

app = FastAPI(title="Nistula Guest Message Handler")

class GuestMessage(BaseModel):
    source: str
    guest_name: str
    message: str
    booking_ref: str = "new_lead"
    property_id: str

@app.post("/webhook/message")
async def handle_message(payload: GuestMessage):
    context = "Property Villa B1: Assagao, Goa. 3 Bedrooms. Rate 18k/night. WiFi: Nistula@2024. Available April 20-24."
    
    try:
        # 1. Call AI Service (from anthropic_service.py)
        ai_data = await get_ai_draft(payload.message, payload.guest_name, context)
        
        # 2. Calculate Confidence & Action (from scoring_service.py)
        score = calculate_confidence(ai_data['query_type'], payload.message, payload.booking_ref != "new_lead")
        action = get_action(score, ai_data['query_type'])
        
        return {
            "message_id": str(uuid.uuid4()),
            "query_type": ai_data['query_type'],
            "drafted_reply": ai_data['drafted_reply'],
            "confidence_score": score,
            "action": action
        }
    except Exception as e:
        
        print(f"LOG: AI call failed ({e}). Using heuristic fallback.")
        msg = payload.message.lower()
        if "available" in msg or "dates" in msg:
            query_type, drafted_reply = "pre_sales_availability", f"Hi {payload.guest_name}! Villa B1 is currently available."
        elif "happy" in msg or "broken" in msg:
            query_type, drafted_reply = "complaint", "I am so sorry. I am escalating this to our manager immediately."
        else:
            query_type, drafted_reply = "general_enquiry", "Thank you for reaching out. An agent will get back to you shortly."
            
        score = calculate_confidence(query_type, payload.message, payload.booking_ref != "new_lead")
        action = get_action(score, query_type)
        
        return {
            "message_id": str(uuid.uuid4()),
            "query_type": query_type,
            "drafted_reply": drafted_reply,
            "confidence_score": score,
            "action": action
        }


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5050))
    uvicorn.run(app, host="0.0.0.0", port=port)
