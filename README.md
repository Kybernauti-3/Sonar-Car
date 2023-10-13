# Sonar-Car
Auticko ktere jezdi po mistnoti a vytváří její mapu

# Použité součástky

2x Rpi pi pico

[Motory kol](https://www.laskakit.cz/dc-motorek-130-3v-16500-rpm/)

[Otočná kontaktní průchodka, 4 vodiče](https://www.laskakit.cz/otocna-kontaktni-pruchodka--4-vodice/)

[Ultrazvukový senzor vzálenosti](https://www.laskakit.cz/ultrazvukovy-meric-vzdalenosti-hc-sr04/)

[Omniwheels](https://www.printables.com/cs/model/240565-kinisi-mecanum-wheels-model-3-100-mm-10-rollers)

Drátování

# Software tohoto projektu je rozdělen na 3 části:

## 1. Program pro řízení vozítka:
Tento program bude řídit pohyb vozítka v souřadnicovém poli. Bude přijímat příkazy k pohybu a posunutí o určitý počet souřadnic (např. 10 cm) v daném směru. Zahrnuje:

- Řízení motorů omniwheelů pro pohyb ve všech směrech.
- Komunikaci přes sériovou linku s druhou deskou.
- API pro přijímání povelů k pohybu o určitý počet souřadnic v daném směru (dopředu, dozadu, doleva, doprava).
- Překlad příkazů na konkrétní pohyby omni kol pro dosažení požadovaného cíle v souřadnicovém poli.

# 2. Program pro mapování místnosti:
Tento program bude kromě mapování také přijímat aktuální polohu vozítka od skriptu pro řízení vozidla. Zahrnuje:

- Vytváření mapy místnosti, kde jedna jednotka bude reprezentovat 10 cm v reálném světě.
- Přijímání aktuální polohy vozítka od skriptu pro řízení vozidla.
- Aktualizaci mapy na základě nových dat z ultrazvukového senzoru.
- Ukládání dat do pole nebo souboru, který reprezentuje mapu místnosti.
- Poskytování těchto informací skriptu pro řízení vozidla na vyžádání.

# 3. Skript pro řízení vozidla na základě mapy:
Tento skript bude řídit pohyb vozidla na základě aktuální mapy místnosti a bude poskytovat aktuální informace o svém pohybu programu pro mapování. Zahrnuje:

- Pravidelně aktualizovat program pro mapování o svůj aktuální pohyb, včetně souřadnic.
- Analýzu dat z mapy a aktuální polohy k rozhodování, kam se vozidlo má pohybovat.
- Generování příkazů pro pohyb vozidla o určitý počet souřadnic (např. 10 cm) od překážky.
- Odesílání těchto příkazů programu pro řízení vozítka.
- Tímto způsobem bude projekt umožňovat vozítku pohybovat se v místnosti, mapovat prostor a řídit svůj pohyb na základě aktuální mapy.
