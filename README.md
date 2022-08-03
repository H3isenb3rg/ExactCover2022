# ExactCover2022
Progetto Algoritmi e Strutture Dati AA 21/22

# Generating Input Files
InputGenerator generates random Sudoku tables to be used as instances for the exact cover problem  
## Parameters
`parameters.cfg` file inside `InputGenerator/app`
*   `base`: Lenght of a side of a single box of the sudoku table (Base=3 for normal sudoku)
*   `rate`: Percentual of numbers to remove from the full sudoku table

## Execution
```bat
python .\InputGenerator\app
```