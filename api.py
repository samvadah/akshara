"""Module for API calls."""

from fastapi import FastAPI, Query
from akshara import varnakaarya as vk

app = FastAPI()


@app.get("/vinyaasa")
async def api_vinyaasa(
    word: str = Query(..., description="The word to compute the vinyaasa for"),
    count: bool = Query(False, description="Include total character count")
):
    """Return the vinyaasa of a word."""
    try:
        vinyaasa = vk.get_vinyaasa(word)
        status = "success"
    except AssertionError:
        vinyaasa = None
        status = "failure"

    response = {"vinyaasa": vinyaasa, "status": status}
    
    if count:
        response["count"] = len(vinyaasa) if vinyaasa is not None else None

    return response


@app.get("/akshara")
async def api_akshara(
    word: str = Query(..., description="The word to compute the akshara for"),
    count: bool = Query(False, description="Include total character count")
):
    """Return the akshara of a word."""
    try:
        akshara = vk.get_akshara(word)
        status = "success"
    except AssertionError:
        response = {"akshara": None, "status": "failure"}
        if count:
            response["count"] = None
        return response

    response = {"akshara": akshara, "status": status}
    
    if count:
        try:
            response["count"] = len(vk.get_vinyaasa(word))
        except AssertionError:
            response["count"] = None

    return response


@app.get("/shabda")
async def api_shabda(
    letters: str = Query(
        ..., description="Comma-separated letters to compute the shabda for"
    )
):
    """Return the shabda of a list of letters."""
    try:
        letter_list = letters.split(",")
        shabda = vk.get_shabda(letter_list)
        status = "success"
    except AssertionError:
        shabda = None
        status = "failure"

    return {"word": shabda, "status": status}


@app.get("/count")
async def api_count(
    word: str = Query(..., description="The word or sentence to compute the character count for")
):
    """Return the total character count including spaces and dandas."""
    try:
        char_count = len(vk.get_vinyaasa(word))
        status = "success"
    except AssertionError:
        char_count = None
        status = "failure"

    return {"count": char_count, "status": status}
