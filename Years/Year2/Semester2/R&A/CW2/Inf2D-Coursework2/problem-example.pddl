(define (problem travelling-21)
    (:domain travelling)
    (:objects
        Agent - agent
	x - type1
	y z - subtype1
    )

    (:init
	(example2 )
	(example-predicate x)
	
        (= (f y) 10)
	(= (f z) 5)
    )

    (:goal (and
	(not (example-predicate x))

    )
  )
)
