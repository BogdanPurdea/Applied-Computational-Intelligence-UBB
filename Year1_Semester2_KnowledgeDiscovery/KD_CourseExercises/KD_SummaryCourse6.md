<!-- --------------------------------------------------------------- -->
<!-- ---------------------- COURSE 6 Implications ------------------ -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 6 - Implications in FCA, the Stem Base, and the Next-Closure Algorithm**

---

## 📖 6.1 Motivation and Background

🔴 **Attribute Implications represent strict rules indicating that if an object possesses a certain set of attributes, it must also possess another set of attributes**. They allow us to capture exact, deterministic dependencies directly from a data table.

**Key Idea**: In classical Formal Concept Analysis (FCA), we use concept lattices to study the hierarchical grouping of objects and attributes. However, lattices can grow exponentially. Implications provide a compact, lossless, and alternative representation of the exact same structured knowledge.

🔴 **Benefits**: 
* **Knowledge Compression**: Instead of storing thousands of redundant rules, we can find a minimal set of implications that generates all others.
* **Explainability**: Implications correspond to Horn clauses in logic and functional dependencies in database systems, making them highly readable and interpretable.

---

## 📖 6.2 Attribute Implications: Definitions and Semantics

🔴 **An Attribute Implication over an attribute set $M$ is an expression $A \to B$ where $A, B \subseteq M$**.
* $A$ is the **premise** (or antecedent);
* $B$ is the **conclusion** (or consequent).

🔴 **An implication $A \to B$ holds in a formal context $\mathbb{K} = (G, M, I)$** (denoted $\mathbb{K} \models A \to B$) **if and only if every object that has all attributes in $A$ also has all attributes in $B$**. Mathematically, this is equivalent to:
$$A \to B \text{ holds in } \mathbb{K} \iff A' \subseteq B' \iff B \subseteq A''$$

🔴 **Respecting Implications (Models)**: A subset $T \subseteq M$ **respects** (or models) an implication $A \to B$ if:
$$A \not\subseteq T \quad \text{or} \quad B \subseteq T$$
*(i.e., if $T$ contains the premise $A$, it must also contain the conclusion $B$.)*

> ### 📄 Connection to Intents
> The closed attribute sets (intents) of a context $\mathbb{K}$ are exactly those subsets of $M$ that respect all implications that hold in $\mathbb{K}$.

---

## 📖 6.3 The Semantic Closure Operator and Armstrong's Axioms

🔴 **The Implicational Closure of a set $T \subseteq M$ under a set of implications $\mathcal{L}$** (denoted $T^+_{\mathcal{L}}$) **is the smallest superset of $T$ that respects all implications in $\mathcal{L}$**:
$$T^+_{\mathcal{L}} = \bigcap \{ S \supseteq T \mid S \text{ respects all implications in } \mathcal{L} \}$$

### 📑 6.3.1 Forward Chaining Algorithm
To compute $T^+_{\mathcal{L}}$:
1. **Start**: Initialize $S \leftarrow T$.
2. **Rule Application**: For each $A \to B \in \mathcal{L}$: if $A \subseteq S$, then update $S \leftarrow S \cup B$.
3. **Loop**: Repeat step 2 until no further attributes can be added to $S$.
4. **Return**: Return $S$.

### 📑 6.3.2 Armstrong's Axioms (Inference Rules)
To derive implications from a set of implications $\mathcal{L}$ without looking at the context, we use **Armstrong's Axioms**:
* **Reflexivity**: If $B \subseteq A$, then $A \to B$ is always true.
* **Augmentation**: If $A \to B$, then $A \cup C \to B \cup C$ for any $C \subseteq M$.
* **Transitivity**: If $A \to B$ and $B \to C$, then $A \to C$.

**Derived Rules**:
* **Union**: If $A \to B$ and $A \to C$, then $A \to B \cup C$.
* **Decomposition**: If $A \to B \cup C$, then $A \to B$ and $A \to C$.
* **Pseudotransitivity**: If $A \to B$ and $B \cup C \to D$, then $A \cup C \to D$.

---

## 📖 6.4 Implication Bases: Soundness, Completeness, and Minimality

🔴 **An Implication Base $\mathcal{L}$ for a context $\mathbb{K}$ is a set of implications that is both sound and complete**:
1. **Soundness**: Every implication in $\mathcal{L}$ holds in $\mathbb{K}$.
2. **Completeness**: Any implication $A \to B$ that holds in $\mathbb{K}$ can be derived from $\mathcal{L}$ (i.e., $B \subseteq A^+_{\mathcal{L}}$).

🔴 **Redundancy**: An implication $A \to B \in \mathcal{L}$ is **redundant** if it can be derived from the remaining implications $\mathcal{L} \setminus \{A \to B\}$. A base is **non-redundant** if it contains no redundant implications.

🔴 **Minimality**: A base is **minimum** (or optimal) if it contains the absolute minimum number of implications among all possible sound and complete bases.

---

## 📖 6.5 Pseudo-Closed Sets (Pseudo-Intents)

🔴 **A subset $P \subseteq M$ is a Pseudo-Closed Set (or Pseudo-Intent) of a context if and only if**:
1. $P \neq P''$ (it is not a closed set);
2. For every pseudo-closed set $Q \subsetneq P$, we have $Q'' \subseteq P$.

**Intuition**: Pseudo-intents are "minimal non-closed sets". They represent the exact premises of the implications that cannot be derived from smaller rules.

---

## 📖 6.6 The Stem Base (Duquenne-Guigues Base)

🔴 **The Stem Base (also known as the Duquenne-Guigues Base or Canonical Base) is defined as the set of implications**:
$$\mathcal{S} = \{ P \to P'' \mid P \text{ is a pseudo-intent of } \mathbb{K} \}$$

🔴 **Duquenne-Guigues Theorem (1986)**: The stem base $\mathcal{S}$ is the **unique minimum implication base** of a finite formal context $\mathbb{K}$.

| Feature Base | Uniqueness | Minimum Size? | Computational Source |
| :--- | :---: | :---: | :--- |
| **Direct Base** | No | No | Derived directly from context |
| **Non-Redundant Base** | No | No | Pruned via subset checks |
| **Stem / Canonical Base** | **Yes** | **Yes** | Computed via **Next-Closure** |

---

## 📖 6.7 Lectic Ordering and the Candidate Operator ($\oplus_i$)

To compute closed sets and pseudo-intents without checking every subset of $2^|M|$ (which is exponential), Ganter introduced a lexicographic order.

🔴 **Lectic Order ($<_{lec}$)**: Fix an order on attributes $m_1 < m_2 < \dots < m_n$. For two subsets $A, B \subseteq M$, we say $A$ is lectically smaller than $B$ at position $i$ (denoted $A <_i B$) if:
$$i \notin A, \quad i \in B, \quad \text{and} \quad A \cap \{m_1, \dots, m_{i-1}\} = B \cap \{m_1, \dots, m_{i-1}\}$$
We write $A <_{lec} B$ if $A <_i B$ for some attribute $i$.

> ### 💡 Binary Counting Analogy
> If we represent subsets as bit-strings (with $m_1$ as the most significant bit and $m_n$ as the least significant bit), the lectic order corresponds exactly to the standard binary counting order (from $0000$ to $1111$).

🔴 **The Candidate Operator ($\oplus_i$)**: For a subset $A \subseteq M$ and attribute $m_i \in M$, the candidate $A \oplus_i$ is the lectically next set obtained by keeping all attributes before $m_i$, adding $m_i$, and discarding all attributes after $m_i$:
$$A \oplus_i = (A \cap \{m_1, \dots, m_{i-1}\}) \cup \{m_i\}$$

---

## 📖 6.8 The Next-Closure Algorithm (Ganter 1984)

🔴 **The Next-Closure algorithm is a method that enumerates all closed sets in lectic order, starting from the closure of the empty set $\phi(\emptyset)$**.

### 📑 6.8.1 Next-Closure Logic
Given the current closed set $A$, to find the lectically next closed set:
1. Scan the attributes $m_i$ from right-to-left (largest $m_n$ down to smallest $m_1$):
2. If $m_i \notin A$:
   * Form the candidate $P = A \oplus_i = (A \cap \{m_1, \dots, m_{i-1}\}) \cup \{m_i\}$.
   * Compute its closure $B = \phi(P) = P''$.
   * Check if $B$ agrees with $A$ on all elements before $m_i$:
     $$B \cap \{m_1, \dots, m_{i-1}\} = A \cap \{m_1, \dots, m_{i-1}\}$$
   * If this check passes, then $B$ is the next closed set. Set $A \leftarrow B$ and break the loop.

---

## 📖 6.9 Stem Base via Next-Closure Algorithm

🔴 **By integrating pseudo-intent recognition into Next-Closure, we can compute the Stem Base and all closed sets simultaneously**. When the lectic check for a candidate $P = A \oplus_i$ fails, it indicates that $P$ is not closed. If $P$ contains the closures of all its proper pseudo-closed subsets, then $P$ is a pseudo-intent, and we add $P \to P''$ to our stem base.

### 📑 6.9.1 Step-by-Step Integrated Pseudocode
```python
Algorithm: Stem-Base-Next-Closure
Input: Context K = (G, M, I), Attribute order m_1 < m_2 < ... < m_n
Output: Stem Base S, All Closed Sets (Intents)

S = []
A = closure(empty_set)
output A

while A != M:
    for i from n down to 1:
        if m_i not in A:
            P = (A intersect {m_1, ..., m_{i-1}}) union {m_i}
            B = closure(P)
            
            # Check if B agrees with A on prefix
            if (B intersect {m_1, ..., m_{i-1}}) == (A intersect {m_1, ..., m_{i-1}}):
                if P != B:
                    # P is a pseudo-intent
                    S.append(P -> B)
                A = B
                output A
                break
return S
```

---

## 📖 6.10 Python Implementation

Here is a complete, clean Python implementation of the closure and stem base algorithms.

```python
def closure(context, B):
    """
    Computes B'' (attribute closure) in a formal context.
    context: dict {object_id: set_of_attributes}
    B: frozenset of attributes
    """
    if not B:
        objects = set(context.keys())
    else:
        objects = {g for g, attrs in context.items() if B.issubset(attrs)}
        
    if not objects:
        all_attrs = set()
        for attrs in context.values():
            all_attrs.update(attrs)
        return frozenset(all_attrs)
        
    objs_list = list(objects)
    result = set(context[objs_list[0]])
    for g in objs_list[1:]:
        result.intersection_update(context[g])
    return frozenset(result)

def implicational_closure(S, B):
    """
    Computes B+ (implicational closure) under implication set S.
    S: list of (premise, conclusion) tuples
    B: frozenset of attributes
    """
    T = set(B)
    changed = True
    while changed:
        changed = False
        for premise, conclusion in S:
            if premise.issubset(T):
                new_T = T | conclusion
                if len(new_T) > len(T):
                    T = new_T
                    changed = True
    return frozenset(T)

def stem_base(context, attributes):
    """
    Computes the stem base (canonical implication base) using Next-Closure.
    attributes: ordered list of attributes [m1, m2, ..., mn]
    """
    phi = lambda B: closure(context, B)
    S = []
    A = phi(frozenset())
    n = len(attributes)
    
    while A != frozenset(attributes):
        found = False
        for i in range(n - 1, -1, -1):
            mi = attributes[i]
            if mi not in A:
                prefix = frozenset(attributes[:i])
                P = (A & prefix) | {mi}
                B = implicational_closure(S, P)
                
                # Check prefix agreement
                if B & prefix == A & prefix:
                    B_dp = phi(B)
                    if B != B_dp:
                        # B is a pseudo-intent!
                        S.append((B, B_dp))
                        # continue loop to find the next closed set
                    else:
                        A = B
                        found = True
                        break
        if not found:
            A = frozenset(attributes)
            
    return S

```

---

## 📖 6.11 Worked Example: Technology Features Context

### 📑 6.11.1 Formal Context
Let $M = \{a, b, c, d, e\}$ representing:
* $a$: auth, $b$: logging, $c$: caching, $d$: encryption, $e$: monitoring.

Suppose we have the following systems (objects) in our database:
* **Sys1**: $\{a, b, c\}$
* **Sys2**: $\{a, d, e\}$
* **Sys3**: $\{b, c, e\}$
* **Sys4**: $\{d, e\}$
* **Sys5**: $\{a, b, d\}$

| System | auth ($a$) | logging ($b$) | caching ($c$) | encryption ($d$) | monitoring ($e$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Sys1** | × | × | × |   |   |
| **Sys2** | × |   |   | × | × |
| **Sys3** |   | × | × |   | × |
| **Sys4** |   |   |   | × | × |
| **Sys5** | × | × |   | × |   |

### 📑 6.11.2 Closed Sets and Pseudo-Intents Computation
Executing the closure operator on this corrected context gives:
* **Closed Sets (Intents)**: $\emptyset, \{e\}, \{d\}, \{d, e\}, \{b\}, \{b, c\}, \{b, c, e\}, \{a\}, \{a, d\}, \{a, d, e\}, \{a, b\}, \{a, b, d\}, \{a, b, c\}, M$.
* **Pseudo-Intents and Stem Base**:
  1. $\{c\}$ (closure is $\{b, c\}$) $\implies$ Implication: $\{c\} \to \{b\}$ (caching implies logging)
  2. $\{b, e\}$ (closure is $\{b, c, e\}$) $\implies$ Implication: $\{b, e\} \to \{c\}$ (logging + monitoring implies caching)
  3. $\{b, d\}$ (closure is $\{a, b, d\}$) $\implies$ Implication: $\{b, d\} \to \{a\}$ (logging + encryption implies auth)
  4. $\{a, e\}$ (closure is $\{a, d, e\}$) $\implies$ Implication: $\{a, e\} \to \{d\}$ (auth + monitoring implies encryption)
  5. $\{a, b, c, d\}$ (closure is $M$) $\implies$ Implication: $\{a, b, c, d\} \to \{e\}$ (auth + logging + caching + encryption implies monitoring)

---

## 📖 6.12 Practical Connections: Database Theory, Logic, and AI

* **Database Functional Dependencies (FDs)**: In relational databases, attributes represent columns and tuples represent rows. An FD $X \to Y$ means the values in columns $X$ determine the values in columns $Y$. The **canonical cover** of FDs in database theory is mathematically equivalent to the **stem base** in FCA!
* **Propositional Logic**: Implications are equivalent to Horn clauses ($p \land q \to r$). The forward chaining closure algorithm corresponds directly to unit propagation in SAT solvers.
* **Interactive Knowledge Acquisition (Attribute Exploration)**: When the exact formal context is not fully known, we can interactively compute the stem base. The algorithm generates candidate implications and asks a domain expert to confirm them. If the expert rejects a rule, they must provide a counterexample, which is added as a new object in the context, dynamically refining the lattice.

---

## 📖 6.13 Practice Problems

### 📑 6.13.1 Practice Problem 1
Given the context with attributes $M = \{p, q, r, s\}$ and 5 objects:

| Object | $p$ | $q$ | $r$ | $s$ |
| :--- | :---: | :---: | :---: | :---: |
| **1** | × | × | | |
| **2** | | × | × | |
| **3** | | | × | × |
| **4** | × | | | × |
| **5** | × | | × | |

#### 📝 Tasks:
1. Compute $\{p, r\}''$ and $\{q, s\}''$.
2. List all closed sets in lectic order.
3. Identify all pseudo-intents.
4. Write out the stem base.

#### 💡 Solutions:
1. **Closures**:
   * $\{p, r\}' = \{1, 4, 5\} \cap \{2, 3, 5\} = \{5\}$. Thus $\{p, r\}'' = \{5\}' = \{p, r\}$ (Closed).
   * $\{q, s\}' = \{1, 2\} \cap \{3, 4\} = \emptyset$. Thus $\{q, s\}'' = \emptyset' = \{p, q, r, s\}$ (Not Closed).

2. **Closed Sets in Lectic Order** ($p < q < r < s$):
   $$\emptyset, \{s\}, \{r\}, \{r, s\}, \{q\}, \{q, r\}, \{p\}, \{p, s\}, \{p, r\}, \{p, q\}, \{p, q, r, s\}$$

3. **Pseudo-Intents**:
   * $\{q, s\}$ (closure is $M$)
   * $\{p, q, r\}$ (closure is $M$)
   * $\{p, r, s\}$ (closure is $M$)

4. **Stem Base**:
   $$\mathcal{S} = \{ \{q, s\} \to \{p, r\}, \ \{p, q, r\} \to \{s\}, \ \{p, r, s\} \to \{q\} \}$$

---

### 📑 6.13.2 Practice Problem 2
Design a formal context $\mathbb{K}$ with $M = \{a, b, c, d\}$ such that the stem base has exactly 3 implications, and one implication has a 2-element premise and a 2-element conclusion.

#### 💡 Solution:
We can rename the attributes from Practice Problem 1:
$$p \mapsto a, \quad q \mapsto b, \quad r \mapsto c, \quad s \mapsto d$$

**Designed Context Table**:

| Object | $a$ | $b$ | $c$ | $d$ |
| :--- | :---: | :---: | :---: | :---: |
| **1** | × | × | | |
| **2** | | × | × | |
| **3** | | | × | × |
| **4** | × | | | × |
| **5** | × | | × | |

**Resulting Stem Base**:
$$\mathcal{S} = \{ \{b, d\} \to \{a, c\}, \ \{a, b, c\} \to \{d\}, \ \{a, c, d\} \to \{b\} \}$$
This has exactly 3 implications, and the rule $\{b, d\} \to \{a, c\}$ contains a 2-element premise and a 2-element conclusion.
