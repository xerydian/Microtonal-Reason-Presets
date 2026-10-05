# Microtonal Init Presets For Reason

This repo contains presets for multiple Reason Rack devices, grouped by tuning.

To get started,
[download here](https://github.com/xerydian/Microtonal-Init-Presets/archive/refs/heads/main.zip)
and extract it in ~/Music/Reason Studios/User Library

This repo also contains the scripts to generate the presets.
<br>You can tweak the list of tunings, and other settings in `config.py`

```bash
git clone https://github.com/xerydian/Microtonal-Init-Presets
cd Microtonal-Init-Presets
uv run generate-presets
```


### Contents

This pack contains presets in:
- 14edo, 15edo, 16edo, 17edo, 19edo, 22edo, 24edo, 27edo, 29edo,
<br>31edo, 34edo, 36edo, 41edo, 43edo, 53edo
- 44ed6 (~17edo), 49ed6 (~19edo), 57ed6 (~22edo), 70ed6 (~27edo), 88ed6 (~34edo),
- 26edt (double BP), 39edt (triple BP), 22edt (~14edo), 27edt (~~17edo), 30edt (~~19edo), 
<br>43edt (~~27edo), 54edt (~~34edo)
- Wendy Carlos' Alpha, Beta & Gamma
- 38zpi, 39zpi, 42zpi, 45zpi, 47zpi, 51zpi, 53zpi, 56zpi, 59zpi, 61zpi, 65zpi, 70zpi, 
 71zpi, 75zpi, 80zpi, 84zpi, 100zpi, 106zpi, 116zpi, 127zpi, 137zpi, 144zpi, 184zpi, 

For the following Rack instruments:
- **Reason Studio**: Complex-1, Europa, Grain, Parsec, Polytone
- **Third Party**: Arkana, Autosub, BitSynthzr, MonoPoly, Noxious, Rama, Spectra, VK-2 Synthesizer
    - **Synapse Audio**: Antidote, Obsession, The Legend HZ
    - **Lectric Panda**: Nostromo, Torsion
    - **Turn2on**: Blackpole Station, DyingStar


### CV Helpers

Universally microtune (almost) any Rack instrument.
<br>Requires: CV out, CV splitter, x2 Tinker instances, an instrument with Pitch Bend support.
<br>Example setup: 
```
Blamsoft Distributor
  |--> Voice 1 --> CV splitter 
  |                   |--> (In A) Tinker: Note (Result) --> (Note CV) Instrument #1
  |                   |--> (In A) Tinker: Bend (Result) --> (Pitch Bend)
  |--> Voice 2 (Optional) (Same setup)
  |--> ...

(Tweak the 'Number of Voices' parameter accordingly)
```

Note: Some devices don't expose a Pitch Bend CV jack but do accept Pitch Bend input, 
<br>Place the  Combinator to achieve this
- **One voice**: 
  <br>CV Connections (Rear view)
  <br>- Tinker: Bend (Result) --> Combinator (Wheel CV In) Pitch Bend
- **Multiple voices**:
  <br>CV Connections (Rear view)
  <br>- Tinker: Bend (Result) --> Combinator CV1, or CV2, ..., CV8
  <br>Editor mapping (Front view)
  <br>- Source: CV In 1, or CV In 2, ..., CV In 8
  <br>- Target: Pitch Bend
