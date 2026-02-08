# MOCK AI PROCESSOR MODULE
# Restored because file was missing

def summarize(bill_text):
    """
    Mock function to summarize bill text and extract tags.
    """
    print(f"[MOCK] AI Processor: Summarizing '{bill_text[:30]}...'")
    
    # Simple logic to simulate AI analysis
    summary = f"SUMMARY: {bill_text}"
    tags = ["politics"]
    
    if "taco" in bill_text.lower():
        tags.append("food")
    if "health" in bill_text.lower():
        tags.append("healthcare")
        tags.append("women")
        
    return {
        "summary": summary,
        "tags": tags,
        "impact_score": 8.5
    }
