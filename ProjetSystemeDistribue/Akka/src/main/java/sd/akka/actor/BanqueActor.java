package sd.akka.actor;

import akka.actor.AbstractActor;
import akka.actor.Props;
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.io.Tcp;
import akka.pattern.Patterns;

import java.sql.Connection;
import java.time.Duration;
import java.util.Scanner;
import java.util.concurrent.CompletionStage;
import sd.akka.actor.BanquierActor.DemandeDepot;
import sd.akka.actor.BanquierActor.DemandeRetrait;


public class BanqueActor extends AbstractActor {

    private final ActorRef banquierActor;

public BanqueActor() {
        this.banquierActor = getContext().actorOf(BanquierActor.props(), "banquierActor");
    }
    static public Props props() {
        return Props.create(BanquierActor.class, BanquierActor::new);
    }

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(DemandeDepot.class, demandeDepot -> {
                // Transmission de la demande de dépôt au banquier
                System.out.println("Le banque a recu la demande de depot");
                banquierActor.tell(demandeDepot, getSender());
            })
            .match(DemandeRetrait.class, demandeRetrait -> {
                // Transmission de la demande de retrait au banquier
                System.out.println("Le banque a recu la demande de retrait");
                banquierActor.tell(demandeRetrait, getSender());
            })
            .match(Integer.class, resultat -> {
                // Renvoi du résultat au client
                System.out.println("Le banque envoie un résultat au client");
                getSender().tell(resultat, getSelf());
            })
            .matchAny(o -> System.out.println("Le banque a reçu un message non reconnu : " + o))
            .build();

    }
   



    
}
