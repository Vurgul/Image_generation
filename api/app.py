import requests
import redis
from fastapi import Response, Depends
from starlette.responses import RedirectResponse

from auth.auth import app, oauth2_scheme


cache = redis.StrictRedis(host='redis', port=6379, db=0)  # redis -> localhost


@app.get('/', response_class=RedirectResponse)
async def root(token: str = Depends(oauth2_scheme)):
    response = RedirectResponse(url=f'/monster')
    return response


@app.get('/monster')
async def image_generation_redirect(token: str = Depends(oauth2_scheme)):
    return {'message': 'In the address bar, '
                       'enter the text of the request to get the picture'}


@app.get('/monster/{slug}')
async def image_generation(slug: str, token: str = Depends(oauth2_scheme)):
    """
    The function takes the request text as input and either
    returns the generated image or retrieves it from the cache
    """
    image = cache.get(slug)
    if image is None:
        response = requests.get(f'http://dnmonster:8080/monster/{slug}')  # dnmonster -> localhost
        image = response.content
        cache.set(slug, image)

    return Response(image, media_type='image/png')
