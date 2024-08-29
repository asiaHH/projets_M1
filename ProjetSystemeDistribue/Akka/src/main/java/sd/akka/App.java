package sd.akka;

import java.sql.*;
import java.time.Duration;
import java.util.concurrent.CompletionStage;
import java.util.concurrent.ExecutionException;
import java.util.Scanner;


import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.pattern.Patterns;
import akka.routing.RoundRobinPool;
import sd.akka.actor.*;
import java.io.*;
import java.lang.Thread;
import java.util.Random;
import sd.akka.actor.BanquierActor.DemandeDepot;
import sd.akka.actor.BanquierActor.DemandeRetrait;
import sd.akka.actor.BanquierActor.Transaction;
import sd.akka.actor.ClientActor.SoldeMessage;


import static java.lang.Integer.parseInt;

public class App {
 private static Scanner scanner = new Scanner(System.in);
  

  private static boolean checkDatabaseForId(Connection con, int id) {
    try {
        // Créé une requête SQL pour vérifier si l'ID existe dans la table CLIENT
        String query = "SELECT * FROM CLIENT WHERE idClient = ?";
        PreparedStatement stmt = con.prepareStatement(query);
        stmt.setInt(1, id);

        // Exécutez la requête et récupérez le résultat
        ResultSet rs = stmt.executeQuery();

        // Si le ResultSet contient au moins une ligne, cela signifie que l'ID existe
        boolean idExists = rs.next();

        // Ferme les ressources
        rs.close();
        stmt.close();

        return idExists;
    } catch (SQLException e) {
        e.printStackTrace();
        return false;
    }
}

    public static void main(String[] args) throws InterruptedException {

        // Création du système d'acteurs
        ActorSystem system = ActorSystem.create("BanqueSystem");

        // Création des acteurs
        ActorRef banqueActor = system.actorOf(BanqueActor.props(), "banqueActor");
        ActorRef banquierActor = system.actorOf(BanquierActor.props(), "banquierActor");
        ActorRef clientActor = system.actorOf(ClientActor.props(banqueActor), "clientActor");



       clientActor.tell("start", ActorRef.noSender());
       System.out.println("Bonjour bienvenue!");

     

        String url = "jdbc:oracle:thin:@butor:1521:ENSB2023";
        String user = "ah975865";
        String mdp = "ah975865";
        Connection con = null;
        Connection con1 = null;

        try {
            Class.forName("oracle.jdbc.driver.OracleDriver");
            try {
                con = DriverManager.getConnection(url, user, mdp);
                Statement stmtExecute = con.createStatement();
    

try{
        Scanner scanner = new Scanner(System.in);
        System.out.println("Veuillez entrer votre ID entre 1 et 6 :");
        int id = scanner.nextInt();
        System.out.println("Vous avez choisi l'id: "+ id);
            
            
            

      
        boolean idExists = checkDatabaseForId(con, id);

        if (idExists) {
            Statement statement = con.createStatement();
            ResultSet resultat = statement.executeQuery("SELECT * FROM CLIENT WHERE idClient = " + id);
        
            String nom = "";
          
            
             while (resultat.next()) {
                String nomClient = resultat.getString("nom");
               int solde = resultat.getInt("solde");

                System.out.println(" Bonjour M." + nomClient + ", votre solde actuel est de : " + solde + " euros.");
               
                SoldeMessage soldeMessage = new SoldeMessage(id, solde);
                clientActor.tell(soldeMessage, ActorRef.noSender());
               
            }
                System.out.println("Choisissez une action :");
                System.out.println("1 - Effectuer un dépôt");
                System.out.println("2 - Effectuer un retrait");
                int transactionType = scanner.nextInt();
                System.out.println("Veuillez entrer le montant :");
                int montant = scanner.nextInt();
                Transaction transaction = new Transaction(transactionType, montant);
                clientActor.tell(transaction, ActorRef.noSender());
            
            
            statement.close();
            resultat.close(); 
        } else {
            System.out.println("ID non trouvé");
        }
        
        }catch (SQLException e) {
            e.printStackTrace(); 
            throw e;
        }

  
             con.close(); 
             System.exit(99);   
                
                
            } catch (SQLException e) {
                System.err.println("Connection a la base de donnees impossible");
                System.exit(99);
            }

        } catch (ClassNotFoundException e) {
            System.err.println("Impossible de charger le pilote jdbc:odbc");
             e.printStackTrace();
            System.exit(99);
        }
        
system.terminate();
	}


}
