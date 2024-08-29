package sd.akka.actor;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import java.io.Serializable;

import java.sql.*;

public class BanquierActor extends AbstractActor {

   static public Props props() {
        return Props.create(BanquierActor.class, BanquierActor::new);
    }

    @Override
   public Receive createReceive() {
        return receiveBuilder()
            .match(DemandeDepot.class, demandeDepot -> {
                int nouveauSolde = demandeDepot.getSolde() + demandeDepot.getMontant();
                // Renvoie le résultat à la banque

                getSender().tell(nouveauSolde, getSelf());
               
            })
            .match(DemandeRetrait.class, demandeRetrait -> {
                int montant = demandeRetrait.getMontant();
                int soldeActuel = demandeRetrait.getSolde();

                if (soldeActuel >= montant) {
                    int nouveauSolde = soldeActuel - montant;
                    // Renvoie le résultat à la banque
                    getSender().tell(nouveauSolde, getSelf());
                   
                } else {
                    // Renvoie un signal indiquant que le retrait est impossible
                    getSender().tell("Solde insuffisant", getSelf());
                }
            })
            .build();

    }
    public static class Transaction implements Serializable {
    private final int type;
    private final int montant;

    public Transaction(int type, int montant) {
        this.type = type;
        this.montant = montant;
    }

    public int getType() {
        return type;
    }

    public int getMontant() {
        return montant;
    }
}


    public interface Message {}

public static class DemandeDepot implements Message {
        private final int solde;
        private final int montant;

        public DemandeDepot(int solde, int montant) {
            this.solde = solde;
            this.montant = montant;
        }

        public int getSolde() {
            return solde;
        }

        public int getMontant() {
            return montant;
        }
    }

    public static class DemandeRetrait implements Message {
        private final int solde;
        private final int montant;

        public DemandeRetrait(int solde, int montant) {
            this.solde = solde;
            this.montant = montant;
        }

        public int getSolde() {
            return solde;
        }

        public int getMontant() {
            return montant;
        }
    }
    
}
