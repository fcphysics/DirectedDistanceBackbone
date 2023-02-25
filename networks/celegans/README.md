# C. elegans connectome network - Synapitc interactions

Data Source: <https://www.wormwiring.org/pages/adjacency.html>
Reference: Cook et al., "Whole-animal connectomes of both Caenorhabditis elegans sexes." Nature 571, 63-71 (2019) [Link](https://www.nature.com/articles/s41586-019-1352-7)

Files used:
- `SI 2 Synapse adjacency matrices.xlsx`: data


The C. elegans connectome has two different types of connections. The gap junctions, which are symmetric and the pre-post synapitc cell interactions, which are assymetric. Here we consider the former, and also distinguish the hermaphrodite and the male sex. Edge weight is the number of synapses between cells relative to the total number of synapses.

Both networks contains multiple weakly connected components with the largest one comparising approximately 69% (64%) of the network in the case of the hermaphrodite (male) sex.