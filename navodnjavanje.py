#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade



class AgentAutomat(Agent):

    class PonasanjeKA(FSMBehaviour):
        async def on_start(self):
            print("Pokrenut agent za navodnjavanje.")

        async def on_end(self):
            print("Ugasen agent za navodnjavanje.")

    class PustanjeVode(State):
        async def run(self):
            print("Ovo je stanje u kojem je navodnjavanje upaljeno.")
            msg = await self.receive(timeout=5)
            if msg:
                if (msg.body.__contains__("navodnjavanje_1")):
                    self.set_next_state("PustanjeVode")
                else:
                    self.set_next_state("NeRadiNista")
            else:
                self.set_next_state("PustanjeVode")
    class NeRadiNista(State):
        async def run(self):
            print("Ovo je stanje u kojem je navodnjavanje ugaseno.")
            msg = await self.receive(timeout=5)
            if msg:
                if (msg.body.__contains__("navodnjavanje_1")):
                    self.set_next_state("PustanjeVode")
                else:
                    self.set_next_state("NeRadiNista")
            else:
                self.set_next_state("NeRadiNista")


    async def setup(self):
        fsm = self.PonasanjeKA()

        fsm.add_state(name="PustanjeVode", state=self.PustanjeVode())
        fsm.add_state(name="NeRadiNista", state=self.NeRadiNista(), initial=True)

        fsm.add_transition(source="PustanjeVode", dest="NeRadiNista")
        fsm.add_transition(source="NeRadiNista", dest="PustanjeVode")
        fsm.add_transition(source="PustanjeVode", dest="PustanjeVode")
        fsm.add_transition(source="NeRadiNista", dest="NeRadiNista")

        self.add_behaviour(fsm)


if __name__ == '__main__':

    agentautomat = AgentAutomat("sender@rec.foi.hr", "secret")
    pokretanje = agentautomat.start()
    pokretanje.result()

    while agentautomat.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    agentautomat.stop()
    quit_spade()