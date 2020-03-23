(define (domain travelling)

    (:requirements :adl)
        
    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        location
        physical
        car - physical
        car_vendor - physical
        agent - physical
    )

    (:constants
        ;; You should not need to add any additional constants
        Agent - agent
        
    )

    (:predicates
        (visited ?x - location)
        (at ?x - physical ?y - location)
        (owned_by ?x - car ?y - car_vendor)
        (rented_car ?x - agent ?y - car)
        (LAND_ROUTE ?x - location ?y - location)
        (AIR_ROUTE ?x - location ?y - location)
    )

    (:functions 
        (hire_cost)
        (car_cost)
        (bus_cost)
        (plane_cost)
        (budget ?x - agent)
        (cars_rented ?x -agent)
    )

    (:action HIRE_CAR
        :parameters (?c - car ?x - location ?v - car_vendor)
        :precondition (and (>= (budget Agent) (hire_cost)) (at ?c ?x) (at ?v ?x) (at Agent ?x) (owned_by ?c ?v))
        :effect (and (decrease (budget Agent) (hire_cost)) (increase (cars_rented Agent) 1)(rented_car Agent ?c))
    )
    

    (:action RETURN_CAR
        :parameters (?c -car ?x - location ?v -car_vendor)
        :precondition (and (at Agent ?x) (at ?c ?x) (at ?v ?x) (owned_by ?c ?v) (rented_car Agent ?c))
        :effect (and (not (rented_car Agent ?c)) (decrease (cars_rented Agent) 1))
        )

    (:action DRIVE
        :parameters (?c - car ?x - location ?y - location)
        :precondition (and (>= (budget Agent) (car_cost)) (rented_car Agent ?c) (at ?c ?x) (at Agent ?x) (LAND_ROUTE ?x ?y))
        :effect (and (decrease (budget Agent) (car_cost)) (not (at Agent ?x)) (not (at ?c ?x)) (at Agent ?y) (at ?c ?y))
    )

    (:action FLY
        :parameters (?x - location ?y - location)
        :precondition (and (>= (budget Agent) (plane_cost)) (at Agent ?x) (AIR_ROUTE ?x ?y))
        :effect (and (decrease (budget Agent) (plane_cost)) (not (at Agent ?x)) (at Agent ?y))
    )

    (:action VISIT
        :parameters (?x - location)
        :precondition (and (at Agent ?x) (not (visited ?x)))
        :effect (visited ?x)
    )

    (:action BUS
        :parameters (?x -location ?y - location)
        :precondition (and (>= (budget Agent) (bus_cost)) (at Agent ?x) (LAND_ROUTE ?x ?y))
        :effect (and (decrease (budget Agent) (bus_cost)) (not (at Agent ?x)) (at Agent ?y) )
    )
)