# Temporal Graph Formal Definition

## Temporal Graph

Let $\mathcal{G} (\mathcal{V},\mathcal{E})$, where:

- $\mathcal{G}$, directed temporal graph 

- $\mathcal{E}$, set of vertices and set of temporal edges. Each temporal edge $e \in \mathcal{E}$ is a triplet $\langle u, v, t\rangle$, where vertices $u, v \in \mathcal{V}$, and $t$ is the connection time from $u$ to $v$

With:

- $n = |\mathcal{V}|$, number of vertices

- $m = |\mathcal{E}|$, number of edges

## Neighbor Set

Given a vertex $u \in \mathcal{V}$:

- $N_{out}(u) = \lbrace \langle v, t\rangle | (u,v,t) \in \mathcal{E} \rbrace$, the out-neighbor set of $u$

- $N_{in}(u) = \lbrace \langle v, t\rangle | (u,v,t) \in \mathcal{E} \rbrace$, the in-neighbor set of $u$

- $degr_{out}(u) = |N_{out}|$, out-degree

- $degr_{in}(u) = |N_{in}|$, in-degree
