# ACTN
 
BAREM TEMA 1

-generarea parametrului p, numar prim mare (peste 161 biti) (1p)
  (folosind o biblioteca dedicata numerelor mari (BigInteger pentru Java, NTL/GMP pentru C/C++ etc.))


----------------Codificare----------------

-codificarea input-ului (specificat initial ca un sir de caractere) ca vector de numere naturale mai mici decat p (1p)

-codificarea efectiva, folosind schema lui Horner pentru evaluarea polinomului P(x) in punctele 1,2,...,n (2p)


---------------Decodificare---------------

-calculul coeficientului liber - maxim (3p), dupa cum urmeaza:
                     - varianta folosind k(k-1) inversari (1p)
                     - varianta folosind k inversari (1p)
                     - varianta folosind o singura inversare (1p)

-comparatii din punct de vedere al timpului pentru variantele precedente (1p)
-reconstructia polinomului P(x) in faza finala a decodificarii, creand propria functie/procedura pentru inmultirea de polinoame avand coeficienti numere naturale mai mici decat p (2p)