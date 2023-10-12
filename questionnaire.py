import json
import sys

#---------------------              Le Quizz    ---------------------------------          

# ********************************************************************************

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
        # Si la réponse n'est pas fournie ou s'il y a plusieurs réponses : on ajoute pas la question !
        if len(bonne_reponse) != 1:
            return None
        #Instanciation de la question 
        q = Question(titre, choix, bonne_reponse[0])
         #print(bonne_reponse) #==> on obtient une liste donc on prend le premier item
            
        return q

    def poser(self, num_question, nb_questions ):
        print(f"QUESTION {num_question} / {nb_questions}")
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
        if not data.get("questions"):
            return None

        questionnaires = data["questions"]
        questions = [Question.extract_question(question) for question in questionnaires]
        # Ignore les questions non construits (None)
        questions = [question for question in questions if question]

        # ---------  Ajout suite test unitaire negatif  sur le format des donnees
        # Permet de creer le questionnaire meme sans categorie et difficulté 
        if not data.get("categorie"):
            data["categorie"] = "inconnue"

        if not data.get("difficulte"):
            data["difficulte"] = "inconnue"

        if not data.get("titre"):
            return None
        
        # ------- Fin  Ajout suite tests negatif  sur le format
        
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])
    
    # Pour lancer directement le questionnaire à partir d'un fichier Json
    def questionnaire_from_json_file(filename):
        try:
            with open(filename, "r") as file:
                json_data = file.read()
            questionnaire_data = json.loads(json_data)
            #questionnaires = questionnaire_data["questions"]
        except:
            print("Erreur lors de l'ouverture ou à la lecture du fichier")
            return None

        return Questionnaire.extract_json_data(questionnaire_data)


    def lancer(self):
        score = 0
        nb_questions = len(self.questions)

        print("*"*28)
        print()
        print("QUESTIONNAIRE : " + self.titre)
        print("  Categorie : " + self.categorie)
        print("  Difficulte : " + self.difficulte)
        print("  Nombre de questions : " + str(nb_questions))
        print()
        print("*"*28)
        print()

        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser(i+1, nb_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score



#*******************   Lancemant du questionnaire   ********************** 

if __name__ == "__main__":

    # 1 Lancement en directe
    #filename = "animaux_abeillesdurucher_confirme.json"
    #filename = "animaux_leschats_confirme.json"
    #Questionnaire.questionnaire_from_json_file(filename).lancer()

    # 2 Lancement en ligne de commande

    if len(sys.argv) < 2:
        print("ERREUR : Vous devez spécifier le nom du fichier json à charger")
        exit(0)

    filename = sys.argv[1]
    questionnaire = Questionnaire.questionnaire_from_json_file(filename)
    if questionnaire:
        questionnaire.lancer()

