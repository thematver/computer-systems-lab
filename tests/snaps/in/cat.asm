.data
    f
    o
    o
    32
    o
    u
    t
    p
    u
    t
    32
    h
    e
    l
    l
    o
    stop: -1
    counter: 0
.code
start:
        LD #counter
        CMP stop
        BEQ end
        LD $counter
        COUT
        LD #counter
        INC
        ST #counter
        jump start
end:    HALT
