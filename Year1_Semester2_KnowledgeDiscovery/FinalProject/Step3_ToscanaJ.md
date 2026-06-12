# Step 3: ToscanaJ System & Conceptual Scaling

In order to construct a ToscanaJ system based on the Continuous Casting of Steel dataset, we need to transform quantitative and categorical parameters into a many-valued context and subsequently into conceptual scales.

## 1. Context Construction
Since the dataset has over 17,000 rows, rendering a conceptual lattice for all individual casts would lead to an unreadable diagram (a common issue in FCA known as the "line diagram explosion").
Instead, we aggregated the data, creating "Objects" grouped by `steel_type` and `workpiece_slice_geometry` (e.g., `Arm240_150x150`, `St3sp_150x150`).

## 2. Scale Building
For ToscanaJ, we defined several conceptual scales. Be inventive, the knowledge gems are hidden in the proper discretization!

### A. RUL Scale (Ordinal Scale)
We discretized the Remaining Useful Life (RUL) into three buckets:
- **Low RUL**: <= 200 tons
- **Medium RUL**: 200 - 400 tons
- **High RUL**: > 400 tons

In an Ordinal Scale setup, having High RUL implies having achieved Medium and Low RUL boundaries.
*Extracted Knowledge:* By mapping steel types on this scale, we immediately see which combinations of geometry and steel grade consistently guarantee a long life. For instance, the `St3sp` grade often clusters in lower RUL tiers compared to specific profiles of `Arm240`.

### B. Temperature Scale (Nominal Scale)
Using the median steel temperature, we created a nominal dichotomy: `High_Temp` vs `Low_Temp`.

### C. Alloy Speed Scale (Nominal/Ordinal)
Based on `alloy_speed`, we categorized objects into `Fast_Speed` and `Slow_Speed`.

## 3. Knowledge Extracted via ToscanaJ Paradigm
By joining these scales in ToscanaJ (or mathematically intersecting their formal concepts):
- We observe an implication: `High_Temp` combined with `Fast_Speed` frequently implies a transition towards `Low_RUL`. This means pushing the machine fast at higher temperatures degrades the sleeve rapidly.
- We generated the `.cxt` (Burmeister formal context) files in the `ToscanaJ_Scales` directory. These files (`Steel_Casting_Context.cxt`, `RUL_Ordinal_Scale.cxt`) can be directly imported into ToscanaJ or Concept Explorer (ConExp) to visually navigate the nested line diagrams.

This system acts as a navigation tool for engineers to filter casting conditions and visually see the risk of sleeve failure.
