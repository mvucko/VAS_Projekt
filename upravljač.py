#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import time

import spade
import spade.message
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State, CyclicBehaviour

status = {
}

def izracunajPoruku() -> []:
    poruke=[]
    global status
    vrijeme=datetime.datetime.fromtimestamp(status.get("date_time"))
    status["temperatura"]=int(status["temperatura"])
    status["vlaga"] = int(status["vlaga"])
    status["svjetlost"] = int(status["svjetlost"])
    if(vrijeme.month>9):
        if (status.get("temperatura") > 12):
            poruke.append("pokrij_0")
        elif (status.get("temperatura") < 10):
            poruke.append("pokrij_1")
        if(status.get("temperatura")<3):
            poruke.append("grijanje_1")
        if(status.get("temperatura") >6):
            poruke.append("grijanje_0")
    else:
        poruke.append("pokrij_0")
        poruke.append("grijanje_0")
    if(status.get("vlaga")<30):
        poruke.append("navodnjavanje_1")
    if (status.get("vlaga") > 60):
        poruke.append("navodnjavanje_0")
    if ((vrijeme.month == 9 or vrijeme.month == 8)):
        if(vrijeme.hour>=19 or vrijeme.hour<8):
            if(status.get("svjetlost") < 10 and status.get("vlaga")>=99):
                poruke.append("zamraci_0")
            else:
                poruke.append("zamraci_1")
    else:
        poruke.append("zamraci_0")
    return poruke

class Drugi(Agent):
    class Radi(CyclicBehaviour):
        async def run(self):
            msg=await self.receive()
            if msg:
                global status
                status = json.loads(msg.body)
                print(status)
                trebamPoslat=izracunajPoruku()
                res=""
                if(len([i for i in trebamPoslat if "navodnjavanje" in i])>0):
                    res = [i for i in trebamPoslat if "navodnjavanje" in i].pop()
                    trebamPoslat.remove(res)
                await self.send(spade.message.Message(
                    to="sender@rec.foi.hr",
                    body="".join(trebamPoslat),
                    metadata={
                        "ontology": "plastenik_najlon",
                        "language": "english",
                        "performative": "inform"}))
                if(len(res)>2):
                    await self.send(spade.message.Message(
                        to="sender@rec.foi.hr",
                        body=res,
                        metadata={
                            "ontology": "plastenik_navodnjavanje",
                            "language": "english",
                            "performative": "inform"}))
                print(f"Posiljatelj: Poruka je poslana!")



    async def setup(self):
        print("Upravljački agent: Starting!")
        igra = spade.template.Template(
            metadata={'ontology': 'plastenik', 'language': 'english', 'performative': 'inform'}
        )
        behaviour = self.Radi()
        self.add_behaviour(behaviour, igra)


if __name__ == '__main__':

    drugi = Drugi("receiver@rec.foi.hr", "secret")
    drugi.start()

    input("Press ENTER to exit.\n")
    drugi.stop()
    spade.quit_spade()
