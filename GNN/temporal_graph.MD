# Temporal Graph Formal Definition

## Temporal Graph

![image](https://github.com/hughiephan/DPL/assets/16631121/c8fbd242-7518-4ea6-b689-5c15f2565f4a)

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

## Projected Graph

![image](https://github.com/hughiephan/DPL/assets/16631121/dafa16d8-6d3f-4ebb-8e2f-b9063d77d30b)

$\mathcal{G}_{[t_s, t_e]}$ is the projected graph of $\mathcal{G}$ in time interval $[t_s, t_e]$, with:

- $V(\mathcal{G}_{[t_s, t_e]}) = \mathcal{V}$

- $E(\mathcal{G}_{[t_s, t_e]}) = \lbrace (u, v) | (u,v,t) \in \mathcal{E}, t \in [t_s, t_e] \rbrace$

And length of interval $[t_s, t_e]$ is $t_e - t_s + 1$

## Span Reachability

Given a temporal graph $\mathcal{G}$, two vertices $u, v$ and a time interval $[t_s, t_e]$, then $u$ span-reaches $v$ in $[t_s, t_e]$, denoted as
$u \rightsquigarrow_{[t_s, t_e]} v$ if $u$ reaches $v$ in the projected graph $\mathcal{G}_{[t_s, t_e]}$


