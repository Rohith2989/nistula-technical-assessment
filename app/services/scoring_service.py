def calculate_confidence(query_type: str, message: str, has_booking: bool) -> float:
    # 1. Set Base Scores
    base_map = {
        "post_sales_checkin": 0.95,
        "pre_sales_availability": 0.92,
        "pre_sales_pricing": 0.90,
        "general_enquiry": 0.80,
        "special_request": 0.70,
        "complaint": 0.40  # Always low to force human escalation
    }
    
    score = base_map.get(query_type, 0.50)
    
    # 2. Apply Deterministic Modifiers
    if has_booking: score += 0.05
    if len(message.split()) < 5: score -= 0.10  # Penalize vague short messages
    if message.count('?') > 2: score -= 0.05    # Penalize complex multi-questions
    
    return round(max(0.0, min(1.0, score)), 2)

def get_action(score: float, query_type: str) -> str:
    if query_type == "complaint" or score < 0.60:
        return "escalate"
    return "auto_send" if score >= 0.85 else "agent_review"