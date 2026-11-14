def build_context(query,candidates):
    lines=["IMAGE QUERY:",query.model_dump_json(),"","CANDIDATES:"]
    for i,p in enumerate(candidates,1):
        lines.append("Candidate %d\nID: %s\nName: %s\nCategory: %s\nSubcategory: %s\nBrand: %s\nColor: %s\nPrice: %s\nAttributes: %s\nVisual similarity: %.4f\nDescription: %s"%(i,p["product_id"],p["name"],p["category"],p["subcategory"],p["brand"],p["color"],p["price"],p["attributes"],p["similarity"],p["description"]))
    return "\n\n".join(lines)
