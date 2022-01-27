import redis
import httpx
from fastapi import Response, Depends
from auth.auth import oauth2_scheme
from auth.views import app


cache = redis.StrictRedis(host='redis', port=6379, db=0)  # redis -> localhost
TTL = 1800


@app.get('/monster/{slug}')
async def image_generation(slug: str, token: str = Depends(oauth2_scheme)):
    """
    Returns the generated image or retrieves it from the cache
    """
    image = cache.get(slug)
    if image is None:
        response = httpx.get(f'http://dnmonster:8080/monster/{slug}')  # dnmonster -> localhost
        image = response.content
        cache.set(slug, image, ex=TTL)

    return Response(image, media_type='image/png')
