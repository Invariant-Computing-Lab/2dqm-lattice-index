from pathlib import Path
from math import pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SIGMA1=np.array([[0,1],[1,0]],complex)
SIGMA2=np.array([[0,-1j],[1j,0]],complex)
SIGMA3=np.array([[1,0],[0,-1]],complex)
GAMMAS=[SIGMA1,SIGMA2]


def torus_u1_links(L,d):
    B=2*pi*d/(L*L)
    y=np.arange(L)
    Ux=np.exp(-1j*B*np.tile(y,(L,1)))
    Uy=np.ones((L,L),complex)
    Uy[:,L-1]=np.exp(1j*B*L*np.arange(L))
    return Ux,Uy


def plaquette(Ux,Uy):
    return Ux*np.roll(Uy,-1,axis=0)*np.conj(np.roll(Ux,-1,axis=1))*np.conj(Uy)


def gauge_transform(Ux,Uy,rng):
    L=Ux.shape[0]
    th=rng.uniform(-pi,pi,size=(L,L))
    g=np.exp(1j*th)
    return g*Ux*np.conj(np.roll(g,-1,axis=0)), g*Uy*np.conj(np.roll(g,-1,axis=1))


def wilson_dirac(Ux,Uy,m0=1.0,r=1.0):
    L=Ux.shape[0]; ns=L*L
    D=np.zeros((2*ns,2*ns),complex); I=np.eye(2); links=[Ux,Uy]
    idx=lambda x,y:x*L+y
    for x in range(L):
        for y in range(L):
            s=idx(x,y)
            D[2*s:2*s+2,2*s:2*s+2]+=(2*r-m0)*I
            for mu in range(2):
                xp,yp=x,y
                if mu==0: xp=(x+1)%L
                else: yp=(y+1)%L
                sf=idx(xp,yp); U=links[mu][x,y]
                D[2*s:2*s+2,2*sf:2*sf+2]+=-.5*(r*I-GAMMAS[mu])*U
                xm,ym=x,y
                if mu==0: xm=(x-1)%L
                else: ym=(y-1)%L
                sb=idx(xm,ym); Ub=np.conj(links[mu][xm,ym])
                D[2*s:2*s+2,2*sb:2*sb+2]+=-.5*(r*I+GAMMAS[mu])*Ub
    return D


def overlap_index(Ux,Uy,m0=1.0):
    L=Ux.shape[0]
    H=np.kron(np.eye(L*L),SIGMA3)@wilson_dirac(Ux,Uy,m0=m0)
    H=(H+H.conj().T)/2
    ev=np.linalg.eigvalsh(H)
    return float(-.5*np.sum(np.sign(ev))), float(np.min(np.abs(ev)))


def run(root,seed=20260812):
    root=Path(root); results=root/'results'; figs=root/'figures'
    rng=np.random.default_rng(seed)
    rows=[]
    for L in [6,8,10,12]:
        for d in range(-3,4):
            Ux,Uy=torus_u1_links(L,d)
            q0=np.angle(plaquette(Ux,Uy)).sum()/(2*pi)
            i0,gap=overlap_index(Ux,Uy)
            ig=[]; qg=[]
            for _ in range(20):
                Vx,Vy=gauge_transform(Ux,Uy,rng)
                ii,_=overlap_index(Vx,Vy)
                ig.append(ii); qg.append(np.angle(plaquette(Vx,Vy)).sum()/(2*pi))
            rows.append([L,d,q0,i0,-d,gap,np.max(np.abs(np.asarray(ig)-i0)),np.max(np.abs(np.asarray(qg)-q0))])
    df=pd.DataFrame(rows,columns=['L','degree_target','geometric_charge','overlap_index','expected_index_orientation','min_kernel_gap','max_index_change_under_gauge','max_geometric_charge_change_under_gauge'])
    df.to_csv(results/'F1_overlap_index_gauge.csv',index=False)

    ts=np.unique(np.r_[np.linspace(0,.45,46),np.linspace(.45,.57,241),np.linspace(.57,1,44)])
    flow=[]
    for t in ts:
        Ux,Uy=torus_u1_links(8,float(t)); ii,gap=overlap_index(Ux,Uy)
        q=np.angle(plaquette(Ux,Uy)).sum()/(2*pi)
        flow.append([t,ii,gap,q])
    f=pd.DataFrame(flow,columns=['interpolation_t','overlap_index','kernel_gap','geometric_charge_principal'])
    f.to_csv(results/'F2_topology_changing_spectral_flow.csv',index=False)

    sub=df[df.L==8]
    plt.figure(figsize=(7.2,4.8)); plt.plot(sub.degree_target,sub.overlap_index,'o-',label='Overlap index'); plt.plot(sub.degree_target,-sub.degree_target,'x--',label='Expected -d'); plt.xlabel('Topological degree d'); plt.ylabel('Index'); plt.title('Explicit lattice index test on the 2D U(1) torus'); plt.legend(); plt.tight_layout(); plt.savefig(figs/'Fig1_overlap_index_degree.png',dpi=300); plt.close()
    ic=f.kernel_gap.idxmin(); tc=float(f.loc[ic,'interpolation_t'])
    plt.figure(figsize=(7.2,4.8)); plt.plot(f.interpolation_t,f.kernel_gap); plt.axvline(tc,linestyle='--'); plt.xlabel('Topology-changing interpolation t'); plt.ylabel('min |eigenvalue(H_W)|'); plt.title('Kernel-gap closure at the topological transition'); plt.tight_layout(); plt.savefig(figs/'Fig2_topology_transition_gap.png',dpi=300); plt.close()
    return {'index_match_rate':float(np.mean(df.overlap_index==df.expected_index_orientation)),'max_gauge_index_change':float(df.max_index_change_under_gauge.max()),'critical_t_grid':tc,'critical_gap':float(f.loc[ic,'kernel_gap'])}
