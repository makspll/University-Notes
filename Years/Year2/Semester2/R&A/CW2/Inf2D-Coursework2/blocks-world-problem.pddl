(define (problem block-problem)
    (:domain blocks-world)
    (:objects 
        A - block
        B - block
        C - block
    )
    
    (:init
        (On A Table)
        (On B Table)
        (On C Table)
        (Clear A)
        (Clear B)
        (Clear C)
    )
    (:goal (and
        (On A B)
        (On B C)
    ))
)