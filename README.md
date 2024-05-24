# ChessTwoRooksCheckmatePython

Jak coś nie działa to pobrać:
gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe
pip install pycairo
zrestartować kernele i odpalić


## Biblioteki użyte w programie
chess: Biblioteka chess umożliwia symulację gier w szachy, zarówno dla komputera jak i graczy ludzkich, oferując funkcje takie jak sprawdzanie legalności ruchów, wyliczanie wyników partii oraz analizę pozycji.
random: Moduł random dostarcza funkcje do generowania liczb losowych, co jest przydatne w wielu aplikacjach, od generowania losowych ruchów w grze w szachy po tworzenie losowych danych testowe.
time: Moduł time pozwala na mierzenie czasu wykonania operacji lub oczekiwania na określony czas, co może być użyteczne w programach wymagających precyzyjnego śledzenia czasu, np. w symulacjach gier.
chess.svg: Moduł chess.svg z biblioteki chess umożliwia generowanie reprezentacji stanu szachowego w formacie SVG, co jest przydatne do tworzenia graficznych prezentacji gier szachowych.
cairosvg: CairoSVG to narzędzie do konwersji plików SVG na inne formaty, takie jak PNG czy PDF, co pozwala na łatwe przetwarzanie i wyświetlanie grafiki w różnych aplikacjach.
ImageTk: Moduł ImageTk jest częścią biblioteki Pillow i służy do integracji obrazów Pythona z interfejsem Tkinter, umożliwiając wyświetlanie obrazów w aplikacjach GUI.
tkinter: Tkinter to standardowa biblioteka GUI w Pythonie, która umożliwia tworzenie prostych i zaawansowanych interfejsów użytkownika, oferując elementy takie jak okna, przyciski, pola tekstowe i wiele innych.


## Przykładowa schemat matowania dwoma wieżami:
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
  Przykład algorytmu A* w kodzie.
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/1dc6aacd-8cde-46ea-9cad-998b1c1f139f" />
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

Wyjątek, schowania króla do rogu
<p align="left">
  <img src="https://github.com/KonraW/ChessTwoRooksCheckmatePython/assets/64143856/cef746ba-7294-4984-a4a0-e5a3e4840965" />
</p>


