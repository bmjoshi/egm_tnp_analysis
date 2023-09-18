/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: PhysicsTools/TagAndProbe/RooExpoShape
 *
 *
 * Authors:
 * Bhargav Madhusudan Joshi
 *
 * Description:
 *   Defines a probability density function which has sum of two exponential decays

 *   
 *
 *****************************************************************************/

#include "RooExpoShape.h"

ClassImp(RooExpoShape) 

 RooExpoShape::RooExpoShape(const char *name, const char *title, 
                        RooAbsReal& _x,
                        RooAbsReal& _f,
                        RooAbsReal& _tau1,
                        RooAbsReal& _tau2,
                        RooAbsReal& _peak1,
                        RooAbsReal& _peak2) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
   f("f", "f",this,_f),
   tau1("tau1","tau1",this,_tau1),
   tau2("tau2","tau2",this,_tau2),
   peak1("peak1","peak1",this,_peak1),
   peak2("peak2","peak2",this,_peak2)
 { } 


 RooExpoShape::RooExpoShape(const RooExpoShape& other, const char* name):
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   f("f",this,other.f),
   tau1("tau1",this,other.tau1),
   tau2("tau2",this,other.tau2),
   peak1("peak1",this,other.peak1),
   peak2("peak2",this,other.peak2)
 { } 


 Double_t RooExpoShape::evaluate() const 
 { 
  // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
 
  Double_t z1 = (x - peak1); 
  Double_t z2 = (x - peak2); 

  bool cut_off_1 = (z1 > 0.0);
  bool cut_off_2 = (z2 > 0.0);

  Double_t f1 = f*( exp(tau1*(x - peak1))*cut_off_1 + (!cut_off_1)*1.0 );
  Double_t f2 = (1-f)*( exp(tau2*(x - peak1))*cut_off_2 + (!cut_off_2)*1.0 );

  return f1+f2;

 } 
