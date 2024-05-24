# ChessTwoRooksCheckmatePython

Jak coś nie działa to pobrać:
gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe
pip install pycairo
zrestartować kernele i odpalić

Przykładowa schemat matowania dwoma wieżami:
<p align="left">
  <p>
    Skrypt powoduje, że dwie wieże najpierw się z sobą łączą tak, żeby nie dało się ich zbić, najpierw idą na jedną linię.
  </p>
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/5cc8a23f-e5f0-43cb-a45b-4207851dfef6" />    
  <br />
</p>

<p align="left">
  <p>
    Następnie stają obok siebie (poziomo lub pionowo)
  </p>
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/63a1a226-f9a5-4228-b820-602d4b7eec7f" />    
  <br />
</p>

<p align="left">
  W kolejnym kroku biały król udaje się do narożnika do którego ma bliżej niż czarny król, jeżeli w narożniku znajduje się wieża to skrypt zwalnia miejsce w narożniku poruszając wieże o jedno pole, tak, żeby król mógł tam wskoczyć.
  Do obliczenia najkrótszej trasy używamy algorytm A*
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/50de2fa0-c93c-425b-8c20-42fffd5d8d06" />
</p>

<p align="left">
  Po dojściu króla do konkretnego narożnika i złączeniu wież następuje proces matowania (schodkowy)
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/dbc57080-cf67-4b62-a6bc-8064d74b0a5f" />
</p>

<p align="left">
  Z każdym kolejnym ruchem król jest spychany do bocznej linii planszy gdzie ostatecznie zostanie zamatowany
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/9a8fbdf5-d33b-4ec1-8b2a-30f32cfab306" />
</p>

<p align="left">
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/948c7edf-8721-40f8-b9cc-0d71798f2b0b" />
</p>
  Końcowy rezultat matowania

Większość wyjątkowych, nietypowych sytuacji została zawarta w skrypcie.

