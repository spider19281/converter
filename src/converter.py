import aiohttp
import asyncio
from pydantic import BaseModel, Field, field_validator, ValidationError
import urllib.parse
import re

from bs4 import BeautifulSoup as bs


class Converter(BaseModel):
    currency_from: str = Field(min_length=3, max_length=3, description="Сurrency from which the conversion")
    currency_to: str = Field(min_length=3, max_length=3, description="Сurrency to which the conversion")
    amount: float

    @field_validator('currency_from', 'currency_to')
    @classmethod
    def validate_upper_case(cls, value):
        if value != value.upper() or not value.isalpha():
            raise ValueError("Field must contain letters in upper case!")
        return value

    async def get_html(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text(), resp.status

    async def get_amount(self, url) -> float:
        params = {'Amount': self.amount, 'From': self.currency_from, 'To': self.currency_to}
        response, status = await self.get_html(url + '?' + urllib.parse.urlencode(params))
        if status == 404:
            return {'result': '404 - Not Found'}
        soup = bs(response, "html.parser")
        result = soup.find_all("p")[2].find_all('span')[0].previousSibling
        return {'result': result}