![roveri](/images/roveri.svg)

# Roveri-server-socket

Yksinkertainen socket-palvelin, jonka kautta TurtleBot 4 ja kaksi yhteistyörobottia saavat tietoa toistensa tiloista.

## Sovelluksen ajaminen

```
python3 sockserver.py
```
Palvelimen voi sammuttaa painamalla Ctrl+c.

## Laitteiden tilat

ABB- ja UR5-yhteistyörobottien tilat ovat
* **waiting** robotti odottaa TurtleBotin saapumista
* **working** robotti suorittaa omaa työkiertoaan
* **ready** robotti on suorittanut oman työkiertonsa

TurtleBotin tilat ovat
* **docked** TurtleBot on telakoitunut latausasemaan
* **moving** TurtleBot on navigoimassa kohti kohdetta tai paikallaan irti latausasemasta
* **onABB** TurtleBot on navigoinut ABB:n viereen
* **onUR5** TurtleBot on navigoinut UR5:n viereen

## Laitteiden nimet
* **abb** ABB CoFa -yhteistyörobotti
* **ur5** UR5-yhteistyörobotti
* **tb4** TurtleBot 4 -mobiilirobotti

## Viestit

![viestit](/images/viestit.png)
Laitteiden lähettämät viestit.

TurtleBot ja yhteistyörobotit saavat palvelimen kautta tietoa toistensa tilasta. Ne myös ilmoittavat palvelimelle tilansa, kun siinä tapahtuu muutos.

Tilakysely-viestit koostuvat komennosta *getState* ja sen laitteen nimestä, jonka tila halutaan tietää. Komento ja laitteen nimi on erotettu toisistaan pilkulla.
```
"getState,myDeviceName"
```
Palvelin palauttaa tilakysely-viestiin viestissä olevan laitteen tilan.

Tilapäivitys-viestit koostuvat komennosta *setState*, laitteen nimestä ja laitteen uudesta tilasta. Pilkkua käytetään tässäkin viestissä erottimena.
```
"setState,myDeviceName,myNewState"
```
Palvelin palauttaa tilapäivitysviestiin "ok". Jos viestissä on jotain väärää (esim. tuntematon tila), palvelin palauttaa viestin "notOk".


## Tekijätiedot

Hannu Hakalahti, Asiantuntija TKI, Seinäjoen ammattikorkeakoulu

## Hanketiedot

* Hankkeen nimi: Autonomiset ajoneuvot esiselvityshanke
* Rahoittaja: Töysän säästöpankkisäätiön tutkimusrahasto
* Aikataulu: 01.08.2023 - 31.06.2024
---
![rahoittajan_logo](/images/toysan_sp_saatio.jpg)

![seamk_logo](/images/SEAMK.jpg)