
MAX_X = 9
MAX_Y = 14

# format after processing:
# each level is a dictionary:
# geometry: list of strings, each string is a line, each character a field:
#   space: no field
#   b : blank field
#   e : end field
#   s : round switch, can be hit by any part of the block
#   h : x switch, can be switched only if the block hits the switch vertically
#   l, r : if a switch is hit, these fields appear or disappear
#   k, q : same as l and r, but initially on instead of off
#   f : can be visited only in split mode, or not standing
# start: x, y start coordinate of the block

levels = [
    # {  
    #      'geometry': [  'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbb',
    #                     'bbbbbbbbbe'],
    #     'start': {'x': 0, 'y': 0},
    #     'swatches': []},
    
       {   'geometry': [   '          ',
                        '          ',
                        '     bbb  ',
                        '    bbbb  ',
                        '    bbbb  ',
                        '    bbb   ',
                        '    bbb   ',
                        '   bbbb   ',
                        '  bbbb    ',
                        '  bebb    ',
                        '  bbbb    ',
                        '   bb     ',
                        '          ',
                        '          ',
                        '          '],
        'start': {'x': 6, 'y': 3},
        'swatches': []}]