import asyncio
import datetime
import json
import random
import time

import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour, OneShotBehaviour

status = {
    "temperatura": 20,
    "vlaga": 80,
    "svjetlost": 40,
    "date_time": 1234
}


class Posiljatelj(Agent):
    class PosaljiPoruku(OneShotBehaviour):
        async def run(self):

            await asyncio.sleep(1)
            await self.send(spade.message.Message(
                to="receiver@rec.foi.hr",
                body=json.dumps(status),
                metadata={
                    "ontology": "plastenik",
                    "language": "english",
                    "performative": "inform"}))
            print(f"Posiljatelj: Poruka je poslana!")
            await asyncio.sleep(1)

    async def setup(self):
        print("Posiljatelj: Pokrećem se!")
        ponasanje = self.PosaljiPoruku()
        self.add_behaviour(ponasanje)

if __name__ == '__main__':
    posiljatelj = Posiljatelj("mislav.vucko@rec.foi.hr", "Kulsifra69")
    while True:
        laststatus=status

        laststatus["temperatura"]=input('Temperatura: ')
        laststatus["vlaga"] = input('Vlaga: ')
        laststatus["svjetlost"] = input('Svjetlost: ')
        date_entry = input('Vrijeme YYYY-MM-DD-HH-mm format: ')
        year, month, day, hour, minute = map(int, date_entry.split('-'))
        date1 = datetime.datetime(year, month, day, hour, minute)
        laststatus["date_time"]=date1.timestamp()
        status=laststatus
        posiljatelj.start()
        posiljatelj.stop()
        time.sleep(3)
    input("Press ENTER to exit.\n")
    spade.quit_spade()
