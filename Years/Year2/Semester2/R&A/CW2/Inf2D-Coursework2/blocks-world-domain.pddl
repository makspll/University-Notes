(define (domain blocks-world)
    (:requirements :adl)
    
    (:types table block)
    
    (:predicates 
        (On ?x - block ?y - object)
        (Clear ?b - object)
    )
    
    (:constants Table - table)
    
    (:action MOVE
        :parameters (?b -block ?x - object ?y - block)
        :precondition (and (On ?b ?x) (Clear ?b) (Clear ?y) (not (= ?b ?x)) (not (= ?b ?y)) (not (= ?x ?y)))
        :effect (and (On ?b ?y) (Clear ?x) (not (On ?b ?x)) (not (Clear ?y)))
    )
    
    (:action MOVE-TO-TABLE
        :parameters (?b - block ?x - block)
        :precondition (and (On ?b ?x) (Clear ?b) (not (= ?b ?x)))
        :effect (and (On ?b Table) (Clear ?x) (not (On ?b ?x)))
    )
)