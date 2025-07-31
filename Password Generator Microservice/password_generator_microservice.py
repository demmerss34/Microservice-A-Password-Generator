from fastapi import FastAPI, Query, HTTPException
import random
import string

app = FastAPI()

DEFAULT_LENGTHS = {
    "PIN": 4,
    "Medium": 8,
    "Strong": 12
}

VALID_LENGTHS = {
    "PIN": (4, 6),
    "Medium": (6, 12),
    "Strong": (8, 20),
    "Custom": (1, 64)
}


@app.get("/generate_password")
def generate_password(
    type: str = Query(..., pattern="^(PIN|Medium|Strong|Custom)$"),
    length: int = None,
    symbols: bool = False
):
    print("📥 Received request with parameters:")
    print(f"Type: {type}")
    print(f"Length: {length if length else '(default)'}")
    print(f"Symbols: {symbols}")

    # Validate and apply default length
    if not length:
        length = DEFAULT_LENGTHS.get(type, 12)

    min_len, max_len = VALID_LENGTHS[type]
    if length < min_len or length > max_len:
        raise HTTPException(
            status_code=400,
            detail=f"Length for type '{type}' must be between "
                   f"{min_len} and {max_len}"
        )

    # Character selection based on type
    if type == "PIN":
        if symbols:
            raise HTTPException(
                status_code=400,
                detail="Symbols are not allowed for type 'PIN'"
            )
        chars = string.digits

    elif type == "Medium":
        if symbols:
            raise HTTPException(
                status_code=400,
                detail="Symbols are not allowed for type 'Medium'"
            )
        chars = string.ascii_letters + string.digits

    elif type in ["Strong", "Custom"]:
        chars = string.ascii_letters + string.digits
        if symbols:
            chars += string.punctuation

    else:
        raise HTTPException(status_code=400, detail="Invalid password type")

    # Generate and return password
    password = ''.join(random.choices(chars, k=length))
    print(f"Generated password: {password}")
    return {"password": password}


