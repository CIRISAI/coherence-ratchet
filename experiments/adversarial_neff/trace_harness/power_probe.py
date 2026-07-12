import numpy as np, sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import loader as L, harness_neff as H
rows=L.load_context()
# use the largest clean pool: Ally qa_eval CORE4 complete-case, subsample to n, measure bootstrap SE of N_eff_PR
g=L.group(rows,agent="Ally",task_class="qa_eval")
X,_=L.axis_matrix(g,L.CORE4,complete_case=True)
rng=np.random.default_rng(0)
print("Empirical bootstrap SE of N_eff_PR (CORE4, k=4) vs sample size n:")
print(f"{'n':>6} {'SE(N_eff_PR)':>14} {'~min resolvable Δ @3σ':>24}")
for n in [20,36,50,100,150,200,300,500]:
    ses=[]
    for rep in range(40):
        s=rng.integers(0,len(X),n); Xs=X[s]
        # inner bootstrap SE
        prs=[]
        for _ in range(200):
            ss=rng.integers(0,n,n); R,keep=H.corr(Xs[ss])
            if R is not None: prs.append(H.neff_pr(R))
        ses.append(np.std(prs))
    se=np.mean(ses)
    # to separate two conditions at 3σ: 3*sqrt(2)*se <= Δ
    dmin=3*np.sqrt(2)*se
    print(f"{n:>6} {se:>14.3f} {dmin:>24.2f}")
