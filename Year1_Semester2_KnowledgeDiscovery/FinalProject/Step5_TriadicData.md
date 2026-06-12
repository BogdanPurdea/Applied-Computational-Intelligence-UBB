# Step 5: Triadic Data Analysis

Formal Concept Analysis traditionally deals with dyadic contexts (Objects $\times$ Attributes). However, many real-world datasets naturally exhibit a triadic structure (Objects $\times$ Attributes $\times$ Conditions).

## 1. Triadic Context Construction
We derived a triadic context from the Continuous Casting dataset:
- **Objects ($O$):** `steel_type` (e.g., Arm240, St3sp)
- **Attributes ($A$):** Predominant performance traits (`Low_RUL`, `High_RUL`, `High_Temp`, `Low_Temp`)
- **Conditions ($C$):** `Cast_Stage`, derived from `cast_in_row`. We define `Initial_Casts` (1st to 3rd cast) and `Subsequent_Casts` (>3).

A triplet $(o, a, c) \in Y$ means: "The steel type $o$ exhibits attribute $a$ under condition $c$".

## 2. Triadic Knowledge Discovery
By cross-tabulating the data, we discovered several interesting triadic relationships (Triadic Concepts):

### Concept 1: The Stability of `Arm240`
**Objects:** {`Arm240`}
**Attributes:** {`High_RUL`}
**Conditions:** {`Initial_Casts`, `Subsequent_Casts`}
*Interpretation:* The Arm240 steel grade consistently demonstrates a high Remaining Useful Life regardless of whether it is poured in the initial phase of the sequence or during subsequent casts. This implies the casting parameters for Arm240 are highly optimized and stable over time.

### Concept 2: The Thermal Shift of `St3sp`
**Objects:** {`St3sp`}
**Attributes:** {`High_Temp`, `Low_RUL`}
**Conditions:** {`Subsequent_Casts`}
*Interpretation:* When casting the `St3sp` grade in subsequent runs (cast in row > 3), the predominant temperature is high, which strongly coincides with a Low RUL. In initial casts, `St3sp` might not be as hot or destructive, but as the casting sequence lengthens, thermal buildup leads to rapid sleeve degradation.

## 3. Conclusions from Triadic Analysis
Triadic FCA allows us to see how relationships between objects and attributes evolve or depend on external conditions. In this case, sequence position (`cast_in_row`) acts as a crucial dimension. We learned that the degradation of the crystallizer sleeve is not just a function of the steel type, but a function of the *steel type in the context of the operational sequence*.
