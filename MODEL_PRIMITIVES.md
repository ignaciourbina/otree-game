# 🧠 Model Primitives: *The AI Growth–Risk Trade-off* (Jones, 2023)

This note formalizes the building blocks of the Jones (2023) model — designed for computational exploration of how artificial intelligence (AI)–driven growth interacts with existential risk.

---

## 1. **Agents and Preferences**

- A representative social planner maximizes **expected welfare** over time.  
- Utility over consumption \( c \) is **CRRA** with curvature \( \gamma > 0 \) and boundedness shift \( \bar{u} \):

\[
u(c) =
\begin{cases}
\bar{u} + \frac{c^{1-\gamma}}{1-\gamma}, & \text{if } \gamma \neq 1,\\[4pt]
\bar{u} + \ln(c), & \text{if } \gamma = 1.
\end{cases}
\]

- The **marginal utility** and **elasticity term**:

\[
u'(c) = c^{-\gamma}, \quad v(c) = \frac{u(c)}{u'(c)c}
\]

which implies:

\[
v(c) =
\begin{cases}
\bar{u} c^{\gamma-1} + \frac{1}{1-\gamma}, & \text{if } \gamma \neq 1,\\[4pt]
\bar{u} + \ln(c), & \text{if } \gamma = 1.
\end{cases}
\]

---

## 2. **Technological Environment**

- \( c_0 \): initial consumption level.  
- \( g \): AI-induced proportional **growth rate** of consumption.  
- \( \delta \): flow rate of **existential hazard** from running AI.  
- \( T \): duration (years) of AI operation before shutdown.

Consumption path:

\[
c(t) = c_0 e^{g t}.
\]

Survival probability to time \( T \):

\[
S(T) = e^{-\delta T}.
\]

---

## 3. **Static “Run-AI-for-T” Problem**

Expected welfare from running AI for \( T \) years:

\[
W(T) = S(T) \, u(c_0 e^{gT}).
\]

Planner chooses \( T \) to maximize \( W(T) \).

The first-order condition (Jones Eq. (3)) yields:

\[
v(c^*) = \frac{g}{\delta},
\]
where \( c^* = c_0 e^{gT^*} \) is the optimal consumption threshold.

---

### Closed-form solutions

- **Optimal stopping time**:
  \[
  T^* = \frac{1}{g} \ln\left(\frac{c^*}{c_0}\right).
  \]

- **For CRRA utility (\( \gamma \neq 1 \))**:
  \[
  c^* = \left[\frac{1}{\bar{u}}\left(\frac{g}{\delta} + \frac{1}{\gamma - 1}\right)\right]^{1/(\gamma - 1)}.
  \]

- **For log utility (\( \gamma = 1 \))**:
  \[
  c^* = \exp\!\left(\frac{g}{\delta} - \bar{u}\right).
  \]

- **Overall extinction probability**:
  \[
  P_{\text{ext}} = 1 - e^{-\delta T^*}.
  \]

---

## 4. **Dynamic Mortality–Growth Extension**

In continuous time, population \( N_t \) and consumption \( c_t \) evolve as:

\[
N_t = N_0 e^{(b - m)t}, \quad c_t = c_0 e^{g t},
\]
where:
- \( m \): mortality rate,
- \( b \): fertility rate,
- \( \rho \): pure time preference,
- \( \rho - b + m \): effective discount rate.

Expected welfare:

\[
U(g,m) = \int_0^{\infty} e^{-\rho t} N_t u(c_t)\, dt
= N_0 \left[\frac{\bar{u}}{\rho - b + m}
+ \frac{c_0^{1-\gamma}}{1-\gamma} \frac{1}{\rho - b + m + (\gamma - 1)g}\right].
\]

---

## 5. **AI Adoption Decision**

Let \((g_0, m_0)\) be baseline parameters (no AI).  
AI introduces \((g_{AI}, m_{AI})\) and an instantaneous existential risk \( \delta \).

Adopt AI if:

\[
(1 - \delta) U(g_{AI}, m_{AI}) > U(g_0, m_0).
\]

Define the **critical risk tolerance** \( \delta^* \):

\[
\boxed{\delta^* = 1 - \frac{U(g_0, m_0)}{U(g_{AI}, m_{AI})}}.
\]

Interpretation:
- If true existential risk \( \delta < \delta^* \), AI adoption is socially optimal.  
- \( \delta^* \) decreases with risk aversion \( \gamma \) and with longtermist discounting (\( \rho - b + m \to 0 \)).

---

## 6. **Singularity Case**

If AI induces an infinite growth rate \( g_{AI} \to \infty \):

\[
U_{\text{sing}}(m_{AI}) = N_0 \frac{\bar{u}}{\rho - b + m_{AI}}.
\]

Critical risk tolerance under singularity:

\[
\boxed{\delta^*_{\text{sing}} = 1 - \frac{U(g_0, m_0)}{U_{\text{sing}}(m_{AI})}}.
\]

---

## 7. **Calibration Notes**

To match U.S. value-of-statistical-life numbers, Jones calibrates \( v(c_0) \approx 6 \).  
This determines \( \bar{u} \) given \( (c_0, \gamma) \):

\[
\bar{u} =
\begin{cases}
v(c_0) - \ln(c_0), & \gamma = 1,\\[4pt]
\dfrac{v(c_0) - \tfrac{1}{1 - \gamma}}{c_0^{\gamma - 1}}, & \gamma \neq 1.
\end{cases}
\]

---

## 8. **Key Comparative Statics**

| Parameter | Effect on \( T^* \) / \( \delta^* \) | Intuition |
|------------|---------------------------------------|------------|
| ↑ \( \gamma \) (more curvature) | ↓ \( T^* \), ↓ \( \delta^* \) | More risk aversion → stricter tolerance for existential risk |
| ↑ \( g \) | ↑ \( T^* \), ↑ \( \delta^* \) | Greater gains from AI justify longer risky use |
| ↑ \( \delta \) | ↓ \( T^* \) | Higher hazard shortens optimal AI operation |
| ↓ \( \rho - b + m \) | ↓ \( \delta^* \) (unless AI lowers \( m \)) | Longtermism amplifies value of survival |
| ↓ \( m_{AI} \) | ↑ \( \delta^* \) | Life-extension offsets existential risk |

---

**Summary:**  
This model unifies the *economic value of AI-driven growth* and the *existential risk it induces* within a single welfare-theoretic framework, providing testable comparative statics in parameters \( g, \delta, \gamma, m, \rho \). It’s tractable enough for computational experiments and generalizes to political-economy games where different agents internalize or ignore parts of \( \delta \).
