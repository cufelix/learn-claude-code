# Klíč řešení: rovnice s parametrem (ověřeno)

Ověření: `klic.py` (ve stejné složce) porovnal každý výsledek se `sympy.solveset` pro 772 kombinací parametru (krok 1/3 na [-4,4], plus 21/4, 3/2; u dvou parametrů mřížka -2..3). 2 "nesoulady" jsou chyby sympy, ne klíče (viz konec). Mezní hodnoty parametru jsou ve vzorkování vždy.

Konvence: $x\in\mathbb R$; parametr také reálný; odmocnina vyžaduje nezáporný radikand a je $\ge 0$.

## A. Lineární

**Př.1** $2xp+p(1-x)=3p-4+2x \Rightarrow xp-2x=2p-4 \Rightarrow (p-2)x=2(p-2)$.
- $p\ne2$: $x=2$. $p=2$: $0=0$, $x\in\mathbb R$.

**Př.3** $t(t+3)x=2t$.
- $t=0$: $0=0$, $x\in\mathbb R$. $t=-3$: $0=-6$, žádné řešení. Jinak $x=\dfrac{2}{t+3}$.
- Past: nedělit $t$ bez rozboru $t=0$.

**Př.5** $(p-1)(p+1)x=p(p+1)$.
- $p\ne\pm1$: $x=\dfrac{p}{p-1}$. $p=1$: $0=2$, nemá řešení. $p=-1$: $0=0$, $x\in\mathbb R$.
- Past: $p=-1$ a $p=1$ dopadnou RŮZNĚ (pravá strana se nuluje jen u $-1$).

**Př.6** $p(xp-1)=1-x \Rightarrow (p^2+1)x=p+1$.
- Pro všechna $p\in\mathbb R$: $x=\dfrac{p+1}{p^2+1}$, protože $p^2+1>0$. Žádná diskuze není potřeba (past: student hledá případy, které neexistují). V $\mathbb C$ by to bylo jinak, ale ne zde.

**Př.7** $p(xp+1)=2(x+1)+xp \Rightarrow (p-2)(p+1)x=-(p-2)$.
- $p\ne2,\,p\ne-1$: $x=-\dfrac1{p+1}$. $p=2$: $0=0$, každé $x$. $p=-1$: $0=3$, nic.
- Kladné řešení: $-\frac1{p+1}>0\iff p<-1$. **Odpověď: $p\in(-\infty,-1)$.**
- Nejednoznačnost zadání: pro $p=2$ jsou řešením všechna čísla včetně kladných. Standardní čtení ("řešení je kladné číslo" = jediné řešení kladné) dává $p<-1$. Doporučení: ukázat studentovi i poznámku o $p=2$ a nechat ho to zdůvodnit.

## B. Podílový tvar

**Př.1** $\dfrac{t}{x-2}=\dfrac{2}{x-t}$, podmínky $x\ne2,\ x\ne t$.
$t(x-t)=2(x-2)\Rightarrow (t-2)x=t^2-4=(t-2)(t+2)$.
- $t\ne2$: kandidát $x=t+2$. Podmínka $x\ne2\iff t\ne0$; $x\ne t$ platí vždy. Tedy $t\notin\{0,2\}$: $x=t+2$.
- $t=0$: kandidát $x=2$ je zakázaný, **žádné řešení** (ověření: $0=2/x$ nemá řešení).
- $t=2$: rovnice $\frac{2}{x-2}=\frac{2}{x-2}$, platí pro $x\in\mathbb R\setminus\{2\}$.

**Př.2** $\dfrac{3x}{x+2}=\dfrac{t}{t-1}$, podmínky $x\ne-2$, $t\ne1$ (jinak rovnice nemá smysl).
$3x(t-1)=t(x+2)\Rightarrow (2t-3)x=2t$.
- $t=1$: rovnice není definována. $t=\frac32$: $0=3$, nemá řešení.
- $t\ne1,\frac32$: $x=\dfrac{2t}{2t-3}$. Zkouška $x\ne-2$: $2t=-4t+6\iff t=1$, tedy vždy splněno. (Past: zkoumat to je správné, vyjde ale "nic nového".)

**Př.4** $x(p^2+4q^2)=p^2-4q^2$ (x; p,q).
- $p^2+4q^2=0\iff p=q=0$: $0=0$, $x\in\mathbb R$.
- Jinak $x=\dfrac{p^2-4q^2}{p^2+4q^2}$. Jmenovatel je nulový jen pro $p=q=0$.
- Zadání bez podmínky: je to lineární rovnice, žádný jmenovatel s $x$. Název "podílový tvar" = výsledek je podíl.

**Př.5** $(p-q)(p+q)x=p+q$ (x; p,q).
- $p+q\ne0,\ p\ne q$: $x=\dfrac1{p-q}$.
- $p=-q$ (včetně $p=q=0$): $0=0$, $x\in\mathbb R$.
- $p=q\ne0$: $0=2p$, nemá řešení.
- Pořadí případů: nejdřív $p+q=0$, pak $p=q$. Past: $p=q=0$ patří do prvního.

## C. Kvadratické

**Př.1** $tx^2+t^2x+t=0$.
- $t=0$: $0=0$, $x\in\mathbb R$ (není kvadratická).
- $t\ne0$: vydělit $t$: $x^2+tx+1=0$, $D=t^2-4$.
  - $|t|>2$: $x_{1,2}=\dfrac{-t\pm\sqrt{t^2-4}}2$.
  - $t=2$: $x=-1$; $t=-2$: $x=1$ (dvojnásobný kořen).
  - $|t|<2,\ t\ne0$: žádný reálný kořen.
- Past: dělit $t$ bez $t=0$; psát $D=t^2-4<0\Rightarrow t<2$ místo $|t|<2$.

**Př.3** $\dfrac{y^2+3y}{3-a}=1$, podmínka $a\ne3$.
$y^2+3y+a-3=0$, $D=9-4(a-3)=21-4a$.
- $a=3$: rovnice nemá smysl. (Past: dosadit a dostat $y\in\{0,-3\}$.)
- $a<\frac{21}4,\ a\ne3$: $y_{1,2}=\dfrac{-3\pm\sqrt{21-4a}}2$. $a=\frac{21}4$: $y=-\frac32$. $a>\frac{21}4$: žádné.

**Př.4** $(1-t)x^2+(t-2)x+1=0$. Rozklad: $(x-1)\big((1-t)x-1\big)=0$.
- $t=1$: lineární, $x=1$.
- $t\ne1$: $D=t^2\ge0$ vždy, kořeny $x_1=1,\ x_2=\dfrac1{1-t}$. Splynou pro $t=0$ (dvojnásobný $x=1$).
- Past: nechat se vyvést z míry tím, že $D=t^2$ je čtverec, a nevšimnout si kořene $x=1$ (součet koeficientů je 0 pro každé t). Rychlý trik: $x=1$ dosazením.

## D. Iracionální

**Př.2** $\sqrt{x^2+3p^2}=x+p$. Radikand $\ge0$ vždy, tedy $D=\mathbb R$; podmínka $x+p\ge0$.
Umocnění: $2p^2=2px\Rightarrow p(p-x)=0$.
- $p=0$: $|x|=x$, **$x\in[0,\infty)$**.
- $p\ne0$: $x=p$; zkouška $x+p=2p\ge0\iff p>0$; $\sqrt{4p^2}=2p$ ok.
- Výsledek: $p>0$: $x=p$; $p=0$: $x\ge0$; $p<0$: žádné řešení.

**Př.3** $a\sqrt{y+a}=a^2$, $y\ge-a$.
- $a=0$: $0=0$, $y\ge0$ (z podmínky $y+a\ge0$), tedy $y\in[0,\infty)$.
- $a\ne0$: $\sqrt{y+a}=a$, nutně $a>0$; $y=a^2-a$; podmínka $y\ge-a\iff a^2\ge0$ ok.
- $a>0$: $y=a^2-a$; $a=0$: $y\ge0$; $a<0$: žádné.

**Př.4** $\sqrt{x^2-1}=x-p$ (**přepis nejednoznačný**: chybí "neznámá x, parametr p" a případná otázka; předpokládám řešit v $x$ s diskuzí podle $p$. Ověřit podle `zadani.jpg`).
Podmínky: $|x|\ge1$, $x\ge p$. Umocnění: $-1=-2px+p^2\Rightarrow 2px=p^2+1$.
- $p=0$: $0=1$, žádné řešení.
- $p\ne0$: $x=\dfrac{p^2+1}{2p}$. $|x|\ge1\iff (|p|-1)^2\ge0$, vždy platí. Zbývá $x-p=\dfrac{1-p^2}{2p}\ge0$.
  - $p>0$: $p\le1$. $p<0$: $1-p^2\le0\iff p\le-1$.
- **Výsledek:** $p\in(-\infty,-1]\cup(0,1]$: $x=\dfrac{p^2+1}{2p}$; jinak žádné řešení.
- Kontrola mezí: $p=1$: $x=1$, $0=0$. $p=-1$: $x=-1$, $0=0$. $p=\frac12$: $x=\frac54$, $\sqrt{9/16}=\frac34=\frac54-\frac12$. $p=2$: $x=\frac54$, $\frac34\ne-\frac34$: zkouška vyřadí.

## E. Prerekvizitní vlákna a nepodmíněné pravdy

Vlákna: (1) ekvivalentní úpravy, kdy lze dělit; (2) $ax=b$ má tři chování; (3) definiční obor zlomku, odmocniny; (4) kvadratická rovnice a diskriminant; (5) umocnění není ekvivalentní úprava; (6) vytýkání a rozklad ($a^2-b^2$, vytknutí $(p-2)$); (7) nerovnice (lineární) pro Př.7 a podmínky v iracionálních.

Nepodmíněné pravdy, na kterých stavět:
1. $0\cdot x=0$ platí pro každé $x$; $0\cdot x=c$, $c\ne0$, nemá řešení.
2. Dělit lze jen nenulovým výrazem; jinak rovnice zůstane, jen se rozpadne na případy.
3. Zlomek s nulovým jmenovatelem neexistuje; odmocnina záporného čísla v $\mathbb R$ neexistuje; $\sqrt{\cdot}\ge0$.
4. Diskuze = rozdělení parametrického prostoru na případy podle toho, kde se změní TVAR řešení; "kritické hodnoty" jsou nuly koeficientu u neznámé.
5. Umocnění na druhou ztrácí informaci o znaménku, proto zkouška (nebo podmínka).
6. Řešení nesmí porušit definiční obor původní rovnice, i když parametr byl v algebře krásný.

Typické chyby: dělit výrazem s parametrem bez rozboru nuly; zapomenout případ "všechna x"; zaměnit "nemá řešení" a "všechna x"; zkoumat kritické hodnoty, které nejsou kritické (Př.6); nevyloučit hodnotu, při které kandidát porušuje DO (Př. pod.1, $t=0$); u $p+q=0$ s více parametry; $D<0$ vs. $|t|<2$; kvadratická se zapomenutým $t=0$/$t=1$ (lineární případ); iracionální bez zkoušky či bez podmínky $x+p\ge0$; v odpovědi chybí závěrečná tabulka případů.

## F. Návrh: klíč a kontrola pro tutora

Soubor `klic.py` (v této složce, ~60 řádků, sympy 1.14 je nainstalováno). Navrhuji ho zkopírovat do `.claude/learn/klic.py`. Obsahuje jednu tabulku `EX`: pro každý příklad neznámou, levou a pravou stranu a lambdu s klíčovým výsledkem (množina pro konkrétní parametry).
- `python3 .claude/learn/klic.py` — selftest klíče proti `solveset`.
- `python3 .claude/learn/klic.py lin5 p=-1` — správná množina pro dané p (tutor to použije před hodnocením nebo před tvorbou kvízu).
- `python3 .claude/learn/klic.py lin5 p=2 x=2` — vypíše `RESI`/`NERESI` (dosazením do původní rovnice; nulový jmenovatel nebo záporná odmocnina dají `NERESI`).
Tutor tak: nikdy neověřuje studentův výsledek z hlavy; pro studentovo tvrzení "pro p=... je řešení ..." spustí kontrolu v několika bodech (kritické hodnoty a body mezi nimi). Při diskuzi stačí otestovat každou kritickou hodnotu a po jednom bodě v každém intervalu.

Dva "nesoulady" selftestu jsou artefakty sympy (ignoruje DO): `pod1` $t=2$ (sympy vrací $\mathbb R$, správně $\mathbb R\setminus\{2\}$) a `irr3` $a=0$ (sympy vrací $\mathbb R$, v reálném oboru se $\sqrt{y}$ vyžaduje $y\ge0$). Klíč je tu správný; je dobré tyto dva příklady použít jako cvičení "kde sympy lže a proč".
