import pandas as pd
import numpy as np
  
    
def l_nusselta(dyfuzja_cieplna, wymiar_charakterystyczny, przewodzenie_ciepla):
    return (dyfuzja_cieplna*wymiar_charakterystyczny)/przewodzenie_ciepla

def l_reynoldsa(predkosc_plynu, wymiar_charakterystyczny, lepkosc_kinematyczna):
    return (predkosc_plynu*wymiar_charakterystyczny)/lepkosc_kinematyczna

def l_prandtla(lepkosc_kinematyczna, stala_dyfucji_cieplnej):
    return lepkosc_kinematyczna/stala_dyfucji_cieplnej

def l_prandtla_cp(cieplo_wlasciwe,lepkosc_dynamiczna, przewodzenie_ciepla):
    return (cieplo_wlasciwe*lepkosc_dynamiczna)/przewodzenie_ciepla






if __name__ == "__main__":
    
    materials = np.array([
        ["nazwa","woda"],
        ["gestosc",995.7],
        ["cieplo wlasciwe", 4187],
        ["lepkosc kinematyczna", 0.805e-6],
        ["lepkosc dynamiczna", 801.5e-6 ],
        ["wspolczynnik przewodzenia ciepla",61.8e-2],
        ["stala dyfuzji cieplnej", 14.9e-8]
        ])
    
    
    materials_odczyt = pd.DataFrame(data = materials)
    
    print(materials_odczyt)
    
    print(l_prandtla_cp(float(materials[2,1]),
                        float(materials[4,1]),
                        float(materials[5,1])))
    
    
    
    