import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

palavra_chave = ["bot", "robozin","zezin","faz tudo","Faz tudo"]

starter_respostas = [
  "Opa",
  "Bença vô",
  "QUERO DURMI"
]

if "responding" not in db.keys():
  db["responding"] = True


def update_respostas(respondendo_message):
  if "respostas" in db.keys():
    respostas = db["respostas"]
    respostas.append(respondendo_message)
    db["respostas"] = respostas
  else:
    db["respostas"] = [respondendo_message]

def delete_encouragment(index):
  respostas = db["respostas"]
  if len(respostas) > index:
    del respostas[index]
    db["respostas"] = respostas

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$oi'):
    await message.channel.send("Teu pai tem boi?")

  if db["responding"]:
    options = starter_respostas
    if "respostas" in db.keys():
      options.extend(db["respostas"])

    if any(word in msg for word in palavra_chave):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    respondendo_message = msg.split("$new ",1)[1]
    update_respostas(respondendo_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    respostas = []
    if "respostas" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      respostas = db["respostas"]
    await message.channel.send(respostas)

  if msg.startswith("$list"):
    respostas = []
    if "respostas" in db.keys():
      respostas = db["respostas"]
    await message.channel.send(respostas)

  if msg.startswith("$responder"):
    value = msg.split("$responder ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Pai tá on.")
    else:
      db["responding"] = False
      await message.channel.send("Pai tá off.")

keep_alive()
client.run(os.environ['TOKEN'])