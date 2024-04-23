#include "udf.h"

#define M_vapour 18.0152 // kg/kmol
#define M_air 28.966 // kg/kmol

DEFINE_PROPERTY(saturation_temperature, c, t)
{
    real sat_temp;

    Thread *pt = THREAD_SUB_THREAD(t, 0); // Primary phase (humid air) thread
    Thread *st = THREAD_SUB_THREAD(t, 1); // Secondary phase (water liquid) thread

    real vapour_mass_frac = C_YI(c, pt, 0);
    real vapour_mole_frac = vapour_mass_frac / M_vapour / (vapour_mass_frac / M_vapour + (1 - vapour_mass_frac) / M_air);

    // Mixture pressure p_abs assumed equal to operating pressure
    real p_abs = RP_Get_Real("operating-pressure");

    real vf_liquid = C_VOF(c, st);
    real p_vapour;
    real p_water;

    // Calculate water vapour partial pressure
    p_vapour = p_abs * vapour_mole_frac;
   
    // Calculate water liquid/vapour pressure used in Antoine equation
    p_water = p_vapour + (p_abs - p_vapour) * vf_liquid;

    // Calculate saturation temperature using Antoine equation
    sat_temp = 1687.5 / (5.1156 - log10((p_water) / 100000)) - 230.17 + 273.15;

    // Store data for visualisation and debugging
    C_UDMI(c, t, 0) = sat_temp;
    C_UDMI(c, t, 1) = p_water;
    C_UDMI(c, t, 2) = vapour_mass_frac;
    C_UDMI(c, t, 3) = vapour_mole_frac;
    C_UDMI(c, t, 4) = vf_liquid;

    return sat_temp;
}
