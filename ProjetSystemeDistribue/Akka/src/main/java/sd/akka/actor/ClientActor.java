package sd.akka.actor;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;
import java.util.Random;
import sd.akka.actor.BanquierActor.DemandeDepot;
import sd.akka.actor.BanquierActor.DemandeRetrait;
import sd.akka.actor.BanquierActor.Transaction;
import java.io.Serializable;



public class ClientActor extends AbstractActor {
private final ActorRef banqueActor;
private int solde;

    public ClientActor(ActorRef banqueActor) {
        this.banqueActor = banqueActor;
    }

    static public Props props(ActorRef banqueActor) {
        return Props.create(ClientActor.class, () -> new ClientActor(banqueActor));
    }
    public static class SoldeMessage implements Serializable {
    private final int id;
    private final int solde;

    public SoldeMessage(int id, int solde) {
        this.id = id;
        this.solde = solde;
    }

    public int getId() {
        return id;
    }

    public int getSolde() {
        return solde;
    }
}

    @Override
    public Receive createReceive() {
        return receiveBuilder()
             .match(SoldeMessage.class, soldeMessage -> {
                // Recevoir le message de solde et mettre à jour la variable solde
                this.solde = soldeMessage.getSolde();
                
            })
            .match(Transaction.class, transaction -> {
                int transactionType = transaction.getType();
                int montant = transaction.getMontant();

                if (transactionType == 1) {
                    System.out.println("Vous avez choisi d'effectuer une demande de dépôt.");
                        banqueActor.tell(new DemandeDepot(solde, montant), getSelf());
                } else if (transactionType == 2) {
                   System.out.println("Vous avez choisi d'effectuer une demande de retrait.");
                        banqueActor.tell(new DemandeRetrait(solde, montant), getSelf());
                }
            })
             .match(Integer.class, result -> {
                System.out.println("Votre solde est de : " + result+ " euros.");
            })
            .build();

    
    }
   
}




          