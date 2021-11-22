### 矩阵求导

#### 标量对向量求导

设$f=\left \|xw-y \right \|^2$,求$w$的解析解

解:

1.求微分

$df=d \left( xw-y \right)^T \left( xw-y \right)$

$=(xdw)^T (xw-y) + (xw-y)^T xdw$

2.求迹函数

$tr \left(df \right)=tr \left((\frac{\partial f}{\partial w})^T dw \right)=tr \left( 2(xw-y)^T xdw \right)$

3.求$\frac{\partial f}{\partial w}=0$的解

$\because \frac{\partial f}{\partial w}=0$

$=>2x^T (xw-y)=0$

$\therefore w=(x^T x)^{-1} x^T y$

已知$sigmoid = \frac{1}{1 + e^{-x}}$，求导数

$sigmoid'=\left( \frac{e^x}{1+e^x} \right)'
=\frac{e^x}{1 + e^x}(1 - \frac{e^x}{1 + e^x})
=sigmod(1 - sigmoid)$
