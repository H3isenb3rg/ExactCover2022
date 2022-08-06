# ExactCover2022
Progetto Algoritmi e Strutture Dati AA 21/22

# Generating Input Files
## SudoKu Board
InputGenerator generates random Sudoku tables to be used as instances for the exact cover problem  
[Algorithm Used for Sudoku Board Generation](https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python#:~:text=The%20algorithm%20below%20will%20generate%20a%20NxN%20random%20sudoku%20solution%20board%20instantly%20for%20N%20%3C%201000.)  
[Convention used to convert Sudoku Board to Matrix for the exact cover problem](http://www.ams.org/publicoutreach/feature-column/fcarc-kanoodle#:~:text=With%20the%20rules%20explained%20as,boxes%20and%20nine%20possible%20symbols.) (NB: generalized to use different `base` values)
### Parameters
`parameters.cfg` file inside `InputGenerator/app`
*   `base`: Lenght of a side of a single box of the sudoku table (Base=3 for normal sudoku) 
    *   1 < `base` < 31
    *   Recommended to use at most 6
*   `rate`: Percentual of numbers to remove from the full sudoku table
    *   0 < `rate` < 1

### Execution
*   Set parameters in `InputGenerator\app\parameters.cfg`
*   Execute the following command from the root folder:
    ```bat
    python .\InputGenerator\app
    ```
