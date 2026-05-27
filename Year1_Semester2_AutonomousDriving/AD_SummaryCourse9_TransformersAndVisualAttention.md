<!-- --------------------------------------------------------------- -->
<!-- --------- COURSE 9 Transformers and Visual Attention ---------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 9 - Transformers and Visual Attention**

---

## 📖 9.1 Neural Machine Translation (NMT) & The Attention Mechanism
* **The Problem with RNNs:** Traditional Encoder-Decoder architectures rely on Recurrent Neural Networks (RNNs), such as LSTMs, to compress a variable-length input sentence into a fixed-length final state. This creates an **information bottleneck** where the model fails to retain necessary context in long sequences.
* **The Solution (Attention):** Instead of a single fixed state, the encoder creates a variable-length representation using Bidirectional RNNs. At each step of translation, the decoder "queries" the encoder to generate a specific context vector relevant to the next predicted word.
* **Pre-Transformer Attention Types:**
    * **Additive Attention (Bahdanau):** Uses a feed-forward network (FFN) to combine query and key states. It is effective but computationally inefficient.
    * **Dot Product Attention (Luong):** Computes similarity via a simple dot product between the query and the key, requiring them to be of equal length.

---

## 📖 9.2 "Attention Is All You Need" (The Transformer)
* **Core Concept:** The Transformer architecture removes RNNs entirely, replacing them with **Multi-Head Self-Attention**;
* **Advantages over RNNs:**
    * **Scalability:** Eliminates the sequential processing path ($O(T)$), allowing for highly parallel computation across all tokens;
    * **No Position Bias:** RNNs tend to over-value the most recently seen information; Transformers model global dependencies equally across the sequence;
* **Scaled Dot-Product Attention:**
    * **Formula:** $$Attention(Q,K,V)=softmax(\frac{QK^{T}}{\sqrt{d_{k}}})V$$ 
    * **Explanation:** The model compares a Query matrix ($Q$) against Key matrices ($K^{T}$) using dot products to find sequence alignments. It scales the result by $\frac{1}{\sqrt{d_{k}}}$ (where $d_{k}$ is the dimension size) to prevent the softmax function from saturating. The resulting normalized weights are multiplied by the Value matrix ($V$) to form the output context;
* **Multi-Head Attention:** Instead of one single attention pass, the model projects $Q$, $K$, and $V$ into multiple different representation spaces ("heads"). This allows the model to simultaneously attend to different types of contextual relationships in parallel;
* **Positional Embeddings:** Because the model lacks recurrence, it has no inherent sense of word order. Constant, position-dependent vectors (often derived from sine and cosine functions) are added to the input word embeddings so the model can recognize relative sequence order;
* **Architecture Components:** The network relies heavily on Skip Connections, Layer Normalization (to aid rapid convergence), and FFNs (to lift token features and increase representational power). The decoder employs **masking** to prevent tokens from "looking ahead" at future words during the training phase.

---

## 📖 9.3 Object Detection with Transformers (DETR)
* **Direct Set Prediction:** DETR (Detection Transformer) shifts object detection from a heuristic-heavy task to a direct set prediction problem. It outputs a fixed number of predictions natively, consisting of bounding boxes and class labels (including $\emptyset$ for a special "no object" class);
* **Elimination of NMS:** Traditional CNN architectures (like Faster R-CNN) rely on Non-Maximum Suppression (NMS) to manually filter out overlapping anchor boxes. DETR bypasses this by generating distinct, non-overlapping predictions through its global attention mechanism;
* **Bipartite Matching Loss (Hungarian Loss):**
    * **Formula:** $$\mathcal{L}_{Hungarian}=\sum_{i=1}^{n}-log\hat{p}_{\sigma_{i}}(c_{i})+[[c_{i}\ne\emptyset]]\cdot\mathcal{L}_{bbox}(b_{i},\hat{b}_{\sigma_{i}})$$ 
    * **Process:** Instead of matching predictions to predefined anchors, DETR uses the Hungarian algorithm to find the optimal one-to-one matching ($\sigma$) between ground truth objects and model predictions. It penalizes classification errors for all outputs, but only computes bounding box errors for predictions matched to actual ground truth objects;
* **Bounding Box Loss & GIoU:**
    * **Formula:** $$\mathcal{L}_{iou}(b,\hat{b})=1-(\frac{|b\cap\hat{b}|}{|b\cup\hat{b}|}-\frac{|B(b,\hat{b})\backslash b\cup\hat{b}|}{|B(b,\hat{b})|})$$ 
    * **Explanation:** The bounding box loss is a linear combination of standard L1 loss and Generalized Intersection over Union (GIoU). Standard IoU yields a zero gradient if two boxes do not overlap at all, which halts learning. GIoU solves this by factoring in $B(b,\hat{b})$, representing the smallest bounding box that completely encloses both the prediction and the ground truth box;
* **DETR Architecture Overview:**
    1.  **Backbone:** A standard CNN extracts a robust set of 2D image features;
    2.  **Transformer Encoder:** Flattens the CNN feature map into a 1D sequence for processing via self-attention;
    3.  **Transformer Decoder:** Takes a fixed number of learned "object queries" (positional embeddings) and attends to the encoder's output in parallel. These queries learn to intrinsically focus on different geometric and semantic regions of an image;
    4.  **Prediction Heads:** Independent FFNs compute the final class assignment and bounding box coordinates for every query;
* **Results & Efficacy:** DETR performs competitively with established models like Faster R-CNN. It excels at detecting large objects due to the global attention mechanism but struggles slightly with small objects. As the transformer decoder becomes deeper (exceeding 3 layers), post-processing with NMS becomes actively unnecessary and can even degrade performance by suppressing valid overlaps.
