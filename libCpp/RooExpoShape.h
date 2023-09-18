
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

#ifndef ROO_EXPO_SHAPE
#define ROO_EXPO_SHAPE

#include "RooExponential.h"
#include "RooAddPdf.h"
#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooExpoShape : public RooAbsPdf {
public:
  RooExpoShape() {};
  RooExpoShape(const char *name, const char *title,
	      RooAbsReal& _x,
         RooAbsReal& _f,
	      RooAbsReal& _tau1,
	      RooAbsReal& _tau2,
	      RooAbsReal& _peak1,
	      RooAbsReal& _peak2
         );

  RooExpoShape(const RooExpoShape& other, const char* name);
  inline virtual TObject* clone(const char* newname) const { return new RooExpoShape(*this,newname); }
  inline ~RooExpoShape() {}
  Double_t evaluate() const ;

  ClassDef(RooExpoShape,2);

protected:

  RooRealProxy x ;
  RooRealProxy f;
  RooRealProxy tau1;
  RooRealProxy tau2;
  RooRealProxy peak1;
  RooRealProxy peak2;
  
};
 
#endif
