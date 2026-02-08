"""
AI Processor module - summarizes bills and extracts tags
Gabe's code - simplified for hackathon MVP
"""


def summarize(bill_text):
    """
    Summarize bill text using AI
    For MVP: returns a simple summary
    TODO: Integrate with Gemini API for real summarization
    """
    if not bill_text or len(bill_text) < 50:
        return "Summary not available - bill text is too short."
    
    # MOCK: Simple extraction of first few sentences
    sentences = bill_text.split('.')[:3]
    summary = '. '.join(sentences).strip() + '.'
    
    print(f"[MOCK] AI Processor: Generated summary ({len(summary)} chars)")
    
    # TODO: Replace with real Gemini API call:
    # import google.generativeai as genai
    # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # model = genai.GenerativeModel('gemini-pro')
    # prompt = f"Summarize this bill in 2-3 sentences: {bill_text}"
    # response = model.generate_content(prompt)
    # return response.text
    
    return summary


def extract_tags(bill_text):
    """
    Extract relevant tags/categories from bill text
    For MVP: uses simple keyword matching
    TODO: Use Gemini API for intelligent tag extraction
    """
    if not bill_text:
        return []
    
    # Convert to lowercase for matching
    text_lower = bill_text.lower()
    
    # Define keyword mappings to tags
    tag_keywords = {
        'reproductive_rights': ['abortion', 'contraception', 'reproductive', 'pregnancy', 'maternal'],
        'healthcare': ['health', 'medical', 'hospital', 'medicaid', 'medicare', 'insurance'],
        'education': ['school', 'teacher', 'student', 'education', 'university', 'college'],
        'lgbtq_rights': ['lgbtq', 'transgender', 'gay', 'lesbian', 'sexual orientation', 'gender identity'],
        'voting_access': ['voting', 'voter', 'election', 'ballot', 'polling'],
        'employment': ['employment', 'worker', 'wage', 'salary', 'labor', 'workplace'],
        'housing': ['housing', 'rent', 'tenant', 'landlord', 'eviction'],
        'criminal_justice': ['prison', 'jail', 'sentencing', 'criminal', 'police', 'arrest'],
        'immigration': ['immigration', 'immigrant', 'visa', 'asylum', 'deportation'],
        'environment': ['environment', 'climate', 'pollution', 'clean air', 'clean water'],
        'civil_rights': ['discrimination', 'civil rights', 'equal protection', 'rights'],
        'women': ['woman', 'women', 'female', 'maternity', 'breastfeeding', 'pregnancy'],
    }
    
    # Find matching tags
    matched_tags = []
    for tag, keywords in tag_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                matched_tags.append(tag)
                break  # Only add each tag once
    
    # If no tags matched, default to 'general'
    if not matched_tags:
        matched_tags = ['general']
    
    print(f"[MOCK] AI Processor: Extracted tags: {matched_tags}")
    
    # TODO: Replace with real Gemini API call:
    # prompt = f"Extract relevant policy categories from this bill. Return as comma-separated list: {bill_text}"
    # response = model.generate_content(prompt)
    # tags = [tag.strip() for tag in response.text.split(',')]
    
    return matched_tags


def process_bill(bill_text):
    """
    Convenience function to do both summarize and extract_tags
    """
    summary = summarize(bill_text)
    tags = extract_tags(bill_text)
    
    return {
        'summary': summary,
        'tags': tags
    }