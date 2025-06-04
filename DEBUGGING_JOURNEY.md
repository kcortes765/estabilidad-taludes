# Debugging Journey: Slope Stability Analysis

This document outlines the key problems encountered during the development and debugging of the slope stability analysis software, primarily focusing on the "Caso Crítico Realista," and the steps taken to address them.

## 1. Initial Core Problem

The most persistent issue was the failure of analyses for specific test cases, notably the "Caso Crítico Realista." This manifested as critical errors:
- For Bishop's Modified Method: `"Suma de fuerzas actuantes ≤ 0: superficie de falla inválida"`
- For Fellenius's Method: `"Momento actuante ≤ 0: superficie de falla inválida"`

These errors indicated that the calculated driving forces or moments were negative or zero, which is physically unrealistic for a typical failure mechanism and incompatible with the Factor of Safety (FS) calculation formulas.

## 2. Debugging Dovela Creation and Geometric Issues

Early investigations pointed towards problems with the geometry of the failure surface and the discretization into dovelas (slices).

### Problem: Invalid Dovela Heights
- **Symptom:** Some failure circle geometries initially caused dovelas to have negative or zero heights. This occurred when the defined failure circle was positioned too high relative to the ground surface, or its radius was too small, leading to parts of the circle being above ground at the toe or crest.
- **Example Initial Circle (Problematic):** `CirculoFalla(xc=20, yc=15, radio=18)` for "Caso Crítico Realista".

- **Attempts & Solutions:**
    1.  **Enhanced Debugging:** Added extensive `print` statements within `core.geometry.crear_dovelas` to output detailed properties (coordinates, heights, angles, weights, pore pressures) for each dovela during its creation. This helped pinpoint where and why dovelas were failing.
    2.  **Geometry Adjustment (Y-coordinate):** The `yc` (y-coordinate of the circle center) for "Caso Crítico Realista" in `casos_literatura_adaptados.py` was adjusted downwards (e.g., from `15` to `9.8`). This successfully lowered the circle, ensuring all dovelas could be created with positive heights.
    3.  **Refined Toe Failure Circle:** The circle geometry was further refined to a more realistic toe failure configuration: `CirculoFalla(xc=22, yc=2.67, radio=13)`. This change aimed to produce more plausible dovela angles and ensure all dovelas were geometrically valid.

## 3. Addressing "Suma de Fuerzas Actuantes / Momento Actuante ≤ 0"

Even after all dovelas were created with valid geometric properties, the core error of non-positive acting forces/moments persisted for the `CirculoFalla(xc=22, yc=2.67, radio=13)` configuration.

- **Investigation & Realization (Sign Convention):**
    - A detailed review of the `alpha` angle (angle of the dovela base with the horizontal) and the weight (`W`) of each dovela was conducted.
    - The `alpha` angle was defined as positive if the tangent to the base sloped upwards to the right.
    - For a typical left-to-right failure, dovelas contributing to the driving force (generally on the left and middle parts of the slip surface, where the base slopes *downwards* to the right) would have a *negative* `alpha`. Consequently, `sin(alpha)` would be negative for these driving dovelas.
    - Dovelas contributing to resistance (generally at the toe on the right, where the base slopes *upwards* to the right) would have a *positive* `alpha`, making `sin(alpha)` positive.
    - The sum `Sum[W*sin(alpha)]` was therefore negative for the "Caso Crítico Realista" (e.g., -12.19 in one debug run).
    - **Key Insight:** Conventional formulations of Bishop's and Fellenius's methods define the Factor of Safety as `Sum_Resisting_Forces_Moments / Sum_Driving_Forces_Moments`, where `Sum_Driving_Forces_Moments` is expected to be a positive value. Our direct summation of `W*sin(alpha)` was yielding a negative value, which was then incorrectly used as the denominator.

- **Solutions (Inverting the Sign):**
    1.  **Fix for Bishop's Method:**
        - The function `calcular_fuerza_actuante_bishop` in `core/bishop.py` originally returned `dovela.peso * dovela.sin_alpha`.
        - This was changed to `return -(dovela.peso * dovela.sin_alpha)`.
        - This effectively changed the sign of each dovela's contribution to the sum of acting forces, making the total `suma_actuantes` positive as required by the FS formula and the validation check `if suma_actuantes <= 0`.
    2.  **Fix for Fellenius's Method:**
        - A similar issue affected the `momento_actuante` in Fellenius, which is calculated as `Sum[W*sin(alpha)*Radio]`.
        - The function `calcular_fuerza_actuante_dovela` in `core/fellenius.py` (which contributes to the acting moment calculation) was also changed from `return dovela.peso * dovela.sin_alpha` to `return -(dovela.peso * dovela.sin_alpha)`.
        - This ensures that the sum of these terms, and thus the `momento_actuante`, becomes positive.

## 4. Auxiliary Fixes during Debugging

- **Focused Test Execution:** The script `casos_literatura_adaptados.py` was modified to execute *only* the "Caso Crítico Realista" during intensive debugging phases. This reduced output clutter and allowed for quicker iteration.
- **Python Formatting Errors:** Encountered and fixed `ValueError` exceptions in `casos_literatura_adaptados.py` related to incorrect f-string formatting. This typically involved complex conditional statements within the format specifiers. The solution was to refactor these print statements by preparing the conditional parts of the string in intermediate variables before the final f-string construction.

## 5. Current Status and Next Steps

- With the sign conventions for acting forces/moments corrected in both `core/bishop.py` and `core/fellenius.py`, and f-string formatting errors resolved, the `casos_literatura_adaptados.py` script is expected to run without Python runtime errors.
- Both Bishop's and Fellenius's methods should now complete their calculations and produce Factors of Safety for the "Caso Crítico Realista."
- **Next Steps:**
    1.  Re-run `casos_literatura_adaptados.py` to generate fresh `debug_output.txt`.
    2.  Carefully examine `debug_output.txt` to confirm that both methods provide FS values and that no new errors have been introduced.
    3.  Compare the calculated FS values for "Caso Crítico Realista" against expected literature values. While the sign issue is resolved, the specific geometry (`xc=22, yc=2.67, radio=13`) might still yield FS values that differ from benchmarks, potentially requiring further geometric refinement or parameter adjustments for precise validation.
    4.  Once confirmed, proceed with committing all changes to Git.
