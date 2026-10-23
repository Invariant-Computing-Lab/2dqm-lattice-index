from pathlib import Path
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def fit_affine(g):
    g=g.sort_values('n')
    n=g.n.to_numpy(float); m=g.mass_MeV.to_numpy(float)/1000; sm=g.sigma_MeV.to_numpy(float)/1000
    x=n-1; y=m*m; sy=2*m*sm
    X=np.c_[np.ones(len(x)),x]; W=1/sy**2
    beta=np.linalg.solve((X.T*W)@X,(X.T*W)@y)
    pred=X@beta; res=y-pred; chi=float(np.sum((res/sy)**2)); dof=len(y)-2
    p=float(st.chi2.sf(chi,dof)) if dof>0 else np.nan
    R=(y-y[0])/(y[1]-y[0]); delta=np.diff(y)
    return dict(beta=beta,pred=pred,res=res,chi=chi,dof=dof,p=p,R=R,y=y,sy=sy,delta=delta)


def run(root,seed=20260812):
    root=Path(root); data=root/'data'; results=root/'results'; figs=root/'figures'
    rng=np.random.default_rng(seed)
    pdg=pd.read_csv(data/'pdg2026_bottomonium_locked.csv')
    out=[]; fits={}
    for fam,g in pdg.groupby('family',sort=False):
        f=fit_affine(g); fits[fam]=f
        cv=float(np.std(f['delta'],ddof=1)/np.mean(f['delta'])) if len(f['delta'])>1 else np.nan
        out.append([fam,g.analysis_role.iloc[0],len(g),f['beta'][1],f['beta'][0]/f['beta'][1],f['chi'],f['dof'],f['p'],cv,float(np.max(np.abs(f['res']/f['sy'])))])
    sdf=pd.DataFrame(out,columns=['family','analysis_role','n_states','slope_kappa_GeV2','a','chi2','dof','p_value','spacing_CV','max_abs_standardized_residual'])
    sdf.to_csv(results/'F3_bottomonium_affine_mass2_tests.csv',index=False)

    ug=pdg[pdg.family=='Upsilon_nS'].sort_values('n'); f=fits['Upsilon_nS']
    nr=[]
    for state,n,R in zip(ug.state,ug.n,f['R']): nr.append([state,int(n),R,n-1,R-(n-1)])
    ndf=pd.DataFrame(nr,columns=['state','n','R_observed','R_predicted_linear','deviation']); ndf.to_csv(results/'F4_Upsilon_normalized_spectrum.csv',index=False)

    MC=200000; m=ug.mass_MeV.to_numpy(float)/1000; s=ug.sigma_MeV.to_numpy(float)/1000
    draw=rng.normal(m,s,size=(MC,4)); y=draw**2; den=y[:,1]-y[:,0]
    quantities={'R3':(y[:,2]-y[:,0])/den,'R4':(y[:,3]-y[:,0])/den,'DeltaM2_12':y[:,1]-y[:,0],'DeltaM2_23':y[:,2]-y[:,1],'DeltaM2_34':y[:,3]-y[:,2]}
    targets={'R3':2.0,'R4':3.0}
    rows=[]
    for k,v in quantities.items(): rows.append([k,v.mean(),v.std(ddof=1),np.quantile(v,.025),np.quantile(v,.975),targets.get(k,np.nan)])
    pd.DataFrame(rows,columns=['quantity','mean','sd','q025','q975','model_target']).to_csv(results/'F5_Upsilon_MC_uncertainty.csv',index=False)

    # Practical intrinsic scatter needed on adjacent spacings for reduced chi2 ~ 1.
    y0=m*m; sy0=2*m*s; d=np.diff(y0); sd=np.sqrt(sy0[:-1]**2+sy0[1:]**2)
    taus=np.linspace(0,1,10001); chis=[]
    for tau in taus:
        se=np.sqrt(sd**2+(tau*d)**2); w=1/se**2; mu=np.sum(w*d)/np.sum(w); chis.append(np.sum(((d-mu)/se)**2))
    chis=np.asarray(chis); i=np.argmin(np.abs(chis-2)); tau=float(taus[i])
    pd.DataFrame({'fractional_intrinsic_spacing_scatter':taus,'chi2_constant_spacing':chis}).to_csv(results/'F8_spacing_intrinsic_scatter_curve.csv',index=False)

    x=ug.n.to_numpy(); yy=f['y']; sy=f['sy']
    plt.figure(figsize=(7.2,4.8)); plt.errorbar(x,yy,yerr=sy,fmt='o',capsize=3,label='PDG 2026'); plt.plot(x,f['pred'],label='Best affine 2DQM spectral law'); plt.xlabel('Radial label n'); plt.ylabel(r'$M^2$ (GeV$^2$)'); plt.title(r'Primary falsification: $\Upsilon(1S)$-$\Upsilon(4S)$'); plt.legend(); plt.tight_layout(); plt.savefig(figs/'Fig3_Upsilon_mass2_affine_test.png',dpi=300); plt.close()
    plt.figure(figsize=(7.2,4.8)); plt.plot(ndf.n,ndf.R_observed,'o-',label='Observed invariant ratio'); plt.plot(ndf.n,ndf.R_predicted_linear,'x--',label='Linear-law target'); plt.xlabel('n'); plt.ylabel(r'$R_n=(M_n^2-M_1^2)/(M_2^2-M_1^2)$'); plt.title('Unit-free spectral fingerprint'); plt.legend(); plt.tight_layout(); plt.savefig(figs/'Fig4_Upsilon_normalized_spectrum.png',dpi=300); plt.close()
    plt.figure(figsize=(7.2,4.8)); plt.plot([1,2,3],f['delta'],'o-'); plt.axhline(np.mean(f['delta']),linestyle='--'); plt.xlabel('Adjacent transition'); plt.ylabel(r'$\Delta M^2$ (GeV$^2$)'); plt.xticks([1,2,3],['1S->2S','2S->3S','3S->4S']); plt.title('Adjacent mass-squared spacings are not constant'); plt.tight_layout(); plt.savefig(figs/'Fig5_Upsilon_spacing.png',dpi=300); plt.close()

    pr=sdf[sdf.family=='Upsilon_nS'].iloc[0]
    return {'chi2':float(pr.chi2),'dof':int(pr.dof),'p_value':float(pr.p_value),'spacing_CV':float(pr.spacing_CV),'R3':float(ndf.loc[ndf.n==3,'R_observed'].iloc[0]),'R4':float(ndf.loc[ndf.n==4,'R_observed'].iloc[0]),'spacings_GeV2':f['delta'].tolist(),'intrinsic_spacing_scatter_required':tau}
