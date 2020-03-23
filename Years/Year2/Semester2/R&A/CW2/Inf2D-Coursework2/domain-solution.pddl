(define (domain travelling)

    (:requirements :adl)
        
    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        location
    )

    (:predicates
        (visited ?x - location)
        (agent_at ?x - location)
        (car_at ?x - location)
        (LAND_ROUTE ?x - location ?y - location)
        (AIR_ROUTE ?x - location ?y - location)
    )

    (:action DRIVE
        :parameters (?x - location ?y - location)
        :precondition (and (car_at ?x) (agent_at ?x) (LAND_ROUTE ?x ?y))
        :effect (and (not (agent_at ?x)) (not (car_at ?x)) (agent_at ?y) (car_at ?y))
    )

    (:action FLY
        :parameters (?x - location ?y - location)
        :precondition (and (agent_at ?x) (AIR_ROUTE ?x ?y))
        :effect (and (not (agent_at ?x)) (agent_at ?y))
    )

    (:action VISIT
        :parameters (?x - location)
        :precondition (and (agent_at ?x) (not (visited ?x)))
        :effect (visited ?x)
    )
)