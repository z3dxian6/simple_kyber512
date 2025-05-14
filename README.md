# 🧪 simple_kyber512 – Librairie pédagogique Kyber512 simplifiée (Post-Quantum KEM)

Cette librairie simule un **mécanisme d'encapsulation de clé (KEM)** inspiré de **Kyber512**, avec des **paramètres réduits** pour des démonstrations et CTFs.

> ⚠️ Elle **n’est pas sécurisée en production** (coefficients faibles, bruit simplifié, compression réduite).  
Elle est conçue pour **comprendre** les grands principes de la cryptographie à base de réseaux (LWE).

---

## 🔁 Principe général du protocole


### 1. `KeyGen()`  
- Bob génère une **paire (pk, sk)** :
  - `sk` = vecteur aléatoire mod `Q`
  - `pk = 2 × sk + bruit (e)` mod `Q`

### 2. `Encapsulate(pk)`  
- Alice :
  - Génère un vecteur aléatoire `r` + bruit `e₁`
  - Calcule `u = pk × r + e₁` mod `Q`
  - Compresse `u` et en extrait des **bits de clé** (par MSB)
  - Applique **SHA-256** sur ces bits ⇒ génère la **clé `K`**
  - Renvoie `u_compressed`, `K`

### 3. `Decapsulate(u_compressed, sk)`  
- Bob :
  - Décompresse `u`
  - Recalcule les bits de clé à partir des **MSB**
  - Applique **SHA-256** pour retrouver `K`

→ Alice et Bob ont maintenant la **même clé `K`**, sans que `K` ait jamais transité.

---

## 🧩 Fichiers de la lib

| Fonction | Rôle |
|----------|------|
| `keygen()` | Génère la paire de clés (pk, sk) |
| `encapsulate(pk)` | Produit une clé `K` et son encapsulation compressée |
| `decapsulate(c, sk)` | Récupère la même clé `K` depuis l'encapsulation et la sk |

---

## ▶️ Exemple d’usage minimal

```python
from simple_kyber512 import keygen, encapsulate, decapsulate

# Bob génère sa paire
pk, sk = keygen()

# Alice encapsule
c, k1 = encapsulate(pk)

# Bob décapsule
k2 = decapsulate(c, sk)

assert k1 == k2
print("Clé partagée K:", k1.hex())
```

---

## ⚠️ Limitations

- `N = 8` (vs 256 dans Kyber réel)
- Pas de bruit dans `decapsulate` (ignoré dans `v = ...`)
- Pas de vecteurs/structures Kyber complexes
- Compression très basique (3 bits)
