.data
    result:     0
    cnt_3:      0
    sum_3:      0
    cnt_5:      0
    sum_5:      0
    cnt_15:     0
    sum_15:     0
    temp_3:     0
    temp_5:     0
    temp_15:    0

.code

    clc_3:  ld  #cnt_3
            inc
            st #cnt_3
            mul #3
            st #temp_3
            cmp #1000
            bpl clc_5
            add #sum_3
            st #sum_3
            jump clc_3

    clc_5:  ld #cnt_5
            inc
            st #cnt_5
            mul #5
            st #temp_5
            cmp #1000
            bpl clc_15
            add #sum_5
            st #sum_5
            JUMP clc_5

    clc_15: ld #cnt_15
            inc
            st  #cnt_15
            mul #15
            st  #temp_15
            cmp #1000
            bpl out
            add #sum_15
            st  #sum_15
            jump clc_15

    out:
            ld #sum_3
            add #sum_5
            sub #sum_15
            out
            halt
