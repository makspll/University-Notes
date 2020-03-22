(define (domain travelling)
    (:requirements :adl )

    (:types
        type1
        subtype1 - type2
        ;; Fill in additional types here
    )

    (:constants
        ;; You should not need to add any additional constants
        Agent - agent
    )

    (:predicates
	(example-predicate ?x - type1)
	(example2 )

    )

    (:functions (f ?x - type2 ))


    (:action example 
      :parameters (?x - type1 ?y - subtype1)
      :precondition (and
	  (example-predicate ?x)
          (>= (f ?y) 4)
      )
      :effect (and
	  (not (example-predicate ?x))
          (decrease (f ?y) 3)
          )
    )
)
