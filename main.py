import requests
import json
import os
import discord
import random
#import keep_alive

my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def retrieve_token(token, c):
  try:
    price = requests.get(
      f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies={c}"
    ).text
    price = json.loads(price)
    price = price[f"{token}"][f"{c}"]
    price = float(price)
    return (price)
  except:
    return 0


def ret_gif(sr):
  gif = requests.get(
    f"https://g.tenor.com/v1/search?q={sr}&key=YZM96RK2Y2Q9&limit=7").text
  gif = json.loads(gif)
  var = random.randint(0, 6)
  print(var)
  return (gif['results'][var]['media'][0]['gif']['url'])


@client.event
async def on_ready():
  print('We have logged in as {.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('.'):
    await message.channel.send("Hi, we will calculate your profits")
    acc = message.author

    await message.channel.send(
      "What crypto have you bought?   ! write the name of your crypto !")

    crypto = await client.wait_for("message")

    if crypto.author != acc:
      return

    crypto = crypto.content.lower()

    await message.channel.send(
      "What is your base currency? e.g. usd, eur, jpy, cny")
    c = await client.wait_for("message")
    if c.author != acc:
      return
    c = c.content.lower()

    if retrieve_token(crypto, c) == 0:
      await message.channel.send(
        "Your crypto or your fiat wasn't found, try again  :)")
      return

    await message.channel.send("How many entries did you have?")
    entries = await client.wait_for("message")
    if entries.author != acc:
      return

    entries = int(entries.content)

    await message.channel.send(
      "List your entry prices  ! write only the numbers and with dots(.), not commas(,)!!"
    )

    price = {}
    s_price = 0

    for i in range(entries):
      price[i] = await client.wait_for("message")
      price[i] = float(price[i].content)

    await message.channel.send(
      "List your coin/token entries' quantities  ! write only the numbers !")

    qty = {}
    s_qty = 0

    for a in range(entries):
      qty[a] = await client.wait_for("message")
      qty[a] = float(qty[a].content)
      s_qty += qty[a]

    pos_value = 0
    for b in range(entries):
      pos_value += price[b] * qty[b]

    cur_value = retrieve_token(crypto, c) * s_qty
    profit = cur_value - pos_value
    perc = profit / pos_value * 100

    if cur_value > pos_value:
      await message.channel.send("You are in profit!!! Congrats!")
      await message.channel.send(
        f"Your profit is {profit:.2f}{c} ({perc: .2f}%)")
      await message.channel.send(ret_gif("money"))
    else:
      await message.channel.send("You are in a loss  :(  Better luck next time"
                                 )
      await message.channel.send(f"Your loss is {profit:.2f}{c} ({perc: .2f}%)"
                                 )
      await message.channel.send(ret_gif("cryptocrash"))


#keep_alive()
client.run(my_secret)
