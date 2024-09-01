\documentclass{article}
\usepackage[dvipsnames]{xcolor}
\usepackage{annotate-equations}
\renewcommand{\eqnhighlightheight}{}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{mathtools, nccmath}
\usepackage{wrapfig}
\usepackage{comment}
\usepackage{graphicx}
\usepackage{xspace}
\usepackage{array}
\usepackage{ragged2e}
\newcolumntype{P}[1]{>{\RaggedRight\hspace{0pt}}p{#1}}
\newcolumntype{X}[1]{>{\RaggedRight\hspace*{0pt}}p{#1}}
\colorlet{linecol}{black!75}
\usepackage{xkcdcolors}
\colorlet{mhpurple}{Plum!80}
\newcommand{\lap}{\mathrm{Lap}}
\newcommand{\pr}{\mathrm{Pr}}
\newcommand{\Tset}{\mathcal{T}}
\newcommand{\Dset}{\mathcal{D}}
\newcommand{\Rbound}{\widetilde{\mathcal{R}}}


\begin{document}

$ \text{Let} (\eqnmarkbox[red]{d}d, \eqnmarkbox[red]{M}M \in \mathbb{N} = \{1, 2, 3, \dots\}, \, \mathcal{E} \in C(\mathbb{R}^d, \mathbb{R}), \, x_1, x_2, \dots, x_{M+1} \in \mathbb{R}^d, \, y_1, y_2, \dots, y_M \in \mathbb{R} ) \text{satisfy for all} ( m \in \{1, 2, \dots, M\} )$

\annotate[yshift=2em,xshift=2ex]{above,left}{d}{\textbf{dimension of input}}
\annotate[yshift=2em,xshift=2ex]{above,right}{M}{\textbf{known input-output data pairs}}

$\mathcal{E} : \mathbb{R}^d \rightarrow \mathbb{R}^a, \ \text{unknown function which relates input and output} \ y_m = \mathcal{E}(x_m)$

\end{document}
