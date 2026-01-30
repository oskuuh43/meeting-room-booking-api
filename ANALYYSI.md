
## 1. Mitä tekoäly teki hyvin?

Tekoäly tuotti nopean ja toimivan perusratkaisun, joka onnistui täyttämään kaikki tehtävän vaatimukset. 
Projektin rakenne oli selkeä ja looginen, ja koodin logiikka oli helppo ymmärtää jo lähtötilanteessa.
Projektin ensimmäisen osuuden tekemiseen tarvittiin 3 promptia, mikä korostaa tekoälyn tehokkuutta ohjelmoinnissa, kun sitä ohjataan oikein.

Kokonaisuutena tekoälyn tuottama koodi muodosti hyvän ja toimivan pohjan jatkokehitykselle.



## 2. Mitä tekoäly teki huonosti?

Vaikka perustoiminnallisuus oli kunnossa, tekoälyn tuottamassa koodissa oli useita kohtia, jotka sisältivät potentiaalisia ongelmia tai parannettavaa.

Merkittävin puute liittyi aikakäsittelyyn. Tekoäly ei huomioinnut aikavyöhykkeettömien ja aikavyöhykkeellisten aikaleimojen eroa, 
mikä voisi johtaa virheisiin tietyissä tilanteissa.

Lisäksi, tekoäly ei huomioinut rinnakkaisuuden vaikutuksia. Samaanaikaiset pyynnöt voisivat rikkoa säännön päällekkäisistä varauksista.
Tämä ei aiheuta ongelmaa nykyisessä versiossa, jossa sovellusta käyttää yksi käyttäjä, mutta olisi kriittinen ongelma jos projektia vietäisiin eteenpäin.
Rinnakkaisuuteen liittyvät puutteet jätin tietoisesti korjaamatta, koska tehtävä määritteli järjestelmän in-memory-ratkaisuksi ilman useita käyttäjiä.

Tekoäly jätti myös osittain epäselväksi keskeisten kenttien merkityksen ja käyttötarkoituksen.
Esimerkiksi room_id, start_time, end_time ja booking_id eivät olleet dokumentoituna riittävän selkeästi.
Lisäksi tekoäly ei lisännyt requirements.txt tiedostoa, mikä helpottaisi projektin käyttöönottoa merkittävästi, jos projektia laajentaisiin tulevaisuudessa.

Pienempänä puutteena voidaan myös mainita, että varaukset eivät alun perin palautuneet aikajärjestyksessä, mikä heikensi API:n käytettävyyttä kun useita varauksia lisätään yhteen kokoushuoneeseen.
Myös reitityksessä esiintyi pieni huolimattomuus, jossa reititin jäi aluksi määrittelemättä, mikä esti sovelluksen käynnistymisen ilman korjausta.



## 3. Mitkä olivat tärkeimmät parannukset, jotka teit tekoälyn tuottamaan koodiin ja miksi?

Tärkein tehty parannus tekoälyn koodiin oli aikakäsittelyn korjaaminen. 
Lisäsin validoinnin, joka varmistaa että kaikki aikaleimat ovat aikavyöhykkeellisiä ja normalisoituja samaan aikaan.
Tämä poistaa epäselvyydet aikavyöhykkeiden käsittelyssä ja parantaa varauslogiikan toimivuutta.

Toinen merkittävä parannus API:n käytettävyyteen oli kokoushuoneen varausten listaaminen aikajärjestyksessä.
Tällöin kokoushuoneen varatut ajat näkyvät selkeästi myös silloin, kun varauksia löytyy monta.


