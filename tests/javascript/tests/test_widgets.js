/* editeur.rxGraisse */

QUnit.test( "Teste regex graisse du texte", function(assert) {
  var texte = "Paris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.";
  assert.deepEqual(texte.match(editeur.rxGraisse), [
    "Paris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.",
    "P",
    undefined,
    undefined,
    undefined,
    "aris.",
    " Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale."
  ], "Match a text without bold tags.");


  var texte = "P[aris]. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.";
  assert.deepEqual(texte.match(editeur.rxGraisse), [
    "P[aris]. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.",
    "P",
    "[aris]",
    "[aris",
    "]",
    ". Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux.",
    " Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale."
  ], "Match a text with bold tags.");
});

/* editeur.graissePhraseSuivante() */

QUnit.test( "Teste la fonction qui passe le texte en gras de façon itérative", function(assert) {
  var texte = "Paris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.";
  assert.deepEqual(editeur.graissePhraseSuivante(texte), "P[aris.] Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.", "Match a text without bold tags.");

  texte = "P[aris.] Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.";
  assert.deepEqual(editeur.graissePhraseSuivante(texte), "P[aris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux.] Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.", "Match a text without bold tags.");

  texte = "P[aris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux.] Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.";
  assert.deepEqual(editeur.graissePhraseSuivante(texte), "P[aris. Au grand calme et noyé dans la verdure magnifique mas provençal d’environ 390 m{2} sur un hectare de terrain joliment arboré avec piscine sécurisée, pool-house, enclos chevaux. Cette propriété est composée d'une habitation principale d'environ 150 m{2} sur deux niveaux exposée sud donnant sur une terrasse ombragée, de 5 chambres d'hôtes intégralement rénovées avec goût, d'un gîte Type 3 d'environ 50 m{2}, d'une cuisine d'été équipée avec sa chambre et sa salle d’eau indépendante de la bâtisse principale.]", "Match a text without bold tags.");
});
