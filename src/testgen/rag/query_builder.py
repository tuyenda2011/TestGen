import re
from typing import Dict, Optional

def extract_framework_and_testing_type(query: str) -> Dict[str, Optional[str]]:
    """Extract testing framework and testing type from the user query."""
    result = {"framework": None, "testing_type": None}
    
    query_lower = query.lower()
    
    # Framework extraction
    frameworks = ["pytest-cov", "pytest", "jest", "postman", "selenium", "cypress", "playwright", "coverage", "junit"]
    for fw in frameworks:
        if fw in query_lower:
            result["framework"] = fw
            break
            
    # Testing type extraction
    types = {
        "e2e": ["e2e", "end-to-end", "end to end"],
        "unit": ["unit"],
        "api": ["api", "integration"],
        "ui": ["ui", "frontend", "front-end"]
    }
    
    for tt, keywords in types.items():
        if any(kw in query_lower for kw in keywords):
            result["testing_type"] = tt
            break
            
    return result

def build_enriched_query(query: str) -> str:
    """Enrich the query to improve retrieval quality by adding related context."""
    enriched = query
    query_lower = query.lower()
    
    extracted = extract_framework_and_testing_type(query)
    
    # Synonym expansions
    if any(kw in query_lower for kw in ["mock", "giả lập", "ảo"]):
        enriched += " mocking stubbing spy fake fixtures monkeypatch"
    if any(kw in query_lower for kw in ["assert", "kiểm tra", "xác nhận"]):
        enriched += " assertions expect matching verifying"
    if any(kw in query_lower for kw in ["coverage", "độ bao phủ", "bao phủ"]):
        enriched += " code coverage reports statements branches"
        
    if extracted["framework"]:
        enriched += f" {extracted['framework']} rules guidelines best practices"
        
    if extracted["testing_type"]:
        if extracted["testing_type"] == "e2e":
            enriched += " end-to-end testing browser automation"
        elif extracted["testing_type"] == "api":
            enriched += " API testing endpoints requests responses"
        elif extracted["testing_type"] == "unit":
            enriched += " unit testing assertions"
            
    # Add general context for testgen rag
    if "test" in query_lower or "kiểm thử" in query_lower:
        enriched += " testing methodology test cases scenarios"
        
    return enriched
