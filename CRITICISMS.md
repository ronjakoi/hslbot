# Criticisms

Things said about hslbot.

## [2018-02-12 by Reddit user *toinen-perspektiivi*](https://www.reddit.com/r/Suomi/comments/7wvkz8/koodasin_ircbotin_hsln_reittioppaan_k%C3%A4ytt%C3%B6%C3%B6n/du58lo2/)

Morjens.
Taisin alkaa skrolli-tilaajaksi ansiostasi.

Noin vaan niinku työnantajaperspektiivistä alalta palautetta sikäli kun github profiilisi toimii CVsi jatkeena (esittäydyt profiilissasi omalla nimellä & työpaikalla) tämä projekti ei ole eduksesi.

Ymmärrän, että kyseessä on harrasteprojekti, mutta tässä on muutama perustavanlaatuinen asia, mitkä vahvasti eivät käy eduksesi.

* työn laajuus keskitasolla useamman tietojenkäsittelytieteiden kurssien projektien projektitöiden suhteen
* Laajuus huomioonottaen siinä on kuitenkin 12 committia yhtenä päivänä (mistä 6 ovat READMEn päivityksiä commit viesteillä "fixed a mistake in README" ja seuraava "more mistakes in README..." - miksi roiskitaan committeja repoon?  Etkö tarkasta tekemisiäsi ennen committeja? Huolimattoman kehittäjän merkki?
* Edes alkeellinen poikkeuksenkäsittely HTTP pyynnöissä puuttuu
* HTTP pyynnön jälkeen palautetaan kysyjille suoraan r.json huolimatta siitä mitä oikeasti tapahtui
* Syötät potentiaalisesti väärää dataa funktioille mitkä suoraan viittaavat JSON objektissa oletettuun parametriin
* Testit puuttuvat kokonaan. Joo, pieni harrasteprojekti, mutta kun testin kirjoittaminen dokumentoi mitä tulet tekemään niin on kiva nähdä edistyminenkin kun testit alkavat tulla läpäistyiksi
* Ja kun kyseessä on irc-botti ... niin sille tullaan kilpaa keksimään päättömiä syötteitä ... varmista inputit ennen kuin teet mitään ja kirjoita parille negatiiviselle caselle testit
* git issue - "Include bus numbers, train identifiers etc." - epäselvät tiketit ovat yksi iso stressin ja vitutuksen aiheuttajista alalla "etc" näkeminen tiketissä on aika hirveetä - pidetään itse kehittäjinä huolta että kirjoitamme edes itsellemme tiketit kuten ne haluaisimme meille kirjoitettavan



Yllä olevat asiat huomioonottaen, luulen ettet ole aikaisemmin ollut kehittämässä käyttäjäkäyttöistä softaa tiimissä. Uskon vakaasti, että saat asiat ratkaistua ja toimimaan. Laadukas ohjelmistokehitys yhteispelissä on kuitenkin 80% muuta kuin ohjelma mikä antaa oikean lopputuloksen.

En löydä mielestäni toista alaa, missä tiimissä toinen voi pistää vastaavalla tavalla koko muun tiimin kärsimään pitkässä juoksussa yhtä pahasti kuin ohjelmistokehityksessä. Järkyttävintä on, mikäli mitään tarkkailuprosessia ei ole ollut paikalla ja yksinäinen kehittäjä on jättänyt mädät omenat mädäntymään koodiinsa. Kun tuo henkilö on talosta ulkona ja virheitä alkaa ilmaantua - toisen kehittäjän tulee hypätä puikkoihin mätäpaiseen päälle ja yrittää aluksi ymmärtää mitä ihmettä tämä toinen henkilö on edes ajatellut. Siinä yksittäiset "simppelit" muutokset alkavat maksaa maltaita. Tämmöisiä tilanteita oli aikaisemmin paljon kun kuka tahansa joka sanoi osaavansa koodata oli liiketoimen puolesta palkattu ja pistettiin asiakastöihin tuomaan rahaa taloon.  Ja siellä tehtiin puutteellisella kokemuksella ja puuttellisella ohjauksella ... ja kun ei ymmärretä mitä ei tiedetä niin ei osata ennakoida (unknown unknowns)...  Sittemmin kuvioihin tuli offshoret ja asiat meni vielä suuremmalla skaalalla aivan vitun käsittämättömäksi. Inkkari joka ei ymmärrä liiketoiminnan tarvetta vääntää koodia huonolla osaamisella niin ei helvetti siinä on muutama koukero minkä aivot pitää heittää ympäri ennen kuin saadaan asiat takaisin raiteilleen.  

Et noin niinku...

Perusasioiden puute aiheuttaa pahoja sydämentykytyksiä.

Toki kaikkien on aloitettava jostain ja kyllä tämmöset juniorille annetaan anteeksi mikäli sisäistää ja ottaa huomioon tulevilla kerroilla.  Mutta tällöin ollaan tosiaan vasta alkumetreillä.


Toivotan lämpimästi onnea matkaan mikäli tuleva tiesi vie humanistiselta puolelta jalolle ja elämänantoiselle ohjelmoinnin tielle!

### Resolution

lol

## [2018-02-12 by Reddit user *spiral--*](https://www.reddit.com/r/Suomi/comments/7wvkz8/koodasin_ircbotin_hsln_reittioppaan_k%C3%A4ytt%C3%B6%C3%B6n/du4baih/)

Käytettävyyttä lisäisi huomattavasti jos tuo kertoisi pelkän "BUS" sijaan myös linjanumeron.

### Resolution

Fixed in [#2](https://github.com/ronjakoi/hslbot/issues/2).

