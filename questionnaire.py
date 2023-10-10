import json

#*** Création du quizz avec un seul fichier pour tester les différentes fonctionnalités ***
filename = "animaux_leschats_confirme.json"

with open(filename, "r") as file:
    json_data = file.read()

questionnaire_data = json.loads(json_data)

# *****************************************************************

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def extract_question(data):
       # Extrait Les differents champs pour creer une question
        titre = data["titre"]
        choix = [i[0] for i in data["choix"]]
        bonne_reponse = [i[0] for i in data["choix"] if i[1]] 
            #print(bonne_reponse) c'est une liste donc on prend le premier item
        #Instanciation de la question 
        q = Question(titre, choix, bonne_reponse[0])
            
        return q

    def poser(self):
        print("QUESTION")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
    
class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    
    def extract_json_data(data):
        questionnaires = questionnaire_data["questions"]
        questions = [Question.extract_question(question) for question in questionnaires]
        
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])


    def lancer(self):
        score = 0
        nb_questions = len(self.questions)

        print("-"*20)
        print("QUESTIONNAIRE : " + self.titre)
        print("  Categorie : " + self.categorie)
        print("  Difficulte : " + self.difficulte)
        print("  Nombre de questions : " + str(nb_questions))
        print("-"*20)

        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score

# Lancemant du questionnaire
Questionnaire.extract_json_data(questionnaire_data).lancer()
