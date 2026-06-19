<!-- --------------------------------------------------------------- -->
<!-- ---------------------- COURSE 7 Triadic FCA ------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 7 - Triadic Formal Concept Analysis, Local Navigation, and Association Rules**

---

## 📖 7.1 Motivation and Background

🔴 **Triadic Formal Concept Analysis (3FCA) is a mathematical extension of standard Formal Concept Analysis (FCA) that handles data characterized by three interacting dimensions (sets)**. 

**Key Idea**: In many real-world datasets, attributes do not simply apply to objects globally. Instead, they apply under specific situations, time-points, or contexts. Flattening this three-dimensional relationship into a two-dimensional grid leads to information loss and bloated structures. 3FCA preserves the third dimension.

### 📑 7.1.1 Common Inherently Triadic Domains
* **Folksonomies (Web Tagging)**: $\text{Users} \times \text{Tags} \times \text{Resources}$.
* **Gene Expression (Bioinformatics)**: $\text{Genes} \times \text{Conditions} \times \text{Time-points}$.
* **Software Evolution**: $\text{Methods} \times \text{Code Smells} \times \text{Versions/Commits}$.
* **Educational Data Mining**: $\text{Students} \times \text{Skills} \times \text{Exercises}$.
* **E-Commerce Recommendations**: $\text{Users} \times \text{Items} \times \text{Contexts}$ (e.g., season, weather, device).
* **Cybersecurity (Network Flows)**: $\text{Source IPs} \times \text{Destination IPs} \times \text{Ports/Protocols}$.
* **Knowledge Graphs (RDF)**: $\text{Subjects} \times \text{Predicates} \times \text{Objects}$.

---

## 📖 7.2 Triadic Contexts and Triconcepts

🔴 **A Triadic Context is a quadruple $\mathbb{K} = (K_1, K_2, K_3, Y)$ consisting of three sets $K_1$, $K_2$, and $K_3$, together with a ternary relation $Y \subseteq K_1 \times K_2 \times K_3$**.
* $K_1$: The set of **objects** ($G$);
* $K_2$: The set of **attributes** ($M$);
* $K_3$: The set of **conditions** or **modi** ($B$).
* $(g, m, b) \in Y$ reads: "Object $g$ has attribute $m$ under condition $b$".

> ### 🖼️ Two Equivalent Views of a Triadic Context
> 1. **Stack of matrices**: A sequence of standard dyadic cross-tables, each representing a single condition $b \in K_3$.
> 2. **3D Boolean Tensor**: A three-way boolean cube representing the presence (1) or absence (0) of incidence.

### 📑 7.2.1 Running Example: "Travelling Researcher"
Let:
* **Objects $K_1$** (Researchers): $\{a, b, c\}$
* **Attributes $K_2$** (Equipment): $\{L = \text{laptop}, \ T = \text{tablet}, \ P = \text{paper}\}$
* **Conditions $K_3$** (Places): $\{\text{Office}, \ \text{Train}, \ \text{Café}\}$

The ternary relation $Y$ consists of 18 triples, represented as a stacked stack of three slices:

**Office Slice**:
| Researcher | Laptop ($L$) | Tablet ($T$) | Paper ($P$) |
| :--- | :---: | :---: | :---: |
| **a** | × | × | × |
| **b** | × |   | × |
| **c** | × | × |   |

**Train Slice**:
| Researcher | Laptop ($L$) | Tablet ($T$) | Paper ($P$) |
| :--- | :---: | :---: | :---: |
| **a** |   | × |   |
| **b** |   |   | × |
| **c** | × | × |   |

**Café Slice**:
| Researcher | Laptop ($L$) | Tablet ($T$) | Paper ($P$) |
| :--- | :---: | :---: | :---: |
| **a** | × | × |   |
| **b** |   | × | × |
| **c** |   | × |   |

---

## 📖 7.3 Derivation Operators

To define formal concepts in three dimensions, we introduce two kinds of derivation operators.

🔴 **The (i)-derivations (one set fixed, one varies)**: For $\{i, j, k\} = \{1, 2, 3\}$, a subset $X \subseteq K_i$, and $Z \subseteq K_j \times K_k$:
$$X^{(i)} = \{ (a_j, a_k) \in K_j \times K_k \mid \forall a_i \in X : (a_1, a_2, a_3) \in Y \}$$
$$Z^{(i)} = \{ a_i \in K_i \mid \forall (a_j, a_k) \in Z : (a_1, a_2, a_3) \in Y \}$$
*Each operator pair $(\cdot)^{(i)}$ forms a standard Galois connection.*

🔴 **The (i, j, $X_k$)-derivations (one dimension and a fixed set)**: For $X_i \subseteq K_i$ and $X_k \subseteq K_k$:
$$X_i^{(i, j, X_k)} = \{ a_j \in K_j \mid \forall a_i \in X_i, \forall a_k \in X_k : (a_1, a_2, a_3) \in Y \}$$

🔴 **The $A_k$-restricted dyadic context** (denoted $\mathbb{K}^{(ij)}_{A_k}$) is the projection obtained by intersecting all slices indexed by $A_k$:
$$\mathbb{K}^{(ij)}_{A_k} = \left( K_i, K_j, Y^{(ij)}_{A_k} \right), \quad \text{where } (a_i, a_j) \in Y^{(ij)}_{A_k} \iff \forall a_k \in A_k : (a_1, a_2, a_3) \in Y$$

---

## 📖 7.4 Triadic Concepts (Triconcepts)

🔴 **A Triadic Concept (or Triconcept) of a triadic context $\mathbb{K}$ is a triple $(A_1, A_2, A_3)$ with $A_i \subseteq K_i$ such that $A_1 \times A_2 \times A_3 \subseteq Y$ and the triple is component-wise maximal**.
* $A_1$: The **extent** (objects);
* $A_2$: The **intent** (attributes);
* $A_3$: The **modus** (conditions).

**Cuboid Intuition**: Visually, a triconcept corresponds to a maximal "all-ones" rectangular cuboid inside the 3D Boolean relation tensor $Y$. Enlarging any single component of the triple introduces at least one zero into the cuboid.

### 📑 7.4.1 Triconcept Trade-Off
In our "Travelling Researcher" example, some valid triconcepts include:
* $(\{a\}, \{L, T, P\}, \{\text{Office}\})$
* $(\{a, c\}, \{L, T\}, \{\text{Office}\})$
* $(\{a, c\}, \{T\}, \{\text{Office, Train, Café}\})$
* $(\{b\}, \{P\}, \{\text{Office, Train, Café}\})$

*Observe the trade-off: enlarging the modus (adding more places) typically forces the extent (researchers) or intent (equipment) to shrink.*

---

## 📖 7.5 Trilattices and Wille's Basic Theorem

In dyadic FCA, concepts are ordered vertically in a single lattice. In triadic FCA, we have three independent directions of growth.

🔴 **The Three Quasi-Orders**: Let $\mathfrak{T}(\mathbb{K})$ be the set of all triconcepts of $\mathbb{K}$. For $\{i, j, k\} = \{1, 2, 3\}$, we define:
$$(A_1, A_2, A_3) \lesssim_i (B_1, B_2, B_3) \iff A_i \subseteq B_i$$
*Crucially, $A_1 \subseteq B_1$ does not imply anything about $A_2$ or $A_3$. The orders are independent.*

🔴 **The Concept Trilattice is the structure $(\mathfrak{T}(\mathbb{K}), \lesssim_1, \lesssim_2, \lesssim_3)$**.

🔴 **Basic Theorem of Triadic FCA (Wille, 1995)**: Every complete trilattice is isomorphic to the concept trilattice of some triadic context.

---

## 📖 7.6 Algorithms for Triconcept Extraction

Because the number of triconcepts can grow exponentially, efficient enumeration is vital.

### 📑 7.6.1 TRIAS (Iceberg Trilattice Mining)
* **Strategy**: Flat-and-extend.
* **Core Idea**: It runs a standard dyadic closed-itemset algorithm (like Next-Closure) on the flattened context $\mathbb{K}^{(1)} = (K_1, K_2 \times K_3, Y^{(1)})$ to extract closed pairs $(A_1, A_2)$. It then computes the maximal modus:
  $$A_3 \leftarrow \{ b \in K_3 \mid \forall (g, m) \in A_1 \times A_2 : (g, m, b) \in Y \}$$
* **Iceberg Filtering**: Allows specifying frequency thresholds $(\tau_1, \tau_2, \tau_3)$ so that only triconcepts with $|A_i| \ge \tau_i$ are computed.

### 📑 7.6.2 Data-Peeler
* **Strategy**: Depth-First Search (DFS) on $n$-ary relations.
* **Core Idea**: For each dimension $i$, it maintains two sets: $C_i$ (items currently in the candidate) and $S_i$ (items potentially addable). It recursively makes branching decisions (adding to $C_i$ vs. removing from $S_i$) and enforces closure checking. It excels at mining dense contexts.

---

## 📖 7.7 The Visualization of Trilattices

Capture-drawing all three quasi-orders in a single planar layout is extremely difficult.

### 📑 7.7.1 Visualization Strategies
1. **Layered Slice Diagrams**: Plot the dyadic concept lattices of each condition $b \in K_3$ side-by-side, drawing dashed lines to connect nodes representing the same triconcept across different layers.
2. **Barycentric (Triangular) Layout**: Place triconcepts inside a triangle where the three corners represent the three components. The position of a node is determined by the relative size of its extent, intent, and modus.
3. **3D Hasse Embeddings**: Embed nodes in 3D space, drawing the three quasi-order edge families in three distinct colors (e.g., solid red for extent, dashed blue for intent, dotted green for modus).
4. **Heatmap / Cuboid View**: Plot the Boolean tensor as a series of 2D slices, overlaying color-coded boundaries of selected triconcepts.

---

## 📖 7.8 Local Navigation in Trilattices (FCA Tools Bundle)

Since drawing a global trilattice is often unreadable (due to edge crossings and clutter), Rudolph, Sacarea, and Troanca (2015) proposed replacing global diagrams with **Local Navigation**.

🔴 **Local Navigation operates by showing the user one triconcept at a time and allowing them to walk the trilattice step-by-step by clicking on reachable neighbors, computed on the fly**.

### 📑 7.8.1 The Six Covering Relations ($R_{i \to j}$)
For $\{i, j, k\} = \{1, 2, 3\}$, the relation $R_{i \to j}((A_1, A_2, A_3), (B_1, B_2, B_3))$ holds if the $i$-th component remains unchanged ($A_i = B_i$), and the $j$-th component $B_j$ is a direct cover above $A_j$ in the concept lattice of the slice context $\mathbb{K}^{(jk)}_{A_i}$. This defines six directed neighborhood families:
$$R_{1 \to 2}, \ R_{1 \to 3}, \ R_{2 \to 1}, \ R_{2 \to 3}, \ R_{3 \to 1}, \ R_{3 \to 2}$$

### 📑 7.8.2 Reachability and Clusters
* 🔴 **Mutual Reachability**: Two triconcepts $T$ and $T'$ are mutually reachable if there exists a directed path between them in both directions.
* 🔴 **Reachability Cluster**: A Strongly Connected Component (SCC) of the neighborhood graph under the $R_{i \to j}$ relations.
* 🔴 **Cubic Contexts**: A context where $Y$ is the main spatial diagonal (i.e., $(i, j, l) \in Y \iff i = j = l$). A cubic context of size $n$ always has exactly $n+1$ clusters.

### 📑 7.8.3 Navigation Operations
* **Standard Cover Move**: Follow one of the six $R_{i \to j}$ relations or their inverses.
* **Element-Wise Move**: Add or drop a specific element from a chosen component, which computes a local closure.
* **Pin-and-Explore**: Fix a subset of attributes or conditions and navigate only within the sub-trilattice satisfying that constraint.

---

## 📖 7.9 Triadic Implications

🔴 **A Conditional Attribute Implication is an expression $A \to B \mid C$ where $A, B \subseteq K_2$ and $C \subseteq K_3$. It holds in $\mathbb{K}$ if every object having all attributes in $A$ under all conditions in $C$ also has all attributes in $B$ under all conditions in $C$**.

🔴 **Theorem (Biedermann)**: $A \to B \mid C$ holds in $\mathbb{K}$ if and only if $A \to B$ holds in the $C$-restricted dyadic context $\mathbb{K}_C$.

> ### 💡 Multi-context implications
> * **Conditional implications**: $A \to B \mid C$ (captures context-dependent rules).
> * **Compound implications**: $(A, C) \to (B, D)$ where $A, B \subseteq K_2$ and $C, D \subseteq K_3$. This treats $K_2 \times K_3$ as a single attribute set.

---

## 📖 7.10 Association Rules in FCA

🔴 **FCA provides a lossless, minimal representation of association rules by replacing all frequent itemsets with closed frequent itemsets (intents)**.

### 📑 7.10.1 The Generic Basis of Association Rules
To represent all association rules without redundancy, we construct two bases:
1. **Duquenne-Guigues (DG) Basis (Exact)**:
   A set of exact rules ($P \to P'' \setminus P$) with confidence $= 1.0$, generated from the pseudo-intents.
2. **Luxenburger Basis (Approximate)**:
   A set of partial rules ($B_1 \xrightarrow{c} B_2$) where $B_1 \prec B_2$ are neighboring intents in the concept lattice, and the confidence is:
   $$c = \frac{\text{support}(B_2)}{\text{support}(B_1)}$$

🔴 **A Triadic Association Rule is an expression $A \to B \mid C$ where $A, B \subseteq K_2$ and $C \subseteq K_3$, parameterized by three thresholds**:
* **Support**: The fraction of objects possessing $A \cup B$ under all conditions in $C$.
* **Confidence**: $\frac{\text{support}(A \cup B, C)}{\text{support}(A, C)}$.
* **Condition Support**: $|C| / |K_3|$.

---

## 📖 7.11 Clarified and Reduced Triadic Contexts

Real-world triadic datasets contain duplicate or logically redundant elements.

🔴 **A Triadic Context is clarified if no two objects, attributes, or conditions have identical slices in the relation $Y$**.

🔴 **An element is reducible if its slice (viewed as a subset of the product of the other two dimensions) can be expressed as the intersection of slices of other elements**. Removing reducible elements shrinks the context without changing the trilattice structure.

### 📑 7.11.1 Wille's Arrow Relations and Reducibility
Wille's dyadic arrows ($\swarrow, \nearrow$) generalize to three families of triadic arrows ($\swarrow_i, \nearrow_i$ for $i \in \{1, 2, 3\}$) on the restricted slices.
* **Reducibility Test**: An element $a_i \in K_i$ is reducible if and only if its restricted slice does not contain any arrow of the form $\swarrow\!\!\!\!\nearrow_i$.

> ### 📊 Case Study: Cancer Registry Data (Toscana2Trias)
> An experimental study on patient records demonstrated the power of triadic reduction:
> * **Original context**: 4,686 objects, 11 attributes, 3 conditions (44,545 triples $\to$ 63 triconcepts).
> * **Clarified context**: 61 objects, 11 attributes, 3 conditions.
> * **Reduced context**: 23 objects, 4 attributes, 3 conditions (only 77 triples).
> * *Result: Data size was reduced by over 99.8% with zero loss of conceptual structure!*

---

## 📖 7.12 Worked Exercise

### 📑 7.12.1 Context Definition
Let $\mathbb{K} = (K_1, K_2, K_3, Y)$ with:
* $K_1 = \{1, 2, 3, 4\}$ (Objects)
* $K_2 = \{a, b, c, d\}$ (Attributes)
* $K_3 = \{\alpha, \beta, \gamma\}$ (Conditions)
* $Y = \{(1,a,\beta), (1,a,\gamma), (1,b,\alpha), (1,b,\beta), (1,c,\alpha), (1,c,\beta), (2,b,\alpha), (2,b,\beta), (2,a,\beta), (2,a,\gamma), (3,a,\beta), (3,a,\gamma), (3,d,\alpha), (4,d,\beta), (4,a,\beta), (4,a,\gamma), (4,b,\alpha), (4,b,\beta)\}$

### 📑 7.12.2 Three Slice Matrices

**Slice $\alpha$**:
| Object | $a$ | $b$ | $c$ | $d$ |
| :--- | :---: | :---: | :---: | :---: |
| **1** | | × | × | |
| **2** | | × | | |
| **3** | | | | × |
| **4** | | × | | |

**Slice $\beta$**:
| Object | $a$ | $b$ | $c$ | $d$ |
| :--- | :---: | :---: | :---: | :---: |
| **1** | × | × | × | |
| **2** | × | × | | |
| **3** | × | | | |
| **4** | × | × | | × |

**Slice $\gamma$**:
| Object | $a$ | $b$ | $c$ | $d$ |
| :--- | :---: | :---: | :---: | :---: |
| **1** | × | | | |
| **2** | × | | | |
| **3** | × | | | |
| **4** | × | | | |

### 📑 7.12.3 Verification of Sample Triconcepts

1. **Triconcept $T_A = (\{1, 2, 3, 4\}, \{a\}, \{\beta, \gamma\})$**:
   * **Incidence Check**: $A_1 \times A_2 \times A_3 = \{1, 2, 3, 4\} \times \{a\} \times \{\beta, \gamma\}$. Every researcher $\{1, 2, 3, 4\}$ has equipment $\{a\}$ in places $\{\beta, \gamma\}$. All these 8 triples are in $Y$.
   * **Maximality Check**:
     * Extent: Cannot add more objects (already includes all objects in $K_1$).
     * Intent: No other attribute is shared by all objects $\{1, 2, 3, 4\}$ in $\{\beta, \gamma\}$ (since Obj 3 only has $\{a\}$ in those slices).
     * Modus: The only other condition is $\alpha$. Do they all have $a$ in $\alpha$? No, none of them have $a$ in $\alpha$.
     * *Maximality holds. $T_A$ is a valid triconcept.*

2. **Triconcept $T_B = (\{1, 2, 4\}, \{a, b\}, \{\beta\})$**:
   * **Incidence Check**: $\{1, 2, 4\} \times \{a, b\} \times \{\beta\} \subseteq Y$. All 6 triples are in $Y$.
   * **Maximality Check**:
     * Extent: Cannot add Obj 3 (Obj 3 lacks $b$ in $\beta$).
     * Intent: No other attribute is shared by $\{1, 2, 4\}$ in $\beta$ (since Obj 1 has $c$ but others do not, and Obj 4 has $d$ but others do not).
     * Modus: Can we add other conditions? No, because they don't all share $b$ in $\gamma$ (Obj 1, 2, 4 do not have $b$ in $\gamma$), and they don't all share $a$ in $\alpha$ (Obj 1, 2, 4 do not have $a$ in $\alpha$).
     * *Maximality holds. $T_B$ is a valid triconcept.*

3. **Triconcept $T_C = (\{1\}, \{b, c\}, \{\alpha, \beta\})$**:
   * **Incidence Check**: $\{1\} \times \{b, c\} \times \{\alpha, \beta\} \subseteq Y$. All 4 triples are in $Y$.
   * **Maximality Check**:
     * Extent: Cannot add Obj 2 or Obj 4 (neither has $c$ in both $\alpha$ and $\beta$).
     * Intent: Cannot add $a$ (Obj 1 lacks $a$ in $\alpha$).
     * Modus: Cannot add $\gamma$ (Obj 1 lacks $b$ and $c$ in $\gamma$).
     * *Maximality holds. $T_C$ is a valid triconcept.*
