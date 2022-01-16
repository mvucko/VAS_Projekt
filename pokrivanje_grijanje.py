#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from argparse import ArgumentParser

class AgentAutomat(Agent):

    class PonasanjeKA(FSMBehaviour):
        async def on_start(self):
            print("Pokrenut agent za pokrivanje i grijanje.")

        async def on_end(self):
            print("Ugasen agent za pokrivanje i grijanje.")

    class BudiZamracen(State):
        async def run(self):
            print("Plastenik je zatvoren, CRNI najlon.")
            msg = await self.receive(timeout=5)
            if msg:
                print(f"Primljena poruka : {msg.body} \n Odmracujem.")
                if msg.body.__contains__("zamraci_0"):
                    self.set_next_state("BudiOtkriven")
                else:
                    self.set_next_state("BudiZamracen")
            else:
                self.set_next_state("BudiZamracen")

    class BudiOtkriven(State):
        async def run(self):
            print("Plastenik otkriven.")
            msg = await self.receive(timeout=5)
            if msg:
                if(msg.body.__contains__("zamraci_1")):
                    self.set_next_state("BudiZamracen")
                if (msg.body.__contains__("pokrij_1")):
                    self.set_next_state("BudiPokriven")
            else:
                self.set_next_state("BudiOtkriven")

    class BudiPokriven(State):
        async def run(self):
            print("Plastenik zatvoren PROZIRNIM najlonom.")
            msg = await self.receive(timeout=5)
            if msg:
                if (msg.body.__contains__("pokrij_1")):
                    if(msg.body.__contains__("grijanje_1")):
                        self.set_next_state("UkljucenoGrijanje")
                    else:
                        self.set_next_state("BudiPokriven")
                elif (msg.body.__contains__("pokrij_0")):
                    self.set_next_state("BudiOtkriven")
                else:
                    self.set_next_state("BudiPokriven")
            else:
                self.set_next_state("BudiPokriven")

    class UkljucenoGrijanje(State):
        async def run(self):
            print("PROZIRNI najlon i grijalica je uključena.")
            msg = await self.receive(timeout=5)
            if msg:
                if (msg.body.__contains__("grijanje_1")):
                    self.set_next_state("UkljucenoGrijanje")
                else:
                    self.set_next_state("BudiPokriven")
            else:
                self.set_next_state("UkljucenoGrijanje")

    async def setup(self):
        fsm = self.PonasanjeKA()

        fsm.add_state(name="BudiZamracen", state=self.BudiZamracen())
        fsm.add_state(name="UkljucenoGrijanje", state=self.UkljucenoGrijanje())
        fsm.add_state(name="BudiPokriven", state=self.BudiPokriven())
        fsm.add_state(name="BudiOtkriven", state=self.BudiOtkriven(), initial=True)

        fsm.add_transition(source="BudiZamracen", dest="BudiZamracen")
        fsm.add_transition(source="UkljucenoGrijanje", dest="UkljucenoGrijanje")
        fsm.add_transition(source="BudiPokriven", dest="BudiPokriven")
        fsm.add_transition(source="BudiOtkriven", dest="BudiOtkriven")

        fsm.add_transition(source="BudiOtkriven", dest="BudiZamracen")
        fsm.add_transition(source="BudiOtkriven", dest="BudiPokriven")

        fsm.add_transition(source="BudiZamracen", dest="BudiOtkriven")
        fsm.add_transition(source="BudiPokriven", dest="BudiOtkriven")
        fsm.add_transition(source="BudiPokriven", dest="UkljucenoGrijanje")
        fsm.add_transition(source="UkljucenoGrijanje", dest="BudiPokriven")


        self.add_behaviour(fsm)


if __name__ == '__main__':

    agentautomat = AgentAutomat("sender@rec.foi.hr", "secret")
    pokretanje = agentautomat.start()
    pokretanje.result()  # priÄŤekamo kraj pokretanja agenta

    while agentautomat.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    agentautomat.stop()
    quit_spade()