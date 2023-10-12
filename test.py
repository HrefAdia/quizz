import unittest
from unittest.mock import patch
import os
import json
import questionnaire
import questionnaire_import



# --------------  Tests unitaires du quizz ==> questionnaire  ----------------------

class TestsQuestions(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3")
        q = questionnaire.Question("titre_question", choix, "choix2")
        with patch("builtins.input", return_value="1"):
             self.assertFalse(q.poser(1, 1))
        with patch("builtins.input", return_value="2"):
             self.assertTrue(q.poser(1, 1))
        with patch("builtins.input", return_value="3"):
             self.assertFalse(q.poser(1, 1))


class TestQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("test_data", "cinema_alien_debutant.json")
        q = questionnaire.Questionnaire.questionnaire_from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(len(q.questions), 10)
        self.assertEqual(q.titre, "Alien")
        self.assertEqual(q.categorie, "Cinéma")
        self.assertEqual(q.difficulte, "débutant")
        with patch("builtins.input", return_value="1"):
             self.assertEqual(q.lancer(), 1)

# Test negatif sur données pour eviter quelques exepts
    def test_questionnaire_format_invalide(self):
        # Fichier sans categorie et difficulté
        filename = os.path.join("test_data", "format_invalide1.json")
        q = questionnaire.Questionnaire.questionnaire_from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "inconnue")
        self.assertEqual(q.difficulte, "inconnue")
        self.assertIsNotNone(q.questions)
        
        # Fichier sans categorie, difficulte et titre
        filename = os.path.join("test_data", "format_invalide2.json")
        q = questionnaire.Questionnaire.questionnaire_from_json_file(filename)
        self.assertIsNone(q)

        # Fichier sans questions
        filename = os.path.join("test_data", "format_invalide3.json")
        q = questionnaire.Questionnaire.questionnaire_from_json_file(filename)
        self.assertIsNone(q)


# -------------------    Tests unitaire du fichier d'import de donnees  ==> questionnaire.import  ----------------------

class TestImportQuestionnaire(unittest.TestCase):
    def test_import_json_format(self):
        questionnaire_import.generate_json_file("Animaux", "Abeilles du rucher", "https://download.openquizzdb.org/3237473974/OpenQuizzDB_237/openquizzdb_237.json")
        filenames = ("animaux_abeillesdurucher_confirme.json", "animaux_abeillesdurucher_debutant.json", "animaux_abeillesdurucher_expert.json")           
        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de désérialisation pour le fichier json" + filename)
            
            #Test du format du questionnaire
            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulte"))
            self.assertIsNotNone(data.get("categorie"))

            #Test du format des questions
            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))
                for choix in question.get("choix"):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1], bool))
                bonne_reponses = [i[0] for i in question.get("choix") if i[1]]
                self.assertEqual(len(bonne_reponses), 1)












unittest.main()