
## Project Structure

This project is structured as follows:

- **scripts:** Python scripts used for conducting analysis and generating results.
- **Data:** Contains the model used in our experiments.
- **results:** Output from scripts, for sample set analysis.
- **test_results_mar:** Output from scripts, for test set analysis.
- **MAP_MAR_data.csv**: Contains metrics such as MAP/MAR for various datasets with differing configurations of exponent bits and mantissa bits. Used in Figures 4, 7, and Table 1.
- **AAI_mult**: chisel code avaliable for building hardware
- **floating_mult**: chisel code avaliable for building hardware
- **floating_add**: chisel code avaliable for building hardware

### Recreating Data

1. **Generate MAP/MAR data with different exponent bits, mantisssa bits for Figures 4, 7, and Table 1**:
    ```
    sbatch run.sh
    ```
2. **Resampling**:
    ```
    sbatch run_sample.sh 
    ```
3. **replacement for Figure 6 and Table 4**:
    ```
    sbatch run_replacement.sh 
    ```
4. **figure8**:
    use 'numerical_loss_before' for plot of before error correction
    ```
    python3 analysis.py
    ```
5. **figure9**:
    use data in folder test_results_mar 
    ```
    python3 analysis.py
    ```

