from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from schema import UrlSchema
from models import Url
import os
import nanoid
from decouple import config
router = APIRouter()
BASE_URL = "http://localhost:8000"

@router.post('/', response_model=dict)
async def test(url: UrlSchema):
    url = dict(url)

    if url["customCode"]:
        shortCode = url["customCode"]
    else:
        shortCode = nanoid.generate(size=8)

    shortUrl = os.path.join(BASE_URL, shortCode)

    urlExists = Url.objects(shortCode=shortCode)
    if len(urlExists) != 0:
        raise HTTPException(status_code=400, detail="Short code is invalid, It has been used.")

    try:
        url = Url(
            longUrl=url["longUrl"],
            shortCode=shortCode,
            shortUrl=shortUrl
        )

        url.save()

        return {
            "message": "Successfully shortened URL.",
            "shortUrl": shortUrl,
            "longUrl": url["longUrl"]
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unknown error occurred.")