import config
import logging
import asyncio
import re
from aiogram import Bot, Dispatcher, executor, types
import parse_sber
import parse_aliexpress


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_text = "Hello! I am a bot that can compare your " \
        + "products by their prices in SberMegaMarket and Aliexpress!\n" \
        + "I have following commands:\n" \
        + "/help\n" \
        + "/find_product <product-name> - Find and Compare Products\n"
    await message.answer(start_text)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    help_text = "I can compare your products by their prices " \
        + "in SberMegaMarket and Aliexpress!\n" \
        + "I have following commands:\n" \
        + "/start\n" \
        + "/find_product <product-name> - Find and Compare Products\n"
    await message.answer(help_text)


@dp.message_handler(commands=['find_product'])
async def findProduct(message: types.Message):
    text = re.sub('/find_product', '', message.text)
    if len(text) == 0:
        error_message = "Invalid product name!\n"\
            + "Please, use this format:\n/FindProduct <your-product-name>"
        await message.answer(error_message)
        return
    result = {}
    result["SberMegaMarket"] = parse_sber.findProduct(text)
    result["Aliexpress"] = parse_aliexpress.findProduct(text)
    shops = ["SberMegaMarket", "Aliexpress"]
    text = "I have found these products:\n"
    best_shop = None
    for shop in shops:
        text += '\n'
        if result[shop]["product name"] is None:
            text += "Sorry, "\
                    + "I have not found this product on {0}\n".format(shop)
        else:
            text += "On {0} I have found:\n\n{1}\n\n".format(
                        shop, result[shop]["product name"])
            text += "The cost is {0}₽\n".format(result[shop]["cost"])
            text += "{0}\n".format(result[shop]["link"])
            if best_shop is None or\
                    result[shop]["cost"] < result[best_shop]["cost"]:
                best_shop = shop
    text += '\n'
    if best_shop is None:
        text += "Sorry, I can not compare!\n"
    else:
        text += "I think that "\
                + "{0} has better price for this product!\n".format(best_shop)
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
