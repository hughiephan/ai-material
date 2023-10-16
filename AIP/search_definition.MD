# Progression Search Formal Definition

In AI search algorithms, the state (or search) space is usually represented as a graph, where nodes are states and the edges are the connections (or actions) between the corresponding states. 

# Algorithm 1

\begin{algorithm}
$fringe \gets { \{(s_0, tn_I, \epsilon) \} } $\;
\While{$fringe \neq \emptyset$} {
    $ n \xleftarrow{} fringe.pop() $\;
    \If{$n.isgoal$} { \Return $n$ }
    $ U  \xleftarrow[]{} n.unconstrainedNodes $
    \For{ $t \in U $ } {
        \eIf{$isPrimitive(t)$} { 
            \If{$isApplicable(t)$} {
                $ \acute{n} \xleftarrow[]{} n.apply(t)$\;
                $ fringe.add(\acute{n})$
            }
        }{
             \For{ $m \in t.methods $ } {
                $ \acute{n} \xleftarrow[]{} n.decompose(t,m) $\;
                $ fringe.add(\acute{n})$
             }
        } 
    }
    \Return $unsolvable$
}
\end{algorithm}



## Extra
# Questions

